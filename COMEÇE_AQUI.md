# 🚀 Comece Aqui!

## ✅ Seu projeto está pronto!

Este é um **bot de monitoramento de consultas públicas** do MME. Tudo em HTML, CSS e Tailwind - **nada de Node.js**!

## 📋 Primeiros Passos (5 minutos)

### 1. Abra a página principal

Clique duplo em `docs/index.html` ou arraste para seu navegador.

Você verá:

- ✅ Cards das consultas com cores (verde/amarelo/vermelho)
- ✅ Estatísticas em tempo real
- ✅ Botão "Atualizar" para recarregar

### 2. Carregue dados de teste

1. Abra `scraper.html` no navegador
2. Clique **"Carregar Dados de Teste"**
3. Clique **"Iniciar Scraper"**
4. Clique **"Download"** para salvar `consultas.json`
5. **Salve** em `data/` (mantendo o nome `consultas.json`)
6. Volte para `docs/index.html` e clique **"Atualizar"**

Pronto! Os dados aparecem na página principal.

### 3. (Opcional) Configure notificações

1. Abra `notifier.html`
2. Preencha suas credenciais Twilio (você precisa de uma conta)
3. Teste enviando uma notificação
4. Veja o preview da mensagem em tempo real

## 🎯 Estrutura Rápida

```
📁 bot_consultas_publicas
├─ 📄 docs/index.html           ← PÁGINA PRINCIPAL (abra isso!)
├─ 🔍 scraper.html              ← Para gerenciar dados
├─ 💬 notifier.html             ← Para WhatsApp
├─ 📊 data/consultas.json       ← Arquivo de dados
├─ 📖 README.md                 ← Documentação completa
└─ 📋 COMEÇE_AQUI.md            ← Este arquivo
```

## 📊 Adicionar suas próprias consultas

Edite `data/consultas.json` manualmente:

```json
{
  "consultas": [
    {
      "id": "sua_consulta_1",
      "titulo": "Consulta sobre Energias",
      "descricao": "Descrição breve",
      "data_abertura": "2025-11-26",
      "data_encerramento": "2025-12-10",
      "url_oficial": "https://exemplo.com",
      "dias_restantes": 14,
      "notificado": false
    }
  ],
  "ultimaAtualizacao": "2025-11-26T10:00:00Z"
}
```

**Dicas:**

- Datas sempre em formato `YYYY-MM-DD`
- Cores: verde (>7 dias), amarelo (1-7), vermelho (≤0)
- `notificado: false` = ainda não foi alertado

## 🌐 Publicar no GitHub Pages

Se já tem um repositório GitHub:

### 1. Faça push para GitHub

```bash
git add .
git commit -m "feat: adiciona bot consultas públicas"
git push origin main
```

### 2. Ative GitHub Pages

1. Vá em **Settings → Pages**
2. Escolha:
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/docs**
3. Clique **Save**

### 3. Aguarde 1-2 minutos

Sua página estará em:

```
https://seu-usuario.github.io/bot_consultas_publicas/
```

## 🎨 Personalizar

### Cores dos cards

Edite `docs/index.html`, procure por `.badge`:

```css
.badge.green {
  background: verde;
} /* >7 dias */
.badge.yellow {
  background: amarelo;
} /* 1-7 dias */
.badge.red {
  background: vermelho;
} /* ≤0 dias */
```

### Título e descrição

Na página `docs/index.html`, edite:

- `<h1>` para título
- `<p class="text-blue-100">` para descrição

## 💬 Ativar WhatsApp

Se quer notificações automáticas:

1. Crie conta em [Twilio.com](https://twilio.com)
2. Ative WhatsApp em Messaging
3. Preencha em `notifier.html`
4. (Futuro) Integre com GitHub Actions

## 📚 Próximos Passos

- [ ] Adicionar suas consultas em `data/consultas.json`
- [ ] Fazer push para GitHub
- [ ] Ativar GitHub Pages
- [ ] Compartilhar a URL com interessados
- [ ] (Opcional) Configurar notificações WhatsApp

## ❓ Dúvidas?

- **Página não carrega?** → Verifique se `data/consultas.json` existe
- **Dados não aparecem?** → Abra DevTools (F12) e veja console
- **JSON inválido?** → Teste em [jsonlint.com](https://jsonlint.com)

## 📖 Documentação Completa

Leia `README.md` para mais detalhes técnicos.

---

**Desenvolvido com ❤️ para monitorar consultas públicas do MME**

🎉 **Divirta-se e boa sorte com seu projeto!**
