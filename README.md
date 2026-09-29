# Central Motion Tracker

O projeto possui duas versões:

- `index.html`: demonstração no navegador com cursor virtual.
- `desktop_tracker.py`: versão desktop que pode mover o mouse real do sistema.

## Mouse real (desktop)

Requer Python 3.9 ou superior e uma câmera:

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python desktop_tracker.py
```

Uso:

1. A janela da câmera será aberta.
2. Mova um objeto e clique nele na janela para selecioná-lo.
3. Pressione `F` para ativar o acompanhamento do mouse real.
4. Pressione `F` novamente para pausar e `ESC` para sair.

O programa não realiza cliques automáticos. Para interromper imediatamente, mova o mouse para o canto superior esquerdo: o PyAutoGUI possui um mecanismo de segurança (`FAILSAFE`).

> macOS pode solicitar permissões de Câmera e Acessibilidade. No Linux, pode ser necessário permitir o acesso ao dispositivo de vídeo e ao ambiente gráfico. Em ambientes Wayland, o controle global do ponteiro pode ser bloqueado pelo sistema.

## Versão web

Para executar a demonstração no navegador:

```bash
python3 -m http.server 8000
```

Abra `http://localhost:8000` e permita o uso da câmera. Essa versão move apenas um cursor virtual dentro da página.
