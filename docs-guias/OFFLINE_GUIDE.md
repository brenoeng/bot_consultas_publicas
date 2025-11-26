# 📴 Guia Rápido - Versão 100% Offline

## ✨ O que é?

`docs/offline.html` é uma versão **completamente independente** que funciona:

- ✅ Sem internet
- ✅ Sem servidor
- ✅ Sem fetch de arquivos
- ✅ Sem dependências externas (exceto Tailwind CDN)
- ✅ Offline completo após primeiro carregamento

## 🚀 Como usar

### Opção 1: Abrir direto no navegador

```bash
# Windows
start docs/offline.html

# macOS
open docs/offline.html

# Linux
xdg-open docs/offline.html
```

Ou simplesmente **arraste o arquivo** para o navegador.

### Opção 2: Servidor local

```bash
# Python 3
python -m http.server 8000

# Depois acesse: http://localhost:8000/docs/offline.html
```

## 📝 Como adicionar suas consultas

Abra `docs/offline.html` em um editor de texto e procure por esta seção (próxima ao final do arquivo):

```javascript
// DADOS EMBUTIDOS - Edite aqui para adicionar suas consultas!
const consultas = [
  {
    id: "consulta_001",
    titulo: "Meu Título da Consulta",
    descricao: "Descrição breve...",
    data_abertura: "2025-11-20",
    data_encerramento: "2025-12-10",
    url_oficial: "https://seu-link-aqui.com",
    notificado: false,
  },
  // ... mais consultas aqui
];
```

### Exemplo - Adicionar uma nova consulta:

```javascript
const consultas = [
  // ... consultas anteriores ...
  {
    id: "consulta_nova_001",
    titulo: "Consulta sobre Energia Solar",
    descricao: "Discussão sobre incentivos para energia solar residencial",
    data_abertura: "2025-12-01",
    data_encerramento: "2025-12-20",
    url_oficial: "https://consultas-publicas.mme.gov.br/home",
    notificado: false,
  },
];
```

**Salve o arquivo** e recarregue a página no navegador (F5 ou Ctrl+R).

## 🎨 Entendendo a interface

### Cores dos badges

- 🟢 **Verde**: Encerra em mais de 7 dias
- 🟡 **Amarelo**: Encerra em 1-7 dias (urgente!)
- 🔴 **Vermelho**: Encerrado ou hoje

### Cards

- **Título**: Destacado em azul escuro
- **Descrição**: Resumo da consulta (até 3 linhas)
- **Data**: Exibida em formato DD/MM/YYYY
- **Botão Acessar**: Leva para a URL oficial

### Estatísticas (topo)

- **Total**: Número total de consultas
- **Encerrando em 7 dias**: Urgentes
- **Ativas**: Ainda abertas

## 💾 Como sincronizar com `data/consultas.json`

Se você tem dados em `data/consultas.json` e quer usar em `offline.html`:

1. **Abra `data/consultas.json`** em um editor
2. **Copie os dados** do array `"consultas"`
3. **Cole em `offline.html`**, substituindo o array `const consultas = [...]`
4. **Salve** e recarregue

Exemplo de `data/consultas.json`:

```json
{
  "consultas": [
    {
      "id": "consulta_001",
      "titulo": "...",
      ...
    }
  ],
  "ultimaAtualizacao": "2025-11-20T10:30:00Z"
}
```

Copie tudo dentro de `"consultas": [...]` para `offline.html`.

## ✅ Checklist de uso

- [ ] Abriu `docs/offline.html` com sucesso?
- [ ] Vê as 4 consultas de exemplo?
- [ ] Clica no botão e abre a URL?
- [ ] Quer adicionar suas próprias consultas?
  - [ ] Editou o array `const consultas = [...]`?
  - [ ] Salvou o arquivo HTML?
  - [ ] Recarregou a página (F5)?

## ⚠️ Limitações

- **Não salva dados**: Apenas embutido no arquivo HTML
- **Sem persistência**: Atualizações não são salvas automaticamente
- **Sem notificações**: WhatsApp requer backend (ver `notifier.html`)
- **Sem scraping**: Para atualizar com dados novos do site, precisaria de um servidor

## 🔗 Próximas etapas

Se precisar de **funcionalidades avançadas**:

1. **Notificações WhatsApp**: Use `notifier.html`
2. **Gestão de dados**: Use `scraper.html`
3. **Sincronização com site oficial**: Implemente um backend (Node.js ou Python)
4. **GitHub Pages com dados reais**: Configure o workflow GitHub Actions

## ❓ Dúvidas?

Consulte:

- `COMEÇE_AQUI.md` - Quick start geral
- `README.md` - Documentação técnica
- `ERRO-SOLUCAO.md` - Troubleshooting
