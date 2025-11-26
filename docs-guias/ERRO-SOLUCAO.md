# 🔧 Solução: Erro ao Carregar Consultas

## ❌ O Erro

```
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

Este erro ocorre quando o navegador tenta carregar `data/consultas.json` mas recebe um arquivo HTML em vez de JSON (geralmente um erro 404).

## ✅ Soluções (tente na ordem)

### 1. **Verificar se o arquivo existe**

O arquivo `data/consultas.json` **DEVE** estar na mesma pasta do repositório:

```
bot_consultas_publicas/
├── docs/
│   ├── index.html
│   └── index-simples.html    ← Versão simplificada (tente esta!)
├── data/
│   └── consultas.json        ← DEVE estar aqui!
├── scraper.html
└── ...
```

Se o arquivo não existe:

1. Abra `scraper.html`
2. Clique "Carregar Dados de Teste"
3. Clique "Iniciar Scraper"
4. Clique o botão de **Download**
5. **Salve em `data/`** (mantendo o nome `consultas.json`)

### 2. **Usar a versão simplificada**

Se os erros continuarem, use `index-simples.html`:

```bash
# Abra no navegador:
docs/index-simples.html
```

Esta versão:

- ✅ Mostra dados de exemplo automaticamente
- ✅ Carrega arquivo JSON se existir
- ✅ Fallback para dados de teste se não encontrar
- ✅ Sem erros de caminho relativo

### 3. **Verificar o JSON**

O arquivo `data/consultas.json` deve ter este formato:

```json
{
  "consultas": [
    {
      "id": "consulta_001",
      "titulo": "Título",
      "descricao": "Descrição",
      "data_abertura": "2025-11-26",
      "data_encerramento": "2025-12-10",
      "url_oficial": "https://...",
      "dias_restantes": 14,
      "notificado": false
    }
  ],
  "ultimaAtualizacao": "2025-11-26T10:00:00Z"
}
```

**Valide em:** https://jsonlint.com/

### 4. **Testar localmente com live server**

Se estiver usando VS Code:

```bash
# Instale a extensão "Live Server"
# Clique direito em docs/index.html → "Open with Live Server"
```

Ou use Python:

```bash
cd bot_consultas_publicas
python -m http.server 8000

# Abra no navegador:
# http://localhost:8000/docs/index.html
```

### 5. **Verificar console do navegador**

Pressione **F12** (DevTools) e vá em **Console** para ver mensagens de erro:

```
CTRL + SHIFT + I  (Windows)
CMD + OPTION + I  (Mac)
F12 (ambos)
```

Procure por mensagens como:

- `Failed to fetch` → arquivo não encontrado
- `SyntaxError` → JSON inválido
- Caminhos do arquivo que está procurando

## 🎯 Checklist Rápido

- [ ] Arquivo `data/consultas.json` existe?
- [ ] JSON está válido (testado em jsonlint.com)?
- [ ] Está usando `docs/index-simples.html` ou servidor local?
- [ ] Abriu console (F12) e viu a mensagem de erro exata?
- [ ] Tentou limpar cache (Ctrl+Shift+Delete)?

## 📝 Se ainda não funcionar

1. Abra `scraper.html`
2. Clique "Carregar Dados de Teste" → "Iniciar Scraper"
3. Salve o arquivo em `data/consultas.json`
4. Abra `docs/index-simples.html`
5. Clique "Atualizar"

## 🌐 GitHub Pages

Se vai publicar no GitHub:

1. Faça commit de todos os arquivos (incluindo `data/consultas.json`)
2. Push para main
3. Ative GitHub Pages em Settings → Pages
   - Branch: `main`
   - Folder: `/docs`
4. Espere 1-2 minutos
5. Acesse: `https://seu-usuario.github.io/bot_consultas_publicas/docs/index-simples.html`

---

**Desenvolvido com ❤️ para MME**
