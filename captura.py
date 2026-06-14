import requests
import time
import subprocess
import os
import socket
import ipaddress
import concurrent.futures
import json

# ── Configurações ──────────────────────────────────────────────────────────────
# Endereço do servidor Flask na nuvem (AWS EC2)
AWS_URL   = "http://<IP_DO_SERVIDOR>:5000/upload_frames"

# Credenciais da câmera IP (protocolo RTSP)
RTSP_USER = "<USUARIO_CAMERA>"
RTSP_PASS = "<SENHA_CAMERA>"
RTSP_PORT = 554          # Porta padrão RTSP
RTSP_PATH = "/onvif1"    # Caminho do stream da câmera

# Chave de autenticação da API
API_KEY   = "<API_KEY>"

# Intervalo entre capturas (segundos)
INTERVALO = 15

# Arquivo de cache para o IP da câmera
IP_CACHE  = "camera_ip.json"

# ── Descoberta de IP ───────────────────────────────────────────────────────────

def rtsp_url(ip):
    """Monta a URL RTSP completa para conexão com a câmera."""
    return f"rtsp://{RTSP_USER}:{RTSP_PASS}@{ip}:{RTSP_PORT}{RTSP_PATH}"

def salvar_ip(ip):
    """Salva o IP da câmera em cache para evitar nova varredura."""
    with open(IP_CACHE, "w") as f:
        json.dump({"ip": ip}, f)

def carregar_ip():
    """Carrega o IP da câmera do cache."""
    try:
        with open(IP_CACHE) as f:
            return json.load(f).get("ip")
    except:
        return None

def porta_aberta(ip):
    """Verifica se a porta RTSP está aberta em um IP."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        ok = s.connect_ex((str(ip), RTSP_PORT)) == 0
        s.close()
        return ok
    except:
        return False

def get_subnet():
    """Descobre a sub-rede local automaticamente."""
    try:
        resultado = subprocess.run(["ip", "route"], capture_output=True, text=True, timeout=5)
        for linha in resultado.stdout.splitlines():
            partes = linha.split()
            if partes and "/" in partes[0] and not partes[0].startswith("default"):
                rede = ipaddress.ip_network(partes[0], strict=False)
                if rede.prefixlen >= 16:
                    return partes[0]
    except:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        partes = ip.split(".")
        return f"{partes[0]}.{partes[1]}.{partes[2]}.0/24"
    except:
        return None

def varrer_rede():
    """Varre a rede local em busca de dispositivos com porta 554 aberta."""
    subnet = get_subnet()
    if not subnet:
        return []
    print(f"Varrendo {subnet}...")
    rede = ipaddress.ip_network(subnet, strict=False)
    encontrados = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as ex:
        futuros = {ex.submit(porta_aberta, str(ip)): str(ip) for ip in rede.hosts()}
        for f in concurrent.futures.as_completed(futuros):
            if f.result():
                print(f"Porta 554 aberta: {futuros[f]}")
                encontrados.append(futuros[f])
    return encontrados

def descobrir_camera():
    """Descobre o IP da câmera — tenta o cache primeiro, depois varre a rede."""
    ip = carregar_ip()
    if ip and porta_aberta(ip):
        print(f"Câmera no IP salvo: {ip}")
        return ip
    print("Buscando câmera na rede...")
    candidatos = varrer_rede()
    if len(candidatos) == 1:
        salvar_ip(candidatos[0])
        return candidatos[0]
    if len(candidatos) > 1:
        print(f"{len(candidatos)} candidatos encontrados, usando o primeiro: {candidatos[0]}")
        salvar_ip(candidatos[0])
        return candidatos[0]
    return None

# ── Captura e envio ────────────────────────────────────────────────────────────

def capturar_frame(ip):
    """Captura um frame do stream RTSP usando FFmpeg."""
    if os.path.exists("frame.jpg"):
        os.remove("frame.jpg")

    subprocess.run(
        [
            "ffmpeg",
            "-i", rtsp_url(ip),
            "-an",
            "-frames:v", "1",
            "-pix_fmt", "yuvj420p",  # Corrige formato de cor do encoder da câmera
            "-q:v", "5",
            "-update", "1",
            "-y", "frame.jpg"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=30
    )

    if not os.path.exists("frame.jpg"):
        return False, "Frame não foi criado"

    tamanho = os.path.getsize("frame.jpg")
    if tamanho < 10000:
        return False, f"Frame muito pequeno ({tamanho} bytes)"

    return True, tamanho

def enviar_frame():
    """Envia o frame capturado para o servidor Flask na nuvem via HTTP POST."""
    with open("frame.jpg", "rb") as f:
        img = f.read()
    resp = requests.post(
        AWS_URL,
        files={"frame": ("frame.jpg", img, "image/jpeg")},
        headers={"X-API-KEY": API_KEY},
        timeout=30
    )
    return resp.text

# ── Loop principal ─────────────────────────────────────────────────────────────

ip_camera = None
falhas    = 0

while True:
    try:
        # Descobre o IP da câmera se ainda não tiver
        if ip_camera is None:
            ip_camera = descobrir_camera()

        if ip_camera is None:
            print("Câmera não encontrada. Aguardando 30s...")
            time.sleep(30)
            continue

        # Captura o frame
        print(f"Capturando frame ({ip_camera})...")
        ok, info = capturar_frame(ip_camera)

        if not ok:
            print(f"Erro: {info}")
            falhas += 1
            if falhas >= 3:
                print("3 falhas seguidas — redescobrir IP...")
                ip_camera = None
                falhas = 0
            time.sleep(INTERVALO)
            continue

        # Envia para o servidor
        print(f"Frame: {info} bytes — enviando...")
        resposta = enviar_frame()
        print("Resposta:", resposta)
        falhas = 0

    except subprocess.TimeoutExpired:
        print("Timeout no ffmpeg.")
        falhas += 1
        if falhas >= 3:
            ip_camera = None
            falhas = 0

    except Exception as e:
        print("Erro:", e)
        falhas += 1
        if falhas >= 5:
            ip_camera = None
            falhas = 0

    time.sleep(INTERVALO)
