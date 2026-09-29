#!/usr/bin/env python3
"""
Motion Tracker - Aplicativo standalone

Execute sem ambiente virtual:
    python run.py

Todas as dependências serão instaladas automaticamente na primeira execução.
"""

import sys
import subprocess

required_packages = {
    "cv2": "opencv-python",
    "numpy": "numpy",
    "pyautogui": "PyAutoGUI"
}

def check_and_install_dependencies():
    """Verifica se as dependências estão instaladas. Se não, instala automaticamente."""
    missing = []
    
    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"Instalando dependências: {', '.join(missing)}...\n")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + missing)
            print("✓ Dependências instaladas com sucesso!\n")
        except Exception as e:
            print(f"✗ Erro ao instalar dependências: {e}")
            sys.exit(1)

if __name__ == "__main__":
    check_and_install_dependencies()
    
    # Importa e executa o app
    from app_desktop import main
    try:
        main()
    except KeyboardInterrupt:
        print("\n✓ Aplicação interrompida pelo usuário.")
    except Exception as e:
        print(f"✗ Erro: {e}")
        sys.exit(1)
