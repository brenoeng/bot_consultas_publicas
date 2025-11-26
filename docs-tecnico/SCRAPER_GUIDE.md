# 🕷️ Guia do Scraper - Consultas Públicas

## O que é?

Script Python que **automaticamente**:

- ✅ Acessa https://consultas-publicas.mme.gov.br/home
- ✅ Extrai dados das consultas públicas
- ✅ Salva em `data/consultas.json`
- ✅ Atualiza as páginas HTML automaticamente
- ✅ Roda em GitHub Actions (agendado 3x por dia)

## 🚀 Como Usar

### 1️⃣ Setup Local (Desenvolvimento)

```bash
# Instalar dependências
pip install -r requirements.txt

# Ou usar setup automático
python setup_scraper.py

# Testar scraper
python scraper.py
```

### 2️⃣ Usar GitHub Actions (Automático em Produção)

1. **Commit seu código:**

   ```bash
   git add scraper.py requirements.txt
   git commit -m "Add scraper automático"
   git push origin main
   ```

2. **Ativa automaticamente:**

   - ✅ Todos os dias às 08:00, 12:00 e 18:00 UTC
   - ✅ Manual: Settings → Actions → Workflows → Run

3. **Resultado:**
   - 📝 Dados salvos em `data/consultas.json`
   - 🔄 Commit automático se houver mudanças
   - 📄 GitHub Pages atualiza automaticamente

## 📊 Estrutura de Dados

O scraper gera `data/consultas.json` com este formato:

```json
{
  "consultas": [
    {
      "id": "consulta_unique_id_hash",
      "titulo": "Consulta Pública nº XX/2025 - Título",
      "descricao": "Descrição da consulta",
      "data_abertura": "2025-11-26",
      "data_encerramento": "2025-12-10",
      "url_oficial": "https://consultas-publicas.mme.gov.br/...",
      "dias_restantes": 14,
      "notificado": false
    }
  ],
  "ultimaAtualizacao": "2025-11-26T12:34:56.789Z"
}
```

## 🔧 Configuração

### Frequência de Execução

Edite `.github/workflows/check-consultas.yml`:

```yaml
schedule:
  - cron: "0 8 * * *" # 08:00 UTC
  - cron: "0 12 * * *" # 12:00 UTC
  - cron: "0 18 * * *" # 18:00 UTC
```

[Gerador de cron](https://crontab.guru)

### Variáveis de Ambiente

```bash
# Não necessário atualmente, mas você pode adicionar:
export LOG_LEVEL=INFO
export REQUEST_TIMEOUT=15
export MAX_RETRIES=3
```

## 📊 Monitoramento

### Ver Logs Local

```bash
# Enquanto roda
python scraper.py

# Arquivo de log
tail -f scraper.log
```

### Ver Logs GitHub Actions

1. Vá para seu repositório
2. Aba "Actions"
3. Clique no workflow "Scraper - Consultas Públicas"
4. Clique na execução
5. Veja os logs detalhados

## 🐛 Troubleshooting

### ❌ "Site não carrega"

**Problema:** Timeout ao acessar site
**Solução:** Site pode estar offline ou mudou de estrutura

```bash
# Teste manualmente
python scraper.py

# Verifique logs
cat scraper.log
```

### ❌ "Nenhuma consulta encontrada"

**Problema:** HTML do site mudou
**Solução:** Adaptar seletores CSS em `scraper.py`

```python
# Em scraper.py, linha ~180
# Ajuste os seletores:
seletores = [
    ('div', {'class': lambda x: x and 'consulta' in x}),
    ('div', {'class': lambda x: x and 'card' in x}),
    # Adicione novos aqui
]
```

### ❌ "JSON inválido"

**Problema:** Dados salvos estão mal formatados
**Solução:**

```bash
# Validar JSON
python -m json.tool data/consultas.json

# Se falhar, restaurar backup
git restore data/consultas.json
```

## 🎯 Customizações

### Adicionar Validação Extra

```python
# Em scraper.py, método validar_consulta()
def validar_consulta(self, consulta):
    # ... validações existentes ...

    # Nova validação
    if len(consulta['descricao']) < 10:
        logger.warning("Descrição muito curta")
        return False

    return True
```

### Enviar Notificação WhatsApp

```python
# Descomentar em notifier.py
# E configurar secrets no GitHub:
# - TWILIO_ACCOUNT_SID
# - TWILIO_AUTH_TOKEN
# - TWILIO_PHONE_NUMBER
```

### Salvar Histórico

```python
# Adicionar em scraper.py
import shutil
from datetime import datetime

# Backup antes de salvar
backup_name = f"data/backup_consultas_{datetime.now().isoformat()}.json"
shutil.copy(self.data_file, backup_name)
```

## 📈 Métricas

**Tempo de execução:**

- Local: ~5-15 segundos
- GitHub Actions: ~30-60 segundos (incluindo setup)

**Taxa de sucesso:**

- Esperado: >95%
- Falha: Usa dados anteriores automaticamente

**Tamanho de dados:**

- Arquivo JSON: ~5-50 KB
- Consultas: 10-100 por execução

## 🔄 Pipeline Automático

```
GitHub Actions Trigger (3x/dia)
         ↓
   Checkout código
         ↓
   Setup Python 3.11
         ↓
   Instalar dependências (pip)
         ↓
   Executar scraper.py
         ↓
   Validar JSON
         ↓
   Commit mudanças (se houver)
         ↓
   Push para main
         ↓
   Deploy GitHub Pages
         ↓
   ✓ Páginas atualizadas
```

## 📝 Logging

Scraper cria dois logs:

1. **Console:** Saída em tempo real
2. **Arquivo:** `scraper.log` (sempre presente)

Formato:

```
2025-11-26 12:34:56,789 - INFO - Iniciando scraper...
2025-11-26 12:34:57,890 - INFO - ✓ Página carregada com sucesso
2025-11-26 12:34:58,901 - INFO - ✓ Consulta: Título da Consulta...
2025-11-26 12:35:00,012 - INFO - ✓ Dados salvos em data/consultas.json
```

## ✅ Checklist

- [ ] `requirements.txt` criado
- [ ] `scraper.py` funcionando localmente
- [ ] GitHub Actions workflow ativo
- [ ] `data/consultas.json` populado
- [ ] Páginas HTML exibem dados
- [ ] Log `scraper.log` sendo criado

## 📞 Suporte

Se algo quebrar:

1. Verifique `scraper.log`
2. Teste localmente: `python scraper.py`
3. Verifique logs do GitHub Actions
4. Valide JSON: `python -m json.tool data/consultas.json`

---

**Criado:** Novembro 2025
**Status:** ✅ Pronto para Produção
