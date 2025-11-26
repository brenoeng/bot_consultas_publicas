#!/usr/bin/env python3
"""
Diagnóstico do workflow automático
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def print_header(title):
    """Printa um header formatado"""
    print(f"\n{'=' * 70}")
    print(f"📋 {title}")
    print(f"{'=' * 70}\n")

def check_files():
    """Verifica arquivos necessários"""
    print_header("VERIFICAÇÃO DE ARQUIVOS")
    
    files = {
        'scraper.py': '🕷️  Script de scraping',
        'requirements.txt': '📦 Dependências Python',
        'data/': '💾 Pasta de dados',
        '.github/workflows/check-consultas.yml': '⚙️  Workflow GitHub Actions',
        'docs/index.html': '📄 Página HTML',
    }
    
    all_ok = True
    for file, label in files.items():
        exists = Path(file).exists()
        status = '✅' if exists else '❌'
        print(f"{status} {label:30} → {file}")
        if not exists:
            all_ok = False
    
    return all_ok

def check_scraper():
    """Verifica conteúdo do scraper.py"""
    print_header("VERIFICAÇÃO DO SCRAPER.PY")
    
    if not Path('scraper.py').exists():
        print("❌ scraper.py não encontrado!")
        return False
    
    with open('scraper.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        'def ': 'Contém funções',
        'requests': 'Importa requests',
        'BeautifulSoup': 'Importa BeautifulSoup',
        'selenium': 'Importa Selenium',
        'if __name__': 'Tem bloco main',
        'data/consultas.json': 'Salva em data/consultas.json',
    }
    
    all_ok = True
    for check, label in checks.items():
        found = check in content
        status = '✅' if found else '⚠️ '
        print(f"{status} {label:30} → {check}")
        if not found and check != 'requests':  # requests é opcional
            all_ok = False
    
    # Tamanho do arquivo
    lines = len(content.split('\n'))
    print(f"\n📊 Tamanho: {len(content)} caracteres, {lines} linhas")
    
    return all_ok

def check_requirements():
    """Verifica requirements.txt"""
    print_header("VERIFICAÇÃO DE DEPENDÊNCIAS")
    
    if not Path('requirements.txt').exists():
        print("❌ requirements.txt não encontrado!")
        return False
    
    with open('requirements.txt', 'r') as f:
        reqs = f.read()
    
    required = {
        'selenium': 'Scraping com JavaScript',
        'beautifulsoup4': 'Parse HTML',
        'requests': 'HTTP requests',
        'webdriver-manager': 'Gerenciar ChromeDriver',
    }
    
    all_ok = True
    for pkg, desc in required.items():
        found = pkg in reqs
        status = '✅' if found else '❌'
        print(f"{status} {pkg:20} → {desc}")
        if not found:
            all_ok = False
    
    # Mostra conteúdo
    print(f"\n📝 Conteúdo de requirements.txt:")
    print("─" * 70)
    print(reqs)
    print("─" * 70)
    
    return all_ok

def check_workflow():
    """Verifica workflow YAML"""
    print_header("VERIFICAÇÃO DO WORKFLOW")
    
    workflow_file = Path('.github/workflows/check-consultas.yml')
    
    if not workflow_file.exists():
        print("❌ Workflow não encontrado em .github/workflows/check-consultas.yml")
        return False
    
    with open(workflow_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        'schedule:': 'Tem agendamento (cron)',
        'cron:': 'Configuração cron presente',
        'python scraper.py': 'Executa scraper.py',
        'Setup Python': 'Configura Python',
        'requirements.txt': 'Instala dependências',
        'workflow_dispatch': 'Permite execução manual',
    }
    
    all_ok = True
    for check, label in checks.items():
        found = check in content
        status = '✅' if found else '❌'
        print(f"{status} {label:30} → {check}")
        if not found:
            all_ok = False
    
    # Mostra parte relevante
    if 'schedule:' in content:
        print(f"\n📅 Horários de execução configurados:")
        for line in content.split('\n'):
            if 'cron:' in line:
                print(f"   {line.strip()}")
    
    return all_ok

def check_data():
    """Verifica arquivo de dados"""
    print_header("VERIFICAÇÃO DE DADOS")
    
    data_file = Path('data/consultas.json')
    
    if not data_file.exists():
        print("⚠️  data/consultas.json não encontrado (será criado na primeira execução)")
        return True
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ JSON válido")
        print(f"   Número de consultas: {len(data.get('consultas', []))}")
        print(f"   Última atualização: {data.get('ultimaAtualizacao', 'N/A')}")
        
        if data.get('consultas'):
            print(f"\n📊 Amostra de dados:")
            for i, c in enumerate(data['consultas'][:2], 1):
                print(f"\n   Consulta {i}:")
                print(f"     ID: {c.get('id')}")
                print(f"     Título: {c.get('titulo', '')[:50]}...")
                print(f"     Dias restantes: {c.get('dias_restantes')}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return False

def run_scraper_test():
    """Testa se o scraper pode ser importado"""
    print_header("TESTE DE SCRAPER")
    
    try:
        # Tenta importar
        import sys
        sys.path.insert(0, str(Path.cwd()))
        
        # Verifica sintaxe
        with open('scraper.py', 'r', encoding='utf-8') as f:
            compile(f.read(), 'scraper.py', 'exec')
        
        print("✅ scraper.py tem sintaxe válida (Python)")
        return True
    except SyntaxError as e:
        print(f"❌ Erro de sintaxe em scraper.py:")
        print(f"   Linha {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"⚠️  Não foi possível verificar: {e}")
        return True

def main():
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  🔍 DIAGNÓSTICO - WORKFLOW AUTOMÁTICO DE SCRAPING".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    results = {}
    
    results['files'] = check_files()
    results['scraper'] = check_scraper()
    results['requirements'] = check_requirements()
    results['workflow'] = check_workflow()
    results['data'] = check_data()
    results['syntax'] = run_scraper_test()
    
    # Resumo
    print_header("RESUMO")
    
    all_ok = all(results.values())
    
    status_map = {
        'files': 'Arquivos necessários',
        'scraper': 'Conteúdo do scraper.py',
        'requirements': 'Dependências',
        'workflow': 'Configuração GitHub Actions',
        'data': 'Arquivo de dados',
        'syntax': 'Sintaxe Python',
    }
    
    for key, label in status_map.items():
        status = '✅' if results[key] else '❌'
        print(f"{status} {label}")
    
    print("\n" + "=" * 70)
    
    if all_ok:
        print("✅ TUDO OK! Seu workflow está pronto para usar.")
        print("\n📝 Próximos passos:")
        print("   1. git add .")
        print("   2. git commit -m 'fix: workflow automático'")
        print("   3. git push origin main")
        print("\n   Depois de 5 minutos, vá para:")
        print("   https://github.com/brenoeng/bot_consultas_publicas/actions")
        return 0
    else:
        print("⚠️  PROBLEMAS DETECTADOS - Veja acima os itens com ❌")
        return 1

if __name__ == '__main__':
    sys.exit(main())
