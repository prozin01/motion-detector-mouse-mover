# Central Motion Tracker

O projeto possui duas versões:

- `index.html`: demonstração no navegador com cursor virtual.
- `run.py`: versão desktop que pode mover o mouse real do sistema (sem ambiente virtual).

## 🚀 Versão Desktop (Mouse Real)

**Sem necessidade de ambiente virtual!**

Simplemente execute:

```bash
python run.py
```

Na primeira execução, o script instalará automaticamente as dependências:
- `opencv-python`
- `numpy`
- `PyAutoGUI`

Depois disso, a aplicação será iniciada.

### 🎮 Controles:

- **Clique no alvo** na janela para selecioná-lo
- **Pressione F** para ativar/desativar o mouse real
- **Pressione ESC** para sair
- **Mova o mouse para o canto superior esquerdo** para parar de emergência (PyAutoGUI FAILSAFE)

### ✅ Requisitos:

- Python 3.6+
- Uma câmera conectada
- Acesso à internet (primeira execução para instalar pacotes)

---

## 🌐 Versão Web

Para executar a demonstração no navegador (com cursor virtual apenas):

```bash
python3 -m http.server 8000
```

Abra `http://localhost:8000` no navegador e permita o uso da câmera.

---

## 📋 Estrutura

```
.
├── run.py              # Script principal (instalação + execução)
├── app_desktop.py      # Lógica da aplicação
├── index.html          # Versão web
├── styles.css          # Estilos da versão web
├── app.js              # Lógica da versão web
└── README.md           # Este arquivo
```

---

## ⚠️ Notas de Segurança

- O PyAutoGUI possui um mecanismo `FAILSAFE`: mover o mouse para o canto superior esquerdo interrompe o programa imediatamente.
- A aplicação **não realiza cliques** automaticamente, apenas move o cursor.
- Em ambientes Wayland (Linux), o controle global do ponteiro pode ser bloqueado pelo gerenciador de sessão.
- No macOS, pode ser necessário conceder permissões de **Câmera** e **Acessibilidade** nas Preferências de Segurança.
