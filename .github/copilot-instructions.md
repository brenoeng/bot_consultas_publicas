# Instruções para Agentes de IA - bot_consultas_publicas

## Visão Geral do Projeto

Bot que monitora consultas públicas abertas em https://consultas-publicas.mme.gov.br/home, exibe em página GitHub Pages com cards mostrando título e prazo, e notifica via WhatsApp quando faltam 7 dias para encerramento.

**Componentes principais:**
- **Scraper**: Coleta dados do site do MME (Ministério de Minas e Energia)
- **Data Storage**: Armazena consultas em JSON
- **GitHub Pages Frontend**: Página simples com HTML/CSS/Tailwind com cards de consultas ativas
- **Notificação WhatsApp**: Envia alertas com 7 dias de antecedência via Twilio
- **Scheduler**: Executa scraper periodicamente via GitHub Actions (diariamente)

## Arquitetura e Fluxo de Dados

### Fluxo Principal
1. **Scraper** coleta consultas públicas do site oficial
2. Dados persistem em `data/consultas.json` ou banco de dados
3. **Data Processing** identifica:
   - Novas consultas (para adicionar)
   - Consultas que expiram em 7 dias (para notificar)
   - Consultas encerradas (para remover/arquivar)
4. **WhatsApp Notifier** envia mensagens para contatos cadastrados
5. **GitHub Pages** gera HTML estático com cards das consultas ativas

### Estrutura de Dados - Consulta
```json
{
  "id": "único_identificador",
  "titulo": "Título da Consulta",
  "descricao": "Descrição breve",
  "data_abertura": "YYYY-MM-DD",
  "data_encerramento": "YYYY-MM-DD",
  "url_oficial": "link_para_site_oficial",
  "dias_restantes": 7,
  "notificado": false
}
```

## Padrões de Desenvolvimento

### Web Scraping
- **Site**: https://consultas-publicas.mme.gov.br/home - analisar estrutura HTML para extrair cards de consultas
- Use BeautifulSoup (Python) ou Cheerio (Node.js) para parsing HTML
- Extrair de cada consulta: título, data abertura, data encerramento, descrição e URL oficial
- Implemente retry logic (máx 3 tentativas) para falhas de rede com backoff exponencial
- Adicionar delays entre requisições (2-3 segundos) para respeitar rate limiting
- Validar que todas as datas estão no formato YYYY-MM-DD antes de persistir
- Sempre valide que nenhum campo obrigatório está vazio

### Persistência de Dados
- Guarde consultas em `data/consultas.json` com schema validado
- Implemente deduplicação por ID da consulta oficial
- Mantenha histórico de consultas encerradas (archive)
- Sincronize estado local com dados atualizados do site

### Notificações WhatsApp
- Use Twilio API ou similar para enviar mensagens
- Template de mensagem: `"[ALERTA] '{titulo}' encerra em 7 dias - {data_encerramento} - {url}"`
- Rastreie `notificado: true` para não reenviar
- Log de todas as notificações enviadas
- Trate erros de envio com retry exponencial

### Frontend GitHub Pages (HTML + CSS + Tailwind)
- Gere HTML estático em `docs/index.html` a partir de `data/consultas.json`
- Use **Tailwind CSS** para estilo dos cards (sem build, use CDN)
- Cards exibem: **Título**, **Data de Encerramento**, **Dias Restantes** com cores:
  - Verde (badge): `bg-green-100 text-green-800` para dias > 7
  - Amarelo (badge): `bg-yellow-100 text-yellow-800` para dias 1-7
  - Vermelho (badge): `bg-red-100 text-red-800` para dias ≤ 0
- Cada card tem botão "Acessar" linkando para `url_oficial`
- Layout: Grid responsivo `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- Ordenar por dias_restantes (menor primeiro) para alertar primeiro os que vencem logo
- Deploy automático via GitHub Actions ao atualizar `data/consultas.json`

## Fluxo de Execução

### Scheduler (cron job ou GitHub Actions)
```
Todo dia às 08:00 UTC:
1. Executar scraper
2. Atualizar data/consultas.json
3. Verificar consultas com 7 dias (e notificado=false)
4. Enviar notificações WhatsApp
5. Gerar/atualizar páginas HTML
6. Commit e push para main (GitHub Pages auto-deploy)
```

### Exemplo Workflow GitHub Actions (`.github/workflows/check-consultas.yml`)
- Trigger: schedule (cron) ou push
- Steps: scraper → validação → notificações → build HTML → deploy
- Secrets: credentials WhatsApp, tokens, etc.

## Convenções de Código

### Arquivos Principais
- `src/scraper.js` ou `src/scraper.py` - Coleta dados de https://consultas-publicas.mme.gov.br/home
- `src/notifier.js` ou `src/notifier.py` - Integração WhatsApp via Twilio
- `src/page_generator.js` ou `src/page_generator.py` - Gera HTML estático com Tailwind
- `data/consultas.json` - Arquivo de estado com consultas atualizadas
- `docs/index.html` - Página GitHub Pages final (gerada automaticamente)
- `.github/workflows/check-consultas.yml` - Pipeline de execução automática
- `package.json` (se Node.js) ou `requirements.txt` (se Python)

### Tratamento de Erros
- Capture erros de rede em scraper com retry (máx 3 tentativas, backoff exponencial)
- Log estruturado em JSON para debugging
- Notificações de falha devem ir para logs, não interromper execução
- Validação de dados antes de persistir (schema JSON ou Pydantic)

### Variáveis de Ambiente
```bash
# Twilio WhatsApp
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token
TWILIO_PHONE_NUMBER=+55_seu_numero  # Número Twilio verificado

# Contatos para notificação (múltiplos separados por vírgula)
WHATSAPP_TARGETS=+55_numero1,+55_numero2

# Site oficial
CONSULTAS_URL=https://consultas-publicas.mme.gov.br/home

# Dias para alertar (padrão: 7)
ALERT_DAYS=7

# Logging
LOG_LEVEL=info  # debug, info, warn, error
```

## Pontos de Integração

### Site Oficial de Consultas Públicas
- **URL**: https://consultas-publicas.mme.gov.br/home
- **Ministério**: MME (Ministério de Minas e Energia)
- **Auth**: Sem autenticação necessária (site público)
- **Rate Limiting**: Adicionar delays 2-3s entre requisições
- **Estrutura HTML**: Analisar página para identificar:
  - Seletores CSS dos cards de consultas
  - Atributos de data (abertura/encerramento)
  - Links para cada consulta individual
  - Padrão de URLs para construir `url_oficial`

### Twilio API (WhatsApp)
- Verificar se conta Twilio suporta WhatsApp
- Números devem estar verificados na conta
- Formato: `+55 XX 9XXXX-XXXX` (Brasil)
- Testar em sandbox antes de produção

### GitHub Pages & Actions
- Deploy automático: arquivo gerado em `docs/` ou branch `gh-pages`
- Secrets armazenados em Settings → Secrets and variables
- Workflow file: `.github/workflows/check-consultas.yml`

## Fluxo de Desenvolvimento

1. **Setup Local**: 
   - Node.js ou Python conforme stack escolhido
   - Criar `.env` com variáveis (não comitar!)
   - `npm install` ou `pip install -r requirements.txt`

2. **Testar Scraper**: 
   ```bash
   node src/scraper.js --test
   # Deve baixar dados de https://consultas-publicas.mme.gov.br/home
   # e criar data/consultas.json com estrutura válida
   ```

3. **Testar Geração HTML**: 
   ```bash
   node src/page_generator.js
   # Gera docs/index.html com cards formatados (Tailwind)
   # Verificar cores (verde/amarelo/vermelho) por dias_restantes
   ```

4. **Testar Notificações**: 
   - Use sandbox Twilio (números de teste)
   - Não enviar mensagens reais em dev/test
   - Validar formato e conteúdo das mensagens

5. **Commitar & Push**: 
   - GitHub Actions dispara `.github/workflows/check-consultas.yml`
   - Workflow: scraper → validação → notificações → geração HTML → deploy

## Debugging & Troubleshooting

- **Scraper não coleta dados**: Verificar HTML do site (pode ter mudado), ajustar seletores
- **Notificações não enviam**: Validar credenciais Twilio, logs de erro
- **GitHub Pages não atualiza**: Verificar arquivo gerado em `docs/`, push para main
- **Duplicatas de consultas**: Implementar deduplicação por ID único do site oficial
- **Notificações enviadas múltiplas vezes**: Garantir `notificado: true` persiste no JSON

## Checklist para Novos PRs

- [ ] Scraper trata erros de rede e HTML inválido
- [ ] Dados validados contra schema esperado
- [ ] Sem duplicatas no JSON
- [ ] Notificações testadas em sandbox
- [ ] GitHub Pages HTML gerado corretamente
- [ ] Variáveis de ambiente documentadas
- [ ] Logs são informativos para debug
- [ ] Sem credenciais hard-coded
