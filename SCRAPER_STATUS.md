# Scraper - Consultas Públicas do MME

## Status: ✅ FUNCIONANDO

O scraper agora está **totalmente funcional** e consegue extrair dados reais do site de Consultas Públicas do MME.

## Como Funciona

### Tecnologias Utilizadas

- **Selenium + ChromeDriver**: Renderiza JavaScript e carrega a página completamente
- **BeautifulSoup**: Parse do HTML renderizado
- **Regex**: Extração de padrões de dados (números, datas, títulos)
- **JSON**: Armazenamento de dados estruturados

### Fluxo de Execução

1. **Fetch da Página** (com Selenium)

   - Inicializa browser Chrome headless
   - Acessa https://consultas-publicas.mme.gov.br/home
   - Aguarda carregamento completo do JavaScript Angular

2. **Parse dos Dados**

   - Procura por componentes `app-card-consulta-publica`
   - Extrai padrão: `Consulta Pública n° XXX de DD/MM/YYYY`
   - Procura por padrão de datas: `DD/MM/YYYY até DD/MM/YYYY`
   - Extrai títulos descritivos

3. **Validação e Limpeza**

   - Valida que todos os campos obrigatórios estão presentes
   - Converte datas para formato ISO (YYYY-MM-DD)
   - Remove duplicatas

4. **Salvamento**
   - Salva em `data/consultas.json` com timestamp
   - Preserva status de notificação de consultas anteriores

## Dados Extraídos

```json
{
  "id": "consulta_206",
  "numero": 206,
  "titulo": "Consulta pública sobre Referencial Básico para Mineração Brasileira Sustentável: das Boas Práticas à Promoção do Trabalho Digno e Decente",
  "descricao": "",
  "data_abertura": "2025-11-14",
  "data_encerramento": "2025-12-14",
  "url_oficial": "https://consultas-publicas.mme.gov.br/consulta/206",
  "dias_restantes": 18,
  "notificado": false
}
```

## Uso

### Local (Manual)

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar scraper
python scraper.py
```

Output esperado:

```
[1/4] Buscando página do site...
Tentando com Selenium (renderizacao de JavaScript)...
  Inicializando browser Chrome...
  Acessando https://consultas-publicas.mme.gov.br/home
  Aguardando carregamento...
[OK] Página carregada e renderizada com Selenium

[2/4] Fazendo parsing dos dados...
Encontrados 5 elementos de consulta
[+] Consulta pública sobre Referencial Básico para...
[+] Proposta de Decreto que regulamenta as atividades...
[+] Proposta de Decreto que regulamenta o Programa...
[+] Proposta de Resolução CNPE que estabelece como...
[+] Portaria de Diretrizes e Sistemática do LRCAP...
Total de consultas extraídas: 5

[3/4] Mesclando com dados existentes...
[4/4] Salvando dados...
[OK] Dados salvos em data/consultas.json
```

### GitHub Actions (Automático)

O scraper é executado **3 vezes por dia** via GitHub Actions:

- **08:00 UTC**: Manhã
- **12:00 UTC**: Meio do dia
- **18:00 UTC**: Noite

Configurado em `.github/workflows/check-consultas.yml`

## Dependências

```txt
requests>=2.28.0          # HTTP requests
beautifulsoup4>=4.11.0    # HTML parsing
lxml>=4.9.0               # XML/HTML processing
selenium>=4.0.0           # JavaScript rendering
webdriver-manager>=3.8.0  # Automatic ChromeDriver management
```

### Instalação de ChromeDriver

**Automático** (recomendado):

- `webdriver-manager` baixa automaticamente a versão correta do ChromeDriver
- Funciona em Windows, macOS e Linux

**Manual** (opcional):

- Download em https://chromedriver.chromium.org/
- Copiar para PATH ou especificar caminho em variável de ambiente

## Estrutura de Dados

### Arquivo: `data/consultas.json`

```json
{
  "consultas": [
    {
      "id": "consulta_XXX",
      "numero": 206,
      "titulo": "string",
      "descricao": "string (opcional)",
      "data_abertura": "YYYY-MM-DD",
      "data_encerramento": "YYYY-MM-DD",
      "url_oficial": "https://...",
      "dias_restantes": number,
      "notificado": boolean
    }
  ],
  "ultimaAtualizacao": "2025-11-26T09:08:27.520928"
}
```

## Troubleshooting

### Erro: "chromedriver not found"

- Solução: Reinstalar `webdriver-manager`
  ```bash
  pip install --upgrade webdriver-manager
  ```

### Erro: "Unable to locate Chrome browser"

- Solução: Instalar Google Chrome
  - Windows: Baixar em https://google.com/chrome
  - Linux: `sudo apt-get install google-chrome-stable`
  - macOS: `brew install google-chrome`

### Erro: "timeout waiting for page to load"

- Solução: Aumentar timeout em `scraper.py` (linha ~65)
  - Padrão: 15 segundos
  - Aumentar para: 20-30 segundos

### Nenhuma consulta encontrada

- Verificar se o site mudou de estrutura
- Executar `selenium_inspect.py` para debug
- Atualizar seletores CSS em `parse_consultas()`

### Títulos truncados ou incompletos

- Verificar arquivo `scraper.log`
- Padrão de regex para títulos pode precisar ajuste
- Site pode ter formatação HTML diferente

## Performance

| Métrica               | Valor           |
| --------------------- | --------------- |
| Tempo total           | ~10-15 segundos |
| Inicialização browser | ~3-5 segundos   |
| Carregamento página   | ~4-6 segundos   |
| Parse + salvamento    | ~1-2 segundos   |
| Memória               | ~200-300 MB     |

## Logging

Logs são salvos em:

- **Console**: Output em tempo real
- **Arquivo**: `scraper.log` (UTF-8)

Exemplo:

```
2025-11-26 09:08:27,503 - INFO - [OK] Página carregada e renderizada com Selenium
2025-11-26 09:08:27,519 - INFO - [+] Consulta pública sobre Referencial Básico...
2025-11-26 09:08:27,520 - INFO - Total de consultas extraídas: 5
2025-11-26 09:08:27,520 - INFO - [OK] Dados salvos em data/consultas.json
```

## Próximas Funcionalidades

- [ ] Descrições completas (atualmente vazias)
- [ ] Extração de "Área Responsável"
- [ ] Integração WhatsApp (Twilio)
- [ ] Notificações quando faltam 7 dias para encerramento
- [ ] Histórico/Arquivo de consultas encerradas
- [ ] Busca e filtros na página
- [ ] Categorização por tema/ministério

## Links Úteis

- [Selenium Python Documentation](https://www.selenium.dev/documentation/webdriver/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)
- [Site MME Consultas Públicas](https://consultas-publicas.mme.gov.br/home)

## Autor

Bot Consultas Públicas - Scraper automático do MME

## Licença

MIT
