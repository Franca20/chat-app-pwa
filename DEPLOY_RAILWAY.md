# 🚂 Deploy no Railway - Guia Completo

## 📋 Pré-requisitos

1. Conta no GitHub (gratuita)
2. Conta no Railway (gratuita) - https://railway.app
3. Git instalado no PC

---

## 🚀 Passo a Passo

### 1️⃣ Preparar o projeto para Git

```powershell
cd c:\programacao\app_cell

# Inicializar Git (se ainda não fez)
git init

# Criar .gitignore
echo "__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
.env
.venv/
venv/
*.log" > .gitignore

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Deploy inicial - Chat App"
```

### 2️⃣ Criar repositório no GitHub

1. Acesse https://github.com/new
2. Nome: `chat-app-pwa`
3. Deixe **público** ou **privado**
4. **NÃO** marque "Add README"
5. Clique em "Create repository"

### 3️⃣ Enviar código para GitHub

Copie os comandos que aparecem no GitHub (segunda opção: "...or push an existing repository"):

```powershell
git remote add origin https://github.com/SEU-USUARIO/chat-app-pwa.git
git branch -M main
git push -u origin main
```

### 4️⃣ Deploy no Railway

1. Acesse https://railway.app
2. Faça login com GitHub
3. Clique em **"New Project"**
4. Selecione **"Deploy from GitHub repo"**
5. Escolha o repositório `chat-app-pwa`
6. Railway vai detectar Python automaticamente

### 5️⃣ Configurar variáveis (se necessário)

No painel do Railway:
- Clique em **"Variables"**
- Adicione se precisar de variáveis de ambiente

### 6️⃣ Obter URL pública

1. No Railway, vá em **"Settings"**
2. Clique em **"Generate Domain"**
3. Copie a URL gerada (ex: `chat-app-xxx.up.railway.app`)

### 7️⃣ Atualizar frontend para produção

A URL do WebSocket já está configurada para detectar automaticamente!

O frontend funciona tanto local quanto em produção.

---

## 📱 Hospedar Frontend

### Opção 1: GitHub Pages (GRÁTIS)

```powershell
cd c:\programacao\app_cell

# Criar branch gh-pages
git checkout -b gh-pages

# Copiar frontend para raiz
copy frontend\* .

# Commit e push
git add .
git commit -m "Deploy frontend"
git push origin gh-pages
```

Depois no GitHub:
1. Vá em **Settings** > **Pages**
2. Source: `gh-pages` branch
3. Salvar

Seu app ficará em: `https://SEU-USUARIO.github.io/chat-app-pwa/`

### Opção 2: Vercel (GRÁTIS e MAIS FÁCIL)

1. Acesse https://vercel.com
2. Login com GitHub
3. **Import Project** > Selecione seu repositório
4. **Root Directory**: `frontend`
5. Deploy!

### Opção 3: Netlify (GRÁTIS)

1. Acesse https://netlify.com
2. Arraste a pasta `frontend` para o site
3. Pronto!

---

## 🔧 Atualizar o app

Sempre que fizer alterações:

```powershell
git add .
git commit -m "Descrição da mudança"
git push
```

Railway faz deploy automático! ✨

---

## 📊 Monitorar o app

No Railway:
- **Logs**: Ver logs em tempo real
- **Metrics**: CPU, RAM, requests
- **Deployments**: Histórico de deploys

---

## 💰 Custos

**Railway Free Tier:**
- ✅ $5 USD de créditos grátis por mês
- ✅ Suficiente para apps pequenos
- ✅ Sleep após inatividade (economiza créditos)

**Para evitar custos:**
- Use sleep mode (ativa automaticamente)
- Ou use Railway + Vercel (frontend grátis)

---

## 🎯 Estrutura Final

```
Backend (Railway):  https://chat-app-xxx.up.railway.app
Frontend (Vercel):  https://chat-app-xxx.vercel.app

Celular acessa: https://chat-app-xxx.vercel.app
WebSocket conecta: wss://chat-app-xxx.up.railway.app/ws
```

---

## 🐛 Troubleshooting

### "Build failed"
- Verifique o `requirements.txt`
- Veja os logs no Railway

### "WebSocket não conecta"
- Certifique-se que o backend está rodando
- Veja a URL do WebSocket no console (F12)

### "App muito lento"
- Railway free pode ter cold start (primeiro acesso demora)
- Considere plano pago se precisar

---

## ✅ Checklist Final

- [ ] Código no GitHub
- [ ] Backend no Railway
- [ ] Frontend no Vercel/GitHub Pages
- [ ] WebSocket conectando
- [ ] App funcionando no celular
- [ ] Instalável como PWA

Pronto! Seu app está online 24/7! 🎉
