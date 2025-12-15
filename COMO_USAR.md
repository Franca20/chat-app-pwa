# 🎯 GUIA RÁPIDO - Como Usar o Chat App

## ⚡ Início Rápido (3 minutos)

### Passo 1: Instalar dependências
```bash
cd c:\programacao\app_cell\backend
pip install -r requirements.txt
```

### Passo 2: Iniciar o servidor
```bash
python main.py
```

Você verá:
```
🚀 Iniciando Chat App Backend
📡 Servidor: http://localhost:8000
```

### Passo 3: Abrir o app
Abra o arquivo `frontend/index.html` no navegador ou:

```bash
cd c:\programacao\app_cell\frontend
python -m http.server 8080
```

Acesse: `http://localhost:8080`

---

## 📱 Testar no Celular

### Opção 1: Mesma rede WiFi
1. Descubra seu IP local:
   ```bash
   ipconfig
   # Procure por "Endereço IPv4": 192.168.X.X
   ```

2. No celular, acesse: `http://192.168.X.X:8080`

### Opção 2: Usar ngrok (mais fácil)
```bash
# Instale: https://ngrok.com/download
ngrok http 8000

# Copie o endereço HTTPS gerado
# Atualize em frontend/app.js:
WS_URL: 'wss://seu-endereco.ngrok.io/ws'
```

---

## 🎨 Customizar Respostas

Abra `backend/chat_handler.py` e adicione suas regras:

### Exemplo 1: Resposta simples
```python
if 'oi' in mensagem:
    return {
        'tipo': 'saudacao',
        'texto': 'Olá! Como posso ajudar? 👋'
    }
```

### Exemplo 2: Comando personalizado
```python
if mensagem.startswith('/preco'):
    produto = mensagem.replace('/preco', '').strip()
    return {
        'tipo': 'consulta',
        'texto': f'O preço de {produto} é R$ 100,00'
    }
```

### Exemplo 3: Integração com banco de dados
```python
import sqlite3

if mensagem.startswith('/buscar'):
    termo = mensagem.replace('/buscar', '').strip()
    conn = sqlite3.connect('dados.db')
    resultado = conn.execute('SELECT * FROM produtos WHERE nome=?', (termo,))
    return {
        'tipo': 'busca',
        'texto': f'Resultado: {resultado}'
    }
```

### Exemplo 4: API externa
```python
import requests

if 'clima' in mensagem:
    resposta = requests.get('https://api.openweathermap.org/...')
    dados = resposta.json()
    return {
        'tipo': 'clima',
        'texto': f'Temperatura: {dados["temp"]}°C'
    }
```

---

## 🔧 Solução de Problemas

### "WebSocket não conecta"
✅ Verifique se o backend está rodando  
✅ Confira se a URL em `app.js` está correta  
✅ Desabilite firewall temporariamente

### "App não instala no celular"
✅ Use HTTPS (ngrok fornece isso)  
✅ Use Chrome/Safari atualizado  
✅ Verifique se o manifest.json está correto

### "Mensagens não aparecem"
✅ Abra o Console (F12) e veja erros  
✅ Verifique logs do backend  
✅ Teste se o WebSocket está conectado (indicador verde)

---

## 🚀 Próximos Passos

1. **Adicione autenticação de usuários**
2. **Salve conversas em banco de dados**
3. **Adicione notificações push**
4. **Integre com IA (ChatGPT, Gemini)**
5. **Adicione envio de imagens/arquivos**

---

## 💡 Dicas Úteis

- Use `/help` no chat para ver comandos
- Logs aparecem no terminal do backend
- Console do navegador (F12) mostra erros do frontend
- Edite `style.css` para mudar cores e visual
- Teste em modo incógnito para ver mudanças

---

Pronto para começar? Execute os comandos acima! 🎉
