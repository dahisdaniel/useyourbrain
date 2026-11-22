# useyourbrain

Um guia interativo, baseado em princípios científicos, para decidir **quando usar inteligência artificial, quando usá-la como apoio e quando preservar o esforço humano**.

## Princípios

- **Sem chamadas para modelos ou APIs pagas.** O buscador roda 100% no navegador.
- **3.000 exemplos locais pré-cadastrados** em `catalogo-3000.js`; cada caso pertence a uma das sete categorias: aprendizagem, criatividade, rotina, decisão de alto risco, expressão pessoal, privacidade e uso proibido.
- **Busca aproximada transparente**, por similaridade de palavras e regras de contexto. Não usa IA, embeddings, redes neurais ou tracking.
- **Justificativa científica** específica por categoria, com referências e limitações explícitas. Os artigos fundamentam princípios; *não validaram os 3.000 exemplos nem o algoritmo como um instrumento científico*.
- **Privacidade:** a tarefa digitada não sai do navegador (fontes de texto opcionais vêm do Google Fonts).

> **Importante:** os 3.000 exemplos foram gerados programaticamente a partir de temas e paráfrases. São casos ilustrativos, **não uma amostra dos 3.000 pedidos mais frequentes dos usuários**. A classificação é uma recomendação educacional, não orientação médica, jurídica ou financeira individualizada.

## Rodar localmente

Abra `index.html` diretamente num navegador, ou rode:

```sh
python3 -m http.server 4321
# abra http://localhost:4321
```

## Publicar no Cloudflare Pages usando GitHub

1. Crie um **novo repositório** chamado `useyourbrain` em https://github.com/new (sem modificar o projeto do curso).
2. Envie os arquivos deste diretório para a branch `main`.
3. No painel Cloudflare: **Workers & Pages → Create → Pages → Connect to Git** e selecione **apenas** o repositório `useyourbrain`.
4. Configure **Build command:** `npm run build`; **Build output directory:** `dist`; **Root directory:** `/`.
5. Publique e teste primeiro o domínio `*.pages.dev` atribuído pela Cloudflare.
6. Depois, na configuração do novo projeto Pages, entre em **Custom domains** e adicione `ia.danieldahis.com` se desejar.

Este projeto é estático e **não tem** `wrangler.toml`, rotas, worker ou conexão com `futuro.danieldahis.com`.

## Arquivos

- `index.html`: interface responsiva, textos científicos e motor de recomendação.
- `catalogo-3000.js`: 3.000 casos compilados para busca no navegador.
- `data/catalogo-3000.csv`: mesma base em formato editável.
- `scripts/gerar_catalogo.py`: gera e verifica a base a partir de tópicos e modelos.
- `scripts/build.mjs`: prepara `dist/` para a publicação na Cloudflare.

## Verificações

```sh
npm run build
```

A categorização e os limites éticos devem ser revisados e auditados antes de divulgar o projeto como recomendador validado. A correspondência lexical não compreende sinônimos complexos, sarcasmo ou significados ocultos.