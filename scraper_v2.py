#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper v2 com suporte a JavaScript rendering
"""

import json
import logging
import sys
import os
from pathlib import Path
from datetime import datetime

# Configuração de encoding para Windows
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


def test_selenium():
    """Testa se Selenium pode acessar o site"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service

        logger.info("[Selenium] Inicializando browser...")

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        logger.info("[Selenium] Acessando site...")
        driver.get('https://consultas-publicas.mme.gov.br/home')

        # Aguardar carregamento
        logger.info("[Selenium] Aguardando carregamento de conteúdo...")
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script(
                'return document.readyState') == 'complete'
        )

        # Tentar encontrar elementos de consulta
        logger.info("[Selenium] Procurando elementos...")

        # Vários seletores a tentar
        selectors = [
            'div[class*="card"]',
            'div[class*="consulta"]',
            'div[class*="item"]',
            'article',
            'section[class*="content"]',
            'app-consultation',
            '[role="article"]',
        ]

        found = False
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    logger.info(
                        f"[Selenium] Encontrado: {len(elements)} elementos com '{selector}'")
                    found = True

                    # Analisar primeiro elemento
                    first_elem = elements[0]
                    html = first_elem.get_attribute('outerHTML')[:200]
                    logger.info(f"[Selenium] Amostra: {html}...")
                    break
            except:
                pass

        if not found:
            logger.warning(
                "[Selenium] Nenhum elemento encontrado com seletores conhecidos")
            # Salvar HTML completo para inspeção
            html_content = driver.page_source
            with open('selenium_rendered.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(
                f"[Selenium] HTML salvo em selenium_rendered.html ({len(html_content)} bytes)")

        driver.quit()
        return True

    except ImportError as e:
        logger.error(f"[Selenium] Modulo nao disponivel: {e}")
        return False
    except Exception as e:
        logger.error(f"[Selenium] Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal"""
    logger.info("=" * 70)
    logger.info("Testando acesso ao site com Selenium + JavaScript")
    logger.info("=" * 70)

    # Verificar se Selenium/ChromeDriver estão disponíveis
    logger.info("\n[1/2] Verificando dependências...")
    try:
        from selenium import webdriver
        logger.info("  [OK] Selenium instalado")
    except ImportError:
        logger.error("  [ERRO] Selenium nao instalado")
        logger.info("  Instale com: pip install selenium webdriver-manager")
        return False

    # Tentar com Selenium
    logger.info("\n[2/2] Testando acesso ao site...")
    success = test_selenium()

    if success:
        logger.info("\n[OK] Teste concluido com sucesso!")
        logger.info(
            "     Agora o scraper pode usar Selenium para renderizar JavaScript")
    else:
        logger.warning("\n[AVISO] Teste inconclusivo")
        logger.info("         Verifique os erros acima")

    logger.info("=" * 70)


if __name__ == '__main__':
    main()
