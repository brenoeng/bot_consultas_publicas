#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup e teste do scraper
"""

import subprocess
import sys
import os


def instalar_dependencias():
    """Instala dependências Python"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✓ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("✗ Erro ao instalar dependências")
        return False


def testar_scraper():
    """Testa o scraper"""
    print("\n🧪 Testando scraper...")
    try:
        from scraper import ConsultasPublicasScraper
        scraper = ConsultasPublicasScraper()
        sucesso = scraper.run()
        return sucesso
    except Exception as e:
        print(f"✗ Erro ao executar scraper: {e}")
        return False


def main():
    """Função principal"""
    print("╔════════════════════════════════════════════════╗")
    print("║     Setup do Scraper de Consultas Públicas    ║")
    print("╚════════════════════════════════════════════════╝")

    # Instalar dependências
    if not instalar_dependencias():
        sys.exit(1)

    # Testar scraper
    if not testar_scraper():
        print("\n⚠ Scraper testado mas com avisos")
        sys.exit(1)

    print("\n✓ Setup concluído com sucesso!")
    print("\nPróximos passos:")
    print("  1. Rode: python scraper.py")
    print("  2. Seus dados serão salvos em data/consultas.json")
    print("  3. As páginas HTML carregarão automaticamente os dados")


if __name__ == "__main__":
    main()
