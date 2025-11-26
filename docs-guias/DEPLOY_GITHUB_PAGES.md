# 🚀 Deploy no GitHub Pages - Guia Completo

## Objetivo

Publicar o bot na internet via GitHub Pages para que qualquer pessoa possa acessar as consultas públicas em tempo real.

---

## 📋 PRÉ-REQUISITOS

- [ ] Conta GitHub
- [ ] Git instalado localmente
- [ ] Projeto clonado ou criado
- [ ] Todos os arquivos prontos

---

## 🔧 PASSO 1: Preparar Repositório GitHub

### 1.1 Criar novo repositório

1. Acesse https://github.com/new
2. Nome: `bot_consultas_publicas` (ou seu nome)
3. Descrição: "Bot de monitoramento de consultas públicas do MME"
4. Escolha: **Public** (para acessar via GitHub Pages)
5. ✅ **Create repository**

### 1.2 Você verá instruções. Siga estas (no seu terminal):

```bash
# Navegar para pasta do projeto
cd /c/Users/Usuário/Desktop/code/bot_consultas_publicas

# Inicializar git (se ainda não tem)
git init

# Adicionar origem remota
git remote add origin https://github.com/SEU_USUARIO/bot_consultas_publicas.git

# Renomear branch para main (se necessário)
git branch -M main

# Adicionar todos os arquivos
git add .

# Fazer primeiro commit
git commit -m "feat: bot consultas públicas inicial"

# Fazer push para GitHub
git push -u origin main
```

**Substituir `SEU_USUARIO` pelo seu username do GitHub!**

---

## 🌐 PASSO 2: Ativar GitHub Pages

### 2.1 No GitHub (Website)

1. Vá para seu repositório: https://github.com/SEU_USUARIO/bot_consultas_publicas
2. Clique em **Settings** (ícone de engrenagem)
3. No menu esquerdo, procure por **Pages** (pode estar em "Code and automation")
4. Você verá:

```
Source
Choose a publishing source
```

### 2.2 Configurar Source

1. **Branch**: Selecione `main`
2. **Folder**: Selecione `/docs`
3. Clique em **Save**

Você verá:

```
Your site is ready to be published at:
https://seu-usuario.github.io/bot_consultas_publicas/
```

### 2.3 Aguardar Deploy (1-2 minutos)

A página está sendo construída. Você verá:

- 🟡 **Yellow** = Em construção
- 🟢 **Green** = Pronto!

---

## ✅ PASSO 3: Acessar a Página

Assim que ficar verde, acesse:

```
https://seu-usuario.github.io/bot_consultas_publicas/
```

Você deve ver:

- ✅ Página com título "Consultas Públicas"
- ✅ Cards das 5 consultas
- ✅ Estatísticas no topo
- ✅ Botão "Atualizar"

---

## 🔄 PASSO 4: Testar Atualização de Dados

### 4.1 Executar Scraper Localmente

```bash
# Estar na pasta do projeto
cd /c/Users/Usuário/Desktop/code/bot_consultas_publicas

# Instalar dependências (primeira vez)
pip install -r requirements.txt

# Executar scraper
python scraper.py
```

**Esperado:**

```
[OK] Página carregada com Selenium
[+] Consulta 206: ...
[+] Consulta 205: ...
[+] Consulta 204: ...
[+] Consulta 203: ...
[+] Consulta 202: ...
Total de consultas extraídas: 5
[OK] Dados salvos em data/consultas.json
```

### 4.2 Validar JSON

```bash
# Verificar se JSON é válido
python -m json.tool data/consultas.json | head -30
```

### 4.3 Fazer Push para GitHub

```bash
# Adicionar dados atualizados
git add data/consultas.json

# Fazer commit
git commit -m "update: dados de consultas atualizados"

# Fazer push
git push origin main
```

### 4.4 Atualizar Página

Espere 30 segundos e acesse novamente:

```
https://seu-usuario.github.io/bot_consultas_publicas/
```

Clique em **Atualizar** (botão na página) e veja os dados aparecerem!

---

## 🤖 PASSO 5: Ativar Automação (GitHub Actions)

### 5.1 O que já está configurado

O arquivo `.github/workflows/check-consultas.yml` já contém:

- ✅ Agendamento 3x por dia (08:00, 12:00, 18:00 UTC)
- ✅ Auto-run do scraper
- ✅ Auto-commit dos dados
- ✅ Auto-deploy

### 5.2 Verificar se está ativo

1. Acesse seu repositório no GitHub
2. Vá em **Actions** (aba superior)
3. Você deve ver:
   - "check-consultas" workflow
   - Execuções agendadas
   - Status: ✅ **Success** (se tudo ok) ou ❌ **Failed** (se erro)

### 5.3 Se falhar, verificar erros

Clique na execução que falhou:

1. Vá em **Jobs > scraper**
2. Veja os logs de erro
3. Procure a linha com erro específico

**Erros comuns:**

- ❌ Chrome não instalado → Instalar Google Chrome
- ❌ Timeout → Aumentar timeout em `scraper.py`
- ❌ JSON inválido → Verificar estrutura

---

## 📊 PASSO 6: Monitorar Execuções

### 6.1 Verificar logs

1. Vá em **Actions**
2. Clique no workflow mais recente
3. Veja **Build log** com detalhes completos

### 6.2 Exemplos de sucesso

```
2025-11-26 08:00:15 - INFO - [1/4] Buscando página do site...
2025-11-26 08:00:20 - INFO - [OK] Página carregada com Selenium
2025-11-26 08:00:21 - INFO - [+] Consulta 206
2025-11-26 08:00:21 - INFO - Total de consultas extraídas: 5
2025-11-26 08:00:22 - INFO - [OK] Dados salvos
```

### 6.3 Verificar dados

Acesse via navegador:

```
https://raw.githubusercontent.com/seu-usuario/bot_consultas_publicas/main/data/consultas.json
```

Você verá o JSON com os dados em tempo real!

---

## 🧪 PASSO 7: Testar Funcionalidades

### 7.1 Página Carrega?

- ✅ Abra https://seu-usuario.github.io/bot_consultas_publicas/
- ✅ Veja cards das consultas
- ✅ Verifique cores (verde/amarelo/vermelho)

### 7.2 Dados Aparecem?

- ✅ Clique em "Atualizar"
- ✅ Veja títulos das consultas
- ✅ Verifique datas de encerramento

### 7.3 Links Funcionam?

- ✅ Clique em "Acessar" em qualquer card
- ✅ Deve abrir página da consulta no MME

### 7.4 Estatísticas

- ✅ Verifique contador total de consultas
- ✅ Veja dias restantes para cada uma

---

## 🔐 PASSO 8: Configurar Secrets (Opcional - Para WhatsApp)

Se quiser notificações WhatsApp no futuro:

### 8.1 No GitHub

1. Acesse seu repositório
2. **Settings > Secrets and variables > Actions**
3. Clique **New repository secret**

### 8.2 Adicionar secrets

Quando implementar Twilio, adicione:

```
TWILIO_ACCOUNT_SID = seu_account_sid
TWILIO_AUTH_TOKEN = seu_auth_token
TWILIO_WHATSAPP_NUMBER = +55...
WHATSAPP_TARGET = +55...
```

**NÃO colocar esses valores em arquivos do repositório!** Apenas em Secrets.

---

## 📱 PASSO 9: Compartilhar

### 9.1 URL Para Compartilhar

```
https://seu-usuario.github.io/bot_consultas_publicas/
```

### 9.2 Compartilhe com:

- ✅ Colegas de trabalho
- ✅ Gerentes
- ✅ Stakeholders
- ✅ Público interessado

---

## ❌ TROUBLESHOOTING

### Página não carrega

**Solução:**

1. Verificar se em **Settings > Pages** está corretamente configurado
2. Aguardar 2-3 minutos após primeiro push
3. Limpar cache do navegador (Ctrl+Shift+Delete)
4. Tentar em navegador privado

### Dados não aparecem

**Solução:**

1. Verificar se `data/consultas.json` existe
2. Abrir DevTools (F12) > Console
3. Verificar se há erro JavaScript
4. Executar scraper localmente: `python scraper.py`

### Workflow não executa

**Solução:**

1. Verificar se `.github/workflows/check-consultas.yml` existe
2. Ir em **Actions** e ativar workflows manualmente
3. Clicar em **"I understand my workflows and want to enable them"**

### Erro de autenticação ao fazer push

**Solução:**

```bash
# Resetar credenciais
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Ou usar SSH ao invés de HTTPS
git remote set-url origin git@github.com:seu-usuario/bot_consultas_publicas.git
```

---

## 📋 CHECKLIST FINAL

### Antes de Publicar

- [ ] Todos os arquivos estão no lugar
- [ ] `data/consultas.json` tem dados válidos
- [ ] `docs/index.html` existe
- [ ] `.github/workflows/check-consultas.yml` existe
- [ ] Git está inicializado e configurado

### Publicar

- [ ] Criar repositório GitHub
- [ ] Fazer push inicial (git push)
- [ ] Ativar GitHub Pages (Settings > Pages)
- [ ] Aguardar deploy (1-2 min)

### Validar

- [ ] Página carrega em HTTPS
- [ ] Cards aparecem com dados
- [ ] Cores estão corretas
- [ ] Links funcionam
- [ ] Botão "Atualizar" funciona

### Automação

- [ ] Workflow aparece em Actions
- [ ] Agendamento está correto (3x/dia)
- [ ] Execução foi bem-sucedida
- [ ] Dados foram atualizados automaticamente

### Finalizar

- [ ] Compartilhar URL com stakeholders
- [ ] Comunicar que está em produção
- [ ] Monitorar execuções semanalmente

---

## 🎯 VOCÊ AGORA TEM

✅ **Site publicado** na internet  
✅ **Dados atualizados automaticamente** 3x por dia  
✅ **Página responsiva** em qualquer dispositivo  
✅ **Compartilhável** com qualquer pessoa

---

## 🔗 Links Úteis

- [Seu repositório](https://github.com/seu-usuario/bot_consultas_publicas)
- [Sua página](https://seu-usuario.github.io/bot_consultas_publicas/)
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

**Parabéns! Seu bot está no ar! 🚀**

Qualquer dúvida, consulte a documentação em `ERRO-SOLUCAO.md`
