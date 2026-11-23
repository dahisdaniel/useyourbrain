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

## Força da evidência e autonomia intelectual (versão 2026-11-22)

Cada recomendação mostra: **força da evidência**, o tipo de estudo ou norma que a sustenta, o que foi medido, as limitações e uma ação prática para manter raciocínio e julgamento humano. As etiquetas são **calibração editorial qualitativa**, não um sistema GRADE, metanálise nem ferramenta validada. Uma evidência forte para economia de tempo não implica evidência de dano cognitivo.

- **Moderada**: experimento diretamente na tarefa ou em tarefa bastante parecida (p. ex. e-mails, programação, aprendizagem de matemática). Os efeitos não são universais.
- **Limitada**: poucos testes ou dados próximos, mas não se testou exatamente esta prática (resumos, pesquisa, educação em outras disciplinas).
- **Indireta**: dados de uso, analogia com outras tarefas ou documentação técnica (arquivos, fotos, muitos casos cotidianos).
- **Regra/diretriz/valores**: recomendação fundamentada em segurança, integridade, autoria ou escolha ética; não confundir com resultado de ensaio randomizado.
- **Baixa para esta busca**: o buscador não conseguiu inferir com clareza a tarefa ou finalidade.

Nenhuma etiqueta significa que o usuário perderá QI ou ficará permanentemente menos inteligente por usar IA. Há estudos sobre aprendizagem posterior sem ferramenta em contextos delimitados, mas não prova de declínio geral da inteligência. O propósito do produto é favorecer decisões conscientes sobre o esforço que convém delegar versus preservar.

A avaliação contextual é definida em `evidence-strength.js`, funciona 100% localmente e é copiada para `dist/` pelo build. Não há consultas pagas nem avaliação de cada uma das 50.000 tarefas em experimentos individuais.

## Recomendações híbridas por julgamento intelectual

O arquivo `hybrid-guidance.js` acrescenta regras transparentes para **15 fluxos de trabalho** que envolvem análise crítica: avaliação de estudos, síntese científica, busca bibliográfica, hipóteses e desenho experimental, teses, análise de dados, revisão de código, engenharia, clínica, direito, finanças, estratégia empresarial, seleção de profissionais, docência e criatividade. O sistema preserva prioridades de **privacidade, proibição de IA, aprendizagem e expressão pessoal**; tarefas mecânicas, como organizar fotos ou resumir e-mail, permanecem fora dessas regras.

O fluxo recomendado é **raciocínio humano quando ele é parte do objetivo → IA como crítica/segunda opinião → verificação em fontes ou testes**. Esse fluxo é editorial e plausível, não experimentalmente validado como superior para toda situação. A força da evidência distingue estudos diretos de falhas de fundamentação, experimentos de produtividade e recomendações normativas. A tela exibe fontes aplicáveis e as limitações; não promete evitar perda de inteligência.

## Aprender algo novo — idiomas, programação e outras habilidades

A base de **50.000 situações** preserva o tamanho original e inclui 176 atividades concretas adicionais de aprendizagem, substituindo contextos genéricos; exemplos: aprender inglês, conversação em idioma estrangeiro, aprender Python, dominar SQL, ler artigos científicos e aprender instrumentos e habilidades cotidianas. Sinônimos PT/EN ficam no índice e não contam como tarefas diferentes. A classificação reconhece a intenção explícita de *aprender*, *estudar*, *praticar*, *treinar*, *learn*, *study* ou *practice*, mesmo para assuntos ausentes da lista.

Em tarefas de aprendizagem, recomendar **IA como tutora** não equivale a proibir IA: a pessoa deve praticar ativamente, pedir pistas e feedback e avaliar a própria autonomia. Para idiomas, citamos uma metanálise de 23 estudos sobre ensino de inglês (DOI: 10.1016/j.actpsy.2025.105649; heterogeneidade alta), e para programação, ensaios com 42 e 275 participantes (DOIs: 10.1016/j.caeai.2025.100527 e 10.1016/j.caeai.2025.100537). A força da evidência considera os contextos específicos e não mede perda de QI.

## Lógica de autonomia intelectual (v2)

`cognitive-policy.js` avalia objetivos de aprendizagem, tarefa de escrita, interpretação crítica, autoria, criatividade, tarefas mecânicas e riscos. Não calcula uma pontuação de inteligência nem infere declínio cognitivo. O site mostra **o que vale exercitar**, **o que pode ser delegado** e **como testar a autonomia sem IA**.

Prioridade: proibição/confidencialidade → decisões de alto impacto → aprendizagem → autoria → pensamento crítico/criatividade → comunicação humana → resumo/revisão → rotinas mecanizadas. O mesmo verbo pode gerar recomendações diferentes: escrever um e-mail pessoal não é o mesmo que processar centenas de respostas automáticas; aprender Python não é pedir que a IA gere código de produção.

Estudos relacionados: Bastani et al., PNAS 2025 (10.1073/pnas.2422633122), Noy e Zhang, Science 2023 (10.1126/science.adh2586), pesquisas de uso e produtividade e estudo quase experimental de escrita acadêmica em Frontiers in Psychology 2026 (10.3389/fpsyg.2026.1906199). Uma sequência de escrita humana seguida de revisão por IA é uma recomendação prudencial, não uma intervenção validada para prevenir perda de inteligência. A IA pode fortalecer prática de idiomas ao oferecer conversação e feedback; não há regra universal de não usá-la.

Os testes de regressão são executados em `npm test` e automaticamente antes de `npm run build` (28 atividades, regras de segurança e integridade da interface).
