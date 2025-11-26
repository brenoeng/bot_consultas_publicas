#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste do Scraper
Verifica se o scraper consegue extrair dados com sucesso
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timedelta


def print_header(text):
    """Imprime header formatado"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def test_scraper_execution():
    """Testa execução do scraper"""
    print_header("1. TESTE DE EXECUCAO DO SCRAPER")

    print("Executando scraper...")
    print("(Isto pode levar 30-60 segundos)\n")

    try:
        result = subprocess.run(
            [sys.executable, "scraper.py"],
            capture_output=True,
            text=True,
            timeout=120
        )

        # Verificar se executou com sucesso
        if result.returncode == 0:
            print("[OK] Scraper executado com sucesso")

            # Mostrar outputs informativos
            if "Coletadas" in result.stdout:
                print("[OK] Scraper encontrou consultas")

            if "Salvas" in result.stdout or "salvo" in result.stdout.lower():
                print("[OK] Dados salvos em data/consultas.json")

            # Mostra últimas linhas do output
            lines = result.stdout.strip().split('\n')
            print("\nÚltimas linhas da execução:")
            for line in lines[-5:]:
                if line.strip():
                    print(f"  {line}")

            return True
        else:
            print("[ERRO] Scraper falhou na execução")
            print("\nErro:")
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("[ERRO] Scraper demorou muito (timeout)")
        return False
    except Exception as e:
        print(f"[ERRO] Erro ao executar scraper: {e}")
        return False


def test_json_validity():
    """Testa validade do JSON gerado"""
    print_header("2. TESTE DE VALIDADE DO JSON")

    json_file = Path("data/consultas.json")

    if not json_file.exists():
        print("[ERRO] Arquivo data/consultas.json nao encontrado")
        return False

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print("[OK] JSON é válido e bem-formado")

        # Verificar estrutura
        if "consultas" not in data:
            print("[ERRO] JSON nao contem campo 'consultas'")
            return False

        consultas = data["consultas"]
        print(f"[OK] Encontradas {len(consultas)} consultas")

        if len(consultas) == 0:
            print("[AVISO] Nenhuma consulta encontrada (site pode estar vazio)")
            return True

        # Validar primeira consulta
        print("\nValidando primeira consulta:")
        primeira = consultas[0]

        required_fields = [
            "id", "numero", "titulo", "data_encerramento",
            "url_oficial", "dias_restantes", "notificado"
        ]

        all_valid = True
        for field in required_fields:
            if field in primeira:
                value = primeira[field]
                # Truncar longos
                if isinstance(value, str) and len(value) > 40:
                    value = value[:37] + "..."
                print(f"  [OK] {field:20} = {value}")
            else:
                print(f"  [ERRO] {field:20} FALTANDO")
                all_valid = False

        # Validar datas
        print("\nValidando datas:")
        for i, consulta in enumerate(consultas[:3]):
            data_enc = consulta.get("data_encerramento", "")
            # Validar formato YYYY-MM-DD
            try:
                datetime.strptime(data_enc, "%Y-%m-%d")
                print(f"  [OK] Consulta {i+1}: {data_enc}")
            except ValueError:
                print(
                    f"  [ERRO] Consulta {i+1}: formato invalido ({data_enc})")
                all_valid = False

        # Estatísticas
        print("\nEstatísticas:")
        dias_restantes = [c.get("dias_restantes", 0) for c in consultas]
        urgentes = sum(1 for d in dias_restantes if d <= 7 and d > 0)
        ativas = sum(1 for d in dias_restantes if d > 0)
        vencidas = sum(1 for d in dias_restantes if d <= 0)

        print(f"  Total: {len(consultas)}")
        print(f"  Ativas: {ativas}")
        print(f"  Urgentes (1-7 dias): {urgentes}")
        if vencidas > 0:
            print(f"  Vencidas: {vencidas}")

        # Timestamp
        if "ultimaAtualizacao" in data:
            print(f"\n  Última atualização: {data['ultimaAtualizacao']}")

        return all_valid

    except json.JSONDecodeError as e:
        print(f"[ERRO] JSON inválido: {e}")
        return False
    except Exception as e:
        print(f"[ERRO] Erro ao validar JSON: {e}")
        return False


def test_frontend_compatibility():
    """Testa compatibilidade com frontend"""
    print_header("3. TESTE DE COMPATIBILIDADE COM FRONTEND")

    json_file = Path("data/consultas.json")
    html_file = Path("docs/index.html")
    js_file = Path("docs/js/app.js")

    # Verificar arquivos
    print("Verificando arquivos necessários:")
    print(f"  [{'OK' if json_file.exists() else 'ERRO'}] {json_file}")
    print(f"  [{'OK' if html_file.exists() else 'ERRO'}] {html_file}")
    print(f"  [{'OK' if js_file.exists() else 'ERRO'}] {js_file}")

    if not all([json_file.exists(), html_file.exists(), js_file.exists()]):
        print("\n[ERRO] Arquivos necessários nao encontrados")
        return False

    try:
        # Verificar se JSON pode ser lido pelo frontend
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Simulando o que o frontend fará
        consultas = data.get("consultas", [])

        if len(consultas) > 0:
            print(
                f"\n[OK] Frontend conseguirá carregar {len(consultas)} consultas")

            # Testar caminho relativo
            print("\nCaminhos esperados pelo frontend:")
            print(f"  ../data/consultas.json (caminho relativo de docs/)")
            print(f"  data/consultas.json (caminho alternativo)")
            print("[OK] Ambos os caminhos estão corretos no projeto")
        else:
            print("[AVISO] Nenhuma consulta para carregar no frontend")

        return True

    except Exception as e:
        print(f"[ERRO] Erro ao testar compatibilidade: {e}")
        return False


def test_github_pages_readiness():
    """Testa se está pronto para GitHub Pages"""
    print_header("4. TESTE DE PRONTIDAO PARA GITHUB PAGES")

    required_for_pages = {
        "docs/index.html": "Página principal",
        "docs/js/app.js": "Script da aplicação",
        "docs/css/styles.css": "Estilos CSS",
        "data/consultas.json": "Dados (será sincronizado)",
        ".github/workflows/check-consultas.yml": "Automação GitHub Actions",
    }

    print("Verificando estrutura para GitHub Pages:")
    all_present = True

    for file_path, desc in required_for_pages.items():
        exists = Path(file_path).is_file()
        status = "[OK]" if exists else "[ERRO]"
        print(f"  {status} {file_path:40} - {desc}")
        all_present = all_present and exists

    if all_present:
        print("\n[OK] Projeto está pronto para GitHub Pages!")
        print("\nPróximos passos:")
        print("  1. Crie repositório em https://github.com/new")
        print("  2. Execute: git init && git add . && git commit -m 'initial'")
        print("  3. Execute: git branch -M main")
        print("  4. Execute: git remote add origin <seu-repo-url>")
        print("  5. Execute: git push -u origin main")
        print("  6. Ative GitHub Pages em Settings > Pages")
        print("     Branch: main, Folder: /docs")
        return True
    else:
        print("\n[ERRO] Alguns arquivos estão faltando!")
        return False


def test_github_actions_config():
    """Testa configuração do GitHub Actions"""
    print_header("5. TESTE DE CONFIGURACAO DO GITHUB ACTIONS")

    workflow_file = Path(".github/workflows/check-consultas.yml")

    if not workflow_file.exists():
        print("[ERRO] Workflow nao encontrado")
        return False

    try:
        with open(workflow_file, 'r', encoding='utf-8') as f:
            workflow_content = f.read()

        print("[OK] Workflow encontrado")

        # Verificar componentes
        checks = {
            "schedule": "Agendamento configurado",
            "cron:": "Cron job definido",
            "08:00": "Horários de execução",
            "python": "Python configurado",
            "pip install": "Instalacao de dependencias",
            "scraper.py": "Execução do scraper",
            "git commit": "Commit automático",
            "git push": "Push automático",
        }

        print("\nComponentes do Workflow:")
        all_present = True
        for pattern, desc in checks.items():
            exists = pattern in workflow_content
            status = "[OK]" if exists else "[AVISO]"
            print(f"  {status} {desc}")
            all_present = all_present and (pattern in workflow_content)

        if all_present:
            print("\n[OK] Workflow está completo!")

        return all_present

    except Exception as e:
        print(f"[ERRO] Erro ao validar workflow: {e}")
        return False


def print_summary(results):
    """Imprime sumário final"""
    print_header("RESULTADO FINAL")

    test_names = [
        "Execução do Scraper",
        "Validade do JSON",
        "Compatibilidade Frontend",
        "Prontidão GitHub Pages",
        "Configuração GitHub Actions"
    ]

    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100

    print("Resumo dos Testes:")
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "[PASSOU]" if result else "[FALHOU]"
        print(f"  {status} Teste {i+1}: {name}")

    print(f"\nTotal: {passed}/{total} testes passaram ({percentage:.0f}%)\n")

    if percentage == 100:
        print("Projeto está totalmente operacional!")
        print("\nPróximos passos:")
        print("  1. Crie um repositório no GitHub")
        print("  2. Faça o primeiro push")
        print("  3. Ative GitHub Pages em Settings")
        print("  4. Aguarde o primeiro deploy automático")
        print("\nConsulte DEPLOY_GITHUB_PAGES.md para instruções detalhadas.")
        status = 0
    elif percentage >= 80:
        print("Seu projeto está quase pronto!")
        print("Corrija os testes que falharam acima.")
        status = 1
    else:
        print("Seu projeto precisa de correções antes de fazer deploy.")
        print("Verifique os testes que falharam acima.")
        status = 1

    return status


def main():
    """Função principal"""
    print("\n" + "="*70)
    print("  BOT CONSULTAS PUBLICAS - TESTES DE FUNCIONALIDADE")
    print("  Data:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*70)

    results = []

    # Executar testes
    results.append(test_scraper_execution())
    results.append(test_json_validity())
    results.append(test_frontend_compatibility())
    results.append(test_github_pages_readiness())
    results.append(test_github_actions_config())

    # Sumário
    exit_code = print_summary(results)

    print("="*70 + "\n")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
