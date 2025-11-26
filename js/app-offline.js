/**
 * App-offline.js - Versão 100% offline com dados embutidos
 * Não depende de arquivos externos
 */

// DADOS EMBUTIDOS - Edite aqui para adicionar suas consultas!
const consultasOffline = [
  {
    id: "consulta_001",
    titulo: "Consulta Pública nº 42/2025 - Energias Renováveis",
    descricao:
      "Consulta sobre políticas de incentivo a energias renováveis e sustentáveis no Brasil.",
    data_abertura: "2025-11-20",
    data_encerramento: "2025-12-10",
    url_oficial: "https://consultas-publicas.mme.gov.br/home",
    notificado: false,
  },
  {
    id: "consulta_002",
    titulo: "Consulta Pública nº 43/2025 - Eficiência Energética",
    descricao:
      "Discussão pública sobre programas de eficiência energética industrial.",
    data_abertura: "2025-11-18",
    data_encerramento: "2025-12-03",
    url_oficial: "https://consultas-publicas.mme.gov.br/home",
    notificado: false,
  },
  {
    id: "consulta_003",
    titulo: "Consulta Pública nº 44/2025 - Mineração Sustentável",
    descricao:
      "Regulamentação de práticas de mineração com responsabilidade ambiental.",
    data_abertura: "2025-11-15",
    data_encerramento: "2025-12-01",
    url_oficial: "https://consultas-publicas.mme.gov.br/home",
    notificado: false,
  },
  {
    id: "consulta_004",
    titulo: "Consulta Pública nº 45/2025 - Matriz Energética",
    descricao: "Planejamento da matriz energética brasileira para 2030.",
    data_abertura: "2025-11-10",
    data_encerramento: "2025-11-28",
    url_oficial: "https://consultas-publicas.mme.gov.br/home",
    notificado: false,
  },
];

/**
 * Renderiza uma consulta como HTML string
 * @param {object} consulta - Objeto consulta
 * @returns {string} HTML da consulta
 */
function renderConsultaOffline(consulta) {
  const diasRestantes = calculateDaysRemaining(consulta.data_encerramento);
  const badgeClass = getBadgeClass(diasRestantes);
  const badgeText = getBadgeText(diasRestantes);
  const dataFormatada = formatDate(consulta.data_encerramento);

  return `
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
        
        ${
          consulta.descricao
            ? `<p class="text-gray-600 text-sm mb-4 line-clamp-3">${escapeHTML(
                consulta.descricao
              )}</p>`
            : ""
        }
        
        <div class="border-t border-gray-200 pt-4 mb-4">
          <div class="flex items-center text-sm text-gray-600 mb-2">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v2h16V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 011 1v1h1a1 1 0 110 2H7v1a1 1 0 11-2 0v-1H4a1 1 0 110-2h1V8a1 1 0 011-1z" clip-rule="evenodd"/>
            </svg>
            <strong>Encerramento:</strong>&nbsp;${dataFormatada}
          </div>
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
}

/**
 * Atualiza as estatísticas no topo da página
 * @param {Array} consultasArray - Array de consultas
 */
function updateStatsOffline(consultasArray) {
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
function renderPageOffline(consultasArray) {
  const sorted = sortConsultas([...consultasArray]);
  const container = document.getElementById("consultasContainer");

  if (sorted.length === 0) {
    container.innerHTML =
      '<p class="text-center text-gray-500">Nenhuma consulta carregada</p>';
  } else {
    container.innerHTML = sorted.map(renderConsultaOffline).join("\n");
  }

  updateStatsOffline(sorted);
  document.getElementById(
    "lastUpdate"
  ).textContent = `Última atualização: ${formatDateTime()}`;
}

/**
 * Inicializa a aplicação offline
 */
document.addEventListener("DOMContentLoaded", () => {
  renderPageOffline(consultasOffline);
});
