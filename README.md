# useyourbrain — quando usar IA e quando pensar por conta própria?

Site independente do curso, desenvolvido para hospedagem estática na Cloudflare, com **50.000 cenários de atividades**, busca por sinônimos em português/inglês e referências científicas contextualizadas. Não faz solicitações a modelos de IA nem tem custos por pesquisa.

## O que há no catálogo

- **650 tarefas editoriais essenciais** priorizadas na busca: e-mail, responder mensagens, Gmail/Outlook, organização de arquivos, Google Fotos, notas, agenda, viagens, documentos e trabalho cotidiano, além de pesquisa científica, medicina, engenharia, desenvolvimento de software, negócios, educação e finanças.
- **50.000 situações textuais distintas**, incluindo os casos essenciais e situações profissionais contextualizadas; **208 perfis de profissão/uso e 19 setores**.
- **Sinônimos são buscados, não contados como atividades adicionais.** Exemplos: `escrever e-mail`, `redigir email`, `write an email`; `organizar fotos Google Fotos`, `arrumar minhas fotos`.
- As categorias de orientação consideram **aprendizagem**, **criatividade**, **autoria acadêmica**, **execução de tarefas**, **alto risco**, **sigilo**, **expressão pessoal** e **proibição de IA**.
- Estudos por **tipo de tarefa**: experimentos de e-mails, trabalho de escrita e programação; estudos sobre aprendizagem, busca de literatura, criatividade; evidência clínica, diretrizes de risco e documentação de recursos de fotos. Quando a fonte é **indireta, observacional ou técnica**, o resultado indica essa limitação.

**Aviso de método:** o número de linhas não é um ranking das 50.000 consultas mais frequentes. As entradas são exemplos editoriais construídos a partir de tarefas cotidianas e contextos ocupacionais. Os estudos não validam as 50.000 classificações individualmente, nem o algoritmo como instrumento científico. O buscador lexical pode falhar em sinônimos difíceis, negações e ambiguidades. As recomendações não substituem profissionais habilitados.

## Fontes de definição das tarefas

- [Como as pessoas usam ChatGPT — NBER (2025)](https://doi.org/10.3386/w34255), foco em escrita, busca de informação, orientação e tarefas de trabalho;
- [Anthropic Economic Index](https://www.anthropic.com/economic-index), ocupações e tipos de uso;
- [Pesquisa AMA com médicos (2026)](https://www.ama-assn.org/practice-management/digital-health/more-80-physicians-use-ai-professionally-ama-survey), literatura e documentação clínica;
- [Google Fotos](https://support.google.com/photos/answer/15318661), funcionalidade do produto, não estudo científico;
- [O*NET](https://www.onetcenter.org/database.html), estrutura ocupacional;
- [ICMJE](https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html), regras de autoria e responsabilidade.

## Pesquisas usadas para orientar recomendações

- [Experimento de campo em e-mails, reuniões e escrita](https://doi.org/10.3386/w33795)
- [Experimento de escrita profissional](https://doi.org/10.1126/science.adh2586)
- [Três experimentos com assistentes de programação](https://doi.org/10.1287/mnsc.2025.00535)
- [Síntese de literatura científica com LLMs](https://doi.org/10.1038/s41586-025-10072-4)
- [Criatividade e diversidade de histórias](https://doi.org/10.1126/sciadv.adn5290)
- [Uso de IA e aprendizagem posterior](https://doi.org/10.1073/pnas.2422633122)
- [NIST AI Risk Management Framework: Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1)

## Editar e gerar

```
python3 scripts/gerar_catalogo_50000.py
npm run build
python3 -m http.server 4321 --directory dist
```

Abra `http://localhost:4321`. O build cria `dist/` com `index.html`, dez fragmentos do catálogo e scripts de busca: tudo é local ao navegador. Recomendado na Cloudflare Pages: **Build command** `npm run build`, **output directory** `dist`.

### Arquivos

- `scripts/gerar_catalogo_50000.py` — intenções essenciais, profissões, temas e gerador reproduzível.
- `data/catalogo-50000.csv` — gerado localmente pelo gerador Python; `npm run build` também cria o CSV no `dist/` para download no site.
- `catalogo/parte-00.js` a `parte-09.js` — fragmentos compactos do catálogo para o navegador.
- `catalogo-loader.js`, `search-engine.js`, `autocomplete.js` — buscador automático sem backend.
- `index.html` — interface e biblioteca de evidências.

**Não editar ou vincular ao repositório `daniel-dahis` ou `futuro.danieldahis.com`.**
## Resumos (buscas essenciais)

`Resumir texto` e `Resumir e-mail` são tarefas prioritárias, com sinônimos e variantes PT/EN. O catálogo também distingue resumo de PDFs, Word, vídeos, reuniões, livros, contratos, pesquisa científica e mensagens. O site informa que verificações de fidelidade precisam consultar a fonte original, apoiando-se em FaithBench (NAACL 2025) e, para e-mails, estudo de campo sobre produtividade (não sobre precisão de cada resumo).
