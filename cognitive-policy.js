/*
  Use Your Brain — Cognitive agency policy v2
  Transparent, locally evaluated editorial decision rules. No API, diagnosis
  or experimentally validated cognitive-preservation score.
*/
(() => {
  'use strict';
  const norm = value => String(value || '').toLocaleLowerCase('pt-BR')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
  const matches = (s, re) => re.test(s);
  const languageWords = /\b(ingles|espanhol|frances|alemao|italiano|portugues|hebraico|arabe|japones|mandarim|chines|coreano|libras|idioma|idiomas|lingua|linguas|pronuncia|vocabulario|gramatica|conversacao|fluencia|toefl|ielts|speaking|language)\b/;
  const codeWords = /\b(python|java|javascript|typescript|sql|html|css|git|github|r\b|programar|programacao|codigo|codar|software|debug|algoritmos?|computacao|backend|frontend|coding)\b/;
  const summaryWords = /\b(resumir|resumo|resuma|sumarizar|sintetizar|summarize|summarise|fichar|fichamento)\b/;
  const readWords = /\b(ler|leitura|interpretar|interpretacao|explicar|explicacao|compreender|entender|avaliar|criticar|analisar|analise)\b/;
  const criticalWords = /\b(interpretar|interpretacao|avaliar|avaliacao|criticar|critica|critico|analise|analisar|comparar|comparacao|decidir|decisao|escolher|investigar|validar|validacao|diagnosticar|parecer|argumentar|argumento|hipotese|hipoteses|vies|viesses|revisao critica|verificar evidencias|conclusao|conclusoes|julgar|checar|questionar|priorizar|estrategia|debater|debate)\b/;
  const meaningfulMaterial = /\b(estudo|estudos|artigo|artigos|cientifico|cientifica|paper|papers|metodologia|metodos|dados|resultados|estatistica|evidencia|evidencias|contrato|lei|leis|diagnostico|paciente|exame|risco|investimento|decisao|mercado|produto|projeto|pesquisa|noticia|informacao|fontes|politica)\b/;
  const writingAction = /\b(escrever|escrevendo|redigir|redigindo|elaborar|produzir texto|criar texto|compor|redacao|escrita|write|writing|draft|compose|responder|resposta)\b/;
  const writingObject = /\b(email|e mail|gmail|outlook|mensagem|whatsapp|carta|texto|ensaio|redacao|artigo|tese|dissertacao|manuscrito|relatorio|roteiro|post|legenda|discurso|apresentacao|resposta|proposta|parecer|resenha|newsletter|livro|resumo executivo)\b/;
  const editingAction = /\b(revisar|revisao|corrigir|correcao|editar|reescrever|polir|melhorar gramatic|ajustar tom|proofread|edit|check grammar)\b/;
  const spokenTask = /\b(palestra|palestrar|apresentacao oral|apresentar projeto|falar em publico|falar em uma reuniao|preparar minha fala|preparar um discurso|treinar entrevista|preparar entrevista|debater em publico|comunicacao oral)\b/;
  const routineAction = /\b(organizar|classificar|ordenar|formatar|converter|transcrever|renomear|arquivar|catalogar|separar duplicatas|listar|extrair dados|extrair texto|digitalizar|agendar|padronizar|transcricao|filtrar|limpar pasta|encontrar arquivos|remover duplicatas|sort|transcribe|convert|organize)\b/;
  const bulkWords = /\b(em lote|automaticamente|automatico|automatica|padrao|modelo|template|massa|centenas|milhares|confirmacao automatica|transacional|repetitiv|repetidas|notificacoes automaticas)\b/;
  const practiceWords = /\b(aprender|aprendizado|aprendizagem|estudar|estudando|praticar|praticando|treinar|treinando|memorizar|dominar|compreender|me ensine|learn|learning|study|studying|practice)\b/;
  const creativityWords = /\b(criatividade|criativo|criativa|original|ideias|inventar|inventando|brainstorm|conceito|hipotese|roteiro original|escrita criativa)\b/;

  const STRATEGIES = {
    restricted: {
      title:'Não delegue esta tarefa a uma IA não autorizada.',
      summary:'A restrição de uso ou privacidade vem antes da conveniência. Preserve a responsabilidade humana e verifique quais ferramentas são permitidas.',
      keep:'Integridade da atividade, privacidade e capacidade de decidir o que pode ser compartilhado.',
      delegate:'Somente assistência expressamente autorizada, sem dados protegidos fora de ambientes adequados.',
      check:'Identifique regras, destinatários dos dados e limites antes de usar qualquer ferramenta.'
    },
    highstakes: {
      title:'Use IA como apoio; mantenha o julgamento e a decisão humanos.',
      summary:'Em tarefas de alto impacto, defina hipóteses, riscos e alternativas; depois use IA para ampliar perguntas. Confirme dados e conclusões com fontes e profissionais adequados.',
      keep:'Avaliação de riscos, crítica das premissas e responsabilidade pela decisão.',
      delegate:'Organização de perguntas, síntese preliminar e busca de alternativas, se o ambiente for adequado.',
      check:'Consiga justificar a decisão a partir de evidências independentes, sem depender do texto gerado.'
    },
    learn_language: {
      title:'Pratique o idioma você mesmo. Use IA como parceira de conversação.',
      summary:'Fale e escreva antes de receber a resposta. Depois peça feedback de pronúncia, vocabulário e gramática; repita a prática sem apoio e também com pessoas reais.',
      keep:'Produção de frases, compreensão, recuperação de palavras e conversação ativa.',
      delegate:'Feedback de erros, exercícios graduais e simulações de diálogo.',
      check:'Tente sustentar uma conversa ou escrever um parágrafo novo sem traduções prontas.'
    },
    learn_code: {
      title:'Programe você primeiro. Peça pistas à IA, não a solução pronta.',
      summary:'Tente escrever a lógica, identificar o erro e testar hipóteses. Use IA para receber pistas e explicações, depois resolva um exercício parecido sem assistência.',
      keep:'Raciocínio algorítmico, depuração, leitura e escrita independente de código.',
      delegate:'Explicações pontuais, pistas progressivas e revisão dos testes.',
      check:'Explique a solução e reproduza o raciocínio em outro problema sem IA.'
    },
    learn_any: {
      title:'Aprenda ativamente. Use IA como tutora, não como substituta.',
      summary:'Faça uma tentativa própria, formule dúvidas e peça pistas ou feedback. Priorize prática, recuperação da memória e exercícios sem ajuda depois.',
      keep:'Compreensão, memória, formulação de perguntas e prática da habilidade.',
      delegate:'Exemplos alternativos, feedback, exercícios e esclarecimento de dúvidas.',
      check:'Explique ou execute algo novo, sem consultar a resposta que a IA deu.'
    },
    authored: {
      title:'O argumento é seu. Use IA como revisora crítica.',
      summary:'Escreva e interprete com seu próprio julgamento. Use IA depois para testar coerência, encontrar objeções e revisar a linguagem, respeitando regras de autoria.',
      keep:'Argumentação, escolha de evidências, interpretação e voz autoral.',
      delegate:'Revisão de clareza, contrapontos, organização e detecção de inconsistências.',
      check:'Defenda sua conclusão com as fontes originais, sem depender da redação da IA.'
    },
    linguistic: {
      title:'Escreva a primeira versão. Use IA para revisar.',
      summary:'Escolha as palavras, construa o argumento e registre sua intenção. Depois, peça sugestões de clareza, concisão, tom e gramática; aceite só o que representa sua voz.',
      keep:'Formulação de frases, vocabulário, argumentação e estilo próprio.',
      delegate:'Revisão de tom, clareza, concisão, gramática e inconsistências.',
      check:'Leia a versão final e explique o que quis dizer com suas próprias palavras.'
    },
    critical: {
      title:'Forme sua interpretação. Use IA para desafiar seu raciocínio.',
      summary:'Analise primeiro premissas, evidências e alternativas. Depois peça contra-argumentos e pontos cegos; verifique todas as afirmações importantes nas fontes originais.',
      keep:'Pensamento crítico, inferência, identificação de vieses e julgamento.',
      delegate:'Hipóteses alternativas, questionamentos, organização de informações e revisão de lacunas.',
      check:'Consiga defender ou rejeitar cada conclusão apontando a evidência original.'
    },
    creative: {
      title:'Crie suas primeiras ideias. Use IA como contraponto.',
      summary:'Comece com opções próprias antes de ver sugestões automáticas. Use IA para desafiar pressupostos e trazer analogias diferentes, sem perder sua autoria.',
      keep:'Originalidade, exploração de possibilidades e decisões criativas.',
      delegate:'Crítica de ideias, analogias, variações e objeções.',
      check:'Identifique quais decisões criativas são suas e por que foram escolhidas.'
    },
    summary: {
      title:'Use IA para resumir, mas confira o que importa.',
      summary:'Para poupar tempo, a IA pode criar um resumo inicial. Você define a pergunta e verifica fatos, números, decisões e eventuais omissões no original.',
      keep:'Seleção do que importa e avaliação da fidelidade da informação.',
      delegate:'Primeira síntese, tópicos, organização e extração de pontos principais.',
      check:'Confira datas, números, negações e compromissos antes de usar o resumo.'
    },
    routine: {
      title:'Automatize o mecânico. Preserve o controle.',
      summary:'IA pode acelerar tarefas repetitivas, desde que você defina regras claras e revise operações irreversíveis ou informações importantes.',
      keep:'Critérios de qualidade, privacidade e avaliação do resultado.',
      delegate:'Classificação, organização, formatação, transcrição ou renomeação com salvaguardas.',
      check:'Confira amostras e mantenha cópia de segurança ou forma de desfazer mudanças.'
    },
    spoken: {
      title:'Prepare suas ideias. Treine falando com suas próprias palavras.',
      summary:'Planeje o que quer comunicar e pratique sua explicação sem ler um texto pronto da IA. Use a ferramenta para simular perguntas, apontar trechos confusos e sugerir melhorias.',
      keep:'Organização verbal do raciocínio, vocabulário e clareza na comunicação oral.',
      delegate:'Simulação de perguntas, feedback e revisão de estrutura.',
      check:'Explique novamente o assunto em voz alta, sem consultar um roteiro pronto.'
    },
    review: {
      title:'Use IA para revisar. Você decide o que mudar.',
      summary:'Se o texto já é seu, peça uma revisão de clareza e linguagem. Compare cada mudança e preserve a intenção e as ideias originais.',
      keep:'Sentido, tom, voz e responsabilidade pelo conteúdo.',
      delegate:'Sugestões de correção, estrutura e fluidez.',
      check:'Aceite apenas revisões que você entende e que mantêm sua intenção.'
    },
    unclear: {
      title:'Defina seu objetivo antes de delegar.',
      summary:'A mesma tarefa pode servir para aprender ou apenas economizar tempo. A recomendação é provisória: preserve as decisões importantes e use IA só onde puder verificar o resultado.',
      keep:'Definição do objetivo e critérios de qualidade.',
      delegate:'Apoio preliminar para organizar o trabalho, se apropriado.',
      check:'Pergunte: quero desenvolver essa habilidade ou apenas concluir esta tarefa?'
    }
  };

  function assess(task,result={},settings={}){
    const text=norm(task),category=result.category||'routine';
    const goal=settings.goal||'auto';
    const flags=settings.flags||{};
    const hybrid=settings.hybrid||null;
    const explicitLearn=category==='learn'||goal==='learn';
    const isLanguage=matches(text,languageWords);
    const isCoding=matches(text,codeWords);
    const isWriting=matches(text,writingAction)&&matches(text,writingObject);
    const isSummary=matches(text,summaryWords);
    const isEditing=matches(text,editingAction);
    const isCritical=matches(text,criticalWords)&&(matches(text,meaningfulMaterial)||!result.uncertain);
    const isRoutine=matches(text,routineAction);
    const isBulk=matches(text,bulkWords);
    let mode, reason;
    // Explicit rules and information safety always beat productivity.
    if(category==='noai'||category==='sensitive'||flags.prohibited||flags.sensitive) {
      mode='restricted';reason='Restrições de uso ou privacidade prevalecem sobre a automação.';
    } else if(category==='highrisk'||flags.stakes||goal==='highrisk') {
      mode='highstakes';reason='Alto impacto requer avaliação independente e responsabilidade humana.';
    } else if(explicitLearn) {
      mode=isLanguage?'learn_language':isCoding?'learn_code':'learn_any';
      reason='O objetivo é desenvolver uma capacidade, e não apenas entregar um produto.';
    } else if(category==='authorship'||goal==='authorship') {
      mode='authored';reason='Autoria e interpretação precisam continuar atribuídas a uma pessoa.';
    } else if(hybrid&&hybrid.id) {
      mode=category==='creative'?'creative':'critical';
      reason='A tarefa envolve interpretação ou criação, e a IA pode funcionar como segunda opinião.';
    } else if(category==='personal') {
      mode='linguistic';reason='A expressão pessoal e a escolha das palavras são parte do valor da atividade.';
    } else if(category==='creative'||(matches(text,creativityWords)&&matches(text,/\b(criar|inventar|idealizar|gerar|brainstorm|desenvolver)\b/))) {
      mode='creative';reason='A geração independente de ideias ajuda a preservar uma voz original.';
    } else if(isCritical || (matches(text,meaningfulMaterial)&&matches(text,/\b(limitac\w*|vies\w*|fragilidad\w*|conclus\w*|metodolog\w*)\b/))) {
      mode='critical';reason='A tarefa demanda confronto de evidências, inferência ou julgamento.';
    } else if(matches(text,creativityWords)) {
      mode='creative';reason='A criação e a seleção de ideias se beneficiam de um ponto de partida humano.';
    } else if(isEditing) {
      mode='review';reason='A revisão é uma etapa instrumental, mas o sentido deve continuar sob controle humano.';
    } else if(matches(text,spokenTask)) {
      mode='spoken';reason='Formular e apresentar uma ideia oralmente faz parte da habilidade que você quer preservar.';
    } else if(isWriting&&!isBulk&&!isSummary) {
      mode='linguistic';reason='Escrever envolve formular ideias, selecionar palavras e organizar argumentos.';
    } else if(isSummary) {
      mode='summary';reason='Sintetizar pode poupar trabalho, mas a fidelidade precisa de conferência.';
    } else if(isRoutine||isBulk) {
      mode='routine';reason='A parte principal da atividade é mecânica ou pode ser verificada por amostragem.';
    } else {
      mode=result.uncertain?'unclear':'routine';
      reason=result.uncertain?'A intenção da busca não ficou clara.':'A tarefa não tem um sinal forte de aprendizagem ou julgamento autoral.';
    }
    const base=STRATEGIES[mode];
    let title=base.title,summary=base.summary,keep=base.keep,delegate=base.delegate,check=base.check;
    if(mode==='restricted'&&category==='noai'){
      title='Nesta atividade, não use IA.';
      summary='A tarefa exige trabalho independente. Respeite as regras e pratique as habilidades necessárias; procure ajuda apenas se ela for permitida.';
      delegate='Nenhuma tarefa a uma IA quando as regras proíbem seu uso.';
      check='Conclua a atividade seguindo as regras, com seus próprios recursos.';
    }
    if(mode==='critical'&&hybrid){
      title=hybrid.title;summary=hybrid.summary;
      keep=hybrid.brainAction;
      delegate='Contrapontos, opções e revisão crítica sem tratar a saída como autoridade.';
      check='Verifique as alegações relevantes com evidências originais, cálculos ou testes.';
    }
    if(mode==='creative'&&hybrid) {title=hybrid.title;summary=hybrid.summary;keep=hybrid.brainAction;}
    if(mode==='highstakes'&&hybrid){title=hybrid.title;summary=hybrid.summary;keep=hybrid.brainAction;}
    const domains=[];
    if(['learn_language','learn_code','learn_any'].includes(mode))domains.push('Aprendizagem');
    if(['linguistic','authored','review','learn_language'].includes(mode)||isWriting&&!isBulk)domains.push('Linguagem');
    if(['critical','highstakes','authored'].includes(mode)||(isCritical&&mode!=='creative'))domains.push('Pensamento crítico');
    if(mode==='spoken')domains.push('Linguagem');
    if(mode==='creative')domains.push('Criatividade');
    if(mode==='routine'||mode==='summary')domains.push('Execução e checagem');
    if(!domains.length)domains.push('Autonomia e responsabilidade');
    const strength=mode==='spoken'?{
       grade:'Indireta para comunicação oral',
       method:'Extrapolação de estudos de escrita e apoio cognitivo',
       supports:'Estudos mostram ganhos de IA em algumas tarefas de escrita; a aplicação a preparação de apresentações orais é plausível, mas não foi diretamente testada nas fontes usadas.',
       uncertainty:'Não há experimento aqui que demonstre manutenção ou perda de capacidade oral com assistência por IA. A prática de falar sem roteiro pronto é uma escolha educacional prudente.',
       refs:['noy','risko','lee']
    } : mode==='linguistic'&&category==='routine' ?
      {grade:'Moderada para produtividade; limitada para preservar a escrita',
       method:'Experimentos de produtividade e estudo quase experimental em escrita acadêmica',
       supports:'Há evidências de que IA melhora velocidade e qualidade de determinados textos. Um estudo quase experimental de 2026 sugere que apoio delimitado com reflexão pode favorecer desempenho independente, mas os contrastes entre turmas foram imprecisos.',
       uncertainty:'Não foi comprovado que escrever primeiro e pedir revisão preserve a cognição ou a capacidade linguística no longo prazo. O estudo de escrita envolveu apenas seis turmas e não permite causalidade firme.',
       refs:['noy','writingtransfer','lee']} : null;
    const brainTitles={
      restricted:'Respeite os limites da atividade',
      highstakes:'Mantenha seu julgamento crítico',
      learn_language:'Fale, escreva e compreenda por conta própria',
      learn_code:'Construa seu raciocínio de programação',
      learn_any:'Pratique a habilidade antes de pedir respostas',
      authored:'O argumento e a interpretação são seus',
      linguistic:'Preserve a sua capacidade de escrever',
      spoken:'Preserve sua capacidade de explicar e argumentar',
      critical:'Faça sua própria análise antes da IA',
      creative:'Comece pelas suas próprias ideias',
      summary:'Você define o que merece atenção',
      routine:'Defina os critérios e verifique',
      review:'Preserve o sentido do seu texto',
      unclear:'Defina o que quer aprender ou concluir'
    };
    return {
      mode,title,summary,brainTitle:mode==='critical'&&hybrid?hybrid.brainTitle:brainTitles[mode],
      brainAction:keep,keep,delegate,check,domains,reason,
      evidence:strength,
      // Transparência: são categorias editoriais, não medidas de QI ou desempenho.
      methodology:'Regras editoriais por objetivo, conteúdo e risco. Não é um teste validado de habilidades cognitivas.'
    };
  }
  window.UYB_COGNITION=Object.freeze({assess});
})();