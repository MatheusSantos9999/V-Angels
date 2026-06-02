from flask import Flask, request, jsonify
from ultralytics import YOLO
from twilio.rest import Client
import cv2
import numpy as np
import time
import requests
import os

app = Flask(__name__)

API_KEY              = os.getenv("API_KEY", "teste123")
BOT_TOKEN            = os.getenv("BOT_TOKEN")
CHAT_ID              = os.getenv("CHAT_ID")
TWILIO_SID           = os.getenv("TWILIO_SID")
TWILIO_TOKEN         = os.getenv("TWILIO_TOKEN")
TWILIO_FROM          = os.getenv("TWILIO_FROM")
TELEFONE_MOTORISTA   = os.getenv("TELEFONE_MOTORISTA")

TEMPO_AUSENCIA_MOTORISTA = 10
TEMPO_ESPERA_RESPOSTA    = 15
CONFIANCA_MINIMA         = 0.10

telegram_enviado        = False
ligacao_feita           = False
hora_telegram           = None
motorista_ausente_desde = None
last_update_id          = 0

print("Carregando YOLO...")
model = YOLO("yolov8n.pt")
print("YOLO carregado.")


def inicializar_offset():
    global last_update_id
    if not BOT_TOKEN:
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?limit=1"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get("ok") and data.get("result"):
            last_update_id = data["result"][-1]["update_id"]
    except Exception as e:
        print("Erro ao inicializar Telegram:", e)


def enviar_telegram(mensagem):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram não configurado.")
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        resp = requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem}, timeout=5)
        if resp.status_code == 200:
            print("Telegram enviado.")
        else:
            print("Erro Telegram:", resp.text)
    except Exception as e:
        print("Falha Telegram:", e)


def verificar_resposta_telegram():
    global last_update_id
    if not BOT_TOKEN or not CHAT_ID:
        return False
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=1"
        resp = requests.get(url, timeout=3)
        data = resp.json()
        if data.get("ok") and data.get("result"):
            for update in data["result"]:
                last_update_id = update["update_id"]
                mensagem = update.get("message", {})
                chat_id_msg = str(mensagem.get("chat", {}).get("id", ""))
                if chat_id_msg == str(CHAT_ID):
                    return True
    except Exception:
        pass
    return False


def fazer_ligacao():
    if not all([TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM, TELEFONE_MOTORISTA]):
        print("Twilio não configurado.")
        return
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.calls.create(
            twiml="""
            <Response>
                <Say language="pt-BR">
                    Atenção. Há crianças na van escolar sem a presença do motorista.
                    Por favor, retorne imediatamente.
                </Say>
            </Response>
            """,
            to=TELEFONE_MOTORISTA,
            from_=TWILIO_FROM
        )
        print("Ligação iniciada.")
    except Exception as e:
        print("Erro na ligação:", e)


def detectar_pessoas(frame, nome_area):
    resultados = model(frame, classes=[0], verbose=False)
    quantidade = 0
    for resultado in resultados:
        for box in resultado.boxes:
            confianca = float(box.conf[0])
            print(f"{nome_area}: pessoa detectada com confiança {confianca:.2f}")
            if confianca >= CONFIANCA_MINIMA:
                quantidade += 1
    return quantidade


def processar_logica_alerta(qtd_motorista, qtd_criancas):
    global telegram_enviado, ligacao_feita, hora_telegram, motorista_ausente_desde

    motorista_detectado = qtd_motorista > 0
    crianca_detectada   = qtd_criancas  > 0
    alerta   = False
    mensagem = "Tudo certo. Sistema continua monitorando."

    if motorista_detectado or not crianca_detectada:
        if telegram_enviado or ligacao_feita:
            motivo = "motorista voltou" if motorista_detectado else "sem crianças na van"
            enviar_telegram(f"Alerta cancelado: {motivo}.")
        motorista_ausente_desde = None
        telegram_enviado        = False
        ligacao_feita           = False
        hora_telegram           = None
    else:
        alerta = True
        if motorista_ausente_desde is None:
            motorista_ausente_desde = time.time()
        tempo_ausente = int(time.time() - motorista_ausente_desde)
        mensagem = f"ALERTA: criança detectada sem motorista há {tempo_ausente}s."

        if tempo_ausente >= TEMPO_AUSENCIA_MOTORISTA and not telegram_enviado:
            texto = (
                f"ALERTA — VAN ESCOLAR\n"
                f"Motorista ausente há {tempo_ausente}s com {qtd_criancas} pessoa(s) na área das crianças.\n\n"
                f"Responda esta mensagem para confirmar ciência.\n"
                f"Se não responder em {TEMPO_ESPERA_RESPOSTA}s, o sistema fará uma ligação."
            )
            enviar_telegram(texto)
            telegram_enviado = True
            hora_telegram    = time.time()

        if telegram_enviado and not ligacao_feita:
            if verificar_resposta_telegram():
                enviar_telegram("Resposta recebida. Alerta pausado.")
                telegram_enviado        = False
                motorista_ausente_desde = None
                hora_telegram           = None
            elif hora_telegram and time.time() - hora_telegram >= TEMPO_ESPERA_RESPOSTA:
                fazer_ligacao()
                ligacao_feita = True

    return {
        "motorista_detectado": motorista_detectado,
        "qtd_motorista":       qtd_motorista,
        "crianca_detectada":   crianca_detectada,
        "qtd_criancas":        qtd_criancas,
        "alerta":              alerta,
        "telegram_enviado":    telegram_enviado,
        "ligacao_feita":       ligacao_feita,
        "mensagem":            mensagem
    }


@app.route("/", methods=["GET"])
def home():
    return "Servidor YOLO online"


@app.route("/upload_frames", methods=["POST"])
def upload_frames():
    token = request.headers.get("X-API-KEY")
    if token != API_KEY:
        return jsonify({"erro": "não autorizado"}), 401

    if "frame" not in request.files:
        return jsonify({"erro": "envie o arquivo frame"}), 400

    frame_np = np.frombuffer(request.files["frame"].read(), np.uint8)
    frame    = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"erro": "erro ao decodificar frame"}), 400

    altura, largura, _ = frame.shape
    print(f"Frame recebido: {largura}x{altura}")

    frame_motorista = frame[0:altura // 2, 0:largura]
    frame_criancas  = frame[altura // 2:altura, 0:largura]

    cv2.imwrite("debug_frame_inteiro.jpg", frame)
    cv2.imwrite("debug_motorista.jpg", frame_motorista)
    cv2.imwrite("debug_criancas.jpg", frame_criancas)

    frame_motorista = cv2.resize(frame_motorista, (640, 640))
    frame_criancas  = cv2.resize(frame_criancas,  (640, 640))

    qtd_motorista = detectar_pessoas(frame_motorista, "Motorista")
    qtd_criancas  = detectar_pessoas(frame_criancas,  "Crianças")

    resposta = processar_logica_alerta(qtd_motorista, qtd_criancas)

    print(
        f"Motorista: {resposta['motorista_detectado']} ({qtd_motorista}) | "
        f"Crianças: {resposta['crianca_detectada']} ({qtd_criancas}) | "
        f"Alerta: {resposta['alerta']}"
    )
    return jsonify(resposta)


if __name__ == "__main__":
    inicializar_offset()
    app.run(host="0.0.0.0", port=5000)
