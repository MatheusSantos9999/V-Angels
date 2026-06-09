import { Bell, Heart, CheckCircle, Video, UserCheck } from 'lucide-react';
import blackLogo from '../imports/Black_And_White_Minimalist_Typography_Personal_Logo-3.png';

export default function App() {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="sticky top-0 z-50 shadow-md" style={{ background: 'linear-gradient(135deg, #1098F7 0%, #0D7FD4 60%, #0A6EC0 100%)' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img
              src={blackLogo}
              alt="V-Angels Logo"
              className="h-12 w-auto brightness-0 invert"
            />
            <span className="font-bold text-xl text-white">V-Angels</span>
          </div>
          <nav className="hidden md:flex gap-8">
            <a href="#recursos" className="text-white/80 hover:text-white transition font-medium">Recursos</a>
            <a href="#como-funciona" className="text-white/80 hover:text-white transition font-medium">Como Funciona</a>
            <a href="#beneficios" className="text-white/80 hover:text-white transition font-medium">Benefícios</a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-50 to-indigo-100 py-20 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full mb-6">
              <Heart className="w-4 h-4" />
              <span className="text-sm font-medium">Proteção Inteligente</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Deixe seu transporte mais seguro!
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              V-Angels é o sistema de vigilância inteligente que previne o esquecimento de crianças em vans escolares através de câmeras de monitoramento dos passageiros e do motorista.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="https://www.instagram.com/v_ang3ls/"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-white text-blue-600 border-2 border-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition text-center"
              >
                Saiba Mais
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Video Section */}
      <section className="py-20 bg-white">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative rounded-2xl overflow-hidden shadow-2xl aspect-video">
            <iframe
              className="w-full h-full"
              src="https://www.youtube.com/embed/Or2OivSA-lE"
              title="V-Angels - Sistema de Segurança"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
        </div>
      </section>

      {/* Problema Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Um Problema Sério que Precisa de Solução
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Todos os anos, incidentes de crianças esquecidas em veículos escolares resultam em tragédias evitáveis. O V-Angels foi criado para garantir que isso nunca aconteça.
            </p>
          </div>
        </div>
      </section>

      {/* Recursos Section */}
      <section id="recursos" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Tecnologia Avançada para Máxima Segurança
            </h2>
            <p className="text-xl text-gray-600">
              Combinamos múltiplas tecnologias para garantir proteção total
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mb-6">
                <Video className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Câmera dos Passageiros</h3>
              <p className="text-gray-600 mb-4">
                Câmera de alta resolução apontada para os assentos dos passageiros, detectando a presença de crianças no interior do veículo, mesmo em baixa luminosidade.
              </p>
              <ul className="space-y-2">
                <li className="flex items-start gap-2 text-gray-700">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Detecção em tempo real</span>
                </li>
                <li className="flex items-start gap-2 text-gray-700">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Verificação durante e após o trajeto</span>
                </li>
              </ul>
            </div>

            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mb-6">
                <UserCheck className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Câmera do Motorista</h3>
              <p className="text-gray-600 mb-4">
                Câmera dedicada à posição do motorista, verificando sua presença no veículo e garantindo que o mesmo não deixe o veículo sem verificar os passageiros.
              </p>
              <ul className="space-y-2">
                <li className="flex items-start gap-2 text-gray-700">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Detecção de presença</span>
                </li>
                <li className="flex items-start gap-2 text-gray-700">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Monitoramento contínuo</span>
                </li>
                <li className="flex items-start gap-2 text-gray-700">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Alertas de ausência</span>
                </li>
              </ul>
            </div>

            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mb-6">
                <Bell className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Alertas Inteligentes</h3>
              <p className="text-gray-600 mb-4">
                Sistema de notificações via Telegram quando crianças são detectadas após a saída do motorista, com envio de mensagens seguido de ligação telefônica.
              </p>
              <ul className="space-y-2">
                <li className="flex items-start gap-2 text-gray-700">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Mensagens via Telegram</span>
                </li>
                <li className="flex items-start gap-2 text-gray-700">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Ligação telefônica</span>
                </li>
                <li className="flex items-start gap-2 text-gray-700">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>Escalonamento automático</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Como Funciona Section */}
      <section id="como-funciona" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Como o V-Angels Funciona
            </h2>
            <p className="text-xl text-gray-600">
              Um sistema simples, mas extremamente eficaz
            </p>
          </div>
          <div className="max-w-3xl mx-auto">
            <div className="space-y-8">
              <div className="flex gap-4">
                <div className="bg-blue-600 text-white w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 font-bold">
                  1
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Instalação Simples</h3>
                  <p className="text-gray-600">
                    Nossos técnicos instalam duas câmeras estrategicamente posicionadas: uma voltada para os passageiros e outra para o motorista em sua van escolar.
                  </p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="bg-blue-600 text-white w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 font-bold">
                  2
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Vigilância Contínua</h3>
                  <p className="text-gray-600">
                    As câmeras monitoram continuamente o interior do veículo, detectando a presença de crianças nos assentos e do motorista na posição de direção.
                  </p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="bg-blue-600 text-white w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 font-bold">
                  3
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Detecção Inteligente</h3>
                  <p className="text-gray-600">
                    Quando o motorista sai do veículo, o sistema verifica automaticamente se há crianças nos assentos através da câmera dos passageiros.
                  </p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="bg-blue-600 text-white w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 font-bold">
                  4
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Alertas Programados</h3>
                  <p className="text-gray-600">
                    Se uma criança for detectada após a saída do motorista, alertas são enviados após um período de tempo seguindo ordem de prioridade: primeiro o motorista, depois os responsáveis e, se necessário, as autoridades.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Benefícios Section */}
      <section id="beneficios" className="py-20 text-white" style={{ background: '#111111' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Sistema de Proteção Inteligente
            </h2>
            <p className="text-xl text-blue-100">
              Vigilância constante com alertas escalonados por prioridade
            </p>
          </div>
          <div className="max-w-2xl mx-auto">
            <div className="p-8 rounded-xl border border-white/10" style={{ background: '#1A1A1A' }}>
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
                <Heart className="w-8 h-8" />
                Benefícios do Sistema
              </h3>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-6 h-6 text-green-300 mt-0.5 flex-shrink-0" />
                  <span>Tranquilidade total sabendo que as crianças estão protegidas</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-6 h-6 text-green-300 mt-0.5 flex-shrink-0" />
                  <span>Sistema de alertas escalonados por ordem de prioridade</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-6 h-6 text-green-300 mt-0.5 flex-shrink-0" />
                  <span>Notificações via Telegram para motorista e responsáveis</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-6 h-6 text-green-300 mt-0.5 flex-shrink-0" />
                  <span>Acionamento de autoridades quando necessário</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8 flex flex-col items-center text-center">
            <div className="flex items-center gap-3 mb-4">
              <img
                src={blackLogo}
                alt="V-Angels Logo"
                className="h-10 w-auto"
              />
              <span className="font-bold text-white">V-Angels</span>
            </div>
            <p className="text-sm">
              Tecnologia que salva vidas. Protegendo crianças em transporte escolar desde 2026.
            </p>
          </div>
          <div className="border-t border-gray-800 pt-8 text-sm text-center">
            <p>&copy; 2026 V-Angels. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
