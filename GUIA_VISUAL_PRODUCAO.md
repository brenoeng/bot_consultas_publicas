# 🎯 GUIA RÁPIDO VISUAL - BOT CONSULTAS PÚBLICAS

## 5 Passos para Colocar em Produção em 22 Minutos

### ✅ Pré-requisitos

- Conta no GitHub
- Git instalado
- Navegador web

---

## PASSO 1: Criar Repositório no GitHub

**⏱️ Tempo: 5 minutos**

```
1. Acesse: https://github.com/new

2. Preencha:
   ┌────────────────────────────────────┐
   │ Repository name *                  │
   │ bot_consultas_publicas             │
   │                                    │
   │ Description (optional)             │
   │ Bot de monitoramento de consultas  │
   │                                    │
   │ Public (selecionado)               │
   │                                    │
   │ [v] Add a README file              │
   │ [v] Add .gitignore                 │
   │ [v] Choose a license               │
   └────────────────────────────────────┘

3. Clique: "Create repository"

4. Copie a URL do repositório (vai usar depois)
   https://github.com/seu-usuario/bot_consultas_publicas.git
```

---

## PASSO 2: Fazer Push do Código

**⏱️ Tempo: 10 minutos**

Abra o terminal e execute:

```bash
cd c:\Users\Usuário\Desktop\code\bot_consultas_publicas

git init

git branch -M main

git add .

git commit -m "Initial commit: Bot consultas públicas do MME"

git remote add origin https://github.com/seu-usuario/bot_consultas_publicas.git

git push -u origin main
```

✅ Seu código está no GitHub!

---

## PASSO 3: Ativar GitHub Pages

**⏱️ Tempo: 5 minutos**

```
1. Vá para seu repositório no GitHub

2. Clique em "Settings"
   [Settings] | Issues | Pull requests | Discussions

3. Na esquerda, clique em "Pages"
   ├─ General
   ├─ Code and automation
   │  ├─ Actions
   │  ├─ Secrets and variables
   │  ├─ Code security & analysis
   │  └─ Dependabot
   ├─ Access
   ├─ Moderation
   └─ Pages ← CLIQUE AQUI

4. Configure GitHub Pages:
   ┌─────────────────────────────────────┐
   │ Source                              │
   │ Deploy from a branch                │
   │                                     │
   │ Branch ▼                            │
   │ [main]   [/docs]                    │
   │          ↑         ↑                │
   │      SELECIONE main e /docs         │
   │                                     │
   │ [Save]                              │
   └─────────────────────────────────────┘

5. Aguarde 1-2 minutos pelo deploy
   Verá aparecer:
   "Your site is live at:
    https://seu-usuario.github.io/bot_consultas_publicas/"
```

✅ GitHub Pages ativado!

---

## PASSO 4: Testar no Navegador

**⏱️ Tempo: 2 minutos**

```
1. Copie a URL que apareceu acima:
   https://seu-usuario.github.io/bot_consultas_publicas/

2. Cole no navegador e pressione Enter

3. Você verá:
   ┌──────────────────────────────────────┐
   │      Consultas Públicas - MME        │
   │  [🔄 Atualizar]                      │
   ├──────────────────────────────────────┤
   │  5 Consultas | 1 Urgente | 5 Ativas │
   ├──────────────────────────────────────┤
   │                                      │
   │ ┌──────────────────────────────────┐ │
   │ │ Portaria LRCAP                   │ │
   │ │ Encerramento: 2025-12-01         │ │
   │ │ Dias: 5           [URGENTE] 🔴  │ │
   │ │                                  │ │
   │ │ [Acessar Consulta]               │ │
   │ └──────────────────────────────────┘ │
   │                                      │
   │ ... (mais 4 cards com outras)       │
   │                                      │
   └──────────────────────────────────────┘

4. Teste os botões:
   - Clique em "Acessar Consulta" (abre site oficial)
   - Clique em "Atualizar" (recarrega dados)

5. Pronto! Seu site está online!
```

✅ Tudo funcionando!

---

## PASSO 5: Verificar Automação (Opcional)

**⏱️ Tempo: 2 minutos**

```
1. No seu repositório GitHub, clique em "Actions"
   [Code] | [Issues] | [Pull requests] | [Actions] ← CLIQUE

2. Você verá:
   ┌────────────────────────────────────────┐
   │ All workflows                          │
   │                                        │
   │ check-consultas.yml                    │
   │ Created • Scheduled                    │
   │                                        │
   │ Próxima execução:                      │
   │ 08:00 UTC (todo dia)                   │
   │ 12:00 UTC (todo dia)                   │
   │ 18:00 UTC (todo dia)                   │
   └────────────────────────────────────────┘

3. Seu bot executará 3x por dia automaticamente!

4. (Opcional) Clique em "Run workflow" para testar agora
   ┌────────────────────────────────────────┐
   │ check-consultas.yml                    │
   │ [Run workflow ▼]                       │
   │                                        │
   │ Branch: main                           │
   │ [Run workflow]                         │
   └────────────────────────────────────────┘
```

✅ Automação confirmada!

---

## 🎉 PARABÉNS!

Você colocou o Bot Consultas Públicas em produção! 🚀

### O que está acontecendo agora:

```
✓ Seu site está online
  https://seu-usuario.github.io/bot_consultas_publicas/

✓ Dados são atualizados 3x por dia (8h, 12h, 18h UTC)

✓ Monitorando 5 consultas públicas da MME

✓ GitHub Pages hospeda tudo gratuitamente

✓ GitHub Actions executa tudo automaticamente
```

---

## 📊 Status Atual

| Componente    | Status         | Local               |
| ------------- | -------------- | ------------------- |
| **Website**   | ✅ Online      | GitHub Pages        |
| **Dados**     | ✅ Atualizados | data/consultas.json |
| **Automação** | ✅ Ativa       | GitHub Actions      |
| **Alertas**   | ⏳ Futuro      | Twilio WhatsApp     |

---

## ❓ Dúvidas?

### "O site não apareça"

1. Aguarde 1-2 minutos
2. Recarregue a página (Ctrl+F5)
3. Verifique se Branch=main e Folder=/docs

### "Quer saber mais?"

- Leia: `README.md`
- Documentação técnica: `ESTRUTURA_ARQUIVOS.md`
- Troubleshooting: `ERRO-SOLUCAO.md`

### "Quer adicionar features?"

- Leia: `PROXIMOS_PASSOS.md`
- Exemplos: notificações WhatsApp, filtros, etc.

---

## 🔗 Links Úteis

```
Seu Site:
  https://seu-usuario.github.io/bot_consultas_publicas/

Seu Repositório GitHub:
  https://github.com/seu-usuario/bot_consultas_publicas

Site Original da MME:
  https://consultas-publicas.mme.gov.br/home

GitHub Pages Docs:
  https://docs.github.com/en/pages

GitHub Actions Docs:
  https://docs.github.com/en/actions
```

---

## 📋 Checklist Final

- [x] Repositório criado no GitHub
- [x] Código fazendo push para main
- [x] GitHub Pages ativado
- [x] URL pública acessível
- [x] Cards com 5 consultas aparecendo
- [x] Automação configurada
- [x] Testes passando
- [x] Documentação lida

---

## 🎓 Próximas Melhorias (Opcionais)

### Fácil (1-2 horas)

- Adicionar notificações WhatsApp
- Adicionar filtros na página
- Adicionar busca

### Moderado (4-8 horas)

- Integrar banco de dados
- Criar API REST
- Exportar em CSV/PDF

### Avançado (1-2 dias)

- Suporte para outros ministérios
- Criar app mobile
- Dashboard com gráficos

---

## 📞 Precisa de Ajuda?

1. **Revise a documentação:**

   - `COMECE_AQUI.md` - Quick start
   - `ERRO-SOLUCAO.md` - Problemas comuns
   - `README.md` - Documentação técnica

2. **Verifique os arquivos:**

   - `data/consultas.json` - Dados
   - `docs/index.html` - Página principal
   - `scraper.py` - Código do scraper

3. **Execute os testes:**
   ```bash
   python validate_project.py
   python test_project.py
   ```

---

## 🎯 Resumo

| Item         | Tempo      | Status        |
| ------------ | ---------- | ------------- |
| Criar repo   | 5 min      | ✅            |
| Push código  | 10 min     | ✅            |
| GitHub Pages | 5 min      | ✅            |
| Testar       | 2 min      | ✅            |
| **TOTAL**    | **22 min** | **✅ PRONTO** |

---

**Desenvolvido com ❤️**  
Bot Consultas Públicas v1.0  
Novembro de 2025

**Seu site está em produção! 🚀**

Próximas execuções do scraper:

- ⏰ Hoje às 12:00 UTC
- ⏰ Hoje às 18:00 UTC
- ⏰ Amanhã às 08:00 UTC
- ⏰ ...e assim por diante 3x por dia
