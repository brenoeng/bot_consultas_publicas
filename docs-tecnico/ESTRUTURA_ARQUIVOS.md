# 📁 Estrutura de Arquivos - Melhores Práticas Web

Agora o projeto segue as **melhores práticas de desenvolvimento web** com separação completa de responsabilidades:

## 📂 Estrutura de Diretórios

```
docs/
├── index.html              # Página principal (com fetch de dados)
├── offline.html            # Página offline (dados embutidos)
├── index-simples.html      # Versão simplificada alternativa
├── css/
│   └── styles.css          # Estilos customizados
├── js/
│   ├── utils.js            # Funções reutilizáveis
│   ├── app.js              # Lógica da página index.html
│   └── app-offline.js      # Lógica da página offline.html
└── img/                    # (futuro) Imagens e assets
```

## 📄 Descrição dos Arquivos

### HTML Files

| Arquivo                | Descrição                                           | Uso                              |
| ---------------------- | --------------------------------------------------- | -------------------------------- |
| **index.html**         | Página principal com fetch de `data/consultas.json` | Produção com dados reais         |
| **offline.html**       | Versão 100% offline com dados embutidos             | Quando sem servidor/arquivo JSON |
| **index-simples.html** | Alternativa com fallback automático                 | Desenvolvimento/testes           |

### CSS

**`docs/css/styles.css`**

- Estilos customizados que complementam Tailwind CDN
- Utilities: `.line-clamp-2`, `.line-clamp-3`, `.badge`
- Componentes: `.card`, `.btn`, `.spinner`, `.empty-state`
- Animações: `@keyframes spin`
- Acessibilidade: `:focus-visible`
- Print styles para impressão

### JavaScript

#### `docs/js/utils.js`

Funções **reutilizáveis** compartilhadas entre páginas:

```javascript
// Cálculos
-calculateDaysRemaining(dataEncerramento) -
  formatDate(dateStr) -
  formatDateTime(date) -
  // Renderização
  getBadgeClass(diasRestantes) -
  getBadgeText(diasRestantes) -
  escapeHTML(text) -
  // Lógica de negócio
  sortConsultas(arr) -
  filterProximas(arr) -
  filterAtivas(arr) -
  // Validação
  isValidConsulta(obj) -
  log(message, level);
```

#### `docs/js/app.js`

Lógica específica para **index.html**:

```javascript
// Funções principais
- renderConsulta(consulta)      // Renderiza um card
- updateStats(consultasArray)   // Atualiza estatísticas
- renderPage(consultasArray)    // Renderiza página inteira
- loadConsultas()               // Fetch de data/consultas.json

// Inicialização
- DOMContentLoaded event listeners
```

#### `docs/js/app-offline.js`

Lógica específica para **offline.html**:

```javascript
// Dados embutidos
- const consultasOffline = [...]

// Funções principais
- renderConsultaOffline(consulta)
- updateStatsOffline(consultasArray)
- renderPageOffline(consultasArray)
```

## 🔗 Dependências entre Arquivos

```
HTML (index.html / offline.html)
  ├── Tailwind CSS (CDN)
  ├── css/styles.css
  └── JavaScript:
      ├── js/utils.js (carregado primeiro)
      ├── js/app.js (ou app-offline.js)
```

**Ordem de carregamento importante:**

1. Tailwind CSS (CDN)
2. css/styles.css
3. js/utils.js (define funções)
4. js/app.js (usa funções de utils.js)

## ✨ Benefícios desta Estrutura

### 1. **Separação de Responsabilidades**

- HTML = Estrutura
- CSS = Estilos
- JS = Lógica

### 2. **Reutilização de Código**

- `utils.js` é compartilhado por `app.js` e `app-offline.js`
- Evita duplicação de funções

### 3. **Manutenção Facilitada**

- Encontrar e corrigir bugs é mais fácil
- Mudanças em `utils.js` afetam todas as páginas

### 4. **Performance**

- CSS e JS podem ser cachados separadamente
- Arquivos menores carregam mais rápido

### 5. **Testabilidade**

- Cada módulo pode ser testado isoladamente
- Funções são puras e previsíveis

### 6. **Escalabilidade**

- Fácil adicionar novas páginas
- Estrutura pronta para crescimento

## 🚀 Como Adicionar Novas Funcionalidades

### Adicionar nova função reutilizável

1. Edite `js/utils.js`
2. Adicione a função com JSDoc
3. Use em `app.js` e/ou `app-offline.js`

### Adicionar nova página HTML

1. Crie `docs/nova-pagina.html`
2. Importe `css/styles.css` + `js/utils.js`
3. Crie `js/nova-pagina.js` se necessário

### Customizar estilos

1. Edite `css/styles.css`
2. Adicione novas classes ou overrides
3. Reutilize em templates HTML

## 📋 Checklist de Qualidade

- ✅ HTML semântico, sem lógica JavaScript
- ✅ CSS separado, reutilizável e bem organizado
- ✅ JavaScript modular com funções pequenas
- ✅ Sem duplicação de código
- ✅ Comentários em funções complexas (JSDoc)
- ✅ Arquivo único para estilos customizados
- ✅ Arquivo único para utilitários compartilhados
- ✅ Carregamento de scripts em ordem correta

## 🔍 Comparação com Código Anterior

| Aspecto            | Antes                 | Depois                      |
| ------------------ | --------------------- | --------------------------- |
| **Scripts inline** | Sim (todo no HTML)    | Não (separados em arquivos) |
| **Estilos inline** | Sim (`<style>`)       | Não (`css/styles.css`)      |
| **Reutilização**   | Duplicação de funções | `utils.js` compartilhado    |
| **Linhas HTML**    | ~350 linhas           | ~100 linhas                 |
| **Manutenção**     | Difícil (tudo junto)  | Fácil (separado)            |

## 📝 Próximas Melhorias Opcionais

- [ ] Minificar CSS e JS para produção
- [ ] Adicionar bundler (Webpack/Vite) se crescer
- [ ] Testes unitários para `utils.js`
- [ ] TypeScript para type safety
- [ ] Build pipeline para assets otimizados
