/**
 * Utilitários e funções compartilhadas
 * Usadas em múltiplos módulos
 */

/**
 * Calcula dias restantes até a data de encerramento
 * @param {string} dataEncerramento - Data no formato YYYY-MM-DD
 * @returns {number|null} Número de dias ou null se data inválida
 */
function calculateDaysRemaining(dataEncerramento) {
  if (!dataEncerramento) return null;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const [year, month, day] = dataEncerramento.split("-").map(Number);
  const encerramento = new Date(year, month - 1, day);
  const diffTime = encerramento - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
}

/**
 * Formata data YYYY-MM-DD para DD/MM/YYYY
 * @param {string} dateStr - Data no formato YYYY-MM-DD
 * @returns {string} Data formatada como DD/MM/YYYY
 */
function formatDate(dateStr) {
  if (!dateStr) return "N/A";
  const [year, month, day] = dateStr.split("-");
  return `${day}/${month}/${year}`;
}

/**
 * Retorna classe CSS da badge baseada em dias restantes
 * @param {number|null} diasRestantes - Número de dias ou null
 * @returns {string} Nome da classe CSS
 */
function getBadgeClass(diasRestantes) {
  if (diasRestantes === null) return "gray";
  if (diasRestantes > 7) return "green";
  if (diasRestantes > 0) return "yellow";
  return "red";
}

/**
 * Retorna texto da badge baseado em dias restantes
 * @param {number|null} diasRestantes - Número de dias ou null
 * @returns {string} Texto para exibir na badge
 */
function getBadgeText(diasRestantes) {
  if (diasRestantes === null) return "Data indeterminada";
  if (diasRestantes > 1) return `${diasRestantes} dias`;
  if (diasRestantes === 1) return "1 dia";
  if (diasRestantes === 0) return "Hoje";
  return "Encerrado";
}

/**
 * Escapa caracteres HTML para evitar XSS
 * @param {string} text - Texto a ser escapado
 * @returns {string} Texto escapado
 */
function escapeHTML(text) {
  if (!text) return "";
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Ordena array de consultas por dias restantes (crescente)
 * @param {Array} arr - Array de consultas
 * @returns {Array} Array ordenado
 */
function sortConsultas(arr) {
  return arr.sort((a, b) => {
    const diasA = calculateDaysRemaining(a.data_encerramento) || Infinity;
    const diasB = calculateDaysRemaining(b.data_encerramento) || Infinity;
    return diasA - diasB;
  });
}

/**
 * Filtra consultas que vencem em até 7 dias
 * @param {Array} arr - Array de consultas
 * @returns {Array} Consultas próximas do encerramento
 */
function filterProximas(arr) {
  return arr.filter((c) => {
    const dias = calculateDaysRemaining(c.data_encerramento);
    return dias !== null && dias > 0 && dias <= 7;
  });
}

/**
 * Filtra consultas ativas (ainda abertas)
 * @param {Array} arr - Array de consultas
 * @returns {Array} Consultas ativas
 */
function filterAtivas(arr) {
  return arr.filter((c) => {
    const dias = calculateDaysRemaining(c.data_encerramento);
    return dias !== null && dias > 0;
  });
}

/**
 * Formata timestamp para string legível
 * @param {Date|null} date - Data ou null para usar data atual
 * @returns {string} Data formatada em português
 */
function formatDateTime(date = null) {
  const d = date || new Date();
  return d.toLocaleString("pt-BR");
}

/**
 * Valida se um objeto é uma consulta válida
 * @param {object} obj - Objeto a validar
 * @returns {boolean} True se é uma consulta válida
 */
function isValidConsulta(obj) {
  return (
    obj &&
    typeof obj === "object" &&
    obj.id &&
    obj.titulo &&
    obj.data_encerramento &&
    obj.url_oficial
  );
}

/**
 * Logger com prefixo
 * @param {string} message - Mensagem
 * @param {string} level - Nível (log, warn, error)
 */
function log(message, level = "log") {
  const timestamp = new Date().toISOString();
  console[level](`[${timestamp}] ${message}`);
}
