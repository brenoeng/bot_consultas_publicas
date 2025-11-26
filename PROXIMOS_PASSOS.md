# PRÓXIMOS PASSOS - Melhorias e Funcionalidades

## Status Atual ✅

O scraper está **100% funcional** e extraindo dados reais do site do MME.

## Melhorias Prioritárias

### 1. Extrair Descrições Completas ⭐⭐⭐

**Prioridade**: ALTA

**Problema**: Campo `descricao` está vazio

**Solução**:

```python
# Em parse_consultas(), após extrair o título:
# Procurar por padrão "Área Responsável:" ou próximo parágrafo
area_match = re.search(
    r'Área Responsável:\s*(.+?)(?:Secretaria|\d{1,2}/\d{1,2}|$)',
    text,
    re.IGNORECASE | re.DOTALL
)
if area_match:
    descricao = area_match.group(1).strip()[:500]
```

**Teste**: Verificar `data/consultas.json` se campo tem conteúdo

---

### 2. Integração WhatsApp/Notificações ⭐⭐⭐

**Prioridade**: ALTA (solicitado no projeto)

**Implementação**:

```bash
# Instalar Twilio
pip install twilio

# Adicionar a requirements.txt
echo "twilio>=8.0.0" >> requirements.txt
```

**Código** (novo arquivo `notifier.py`):

```python
from twilio.rest import Client
import os

def enviar_alerta_whatsapp(numero_consulta, titulo, dias_restantes):
    """Envia alerta via WhatsApp quando faltam 7 dias"""

    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
    to_number = os.getenv('WHATSAPP_TARGET')

    client = Client(account_sid, auth_token)

    mensagem = f"""
[ALERTA] Consulta Pública #{numero_consulta}
Título: {titulo}
Dias restantes: {dias_restantes}

Acesse: https://consultas-publicas.mme.gov.br
    """.strip()

    message = client.messages.create(
        from_=f"whatsapp:{from_number}",
        body=mensagem,
        to=f"whatsapp:{to_number}"
    )

    return message.sid
```

**Variáveis de Ambiente** (GitHub Secrets):

```
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_WHATSAPP_NUMBER=+55...(número Twilio)
WHATSAPP_TARGET=+55...(seu número)
```

**Integração em scraper.py**:

```python
# Após salvar dados, verificar para notificações
if dias_restantes == 7 and not notificado:
    try:
        enviar_alerta_whatsapp(...)
        consulta['notificado'] = True
    except Exception as e:
        logger.error(f"Erro ao enviar notificação: {e}")
```

---

### 3. Melhorar Página HTML/Frontend ⭐⭐

**Prioridade**: MÉDIA

**Melhorias**:

- [ ] Adicionar filtro por "Dias Restantes"
- [ ] Busca por título/número
- [ ] Ordenação por data de encerramento
- [ ] Badge colorido (verde > 7 dias, amarelo 1-7, vermelho < 1)
- [ ] Link direto para acessar consulta (novo aba)
- [ ] Estatísticas em tempo real

**Arquivo**: `docs/js/app.js` (já existe, apenas adicionar funcionalidades)

```javascript
// Exemplo: Filtro por status
function filtrarPorStatus(status) {
  const cards = document.querySelectorAll(".card-consulta");
  cards.forEach((card) => {
    const dias = parseInt(card.dataset.dias);
    let mostrar = true;

    if (status === "urgente" && dias > 7) mostrar = false;
    if (status === "ativo" && dias <= 0) mostrar = false;

    card.style.display = mostrar ? "block" : "none";
  });
}
```

---

### 4. Expandir para Outros Ministérios ⭐

**Prioridade**: BAIXA (futuro)

**Possíveis Fontes**:

- Ministério da Saúde: https://www.saude.gov.br/...
- Ministério da Defesa: https://www.defesa.gov.br/...
- Ministério do Trabalho: https://www.gov.br/trabalho/...

**Abordagem**: Parametrizar scraper para aceitar diferentes URLs

```python
class ConsultasPublicasScraper:
    def __init__(self, base_url="https://consultas-publicas.mme.gov.br/home"):
        self.base_url = base_url
        # ...
```

---

### 5. Arquivar Consultas Encerradas ⭐⭐

**Prioridade**: MÉDIA

**Implementação**:

```python
def arquivar_consultas(self, consultas):
    """Move consultas encerradas para arquivo"""
    arquivo_file = Path(__file__).parent / "data" / "consultas_encerradas.json"

    ativas = []
    encerradas = []

    for consulta in consultas:
        if consulta['dias_restantes'] <= 0:
            encerradas.append(consulta)
        else:
            ativas.append(consulta)

    # Salvar encerradas
    if encerradas:
        try:
            with open(arquivo_file, 'a') as f:
                for consulta in encerradas:
                    f.write(json.dumps(consulta) + '\n')
        except:
            pass

    return ativas
```

---

### 6. Melhorar Logging e Monitoramento ⭐⭐

**Prioridade**: MÉDIA

**Implementações**:

- [ ] Logs estruturados em JSON
- [ ] Dashboard com metrics (Grafana/CloudWatch)
- [ ] Alertas para falhas de scraping
- [ ] Estatísticas de execução (tempo, consultas, erros)

```python
# Adicionar ao final de scraper.py
def salvar_metricas(tempo_total, consultas_encontradas, erros):
    """Salva métricas de execução para análise"""
    metricas = {
        "timestamp": datetime.now().isoformat(),
        "tempo_total_segundos": tempo_total,
        "consultas_encontradas": consultas_encontradas,
        "erros_encontrados": len(erros),
        "status": "sucesso" if len(erros) == 0 else "parcial"
    }

    with open('metricas.jsonl', 'a') as f:
        f.write(json.dumps(metricas) + '\n')
```

---

## Roadmap

### Fase 1 (Agora - Semana 1) ✅

- ✅ Scraper básico funcional
- ✅ Extração de dados reais
- ✅ Página HTML para exibição
- [ ] **TODO**: Testar em GitHub Actions

### Fase 2 (Semana 2) ⏳

- [ ] Notificações WhatsApp
- [ ] Descrições completas
- [ ] Melhorias no frontend
- [ ] GitHub Secrets configurados

### Fase 3 (Semana 3) 📅

- [ ] Arquivo de consultas encerradas
- [ ] Dashboard/Estatísticas
- [ ] Tratamento de erros aprimorado
- [ ] Documentação completa

### Fase 4+ (Futuro) 🔮

- [ ] Múltiplos ministérios
- [ ] API REST
- [ ] Banco de dados (PostgreSQL)
- [ ] Mobile app

---

## Como Fazer as Melhorias

### Teste Local

```bash
# 1. Criar branch
git checkout -b feature/melhorias

# 2. Fazer alterações
# ... editar arquivo ...

# 3. Testar
python scraper.py

# 4. Validar JSON
python -m json.tool data/consultas.json

# 5. Commit
git add .
git commit -m "Adicionar notificações WhatsApp"

# 6. Push
git push origin feature/melhorias

# 7. PR no GitHub
```

### GitHub Actions

Após fazer alterações no scraper, o workflow automático executará:

```yaml
# .github/workflows/check-consultas.yml

name: Check Consultas Públicas
on:
  schedule:
    - cron: '0 8,12,18 * * *'  # 3x por dia
  workflow_dispatch:

jobs:
  scraper:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python scraper.py
      - run: git add .
      - run: git commit -m "Bot: Update consultas" || true
      - run: git push
```

---

## Checklist para Deployar

- [ ] Testar scraper localmente 3 vezes
- [ ] Validar JSON output
- [ ] Verificar GitHub Actions secrets configurados
- [ ] Fazer PR e revisar código
- [ ] Merge para main
- [ ] Monitorar primeira execução agendada
- [ ] Verificar GitHub Pages atualizado
- [ ] Documentação atualizada

---

## Links Úteis para Desenvolvimento

- [Twilio WhatsApp API](https://www.twilio.com/whatsapp)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Selenium Best Practices](https://www.selenium.dev/documentation/webdriver/best_practices/)
- [GitHub Pages Auto-Deploy](https://docs.github.com/en/pages/getting-started-with-github-pages)

---

## Suporte

Erros ou dúvidas:

1. Verificar `scraper.log`
2. Procurar em SCRAPER_STATUS.md
3. Testar localmente com `python -u scraper.py` (unbuffered)
4. Abrir issue no GitHub

---

**Última atualização**: 2025-11-26
**Status**: Projeto em evolução ✨
