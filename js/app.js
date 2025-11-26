/**
 * App.js - Lógica principal para carregamento e renderização de consultas
 * Com suporte a fetch de arquivo JSON externo
 */

let consultas = [];

/**
 * Renderiza uma consulta como HTML string
 * @param {object} consulta - Objeto consulta
 * @returns {string} HTML da consulta
 */
function renderConsulta(consulta) {
  const diasRestantes = calculateDaysRemaining(consulta.data_encerramento);
  const badgeClass = getBadgeClass(diasRestantes);
  const badgeText = getBadgeText(diasRestantes);
  const dataFormatada = formatDate(consulta.data_encerramento);
  const dataAbertura = consulta.data_abertura
    ? formatDate(consulta.data_abertura)
    : null;

  let html = `
    <div class="card">
      <div class="p-6">
        <div class="flex items-start justify-between mb-3">
          <h3 class="text-lg font-bold text-gray-800 flex-1 pr-3 line-clamp-2">
            ${escapeHTML(consulta.titulo)}
          </h3>
          <span class="badge ${badgeClass}">
            ${badgeText}
          </span>
        </div>
  `;

  if (consulta.descricao) {
    html += `<p class="text-gray-600 text-sm mb-4 line-clamp-3">${escapeHTML(
      consulta.descricao
    )}</p>`;
  }

  html += `
        <div class="border-t border-gray-200 pt-4 mb-4">
          <div class="flex items-center text-sm text-gray-600 mb-2">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v2h16V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 011 1v1h1a1 1 0 110 2H7v1a1 1 0 11-2 0v-1H4a1 1 0 110-2h1V8a1 1 0 011-1z" clip-rule="evenodd"/>
            </svg>
            <strong>Encerramento:</strong>&nbsp;${dataFormatada}
          </div>
  `;

  if (dataAbertura) {
    html += `
          <div class="flex items-center text-sm text-gray-500">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v2h16V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 011 1v1h1a1 1 0 110 2H7v1a1 1 0 11-2 0v-1H4a1 1 0 110-2h1V8a1 1 0 011-1z" clip-rule="evenodd"/>
            </svg>
            <strong>Abertura:</strong>&nbsp;${dataAbertura}
          </div>
    `;
  }

  html += `
        </div>
        <a 
          href="${escapeHTML(consulta.url_oficial)}" 
          target="_blank" 
          rel="noopener noreferrer"
          class="inline-block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
        >
          Acessar Consulta
        </a>
      </div>
    </div>
  `;

  return html;
}

/**
 * Atualiza as estatísticas no topo da página
 * @param {Array} consultasArray - Array de consultas
 */
function updateStats(consultasArray) {
  const total = consultasArray.length;
  const proximos = filterProximas(consultasArray).length;
  const ativos = filterAtivas(consultasArray).length;

  document.getElementById("totalCount").textContent = total;
  document.getElementById("proximosCount").textContent = proximos;
  document.getElementById("ativosCount").textContent = ativos;
}

/**
 * Renderiza a página completa com consultas
 * @param {Array} consultasArray - Array de consultas
 */
function renderPage(consultasArray) {
  const sorted = sortConsultas([...consultasArray]);
  const container = document.getElementById("consultasContainer");
  const loadingEl = document.getElementById("loading");
  const emptyEl = document.getElementById("emptyState");

  if (sorted.length === 0) {
    emptyEl.classList.remove("hidden");
    container.classList.add("hidden");
  } else {
    emptyEl.classList.add("hidden");
    container.classList.remove("hidden");
    container.innerHTML = sorted.map(renderConsulta).join("\n");
  }

  updateStats(sorted);
  document.getElementById(
    "lastUpdate"
  ).textContent = `Última atualização: ${formatDateTime()}`;
  loadingEl.classList.add("hidden");
}

/**
 * Carrega consultas de arquivo JSON externo
 */
async function loadConsultas() {
  try {
    const loadingEl = document.getElementById("loading");
    const containerEl = document.getElementById("consultasContainer");
    const emptyEl = document.getElementById("emptyState");

    loadingEl.classList.remove("hidden");
    containerEl.classList.add("hidden");
    emptyEl.classList.add("hidden");

    // Tentar carregar de diferentes caminhos
    let dataUrl = "../data/consultas.json";
    let response = await fetch(dataUrl);

    // Se não encontrar em ../data/, tentar em data/
    if (!response.ok && response.status === 404) {
      dataUrl = "data/consultas.json";
      response = await fetch(dataUrl);
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    consultas = data.consultas || [];

    // Validar dados
    consultas = consultas.filter(isValidConsulta);

    renderPage(consultas);
    log(`Carregadas ${consultas.length} consultas`, "log");
  } catch (error) {
    log(`Erro ao carregar consultas: ${error.message}`, "error");
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("emptyState").classList.remove("hidden");
    document.getElementById("lastUpdate").textContent =
      "Erro ao carregar dados - verifique se data/consultas.json existe";
  }
}

/**
 * Inicializa a aplicação
 */
document.addEventListener("DOMContentLoaded", loadConsultas);

/**
 * Event listener para botão de atualizar
 */
document.addEventListener("DOMContentLoaded", () => {
  const refreshBtn = document.querySelector(
    'button[onclick="loadConsultas()"]'
  );
  if (refreshBtn) {
    refreshBtn.addEventListener("click", (e) => {
      e.preventDefault();
      loadConsultas();
    });
  }
});
