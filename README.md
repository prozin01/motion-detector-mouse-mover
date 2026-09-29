# Central Motion Tracker

Aplicativo web demonstrativo que usa a câmera para detectar regiões com movimento. A bolinha central pode ser posicionada automaticamente sobre um objeto selecionado.

## Executar

Abra `index.html` em um servidor local (a câmera normalmente exige HTTPS ou `localhost`):

```bash
python3 -m http.server 8000
```

Depois acesse `http://localhost:8000` e permita o uso da câmera.

## Uso

1. Clique em **Iniciar câmera**.
2. Mova um objeto diante da câmera.
3. Clique no marcador/região correspondente para selecioná-lo.
4. Com **Seguir após selecionar** ativo, o cursor virtual acompanha o movimento.

> Por segurança e pelas limitações dos navegadores, o projeto não controla o cursor real do sistema nem envia cliques para outros aplicativos; a movimentação ocorre somente dentro da área da demonstração.
