# 📱 Chat App - Sistema de Mensagens em Tempo Real

Sistema completo de chat com **app mobile instalável (PWA)** + **backend Python**.

## 🚀 Características

✅ **App instalável no celular** (Android/iOS)  
✅ **Comunicação em tempo real** (WebSocket)  
✅ **Lógica de respostas customizável**  
✅ **Interface moderna estilo WhatsApp**  
✅ **Funciona offline** (PWA)  
✅ **Backend Python com FastAPI**

---

## 📦 Instalação

### 1. Instalar dependências do backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Iniciar o servidor backend

```bash
cd backend
python main.py
```

O servidor estará rodando em: `http://localhost:8000`

### 3. Abrir o app no navegador

Abra o arquivo `frontend/index.html` no navegador ou use um servidor web:

```bash
cd frontend
python -m http.server 8080
```

Acesse: `http://localhost:8080`

---

## 📱 Instalar no Celular

### Android:
1. Abra o app no Chrome
2. Toque no menu (⋮) > "Instalar app" ou "Adicionar à tela inicial"
3. Confirme a instalação

### iOS:
1. Abra o app no Safari
2. Toque no ícone de compartilhar (□↑)
3. Selecione "Adicionar à Tela Inicial"

---

## 🎯 Como Customizar as Respostas

Edite o arquivo **`backend/chat_handler.py`**:

```python
def processar_mensagem(self, user_id: str, mensagem: str) -> Dict[str, str]:
    mensagem = mensagem.strip().lower()
    
    # ===== ADICIONE SUAS REGRAS AQUI =====
    
    if 'preço' in mensagem:
        return {
            'tipo': 'info',
            'texto': 'O preço é R$ 100,00'
        }
    
    if 'horário' in mensagem:
        return {
            'tipo': 'info',
            'texto': 'Funcionamos das 8h às 18h'
        }
    
    # ======================================
```

### Exemplos de uso:

**1. Responder a palavras-chave:**
```python
if 'ajuda' in mensagem:
    return {'tipo': 'ajuda', 'texto': 'Como posso ajudar?'}
```

**2. Usar regex:**
```python
import re
if re.search(r'quanto (custa|é)', mensagem):
    return {'tipo': 'preco', 'texto': 'Veja nossos preços...'}
```

**3. Integrar com APIs:**
```python
import requests
if 'clima' in mensagem:
    resposta = requests.get('https://api.clima.com/...')
    return {'tipo': 'clima', 'texto': resposta.json()['temp']}
```

**4. Integrar com banco de dados:**
```python
if mensagem.startswith('/buscar'):
    resultado = banco.buscar(mensagem)
    return {'tipo': 'busca', 'texto': resultado}
```

---

## 🔌 Endpoints da API

### WebSocket
```
ws://localhost:8000/ws/{user_id}
```

### REST API
- `GET /` - Status da API
- `GET /health` - Health check
- `GET /docs` - Documentação interativa

---

## 🛠️ Estrutura do Projeto

```
app_cell/
├── backend/
│   ├── main.py              # Servidor FastAPI
│   ├── chat_handler.py      # Lógica de respostas (CUSTOMIZE AQUI!)
│   └── requirements.txt     # Dependências Python
│
├── frontend/
│   ├── index.html          # Interface do app
│   ├── style.css           # Estilos
│   ├── app.js              # JavaScript
│   ├── manifest.json       # Configuração PWA
│   └── sw.js               # Service Worker
│
└── README.md
```

---

## 💡 Comandos Disponíveis

Digite no chat:

- `/help` - Lista de comandos
- `/hora` - Hora atual
- `/limpar` - Limpa o histórico

---

## 🔧 Configurações Avançadas

### Alterar porta do servidor:

No arquivo `backend/main.py`, linha final:

```python
uvicorn.run("main:app", host="0.0.0.0", port=8000)
```

### Conectar com servidor remoto:

No arquivo `frontend/app.js`:

```javascript
const CONFIG = {
    WS_URL: 'ws://SEU-IP:8000/ws'
};
```

---

## 📊 Logs e Debug

Logs são salvos em:
- Backend: Console do terminal
- Frontend: Console do navegador (F12)

Para ver logs detalhados:
```python
logging.basicConfig(level=logging.DEBUG)
```

---

## 🎨 Personalizar Interface

Edite `frontend/style.css`:

```css
:root {
    --primary-color: #075e54;    /* Cor principal */
    --accent-color: #25d366;     /* Cor de destaque */
    --bg-color: #e5ddd5;         /* Fundo */
}
```

---

## 🚀 Deploy em Produção

### Opção 1: Railway
1. Faça upload do código no GitHub
2. Conecte no Railway
3. Configure variáveis de ambiente

### Opção 2: Heroku
```bash
heroku create nome-do-app
git push heroku main
```

### Opção 3: VPS próprio
```bash
# Instalar dependências
pip install -r backend/requirements.txt

# Rodar com Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
```

---

## 📝 Licença

MIT - Livre para uso pessoal e comercial

---

## 🤝 Suporte

Problemas? Sugestões? Entre em contato!

**Desenvolvido com ❤️ usando Python + FastAPI + PWA**
