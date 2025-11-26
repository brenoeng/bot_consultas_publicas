# Bot Consultas Públicas ���

Bot para monitorar consultas públicas do MME (Ministério de Minas e Energia). Interface simples com HTML, CSS e Tailwind - sem dependências Node.js!

## ��� O que faz

- ��� **Página estática** com cards das consultas públicas abertas
- ��� **Scraper interativo** em HTML para gerenciar dados
- ��� **Notificador WhatsApp** - configurável via interface
- ��� **100% Responsivo** - funciona em todos os dispositivos
- ��� **GitHub Pages** - deploy automático

## ���️ Arquitetura

```
docs/index.html          ← Página principal (GitHub Pages)
scraper.html             ← Ferramenta gerenciar dados
notifier.html            ← Configurar notificações
data/consultas.json      ← Arquivo de dados (JSON)
```

## ��� Como Usar

### 1️⃣ Visualizar Página Principal

**Localmente:**

```bash
# Abra no navegador o arquivo docs/index.html
```

**GitHub Pages (após push):**

```
https://seu-usuario.github.io/bot_consultas_publicas/
```

### 2️⃣ Adicionar Dados de Consultas

Abra `scraper.html` no navegador:

```bash
# Clique em "Carregar Dados de Teste"
# Clique em "Iniciar Scraper"
# Download do arquivo consultas.json
# Salve em: data/consultas.json
```

Ou edite `data/consultas.json` manualmente.

### 3️⃣ Configurar Notificações WhatsApp

Abra `notifier.html` no navegador:

```bash
# Preencha credenciais Twilio
# Salve configuração
# Teste mensagens
```

## ��� Estrutura

```
bot_consultas_publicas/
├── docs/
│   └── index.html              # ��� Página principal
├── data/
│   └── consultas.json          # ��� Dados das consultas
├── scraper.html                # ��� Ferramenta de dados
├── notifier.html               # ��� Gerenciador WhatsApp
├── .env.example                # ⚙️ Configuração
├── .gitignore                  # Git
└── README.md                   # Este arquivo
```

## ��� Estrutura do JSON

```json
{
  "consultas": [
    {
      "id": "consulta_001",
      "titulo": "Consulta Pública nº 42/2025",
      "descricao": "Descrição breve...",
      "data_abertura": "2025-11-26",
      "data_encerramento": "2025-12-10",
      "url_oficial": "https://...",
      "dias_restantes": 14,
      "notificado": false
    }
  ],
  "ultimaAtualizacao": "2025-11-26T08:00:00Z"
}
```

## ��� Cores dos Cards

- ��� **Verde**: Mais de 7 dias
- ��� **Amarelo**: 1-7 dias (atenção!)
- ��� **Vermelho**: 0 dias ou vencido

## �� Habilitar GitHub Pages

1. Vá para **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** | Folder: **/docs**
4. Clique **Save**

Sua página estará em: `https://seu-usuario.github.io/bot_consultas_publicas/`

## ��� Configuração Manual

Se quiser editar dados manualmente:

1. Abra `data/consultas.json`
2. Adicione/remova consultas no array `consultas`
3. Mantenha formato de datas: `YYYY-MM-DD`
4. Salve o arquivo
5. Commit e push
6. GitHub Pages atualiza automaticamente

## ��� Troubleshooting

### Página em branco

- Verifique se `data/consultas.json` existe
- Verifique formato do JSON (teste em https://jsonlint.com/)
- Abra DevTools (F12) e veja console para erros

### Dados não aparecem

- Confirme que está usando `fetch('data/consultas.json')`
- Teste localmente com live server
- Verifique CORS no navegador

### GitHub Pages não atualiza

- Confirme que `docs/index.html` foi commitado
- Aguarde ~1 minuto para propagação
- Limpe cache (Ctrl+Shift+Delete)
- Verifique em Settings → Pages se está ativado

## ��� Notificações WhatsApp (Futuro)

Para implementar notificações automáticas:

1. Crie conta no [Twilio.com](https://twilio.com)
2. Configure WhatsApp Messaging
3. Use `notifier.html` para testar
4. Integre com GitHub Actions para automatizar

Ou use serviço de scheduler externo (AWS Lambda, Heroku, etc).

## ��� Tecnologias

- **HTML5**: Semântica moderna
- **CSS3**: Estilos nativos
- **Tailwind CSS**: Framework via CDN (sem build!)
- **JavaScript Vanilla**: Sem frameworks
- **Fetch API**: Requisições HTTP
- **LocalStorage**: Persistência no navegador

## ��� Aprender Mais

- [Tailwind CSS Docs](https://tailwindcss.com/)
- [MDN JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/)
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp)

## ��� Licença

MIT

## ��� Contribuir

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit (`git commit -m 'feat: adiciona X'`)
4. Push (`git push origin feature/nova-feature`)
5. Abra PR

---

**Desenvolvido com ❤️ para monitorar consultas públicas do MME**
