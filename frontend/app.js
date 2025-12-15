// Configuração e estado do app
const CONFIG = {
    WS_URL: 'wss://worker-production-47e8.up.railway.app/ws',
    USER_ID: 'user_' + Math.random().toString(36).substr(2, 9)
};

let websocket = null;
let isConnected = false;
let deferredPrompt = null;

// Inicialização
window.addEventListener('load', () => {
    console.log('🚀 App iniciado');
    conectarWebSocket();
    registrarServiceWorker();
    configurarInstalarApp();
});

// ==========================================
// WebSocket
// ==========================================

function conectarWebSocket() {
    const wsUrl = `${CONFIG.WS_URL}/${CONFIG.USER_ID}`;
    console.log('🔌 Conectando ao WebSocket:', wsUrl);
    
    websocket = new WebSocket(wsUrl);
    
    websocket.onopen = () => {
        console.log('✅ WebSocket conectado');
        isConnected = true;
        atualizarStatus(true);
        mostrarToast('Conectado ao servidor');
    };
    
    websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('📨 Mensagem recebida:', data);
        
        if (data.tipo === 'sistema') {
            adicionarMensagemSistema(data.texto);
        } else {
            adicionarMensagemRecebida(data.texto);
        }
    };
    
    websocket.onerror = (error) => {
        console.error('❌ Erro no WebSocket:', error);
        mostrarToast('Erro de conexão');
    };
    
    websocket.onclose = () => {
        console.log('🔴 WebSocket desconectado');
        isConnected = false;
        atualizarStatus(false);
        mostrarToast('Desconectado do servidor');
        
        // Reconectar após 3 segundos
        setTimeout(conectarWebSocket, 3000);
    };
}

function enviarMensagem() {
    const input = document.getElementById('messageInput');
    const mensagem = input.value.trim();
    
    if (!mensagem) return;
    
    if (!isConnected) {
        mostrarToast('⚠️ Não conectado ao servidor');
        return;
    }
    
    // Adiciona mensagem enviada na tela
    adicionarMensagemEnviada(mensagem);
    
    // Envia para o servidor
    const payload = {
        mensagem: mensagem,
        timestamp: new Date().toISOString()
    };
    
    websocket.send(JSON.stringify(payload));
    console.log('📤 Mensagem enviada:', mensagem);
    
    // Limpa input
    input.value = '';
    input.focus();
}

// ==========================================
// Interface de mensagens
// ==========================================

function adicionarMensagemEnviada(texto) {
    removerMensagemBoasVindas();
    
    const container = document.getElementById('messagesContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message sent';
    
    messageDiv.innerHTML = `
        <div class="message-bubble">
            ${formatarTexto(texto)}
            <div class="message-time">${obterHoraAtual()}</div>
        </div>
    `;
    
    container.appendChild(messageDiv);
    scrollParaFinal();
}

function adicionarMensagemRecebida(texto) {
    removerMensagemBoasVindas();
    
    const container = document.getElementById('messagesContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message received';
    
    messageDiv.innerHTML = `
        <div class="message-bubble">
            ${formatarTexto(texto)}
            <div class="message-time">${obterHoraAtual()}</div>
        </div>
    `;
    
    container.appendChild(messageDiv);
    scrollParaFinal();
}

function adicionarMensagemSistema(texto) {
    const container = document.getElementById('messagesContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system';
    
    messageDiv.innerHTML = `
        <div class="message-bubble">
            ${formatarTexto(texto)}
        </div>
    `;
    
    container.appendChild(messageDiv);
    scrollParaFinal();
}

function formatarTexto(texto) {
    // Converte quebras de linha em <br>
    texto = texto.replace(/\n/g, '<br>');
    
    // Converte URLs em links
    texto = texto.replace(
        /(https?:\/\/[^\s]+)/g,
        '<a href="$1" target="_blank">$1</a>'
    );
    
    return texto;
}

function removerMensagemBoasVindas() {
    const welcome = document.querySelector('.welcome-message');
    if (welcome) {
        welcome.remove();
    }
}

function scrollParaFinal() {
    const container = document.getElementById('messagesContainer');
    container.scrollTop = container.scrollHeight;
}

function limparChat() {
    const container = document.getElementById('messagesContainer');
    container.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">👋</div>
            <h2>Chat limpo!</h2>
            <p>Envie uma mensagem para começar</p>
        </div>
    `;
    fecharMenu();
    mostrarToast('Chat limpo');
}

// ==========================================
// Utilidades
// ==========================================

function obterHoraAtual() {
    const now = new Date();
    return now.toLocaleTimeString('pt-BR', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

function atualizarStatus(online) {
    const indicator = document.getElementById('status');
    if (online) {
        indicator.classList.add('online');
    } else {
        indicator.classList.remove('online');
    }
}

function mostrarToast(mensagem) {
    const toast = document.getElementById('toast');
    toast.textContent = mensagem;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        enviarMensagem();
    }
}

function enviarComando(comando) {
    const input = document.getElementById('messageInput');
    input.value = comando;
    enviarMensagem();
    fecharMenu();
}

// ==========================================
// Menu
// ==========================================

function mostrarMenu() {
    document.getElementById('menuOverlay').classList.add('active');
    document.getElementById('menuLateral').classList.add('active');
}

function fecharMenu() {
    document.getElementById('menuOverlay').classList.remove('active');
    document.getElementById('menuLateral').classList.remove('active');
}

function mostrarOpcoes() {
    mostrarToast('Funcionalidade em desenvolvimento');
}

// ==========================================
// PWA
// ==========================================

function registrarServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('sw.js')
            .then(() => console.log('✅ Service Worker registrado'))
            .catch(err => console.error('❌ Erro ao registrar SW:', err));
    }
}

function configurarInstalarApp() {
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        console.log('📲 App pode ser instalado');
    });
}

function instalarApp() {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('✅ App instalado');
                mostrarToast('App instalado com sucesso!');
            }
            deferredPrompt = null;
        });
    } else {
        mostrarToast('App já está instalado ou não pode ser instalado neste navegador');
    }
    fecharMenu();
}
