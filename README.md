# Use Your Brain · quando usar IA e quando pensar sozinho?

Buscador gratuito, estático e transparente para avaliar tarefas reais de trabalho, pesquisa, estudo e vida cotidiana. **Não é um instrumento de decisão validado cientificamente.**

## Conteúdo do catálogo

- **10.000 cenários diferentes**, em português, com categoria de recomendação, profissão, setor e grupo de fontes.
- **198 profissões** distribuídas em **17 setores**, com atenção a pesquisadores, médicos, engenheiros, profissionais de tecnologia, educação, direito, finanças, indústria, atendimento e vida cotidiana.
- **Mais de 100 casos âncora** específicos, além de combinações estruturadas de fluxos e temas ocupacionais.
- Busca aproximada com autocomplete local por descrição e profissão; explorador com filtros; download CSV.
- Sem requisições a modelos externos, sem embeddings pagos, sem login e sem envio da descrição a servidores; os arquivos são executados no navegador.

**O que a base não é:** não são 10.000 consultas observadas, não são as 10.000 tarefas mais frequentes empiricamente e não substitui aconselhamento profissional. Os casos foram **construídos editorialmente** a partir de fluxos de trabalho plausíveis; a literatura apoia tipos de uso, não validou a classificação de cada uma das 10.000 linhas. Tarefas similares em contextos diferentes podem merecer estratégias distintas. O protótipo pode errar.

## Regras de recomendação

| Categoria | Recomendação resumida |
|---|---|
| `routine` | Use IA para acelerar, conferindo dados e fontes |
| `learn` | Faça a primeira tentativa; IA como tutora |
| `creative` | Proponha suas ideias antes; IA como contraponto |
| `authorship` | Mantenha autoria, análise e responsabilidade acadêmica |
| `highrisk` | IA só como apoio; verificação e supervisão especializadas |
| `sensitive` | Não envie dados sigilosos a ferramenta não autorizada |
| `personal` | Preserve sua voz; IA só para ajustes, se desejar |
| `noai` | Não use IA quando as regras proíbem |

Nos resultados aparecem fontes específicas sobre aprendizagem, criatividade e produtividade, além de diretrizes de risco e integridade. Para cada tarefa correspondente é exibido um link ao estudo ou relatório usado para **selecionar o grupo de trabalho**, distinguindo-o da evidência da **recomendação**.

## Fontes de uso de IA / cobertura de ocupações

- [Anthropic Economic Index, 2026](https://www.anthropic.com/economic-index) — distribuição de tarefas de uso de Claude por ocupação.
- [OpenAI / NBER — How People Use ChatGPT](https://www.nber.org/papers/w34255) — categorias predominantes de uso pessoal e no trabalho; não captura todo uso empresarial ou de APIs.
- [OpenAI — From asking to doing, 2026](https://openai.com/index/how-the-world-is-putting-chatgpt-to-work/) — distribuição de padrões de trabalho.
- [AMA physician AI survey, 2026](https://www.ama-assn.org/practice-management/digital-health/more-80-physicians-use-ai-professionally-ama-survey) — tarefas clínicas relatadas por médicos.
- [Technology in Society, 2025](https://doi.org/10.1016/j.techsoc.2025.102813) — levantamento de aplicações científicas em pesquisadores.
- [Thomson Reuters Professional Services, 2026](https://www.thomsonreuters.com/en/institute/reports/2026-ai-in-professional-services-report) — usos de direito, contabilidade, impostos e setores regulados.
- [Gallup 2026](https://news.gallup.com/poll/715364/teachers-using-say-frees-time-matters-mostost.aspx) — aplicações de IA na rotina escolar.
- [O*NET occupational task database](https://www.onetcenter.org/database.html) — referência de abrangência ocupacional, sem alegar que todas as tarefas do arquivo sejam usos observados de IA.
- [ICMJE](https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html) — responsabilidade humana e divulgação do uso de IA em manuscritos biomédicos.

## Código e arquivos

- `index.html`: interface e princípios de decisão.
- `autocomplete.js`: busca aproximada em tarefas e profissões, local ao navegador.
- `explore.js`: exploração por área, profissão e estratégia.
- `catalogo-10000.js`: base compilada para a interface.
- `data/catalogo-10000.csv`: 10.000 linhas para editar e auditar.
- `data/catalogo-10000.json`: versão JSON legível da base.
- `scripts/gerar_catalogo_10000.py`: fonte editável dos perfis, contextos e fluxos de trabalho e verificador de duplicatas.
- `scripts/build.mjs`: empacota dados e scripts no HTML em `dist/` para publicar como Worker com arquivos estáticos.

## Rodar e publicar

```bash
python3 scripts/gerar_catalogo_10000.py
npm run build
python3 -m http.server 4321 --directory dist
```

Abra `http://localhost:4321`. A Cloudflare deve rodar `npm run build` e publicar a pasta `dist`. **Esse repositório é independente** do site do curso `futuro.danieldahis.com`.

## Prioridade de revisão editorial

Os 10.000 cenários foram gerados de perfis de trabalho, fluxos e contextos; podem conter construções pouco naturais. Antes de apresentar o buscador como ferramenta de orientação pública validada, conduzir revisão por profissionais, testar classificações em casos ambíguos, auditar vieses e medir precisão/recall com uma amostra de consultas reais e consentidas. Não afirmar que os resultados foram individualmente avalizados pelas fontes citadas.
