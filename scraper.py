#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper de Consultas Públicas do MME
Extrai dados de https://consultas-publicas.mme.gov.br/home
Salva em data/consultas.json para uso nas páginas HTML
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
import sys
import hashlib
import re
from datetime import datetime
from pathlib import Path

# Configuração de encoding para Windows
import os
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('scraper.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class ConsultasPublicasScraper:
    """Scraper para consultas públicas do MME"""

    def __init__(self):
        self.base_url = "https://consultas-publicas.mme.gov.br/home"
        self.data_file = Path(__file__).parent / "data" / "consultas.json"
        self.max_retries = 3
        self.retry_delay = 2
        self.request_delay = 2.5

        # Criar diretório se não existir
        self.data_file.parent.mkdir(parents=True, exist_ok=True)

    def fetch_page(self):
        """Busca página do site com retry logic (tenta Selenium primeiro)"""
        # Tentar com Selenium para renderizar JavaScript
        logger.info("\nTentando com Selenium (renderizacao de JavaScript)...")
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service

            logger.info("  Inicializando browser Chrome...")
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(
                '--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-extensions')

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            logger.info(f"  Acessando {self.base_url}")
            driver.get(self.base_url)

            logger.info("  Aguardando carregamento...")
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script(
                    'return document.readyState') == 'complete'
            )
            time.sleep(2)  # Extra wait para conteudo dinamico

            html_content = driver.page_source
            driver.quit()

            logger.info("[OK] Página carregada e renderizada com Selenium")
            return html_content

        except Exception as e:
            logger.warning(f"  Selenium falhou: {e}")
            logger.info("  Tentando fallback com requests simples...")

        # Fallback: Tentar com requests (sem JavaScript)
        for attempt in range(self.max_retries):
            try:
                logger.info(
                    f"  Tentativa {attempt + 1}/{self.max_retries} - Requests...")

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }

                response = requests.get(
                    self.base_url, headers=headers, timeout=15)
                response.raise_for_status()

                logger.info("[OK] Página carregada com requests")
                return response.text

            except requests.Timeout:
                logger.warning(f"  Timeout na tentativa {attempt + 1}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (2 ** attempt))
            except requests.ConnectionError:
                logger.warning(f"  Erro de conexão na tentativa {attempt + 1}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (2 ** attempt))
            except requests.RequestException as e:
                logger.warning(f"  Erro HTTP na tentativa {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (2 ** attempt))

        logger.error("Falha ao acessar site após todas as tentativas")
        return None

    def parse_data(self, data_text):
        """Converte texto de data para YYYY-MM-DD"""
        if not data_text:
            return None

        data_text = data_text.lower().strip()

        # Dicionário de meses
        meses = {
            'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
            'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
            'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12',
            'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04',
            'mai': '05', 'jun': '06', 'jul': '07', 'ago': '08',
            'set': '09', 'out': '10', 'nov': '11', 'dez': '12'
        }

        try:
            # Padrão: DD/MM/YYYY
            if '/' in data_text:
                partes = [p.strip() for p in data_text.split('/')]
                if len(partes) == 3 and all(p.isdigit() for p in partes):
                    day, month, year = partes
                    if len(year) == 4:
                        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

            # Padrão: DD de mês de YYYY
            for mes_nome, mes_num in meses.items():
                pattern = rf'(\d{{1,2}})\s+de\s+{mes_nome}\s+de\s+(\d{{4}})'
                match = re.search(pattern, data_text)
                if match:
                    day, year = match.groups()
                    return f"{year}-{mes_num}-{day.zfill(2)}"

                # Padrão: DD mês YYYY
                pattern = rf'(\d{{1,2}})\s+{mes_nome}\s+(\d{{4}})'
                match = re.search(pattern, data_text)
                if match:
                    day, year = match.groups()
                    return f"{year}-{mes_num}-{day.zfill(2)}"

            logger.warning(f"Data não reconhecida: '{data_text}'")
            return None

        except Exception as e:
            logger.warning(f"Erro ao processar data '{data_text}': {e}")
            return None

    def calcular_dias_restantes(self, data_encerramento):
        """Calcula dias entre hoje e data de encerramento"""
        try:
            today = datetime.now().date()
            parts = data_encerramento.split('-')
            end_date = datetime(int(parts[0]), int(
                parts[1]), int(parts[2])).date()
            dias = (end_date - today).days
            return max(dias, 0)  # Não retorna valores negativos
        except:
            return 0

    def gerar_id_unico(self, titulo):
        """Gera ID único baseado no título"""
        # Remove caracteres especiais e converte para minúsculas
        clean = re.sub(r'[^a-z0-9\s]', '', titulo.lower())
        clean = re.sub(r'\s+', '_', clean.strip())
        # Hash para garantir unicidade
        hash_obj = hashlib.md5(titulo.encode())
        return f"consulta_{clean[:30]}_{hash_obj.hexdigest()[:8]}"

    def validar_consulta(self, consulta):
        """Valida se consulta tem campos obrigatórios"""
        campos_obrigatorios = ['id', 'titulo',
                               'data_encerramento', 'url_oficial']

        for campo in campos_obrigatorios:
            if not consulta.get(campo):
                logger.warning(f"Consulta inválida: falta campo '{campo}'")
                return False

        # Validar formato de data
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', consulta.get('data_encerramento', '')):
            logger.warning(
                f"Data inválida: {consulta.get('data_encerramento')}")
            return False

        return True

    def parse_consultas(self, html_content):
        """Extrai dados das consultas do HTML"""
        if not html_content:
            logger.error("HTML vazio")
            return []

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            consultas = []

            # Procurar por componentes app-card-consulta-publica (Angular)
            cards = soup.select('app-card-consulta-publica')

            if not cards:
                # Fallback: procurar por divs com classe "br-card"
                cards = soup.find_all('div', class_='br-card')

            logger.info(f"Encontrados {len(cards)} elementos de consulta")

            for card in cards:
                try:
                    # Extrair todo o texto do card
                    text = card.get_text()

                    # Padrão: "Consulta Pública n° XXX de DD/MM/YYYY"
                    match = re.search(
                        r'Consulta Pública.*?n°?\s*(\d+).*?de\s+(\d{1,2}/\d{1,2}/\d{4})',
                        text,
                        re.IGNORECASE
                    )

                    if not match:
                        continue

                    numero_consulta, data_abertura_str = match.groups()
                    data_abertura = self.parse_data(data_abertura_str)

                    # Procurar por datas de encerramento
                    # Padrão: "DD/MM/YYYY até DD/MM/YYYY"
                    datas_match = re.findall(
                        r'(\d{1,2}/\d{1,2}/\d{4})\s+até\s+(\d{1,2}/\d{1,2}/\d{4})',
                        text
                    )

                    if not datas_match:
                        # Tentar apenas encontrar a segunda data
                        datas = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', text)
                        if len(datas) < 2:
                            continue
                        data_encerramento = self.parse_data(datas[1])
                    else:
                        data_abertura_tmp, data_encerramento_str = datas_match[0]
                        data_encerramento = self.parse_data(
                            data_encerramento_str)

                    if not data_encerramento:
                        continue

                    # Extrair título (após o padrão "Consulta Pública n° XXX de DD/MM/YYYY")
                    # O título começa logo após a data de abertura
                    titulo_pattern = r'Consulta Pública.*?n°?\s*\d+\s+de\s+\d{1,2}/\d{1,2}/\d{4}\s*(.+?)(?:\n|Área Responsável|Secretaria|$)'
                    titulo_match = re.search(
                        titulo_pattern, text, re.IGNORECASE | re.DOTALL)

                    if titulo_match:
                        titulo = titulo_match.group(1).strip()
                        # Limpar e pegar primeira linha significativa
                        linhas = [l.strip()
                                  for l in titulo.split('\n') if l.strip()]
                        titulo = linhas[0] if linhas else titulo
                    else:
                        titulo = f"Consulta Pública {numero_consulta}"

                    # Limpar título
                    titulo = titulo[:200].strip()
                    if not titulo or len(titulo) < 5:
                        titulo = f"Consulta Pública {numero_consulta}"

                    # Procurar por URL/link
                    link = card.find('a', href=True)
                    if link:
                        url_oficial = link['href']
                    else:
                        # Gerar URL padrão baseado no número
                        url_oficial = f"https://consultas-publicas.mme.gov.br/consulta/{numero_consulta}"

                    if url_oficial.startswith('/'):
                        url_oficial = 'https://consultas-publicas.mme.gov.br' + url_oficial

                    # Extrair descrição
                    descricao = ""
                    paragrafos = card.find_all('p')
                    if paragrafos:
                        descricao = paragrafos[0].get_text(strip=True)
                    else:
                        # Pegar primeira linha após o título
                        lines = [l.strip()
                                 for l in text.split('\n') if l.strip()]
                        if len(lines) > 2:
                            descricao = lines[2]

                    descricao = descricao[:500]  # Limitar tamanho

                    # Construir consulta
                    consulta = {
                        "id": f"consulta_{numero_consulta}",
                        "numero": int(numero_consulta),
                        "titulo": titulo,
                        "descricao": descricao,
                        "data_abertura": data_abertura if data_abertura else datetime.now().strftime("%Y-%m-%d"),
                        "data_encerramento": data_encerramento,
                        "url_oficial": url_oficial,
                        "dias_restantes": self.calcular_dias_restantes(data_encerramento),
                        "notificado": False
                    }

                    if self.validar_consulta(consulta):
                        # Evitar duplicatas (mesmo ID)
                        if not any(c['id'] == consulta['id'] for c in consultas):
                            consultas.append(consulta)
                            logger.info(f"[+] {titulo[:60]}")

                except Exception as e:
                    logger.warning(f"Erro ao processar card: {e}")
                    continue

            logger.info(f"Total de consultas extraídas: {len(consultas)}")
            return consultas

        except Exception as e:
            logger.error(f"Erro ao fazer parsing: {e}")
            return []

    def carregar_existentes(self):
        """Carrega consultas existentes do arquivo"""
        if not self.data_file.exists():
            return []

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('consultas', [])
        except:
            return []

    def mesclar_dados(self, novas, existentes):
        """Mescla novas consultas com existentes, mantendo status de notificação"""
        ids_novas = {c['id'] for c in novas}
        ids_existentes = {c['id'] for c in existentes}

        # Manter notificação de consultas que continuam
        for nova in novas:
            for existente in existentes:
                if nova['id'] == existente['id']:
                    nova['notificado'] = existente.get('notificado', False)
                    break

        # Novas consultas
        resultado = list(novas)

        # Manter antigas que saíram da página (para arquivo)
        # para_arquivar = [c for c in existentes if c['id'] not in ids_novas]

        return resultado

    def salvar_dados(self, consultas):
        """Salva consultas em JSON"""
        try:
            # Ordenar por dias restantes (menor primeiro)
            consultas_ordenadas = sorted(
                consultas, key=lambda x: x.get('dias_restantes', 999))

            dados = {
                "consultas": consultas_ordenadas,
                "ultimaAtualizacao": datetime.now().isoformat()
            }

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)

            logger.info(f"[OK] Dados salvos em {self.data_file}")
            logger.info(f"  - {len(consultas)} consultas")
            logger.info(f"  - Atualizado em {dados['ultimaAtualizacao']}")
            return True

        except Exception as e:
            logger.error(f"✗ Erro ao salvar dados: {e}")
            return False

    def run(self):
        """Executa o scraper completo"""
        logger.info("=" * 70)
        logger.info("Iniciando scraper de Consultas Publicas do MME")
        logger.info("=" * 70)

        # 1. Buscar página
        logger.info("\n[1/4] Buscando página do site...")
        html = self.fetch_page()
        if not html:
            logger.error("Falha ao buscar página. Abortando.")
            return False

        # 2. Fazer parsing
        logger.info("\n[2/4] Fazendo parsing dos dados...")
        novas_consultas = self.parse_consultas(html)
        if not novas_consultas:
            logger.warning(
                "Nenhuma consulta encontrada. Site pode ter estrutura diferente.")

        # 3. Mesclar com existentes
        logger.info("\n[3/4] Mesclando com dados existentes...")
        existentes = self.carregar_existentes()
        consultas_finais = self.mesclar_dados(novas_consultas, existentes)

        # 4. Salvar
        logger.info("\n[4/4] Salvando dados...")
        sucesso = self.salvar_dados(consultas_finais)

        logger.info("\n" + "=" * 70)
        if sucesso:
            logger.info("[OK] SCRAPER CONCLUIDO COM SUCESSO")
        else:
            logger.warning("[!] SCRAPER CONCLUIDO COM AVISOS")
        logger.info("=" * 70)

        return sucesso


def main():
    """Função principal"""
    try:
        scraper = ConsultasPublicasScraper()
        sucesso = scraper.run()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        logger.info("\n⚠ Scraper interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        logger.error(f"✗ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
