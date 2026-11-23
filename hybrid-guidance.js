/* Use Your Brain: colaboração humano-IA para tarefas que exigem julgamento.
   Regras editoriais transparentes; não são um modelo de IA ou escala validada. */
(() => {
  'use strict';
  const norm = value => String(value || '').toLocaleLowerCase('pt-BR')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
  const has = (s, re) => re.test(s);
  const science = /\b(artigo cientifico|artigo academico|artigos cientificos|paper|papers|estudo cientifico|ensaio clinico|ensaios clinicos|publicacao cientifica|revisao sistematica|meta analise|metanalise|pesquisa cientifica)\b/;
  const critique = /\b(limitac\w*|critic\w*|vies\w*|vi[eé]s|confundid\w*|metodolog\w*|metodos?|avali\w*|validade|qualidade|fragilidad\w*|interpret\w*|conclus\w*|falhas?|risco de vies|rob 2)\b/;
  const rules = [
    {
      id:'scientific-critique',
      match:s=>has(s,science)&&has(s,critique),
      title:'Leia e critique primeiro. Use a IA como segunda opinião.',
      summary:'A identificação das limitações faz parte da análise científica. Avalie métodos, amostra, confundidores e inferências por conta própria; depois peça à IA que procure pontos adicionais e verifique cada um no texto original.',
      brainTitle:'Faça sua própria avaliação crítica antes da IA',
      brainAction:'Leia objetivo, métodos e resultados; anote forças e limitações sem ajuda. Depois peça à IA argumentos contrários e riscos de viés. Exija que ela cite trechos verificáveis e confira cada alegação no artigo.',
      reason:'Uma avaliação de 97 ensaios identificou justificativas de risco de viés frequentemente sem suporte documental, apesar de bom acerto em julgamentos gerais. A revisão humana e a checagem de trechos são necessárias.',
      method:'Evidência direta de falhas de fundamentação; estratégia híbrida não testada',
      supports:'Avaliações empíricas de risco de viés e síntese científica mostram que modelos podem formular avaliações plausíveis sem sustentação completa nas fontes.',
      uncertainty:'Não foi demonstrado em ensaio que ler primeiro e consultar a IA depois melhore a qualidade de toda avaliação crítica. A ordem é uma escolha prudencial para preservar julgamento e detectar erros.',
      refs:['riskbias','scholar','lee']
    },
    {
      id:'scientific-summary',
      match:s=>has(s,science)&&has(s,/\b(resum\w*|sintetiz\w*|sumariz\w*|summariz\w*|summaris\w*|fichamento)\b/),
      title:'Use IA para sintetizar. Confira o estudo você mesmo.',
      summary:'A IA pode ajudar a estruturar o resumo, mas a interpretação de resultados e limitações exige contato com o artigo original, especialmente métodos, tabelas, estimativas e conclusões.',
      brainTitle:'Identifique primeiro a mensagem e a evidência',
      brainAction:'Leia o resumo e examine os principais resultados. Peça à IA uma síntese com referências a seções do próprio artigo; compare estimativas, números, limitações e afirmações causais com o texto.',
      reason:'Estudos sobre síntese bibliográfica identificaram citações inventadas e falhas de fidelidade, sobretudo sem recuperação e verificação de fontes.',
      method:'Evidência sobre falhas de síntese; método de trabalho híbrido inferido',
      supports:'Há evidência empírica de que saídas de síntese podem conter informações sem suporte e referências inexistentes.',
      uncertainty:'A sequência exata “leitura humana + resumo de IA” não foi validada para todos os artigos ou níveis de conhecimento.',
      refs:['scholar','faithbench','researchsurvey']
    },
    {
      id:'literature-search',
      match:s=>has(s,/\b(busc\w*|encontr\w*|localiz\w*|pesquis\w*|levant\w*|procur\w*|search)\b/)&&has(s,/\b(artigos?|papers?|pubmed|literatura cientifica|bibliograf\w*|referencias cientificas)\b/),
      title:'IA pode ajudar na busca. Você seleciona e avalia os estudos.',
      summary:'Defina a pergunta e os critérios de inclusão; use IA para propor termos e caminhos de busca, mas confirme cada artigo em bases acadêmicas e leia as fontes originais.',
      brainTitle:'A pergunta e os critérios são seus',
      brainAction:'Escolha população, desfechos, período e critérios de relevância. Use IA para ampliar sinônimos e palavras-chave; valide DOI, elegibilidade, metodologia e qualidade dos estudos encontrados.',
      reason:'Modelos sem acesso confiável às fontes podem gerar citações inexistentes ou perder estudos relevantes.',
      method:'Evidência de problemas de referências; fluxo recomendado por prudência',
      supports:'Pesquisas de recuperação bibliográfica documentam limitações de precisão, cobertura e referências nos modelos.',
      uncertainty:'Não foi demonstrado que esta sequência seja ótima para todas as revisões e bases de dados.',
      refs:['scholar','researchsurvey','icmje']
    },
    {
      id:'study-design',
      match:s=>has(s,/\b(hipotes\w*|desenho experimental|delineamento experimental|protocolo de pesquisa|plano de pesquisa|projeto de pesquisa|desenhar estudo|desenho do estudo|elaborar experimento)\b/),
      title:'Formule sua hipótese. Use IA para tentar refutá-la.',
      summary:'Uma boa pesquisa exige ideias, controles e julgamento metodológico. Comece com uma hipótese própria; depois peça críticas, explicações concorrentes e controles que você talvez não tenha considerado.',
      brainTitle:'Sua pergunta vem antes das sugestões',
      brainAction:'Anote hipótese, mecanismo, desenho, desfechos e riscos de viés. Consulte IA para propor controles negativos, confundidores e explicações rivais. Verifique a viabilidade com literatura e especialistas.',
      reason:'Há pesquisas sobre homogeneização de ideias e limites epistêmicos de modelos, mas o desenho humano-primeiro é uma estratégia editorial.',
      method:'Evidência indireta; sequência híbrida ainda não validada',
      supports:'Estudos de criatividade mostram que assistência por IA pode tornar produções individuais mais semelhantes, apesar de ganhos de qualidade.',
      uncertainty:'Os estudos disponíveis não testam diretamente a superioridade dessa ordem para descoberta científica.',
      refs:['doshi','researchsurvey','lee']
    },
    {
      id:'authored-scholarship',
      match:s=>has(s,/\b(tese|dissertacao|manuscrito cientifico|artigo de pesquisa|discussao do artigo|interpretacao da tese|parecer academico)\b/),
      title:'A autoria é sua. Use IA como revisora crítica.',
      summary:'Escreva as perguntas, interpretações e argumentos centrais você mesmo. Use IA para testar consistência, melhorar clareza e detectar lacunas, respeitando as regras de autoria.',
      brainTitle:'Mantenha o argumento e a interpretação humanos',
      brainAction:'Escreva a sua versão e anote por que os dados sustentam cada conclusão. Depois peça à IA objeções e revisão de linguagem; confira todas as fontes e declare seu uso quando exigido.',
      reason:'Diretrizes editoriais mantêm a responsabilidade com autores humanos; modelos podem produzir citações ou afirmações sem apoio.',
      method:'Diretriz de autoria + evidência indireta sobre erros da IA',
      supports:'Responsabilidade editorial é humana, e há documentação de alucinações em sínteses científicas.',
      uncertainty:'Não existe ensaio comprovando que essa sequência preserve a inteligência; políticas institucionais variam.',
      refs:['icmje','scholar','lee']
    },
    {
      id:'data-interpretation',
      match:s=>has(s,/\b(analis\w*|interpret\w*|avali\w*|conclu\w*|compar\w*|explic\w*|model\w*|investig\w*|estim\w*)\b/)&&has(s,/\b(dados|dataset|resultados?|estatistic\w*|regress\w*|risco relativo|odds ratio|p valor|p value|intervalo de confianca|efeito causal|correlacao|graficos?)\b/),
      title:'Interprete os dados primeiro. Use IA para desafiar a análise.',
      summary:'Você define a pergunta, as hipóteses, os pressupostos e o significado dos resultados. A IA pode sugerir testes e explicações alternativas, mas os cálculos e conclusões precisam de verificação.',
      brainTitle:'Faça uma interpretação antes de receber uma pronta',
      brainAction:'Descreva desenho, variáveis, comparações, vieses e hipóteses antes de consultar IA. Depois peça análises de sensibilidade e interpretações rivais; recalcule resultados com ferramentas verificáveis.',
      reason:'IA pode produzir análises plausíveis sem suporte, e confiança excessiva pode reduzir esforço crítico percebido.',
      method:'Evidência indireta; recomendação de boas práticas analíticas',
      supports:'Estudos observacionais de trabalho com IA indicam que verificação e supervisão passam a ser parte importante do pensamento crítico.',
      uncertainty:'Não há ensaio específico provando que a sequência melhora toda interpretação estatística.',
      refs:['lee','nist','risko']
    },
    {
      id:'code-review',
      match:s=>has(s,/\b(codigo|code|python|javascript|script|software|programacao|sql|aplicativo|sistema)\b/)&&has(s,/\b(revis\w*|corrig\w*|depur\w*|debug\w*|otimiz\w*|audit\w*|avali\w*|seguranca|refator\w*|interpret\w*|test\w*)\b/),
      title:'Use IA como revisora de código. Entenda e teste você.',
      summary:'Peça à IA sugestões de correção e alternativas, mas não aceite uma alteração que você não consiga explicar, testar e revisar.',
      brainTitle:'Defina o comportamento esperado e as verificações',
      brainAction:'Identifique o defeito ou critério de qualidade, formule uma hipótese e escreva testes. Compare as sugestões da IA e rode testes automatizados e revisão de segurança antes de integrar.',
      reason:'Experimentos mostram ganhos de produtividade com assistentes de código, mas não garantem correção, ausência de vulnerabilidades ou retenção de habilidades.',
      method:'Evidência para produtividade; supervisão híbrida recomendada',
      supports:'Ensaios com desenvolvedores demonstram efeitos mensuráveis de assistência de programação em tarefas específicas.',
      uncertainty:'Esses ensaios não testaram se começar pela própria hipótese preserva melhor habilidade de programar.',
      refs:['codingrct','nist','lee']
    },
    {
      id:'engineering-review',
      match:s=>has(s,/\b(engenharia|engenheiro|estrutura|estrutural|circuito|eletric\w*|dimension\w*|seguranca de maquina|dispositivo medico|projeto mecanico|simulacao|norma tecnica|calculo de carga|falha de equipamento)\b/)&&has(s,/\b(projet\w*|analis\w*|calcul\w*|avali\w*|dimension\w*|verific\w*|revis\w*|simul\w*|valid\w*|falha\w*)\b/),
      title:'Faça a engenharia. Use IA para conferir hipóteses e documentação.',
      summary:'Defina requisitos, condições de contorno e critérios de segurança. IA pode sugerir alternativas e inconsistências, mas cálculo crítico exige ferramentas validadas, normas e revisão profissional.',
      brainTitle:'O raciocínio técnico e a responsabilidade continuam seus',
      brainAction:'Estabeleça hipóteses, unidades, margens e requisitos. Peça à IA pontos cegos ou normas a consultar, mas confira tudo nos documentos originais e valide o projeto com cálculos, testes e revisão independente.',
      reason:'Dados de adoção ocupacional e estudos de software não validam respostas de engenharia física.',
      method:'Indireta; cautela técnica e normativa',
      supports:'Há evidência de uso de IA em trabalhos técnicos e diretrizes que descrevem riscos de confiabilidade.',
      uncertainty:'Não existe prova de que IA valide projetos estruturais ou decisões de segurança sem verificação independente.',
      refs:['nist','anthropicindex','lee']
    },
    {
      id:'clinical-reasoning',
      match:s=>has(s,/\b(diagnostic\w*|tratamento|conduta|exame clinico|exames clinicos|paciente|sintomas|protocolo medico|prescricao|medicamento|triagem|prontuario|guideline|prognostico)\b/)&&has(s,/\b(interpret\w*|analis\w*|avali\w*|escolh\w*|decid\w*|recomend\w*|elabor\w*|diagnostic\w*|conduta|tratamento|prescri\w*|triagem|estim\w*)\b/),
      title:'IA apenas como apoio. A avaliação clínica exige responsabilidade.',
      summary:'Use IA para organizar perguntas e conferir fontes, nunca como única base para diagnóstico, prescrição ou conduta. Dados de pacientes exigem ambientes autorizados e proteção apropriada.',
      brainTitle:'Priorize avaliação e fontes clínicas confiáveis',
      brainAction:'Defina quadro, sinais de alerta e hipóteses com critérios clínicos. Consulte diretrizes originais e profissionais responsáveis; use IA aprovada apenas como apoio documentado, verificando cada afirmação.',
      reason:'Estudos clínicos documentam falhas de fundamentação em avaliações de evidências produzidas por modelos.',
      method:'Evidência sobre riscos da IA + recomendação de segurança',
      supports:'Há estudos de segurança de resumos clínicos e avaliações de risco de viés com justificativas nem sempre sustentadas por fontes.',
      uncertainty:'Os estudos não testam esta decisão clínica individual; a disponibilidade de ferramentas adequadas varia.',
      refs:['riskbias','clinicalsafety','nist']
    },
    {
      id:'legal-reasoning',
      match:s=>has(s,/\b(contrato|clausula|jurisprudencia|sentenca|peticao|processo judicial|parecer juridico|legislacao|lei|acordo juridico)\b/)&&has(s,/\b(revis\w*|analis\w*|avali\w*|interpret\w*|argument\w*|decid\w*|contest\w*|elabor\w*|redig\w*|defend\w*|compar\w*)\b/),
      title:'Elabore seu raciocínio jurídico. IA só como apoio revisado.',
      summary:'Defina a questão jurídica e as fontes aplicáveis antes de aceitar a análise da IA. Verifique legislação, precedentes, jurisdição e citações em documentos oficiais.',
      brainTitle:'Construa o argumento e teste seus pontos fracos',
      brainAction:'Identifique fatos, norma, precedentes e argumentos adversos. Peça à IA objeções ou uma lista de documentos a consultar; confirme cada citação e submeta a profissionais responsáveis.',
      reason:'Modelos podem formular respostas convincentes e incorretas; normas e precedentes exigem verificação documental.',
      method:'Diretrizes de risco + inferência de estudos adjacentes',
      supports:'Há evidência de erros factuais em modelos e diretrizes para verificação e responsabilidade humana.',
      uncertainty:'Não há ensaio citado que prove que esse fluxo seja superior para toda jurisdição ou tipo de processo.',
      refs:['nist','lee','risko']
    },
    {
      id:'financial-judgment',
      match:s=>has(s,/\b(investiment\w*|investir|acoes|carteira|financiament\w*|credito|taxa de juros|imposto|tribut\w*|valoracao|orcamento|previsao financeira|projecao de receita)\b/)&&has(s,/\b(analis\w*|avali\w*|escolh\w*|compar\w*|decid\w*|calcul\w*|interpret\w*|planej\w*|simul\w*|estim\w*)\b/),
      title:'Defina seus critérios financeiros. Use IA para explorar cenários.',
      summary:'Estabeleça objetivos, restrições e riscos antes das sugestões da IA. Confira taxas, premissas, cálculos e condições em fontes oficiais; não delegue decisões financeiras importantes.',
      brainTitle:'Você escolhe os riscos que está disposto a assumir',
      brainAction:'Liste objetivos, horizonte, liquidez e cenários. Peça à IA alternativas e questões para comparar, mas verifique todos os números e tome decisões com análise independente.',
      reason:'Ganhos de produtividade em escrita não validam previsões de mercado ou decisões financeiras.',
      method:'Evidência indireta + cautela em decisão de alto impacto',
      supports:'Diretrizes técnicas identificam riscos de confiabilidade e ferramentas podem apoiar organização e cenários.',
      uncertainty:'Os estudos citados não estabelecem acurácia preditiva nem vantagem financeira dessa estratégia.',
      refs:['nist','lee','risko']
    },
    {
      id:'business-strategy',
      match:s=>has(s,/\b(estrategia|estrategico|estrategica|decisao executiva|planejamento empresarial|plano de negocios|prioriz\w*|negociacao|escolher fornecedor|comparar fornecedores|lancamento de produto|risco de negocio)\b/),
      title:'Decida os critérios. Use IA para desafiar a estratégia.',
      summary:'Defina objetivos, trade-offs e riscos; então peça à IA perspectivas contrárias e cenários. Julgamento, contexto e responsabilidade pela decisão continuam humanos.',
      brainTitle:'Pense no que faria você mudar de ideia',
      brainAction:'Documente opções, premissas e critérios de sucesso. Peça à IA contra-argumentos e riscos negligenciados; valide dados e discuta com pessoas afetadas antes de decidir.',
      reason:'Há evidência de produtividade em trabalho de escritório, mas não da qualidade de decisões executivas complexas.',
      method:'Evidência indireta; método híbrido não validado',
      supports:'Estudos de IA em tarefas de escritório e pesquisas de pensamento crítico dão suporte ao uso como apoio, sem validar decisão autônoma.',
      uncertainty:'Não está demonstrado que IA melhore toda estratégia empresarial ou que essa ordem seja ótima.',
      refs:['lee','emailfield','nist']
    },
    {
      id:'hiring-appraisal',
      match:s=>has(s,/\b(contrat\w*|candidat\w*|recrut\w*|entrevista de emprego|avaliacao de desempenho|promocao de funcionarios|avaliar curriculo)\b/)&&has(s,/\b(analis\w*|avali\w*|escolh\w*|compar\w*|selecion\w*|decid\w*|classific\w*|entrevist\w*|contrat\w*)\b/),
      title:'Defina critérios justos. Não terceirize a avaliação de pessoas.',
      summary:'IA pode ajudar a organizar perguntas e documentos, mas decisões que afetam pessoas exigem critérios transparentes, revisão e atenção a viés e privacidade.',
      brainTitle:'Faça a avaliação com critérios explícitos',
      brainAction:'Determine competências relevantes e evidências observáveis. Use IA para estruturar perguntas, não para emitir veredictos automáticos sobre candidatos; revise por vieses e mantenha responsabilidade humana.',
      reason:'Princípios de governança de IA exigem atenção a vieses, privacidade e consequências de decisões automatizadas.',
      method:'Diretrizes de risco; sem ensaio específico desta tarefa',
      supports:'Diretrizes técnicas descrevem riscos de confiabilidade e viés em decisões mediadas por IA.',
      uncertainty:'Não há base aqui para afirmar que um modelo identifique talentos com maior precisão ou justiça.',
      refs:['nist','lee']
    },
    {
      id:'teaching-and-assessment',
      match:s=>has(s,/\b(aula|alunos?|estudantes?|prova escolar|provas escolares|exercicio didatico|material didatico|plano de ensino)\b/)&&has(s,/\b(prepar\w*|cri\w*|avali\w*|corrig\w*|planej\w*|explic\w*|elabor\w*|revis\w*)\b/),
      title:'Você define o objetivo pedagógico. IA ajuda a revisar materiais.',
      summary:'Defina o que os alunos precisam aprender e como demonstrar compreensão. IA pode propor exemplos e revisão, mas conteúdos e avaliações devem ser conferidos por quem ensina.',
      brainTitle:'Preserve o planejamento e a avaliação pedagógica',
      brainAction:'Especifique objetivo, progressão, dificuldades esperadas e critérios de correção. Peça à IA exemplos alternativos; confira exatidão e aplique avaliações que meçam aprendizagem sem dependência automática.',
      reason:'Há experimentos sobre aprendizagem com IA que distinguem fornecimento de respostas prontas de tutoria guiada.',
      method:'Experimentos educacionais próximos; extrapolação para docência',
      supports:'Experimentos mostram que o desenho da assistência influencia aprendizagem em matemática, tornando importante o papel de quem planeja o ensino.',
      uncertainty:'Os estudos citados não testaram diretamente esta preparação de aula ou rubrica específica.',
      refs:['pnas','kapur','risko']
    },
    {
      id:'creative-authorship',
      match:s=>has(s,/\b(roteiro|campanha criativa|brainstorm|ideias originais|conceito criativo|artigo de opiniao|criar narrativa|historia original|identidade de marca|texto autoral|design original)\b/),
      title:'Crie algo seu primeiro. Use IA para ampliar, não padronizar.',
      summary:'Comece com sua ideia e seu ponto de vista. Depois peça à IA objeções, analogias ou alternativas diferentes e faça uma seleção consciente.',
      brainTitle:'Preserve as suas primeiras ideias',
      brainAction:'Gere algumas alternativas sem IA, inclusive uma improvável. Só então consulte sugestões do modelo e descarte as que deixam o resultado genérico ou não representam sua intenção.',
      reason:'Um experimento encontrou melhores avaliações de histórias com IA, mas menor diversidade entre elas.',
      method:'Experimento em histórias; extrapolação para outras criações',
      supports:'Existe evidência de homogeneização de produções criativas assistidas por IA em tarefas específicas.',
      uncertainty:'Não foi testado se “humano primeiro” impede essa homogeneização em todo tipo de criatividade.',
      refs:['doshi','lee','risko']
    }
  ];
  function suggest(task, result) {
    if (result && ['noai','sensitive','personal','learn'].includes(result.category)) return null;
    const s = norm(task);
    if (!s || s.length < 8) return null;
    for (const rule of rules) {
      if (rule.match(s)) return {
        id:rule.id, title:rule.title, summary:rule.summary,
        brainTitle:rule.brainTitle, brainAction:rule.brainAction,
        reason:rule.reason, grade:'Limitada', method:rule.method,
        supports:rule.supports, uncertainty:rule.uncertainty, refs:rule.refs
      };
    }
    return null;
  }
  window.UYB_HYBRID = Object.freeze({suggest});
})();
