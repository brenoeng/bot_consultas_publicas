# 🔧 Guia de Manutenção e Desenvolvimento

Guia prático para trabalhar com a estrutura modular do projeto.

## 📋 Tabela de Conteúdos

1. [Como adicionar consultas](#como-adicionar-consultas)
2. [Como customizar estilos](#como-customizar-estilos)
3. [Como adicionar funcionalidades](#como-adicionar-funcionalidades)
4. [Troubleshooting](#troubleshooting)

## 🔄 Como Adicionar Consultas

### Opção 1: Via Arquivo JSON (Recomendado)

1. Edite `data/consultas.json`:

```json
{
  "consultas": [
    {
      "id": "consulta_nova_001",
      "titulo": "Meu Título",
      "descricao": "Minha descrição",
      "data_abertura": "2025-12-01",
      "data_encerramento": "2025-12-20",
      "url_oficial": "https://seu-link.com",
      "notificado": false
    }
  ],
  "ultimaAtualizacao": "2025-11-26T10:00:00Z"
}
```

2. Commit e push:

```bash
git add data/consultas.json
git commit -m "Add consulta: Meu Título"
git push origin main
```

3. A página `index.html` carregará automaticamente

### Opção 2: Modo Offline

Se usar `offline.html`, edite os dados embutidos em `js/app-offline.js`:

```javascript
// Em docs/js/app-offline.js
const consultasOffline = [
  {
    id: "consulta_nova_001",
    titulo: "Meu Título",
    // ... resto do objeto
  },
];
```

Depois recarregue a página.

### Validação de Dados

Consulta válida precisa ter **obrigatoriamente**:

- ✅ `id` (string única)
- ✅ `titulo` (string)
- ✅ `data_encerramento` (formato YYYY-MM-DD)
- ✅ `url_oficial` (URL válida)

Campos opcionais:

- `descricao` (string)
- `data_abertura` (formato YYYY-MM-DD)
- `notificado` (boolean)

## 🎨 Como Customizar Estilos

### Adicionar nova cor de badge

Edite `docs/css/styles.css`:

```css
.badge.blue {
  background-color: #dbeafe; /* azul claro */
  color: #1e40af; /* azul escuro */
}
```

Depois use em `app.js`:

```javascript
function getBadgeClass(diasRestantes) {
  if (diasRestantes === 100) return "blue"; // novo
  // ... resto
}
```

### Adicionar novo componente CSS

```css
/* Em docs/css/styles.css */

.alert {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.alert.info {
  background-color: #dbeafe;
  color: #1e40af;
  border-left: 4px solid #2563eb;
}

.alert.warning {
  background-color: #fef3c7;
  color: #92400e;
  border-left: 4px solid #f59e0b;
}

.alert.error {
  background-color: #fee2e2;
  color: #991b1b;
  border-left: 4px solid #ef4444;
}
```

Use em HTML:

```html
<div class="alert info"><strong>Informação:</strong> Seu conteúdo aqui</div>
```

### Modificar cores principais

1. Abra `docs/index.html` e `docs/offline.html`
2. Procure pela classe `bg-blue-600` (azul principal)
3. Substitua por sua cor Tailwind, ex: `bg-indigo-600`

```html
<!-- Antes -->
<header class="bg-gradient-to-r from-blue-600 to-blue-800">
  <!-- Depois -->
  <header class="bg-gradient-to-r from-indigo-600 to-indigo-800"></header>
</header>
```

## ➕ Como Adicionar Funcionalidades

### Adicionar nova função reutilizável

1. Edite `docs/js/utils.js`:

```javascript
/**
 * Filtra consultas por keyword
 * @param {Array} arr - Array de consultas
 * @param {string} keyword - Termo de busca
 * @returns {Array} Consultas filtradas
 */
function searchConsultas(arr, keyword) {
  const lower = keyword.toLowerCase();
  return arr.filter(
    (c) =>
      c.titulo.toLowerCase().includes(lower) ||
      c.descricao.toLowerCase().includes(lower)
  );
}
```

2. Use em `app.js`:

```javascript
// Em algum event listener
const resultados = searchConsultas(consultas, "energia");
```

### Adicionar novo estado visual

1. Adicione a classe CSS em `styles.css`:

```css
.card.loading {
  opacity: 0.6;
  pointer-events: none;
}

.card.error {
  border: 2px solid #ef4444;
  background-color: #fef2f2;
}

.card.success {
  border: 2px solid #10b981;
  background-color: #f0fdf4;
}
```

2. Use em `app.js`:

```javascript
function renderConsulta(consulta) {
  let classes = "card";

  if (consulta.error) classes += " error";
  if (consulta.success) classes += " success";

  return `<div class="${classes}">...</div>`;
}
```

### Adicionar novo painel/seção

1. Crie novo arquivo `docs/js/stats.js`:

```javascript
/**
 * Renderiza painel de estatísticas avançadas
 */
function renderStatsPanel(consultas) {
  const total = consultas.length;
  const media_dias =
    consultas.reduce((sum, c) => {
      const dias = calculateDaysRemaining(c.data_encerramento);
      return sum + (dias || 0);
    }, 0) / total;

  return `
    <div class="card">
      <div class="p-6">
        <h3 class="font-bold mb-4">Estatísticas Avançadas</h3>
        <p>Média de dias até encerramento: ${Math.round(media_dias)}</p>
      </div>
    </div>
  `;
}
```

2. Adicione em `index.html`:

```html
<!-- Após estatísticas normais -->
<div id="advancedStats" class="mb-8"></div>

<script src="js/stats.js"></script>
```

3. Chame em `app.js`:

```javascript
// No renderPage()
document.getElementById("advancedStats").innerHTML =
  renderStatsPanel(consultas);
```

## 🐛 Troubleshooting

### Problema: Cards não aparecem em index.html

**Causa possível**: `data/consultas.json` não encontrado

**Solução**:

```bash
# Verificar arquivo existe
ls -la data/consultas.json

# Se não existe, criar:
cat > data/consultas.json << 'EOF'
{
  "consultas": [],
  "ultimaAtualizacao": "2025-11-26T10:00:00Z"
}
EOF

# Commit
git add data/consultas.json
git commit -m "Add initial consultas.json"
```

### Problema: Estilos não aparecem

**Causa possível**: Arquivo `css/styles.css` não carregado

**Solução**:

1. Verificar path em HTML:

```html
<!-- Correto: -->
<link rel="stylesheet" href="css/styles.css" />

<!-- Errado: -->
<link rel="stylesheet" href="styles.css" />
<link rel="stylesheet" href="../css/styles.css" />
```

2. Limpar cache:
   - Chrome: Ctrl+Shift+Delete
   - Firefox: Ctrl+Shift+Delete
   - Safari: ⌘+Shift+Delete

### Problema: Offline.html mostra dados antigos

**Causa**: Código desatualizado em `js/app-offline.js`

**Solução**:

1. Abra `js/app-offline.js`
2. Atualize `const consultasOffline = [...]`
3. Recarregue a página (Ctrl+R)

### Problema: JavaScript erros no console

**Solução de debug**:

1. Abra DevTools: F12
2. Vá para aba "Console"
3. Procure por mensagens vermelhas
4. Verifique que `utils.js` está antes de `app.js`:

```html
<script src="js/utils.js"></script>
<!-- Deve vir primeiro -->
<script src="js/app.js"></script>
<!-- Depois -->
```

## 📖 Exemplo Completo: Adicionar Filtro

Vamos adicionar um filtro por data:

### 1. Criar função em `utils.js`

```javascript
/**
 * Filtra consultas por range de datas
 * @param {Array} arr - Array de consultas
 * @param {string} dataInicio - YYYY-MM-DD
 * @param {string} dataFim - YYYY-MM-DD
 * @returns {Array} Consultas no range
 */
function filterByDateRange(arr, dataInicio, dataFim) {
  return arr.filter((c) => {
    const data = c.data_encerramento;
    return data >= dataInicio && data <= dataFim;
  });
}
```

### 2. Adicionar UI em `index.html`

```html
<!-- Antes de consultasContainer -->
<div class="mb-6 flex gap-4">
  <input type="date" id="dataInicio" class="px-4 py-2 border rounded" />
  <input type="date" id="dataFim" class="px-4 py-2 border rounded" />
  <button onclick="applyFilter()" class="btn btn-primary">Filtrar</button>
</div>
```

### 3. Implementar função em `app.js`

```javascript
function applyFilter() {
  const inicio = document.getElementById("dataInicio").value;
  const fim = document.getElementById("dataFim").value;

  if (!inicio || !fim) {
    alert("Preencha ambas as datas");
    return;
  }

  const filtered = filterByDateRange(consultas, inicio, fim);
  renderPage(filtered);
}
```

Pronto! Novo filtro funcional.

## ✅ Checklist de Desenvolvimento

- [ ] Código segue padrão do projeto?
- [ ] Função tem JSDoc comment?
- [ ] Scripts carregam em ordem correta?
- [ ] Testou em navegador (F12 console)?
- [ ] Funcionou em modo offline (offline.html)?
- [ ] Sem erros JavaScript?
- [ ] Estilos aplicados corretamente?
- [ ] Dados validados (isValidConsulta)?
- [ ] Commit com mensagem clara?

---

**Dica**: Mantenha as funções pequenas e reutilizáveis. Quando atingir 200 linhas em um arquivo, considere dividir!
