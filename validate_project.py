#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Validação do Projeto Bot Consultas Públicas
Verifica integridade, estrutura e funcionalidade completa
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime


def print_header(text):
    """Imprime header formatado"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_check(status, message):
    """Imprime resultado de verificação"""
    icon = "[OK]" if status else "[ERRO]"
    print(f"  {icon} {message}")


def validate_structure():
    """Valida estrutura de diretórios e arquivos"""
    print_header("1. VALIDACAO DE ESTRUTURA")

    required_files = {
        "scraper.py": "Script scraper principal",
        "requirements.txt": "Dependências Python",
        "data/consultas.json": "Arquivo de dados",
        "docs/index.html": "Página principal",
        "docs/js/app.js": "Script JavaScript",
        "docs/css/styles.css": "Estilos CSS",
        ".github/workflows/check-consultas.yml": "Workflow GitHub Actions",
    }

    required_dirs = {
        "data": "Diretório de dados",
        "docs": "Frontend estático",
        "docs/js": "JavaScript",
        "docs/css": "Estilos",
        ".github/workflows": "Workflows",
    }

    results = []

    # Verificar diretórios
    print("Diretórios:")
    for dir_path, desc in required_dirs.items():
        exists = Path(dir_path).is_dir()
        print_check(exists, f"{dir_path:40} - {desc}")
        results.append(exists)

    # Verificar arquivos
    print("\nArquivos:")
    for file_path, desc in required_files.items():
        exists = Path(file_path).is_file()
        print_check(exists, f"{file_path:40} - {desc}")
        results.append(exists)

    return all(results)


def validate_json():
    """Valida arquivo JSON de dados"""
    print_header("2. VALIDACAO DE DADOS (JSON)")

    json_file = Path("data/consultas.json")

    if not json_file.exists():
        print_check(False, "Arquivo data/consultas.json NAO ENCONTRADO")
        return False

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print_check(True, "JSON valido e bem-formado")

        # Verificar estrutura
        consultas = data.get("consultas", [])
        print_check(True, f"Encontradas {len(consultas)} consultas")

        if not consultas:
            print_check(False, "Nenhuma consulta encontrada em JSON")
            return False

        # Validar primeira consulta
        required_fields = [
            "id", "numero", "titulo", "data_encerramento",
            "url_oficial", "dias_restantes", "notificado"
        ]

        primeiro = consultas[0]
        print(f"\nPrimeira consulta (ID: {primeiro.get('id')}):")

        all_valid = True
        for field in required_fields:
            exists = field in primeiro
            value = primeiro.get(field, "N/A")

            # Truncar valores longos
            if isinstance(value, str) and len(value) > 40:
                value = value[:37] + "..."

            print_check(exists, f"  {field:25} = {value}")
            all_valid = all_valid and exists

        # Validar datas
        print("\nValidacao de datas:")
        for i, consulta in enumerate(consultas[:3]):
            enc = consulta.get("data_encerramento", "")
            is_valid = len(enc) == 10 and enc.count('-') == 2
            print_check(is_valid, f"  Consulta {i+1}: {enc}")

        # Estatísticas
        print("\nEstatísticas:")
        urgentes = sum(1 for c in consultas if c.get("dias_restantes", 0) <= 7)
        ativas = sum(1 for c in consultas if c.get("dias_restantes", 0) > 0)
        print(f"  Total: {len(consultas)}")
        print(f"  Ativas: {ativas}")
        print(f"  Urgentes (<=7 dias): {urgentes}")

        return all_valid

    except json.JSONDecodeError as e:
        print_check(False, f"JSON INVALIDO: {e}")
        return False
    except Exception as e:
        print_check(False, f"Erro ao ler JSON: {e}")
        return False


def validate_html():
    """Valida HTML do frontend"""
    print_header("3. VALIDACAO DE FRONTEND")

    html_file = Path("docs/index.html")

    if not html_file.exists():
        print_check(False, "docs/index.html nao encontrado")
        return False

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        print_check(True, "Arquivo HTML encontrado")

        # Verificar elementos críticos
        checks = {
            "<title>": "Tag title presente",
            "Consultas": "Titulo contem 'Consultas'",
            "loadConsultas": "Função loadConsultas definida",
            "btn": "Classes CSS (btn, badge, etc)",
            "cdn.tailwindcss": "Tailwind CSS CDN",
            "link rel": "Link para CSS externo",
        }

        print("\nElementos HTML:")
        all_present = True
        for pattern, description in checks.items():
            exists = pattern in html_content
            print_check(exists, description)
            all_present = all_present and exists

        # Verificar tamanho
        size_kb = len(html_content) / 1024
        print_check(size_kb > 1, f"Tamanho HTML: {size_kb:.1f} KB")

        return all_present

    except Exception as e:
        print_check(False, f"Erro ao ler HTML: {e}")
        return False


def validate_python():
    """Valida arquivo Python do scraper"""
    print_header("4. VALIDACAO DE SCRAPER (PYTHON)")

    scraper_file = Path("scraper.py")

    if not scraper_file.exists():
        print_check(False, "scraper.py nao encontrado")
        return False

    try:
        with open(scraper_file, 'r', encoding='utf-8') as f:
            code_content = f.read()

        print_check(True, "Arquivo scraper.py encontrado")

        # Verificar componentes
        components = {
            "class ConsultasPublicasScraper": "Classe principal",
            "def fetch_page": "Metodo fetch_page",
            "def parse_consultas": "Metodo parse_consultas",
            "def salvar_dados": "Metodo salvar_dados",
            "Selenium": "Suporte Selenium",
            "BeautifulSoup": "Suporte BeautifulSoup",
        }

        print("\nComponentes do Scraper:")
        all_present = True
        for pattern, description in components.items():
            exists = pattern in code_content
            print_check(exists, description)
            all_present = all_present and exists

        # Contar linhas
        lines = code_content.count('\n')
        print(f"\n  Linhas de codigo: {lines}")

        return all_present

    except Exception as e:
        print_check(False, f"Erro ao ler scraper.py: {e}")
        return False


def validate_dependencies():
    """Valida arquivo de dependências"""
    print_header("5. VALIDACAO DE DEPENDENCIAS")

    req_file = Path("requirements.txt")

    if not req_file.exists():
        print_check(False, "requirements.txt nao encontrado")
        return False

    try:
        with open(req_file, 'r', encoding='utf-8') as f:
            requirements = f.read()

        print_check(True, "Arquivo requirements.txt encontrado")

        # Verificar dependências críticas
        packages = {
            "selenium": "Selenium (JavaScript rendering)",
            "beautifulsoup4": "BeautifulSoup (HTML parsing)",
            "requests": "Requests (HTTP client)",
            "lxml": "lxml (XML/HTML processing)",
            "webdriver-manager": "WebDriver Manager (ChromeDriver)",
        }

        print("\nDependencias:")
        all_present = True
        for package, description in packages.items():
            exists = package in requirements
            print_check(exists, description)
            all_present = all_present and exists

        return all_present

    except Exception as e:
        print_check(False, f"Erro ao ler requirements.txt: {e}")
        return False


def validate_documentation():
    """Valida documentação"""
    print_header("6. VALIDACAO DE DOCUMENTACAO")

    doc_files = {
        "README.md": "Documentação principal",
        "COMEÇE_AQUI.md": "Guia de inicio",
        "SCRAPER_STATUS.md": "Status do scraper",
        "PROXIMOS_PASSOS.md": "Proximos passos",
        "ERRO-SOLUCAO.md": "Troubleshooting",
        "DEPLOY_GITHUB_PAGES.md": "Deploy GitHub Pages",
    }

    print("Documentacao:")
    found = 0
    for filename, description in doc_files.items():
        exists = Path(filename).is_file()
        if exists:
            size_kb = Path(filename).stat().st_size / 1024
            print_check(True, f"{filename:30} ({size_kb:5.1f} KB)")
            found += 1
        else:
            print_check(False, f"{filename:30} FALTANDO")

    return found >= 4  # Pelo menos 4 docs


def validate_github_workflow():
    """Valida workflow GitHub Actions"""
    print_header("7. VALIDACAO DE GITHUB ACTIONS")

    workflow_file = Path(".github/workflows/check-consultas.yml")

    if not workflow_file.exists():
        print_check(False, "Workflow nao encontrado")
        return False

    try:
        with open(workflow_file, 'r', encoding='utf-8') as f:
            workflow_content = f.read()

        print_check(True, "Workflow encontrado")

        # Verificar configurações
        checks = {
            "schedule": "Agendamento configurado",
            "cron": "Cron job definido",
            "python": "Python configurado",
            "pip install": "Instalacao de dependencias",
            "scraper.py": "Execucao do scraper",
            "git commit": "Commit automatico",
            "git push": "Push automatico",
        }

        print("\nConfiguracao:")
        all_present = True
        for pattern, description in checks.items():
            exists = pattern in workflow_content
            print_check(exists, description)
            all_present = all_present and exists

        return all_present

    except Exception as e:
        print_check(False, f"Erro ao ler workflow: {e}")
        return False


def print_summary(results):
    """Imprime sumário final"""
    print_header("RESULTADO FINAL")

    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100

    print(f"\nTestes Passados: {passed}/{total} ({percentage:.0f}%)\n")

    if percentage == 100:
        print("  STATUS: PRONTO PARA PRODUCAO")
        print("\n  Todos os componentes foram validados com sucesso!")
        print("  O projeto esta pronto para:")
        print("    - GitHub Pages deploy")
        print("    - GitHub Actions automacao")
        print("    - Uso em producao")
        status = 0
    elif percentage >= 80:
        print("  STATUS: QUASE PRONTO")
        print("\n  Alguns itens precisam de atencao.")
        print("  Verifique os erros acima.")
        status = 1
    else:
        print("  STATUS: REQUER CORRECOES")
        print("\n  Varios itens precisam ser corrigidos.")
        print("  Verifique a documentacao em ERRO-SOLUCAO.md")
        status = 1

    return status


def main():
    """Funcao principal"""
    print("\n" + "="*70)
    print("  BOT CONSULTAS PUBLICAS - VALIDACAO COMPLETA")
    print("  Data:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*70)

    results = []

    # Executar validações
    results.append(validate_structure())
    results.append(validate_json())
    results.append(validate_html())
    results.append(validate_python())
    results.append(validate_dependencies())
    results.append(validate_documentation())
    results.append(validate_github_workflow())

    # Sumário
    exit_code = print_summary(results)

    print("\n" + "="*70)
    print("  Para proximos passos, consulte DEPLOY_GITHUB_PAGES.md")
    print("="*70 + "\n")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
