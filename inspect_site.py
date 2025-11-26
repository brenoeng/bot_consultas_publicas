#!/usr/bin/env python3
"""
Script para inspecionar o site do MME usando Playwright
Renderiza JavaScript e extrai HTML final
"""

import asyncio
import json
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def inspect_mme_site():
    url = 'https://consultas-publicas.mme.gov.br/home'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("[1/3] Acessando site...")
        await page.goto(url, wait_until='networkidle', timeout=30000)

        print("[2/3] Aguardando carregamento de conteúdo...")
        # Esperar 3 segundos para JS completar
        await page.wait_for_timeout(3000)

        # Procurar elementos de consulta
        print("[3/3] Analisando conteúdo renderizado...")

        # Procurar por cards/divs com conteúdo de consulta
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # Salvar HTML renderizado
        with open('mme_rendered.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print(
            f"  - HTML renderizado salvo (site_rendered.html, {len(content)} bytes)")

        # Procurar por elementos visíveis
        print("\n=== ANALISE ===")

        # Procurar divs com classes
        divs_with_class = soup.find_all('div', class_=True)
        print(f"  - Total de divs com classe: {len(divs_with_class)}")

        # Classes mais frequentes
        classes_count = {}
        for div in divs_with_class:
            for cls in div.get('class', []):
                classes_count[cls] = classes_count.get(cls, 0) + 1

        print("\n=== TOP 20 CLASSES ===")
        for cls, count in sorted(classes_count.items(), key=lambda x: -x[1])[:20]:
            print(f"  .{cls}: {count}")

        # Procurar por elementos com texto "consulta"
        print("\n=== ELEMENTOS COM 'CONSULTA' ===")
        for elem in soup.find_all(string=lambda x: x and 'consulta' in x.lower())[:5]:
            parent = elem.parent
            text = str(elem)[:80]
            print(f"  - {parent.name}: {text}")

        # Procurar por atributos data-
        print("\n=== ATRIBUTOS DATA- ===")
        elements_with_data = soup.find_all(attrs={'data-testid': True})
        testids = set()
        for elem in elements_with_data:
            testid = elem.get('data-testid', '')
            testids.add(testid)

        if testids:
            for testid in list(testids)[:10]:
                print(f"  data-testid=\"{testid}\"")
        else:
            print("  Nenhum encontrado")

        # Procurar por elementos com role
        print("\n=== ELEMENTOS COM ROLE ===")
        for role in ['main', 'article', 'region', 'list', 'listitem']:
            elems = soup.find_all(attrs={'role': role})
            if elems:
                print(f"  role=\"{role}\": {len(elems)}")

        # Procurar por links que possam ser de consultas
        print("\n=== LINKS ENCONTRADOS (primeiros 10) ===")
        links = soup.find_all('a', href=True)
        consulta_links = []
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)[:60]
            if any(word in href.lower() for word in ['consulta', 'detalhe', 'view', 'id']):
                consulta_links.append((href, text))

        if consulta_links:
            for href, text in consulta_links[:10]:
                print(f"  [{text[:40]}...] -> {href[:60]}")
        else:
            print("  Nenhum link de consulta encontrado")

        # Procurar por datas (padrão YYYY-MM-DD ou DD/MM/YYYY)
        print("\n=== DATAS ENCONTRADAS (primeiros 5) ===")
        import re
        date_pattern = r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}'
        text_content = soup.get_text()
        dates = re.findall(date_pattern, text_content)
        if dates:
            for date in set(dates)[:5]:
                print(f"  {date}")
        else:
            print("  Nenhuma encontrada")

        await browser.close()

if __name__ == '__main__':
    print("=== Inspecionando site do MME ===\n")
    try:
        asyncio.run(inspect_mme_site())
        print("\n[OK] Inspecao concluida!")
    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
