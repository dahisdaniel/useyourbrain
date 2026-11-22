/* Avaliação editorial contextual: não é um escore clínico nem uma escala validada. */
(() => {
  'use strict';
  const norm = s => String(s || '').toLocaleLowerCase('pt-BR')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
  const has = (s, re) => re.test(s);
  const IQ_NOTE = 'Não está demonstrado que usar IA nesta atividade cause uma queda da inteligência geral ou do QI. Preservar momentos de esforço intelectual é uma escolha prudente, não uma prevenção comprovada de “emburrecimento”.';
  const LEARNING_NOTE = 'Em matemática escolar, houve pior desempenho posterior sem IA com assistência irrestrita. Isso mede aprendizagem nessa situação, não perda permanente de inteligência, QI ou um efeito inevitável em outros assuntos.';
  const BRAIN_BY_CATEGORY = {
    learn: ['Tente antes de pedir a resposta', 'Faça um esforço real para resolver ou explicar. Depois peça uma pista e repita uma tarefa parecida sem IA. Sua aprendizagem aparece no que você consegue fazer sozinho.'],
    authorship: ['Mantenha a autoria do raciocínio', 'Escolha a pergunta, construa o argumento e interprete os dados com seu próprio julgamento. Use IA para apontar lacunas e perguntas difíceis, não para substituir suas conclusões.'],
    creative: ['Tenha suas próprias ideias primeiro', 'Pense em alternativas, inclusive as improváveis, antes de ver sugestões do modelo. Use IA para testar, contradizer e ampliar suas possibilidades.'],
    routine: ['Delegue o mecânico, não o julgamento', 'Você não precisa fazer manualmente toda tarefa repetitiva. Defina o objetivo, os critérios de qualidade e confira o resultado: é essa parte que exige seu raciocínio.'],
    highrisk: ['Pense nas consequências e verifique', 'Defina os riscos, as opções e as incertezas. Use IA para formular perguntas, não como autoridade final. Verifique informações com fontes originais e profissionais responsáveis.'],
    personal: ['Preserve o que é verdadeiramente seu', 'Escolha o que quer expressar e por quê. Uma revisão de clareza pode ajudar; terceirizar inteiramente suas palavras é uma escolha de autenticidade, não uma regra científica.'],
    sensitive: ['Decida o que não deve ser compartilhado', 'Antes de buscar conveniência, identifique o que é confidencial e quais ferramentas estão autorizadas. Privacidade é uma condição de uso, não um desafio de criatividade.'],
    noai: ['Exercite sua autonomia', 'Se a tarefa exige trabalho individual, cumpra essa regra. Use a dificuldade para identificar o que você precisa praticar e retome o assunto com ajuda apenas quando for permitido.']
  };
  const RULES = {
    noai: {
      grade:'Regra da atividade', method:'Critério normativo, não força estatística',
      supports:'Se a avaliação ou acordo proíbe IA, não utilizá-la decorre da regra, independentemente de estudos sobre desempenho.',
      uncertainty:'Ensaios educacionais não estabelecem uma proibição geral de IA em todas as tarefas.'
    },
    sensitive: {
      grade:'Diretriz de segurança', method:'Fundamentação técnica, não ensaio da tarefa',
      supports:'A recomendação se apoia na proteção de dados e em controles de risco proporcionais ao contexto e à ferramenta.',
      uncertainty:'Não é correto afirmar que toda ferramenta de IA expõe dados. Contam as autorizações, arquitetura e políticas aplicáveis.'
    },
    highrisk: {
      grade:'Diretriz + evidência indireta', method:'Prudência em decisões de alto impacto',
      supports:'Há documentos técnicos sobre alucinações, confiabilidade e necessidade de validação. Isso justifica não delegar decisões graves.',
      uncertainty:'Não há um experimento que prove que IA seja inferior a todo profissional ou em toda decisão importante.'
    },
    authorship: {
      grade:'Normativa/editorial', method:'Regras de autoria e responsabilidade',
      supports:'Diretrizes editoriais atribuem aos autores humanos responsabilidade por argumentos, dados, fontes e uso declarado de IA.',
      uncertainty:'As regras variam entre instituições. Não há demonstração de que receber ajuda de revisão torne alguém menos inteligente.'
    },
    personal: {
      grade:'Escolha de valores', method:'Juízo ético, não resultado experimental',
      supports:'Preservar a própria voz é uma preferência de autenticidade. A IA pode facilitar a comunicação, inclusive para acessibilidade.',
      uncertainty:'Não existem dados que justifiquem proibir universalmente o uso de IA para mensagens pessoais.'
    }
  };
  const DIRECT = {
    email: {
      grade:'Moderada',method:'Experimentos de campo com trabalho de e-mail',
      supports:'Um experimento com ferramentas de IA integradas ao escritório encontrou menos tempo gasto com e-mails; outro experimento encontrou ganhos de rapidez e qualidade em escrita profissional. Isso apoia usar IA como apoio à edição e revisão.',
      uncertainty:'Esses estudos não compararam diretamente “escrever primeiro e pedir revisão” com “deixar a IA escrever tudo”. Essa sequência é uma recomendação prudente para preservar autoria e julgamento; não há demonstração de que ela previna perda de QI.'
    },
    emailSummary: {
      grade:'Limitada',method:'Evidências próximas, não teste do resumo exato',
      supports:'Há experimento de produtividade no trabalho com e-mails e benchmark que identifica falhas de fidelidade em resumos automáticos.',
      uncertainty:'A economia de tempo com e-mails não demonstra que um resumo específico seja fiel ou que resumir com IA prejudique a memória.'
    },
    summaries: {
      grade:'Limitada',method:'Benchmarks de fidelidade e extrapolação de produtividade',
      supports:'Benchmarks mostram que resumos de IA podem conter invenções e distorções; experimentos com escrita sugerem benefícios próximos de produtividade.',
      uncertainty:'Isso não mede a eficácia de resumir este material nem prova redução de aprendizagem ou de inteligência.'
    },
    coding: {
      grade:'Moderada',method:'Experimentos de campo em desenvolvimento de software',
      supports:'Há estudos randomizados de assistentes de código em contextos profissionais, com mudanças mensuráveis de produtividade.',
      uncertainty:'Os resultados variam conforme a tarefa e não garantem correção, segurança do código nem manutenção de habilidade sem prática.'
    },
    photos: {
      grade:'Indireta',method:'Documentação do produto, sem ensaio independente específico',
      supports:'Há recursos documentados para localizar e organizar fotos. Automatizar classificações pode poupar trabalho mecânico.',
      uncertainty:'A documentação não prova aumento de produtividade nem benefício ou prejuízo cognitivo. Compartilhar ou apagar imagens exige revisão.'
    },
    files: {
      grade:'Indireta',method:'Analogia com tarefas administrativas e documentação de uso',
      supports:'Usos de IA em organização e escrita são documentados; sugerir apoio operacional é plausível quando mudanças são reversíveis.',
      uncertainty:'Não há neste conjunto de fontes ensaio específico para renomear, mover ou organizar suas pastas. Faça backup antes de operações em massa.'
    },
    research: {
      grade:'Limitada',method:'Estudos de síntese e levantamentos de uso científico',
      supports:'Pesquisas documentam o uso de IA em fluxos científicos e limitações para localizar e sintetizar literatura com fontes corretas.',
      uncertainty:'Isso não valida uma revisão bibliográfica particular, uma hipótese, nem dispensa conferência de DOI e artigos originais.'
    },
    clinical: {
      grade:'Limitada',method:'Avaliações clínicas específicas e estudos de adoção',
      supports:'Há estudos sobre qualidade e alucinações em resumos clínicos, além de pesquisas de uso por médicos.',
      uncertainty:'Adoção não comprova segurança clínica em todos os pacientes, hospitais ou decisões; dados sensíveis exigem ferramentas aprovadas.'
    },
    creative: {
      grade:'Limitada',method:'Experimento em histórias curtas; extrapolação',
      supports:'Um experimento observou maior qualidade individual das histórias com IA, mas menor diversidade do conjunto.',
      uncertainty:'Não foi demonstrado que criar ideias antes de consultar IA preserve originalidade em todas as profissões; isso é uma precaução plausível.'
    },
    business: {
      grade:'Limitada',method:'Experimentos em atendimento e escrita profissional',
      supports:'Experimentos de atendimento e escrita encontraram ganhos em certas tarefas profissionais.',
      uncertainty:'Os resultados não se aplicam automaticamente a toda decisão de negócios ou estratégia.'
    },
    office: {
      grade:'Limitada',method:'Experimentos em algumas tarefas administrativas',
      supports:'Estudos sobre e-mail, reuniões e escrita sugerem ganhos práticos em partes do trabalho de escritório.',
      uncertainty:'A abrangência da evidência é menor para tarefas administrativas não testadas.'
    },
    education: {
      grade:'Limitada',method:'Aprendizagem testada em tarefas específicas',
      supports:'Experimentos sobre tutoria e tentativa independente ajudam a orientar práticas pedagógicas.',
      uncertainty:'Preparar aulas não é o mesmo que aprender matemática com IA; resultados não são automaticamente transferíveis.'
    },
    everyday: {
      grade:'Indireta',method:'Dados de uso + princípios gerais',
      supports:'Dados de uso mostram que pessoas pedem orientação, organização e escrita; há um argumento para poupar tempo com tarefas verificáveis.',
      uncertainty:'Frequência de uso não equivale a comprovação de eficácia e não há ensaio para a maioria destas tarefas cotidianas.'
    },
    engineering: {
      grade:'Indireta',method:'Extrapolação de outras tarefas técnicas',
      supports:'A IA é usada em fluxos técnicos e pode ajudar com rascunhos, busca e revisão inicial.',
      uncertainty:'Ensaios de programação não validam projetos elétricos, cálculos estruturais ou dispositivos de segurança.'
    },
    executive: {
      grade:'Limitada',method:'Produtividade de escrita e escritório',
      supports:'Experimentos indicam vantagens de IA para partes da escrita e organização de trabalho.',
      uncertainty:'Não demonstram superioridade em julgamentos estratégicos ou decisões complexas.'
    },
    legal: {
      grade:'Indireta',method:'Diretrizes de risco e evidência análoga',
      supports:'A IA pode estruturar e localizar texto; há preocupação documentada com erros e fontes inexistentes.',
      uncertainty:'Não existe validação universal de respostas jurídicas em toda jurisdição.'
    },
    finance: {
      grade:'Indireta',method:'Produtividade adjacente + cautela técnica',
      supports:'Assistência para organizar dados e comparar cenários pode ser testada com revisão humana.',
      uncertainty:'Essas fontes não validam previsão de mercado, impostos ou decisões financeiras individualizadas.'
    }
  };
  function brainFor(s, category) {
    if (category === 'learn' || category === 'noai' || category === 'authorship' || category === 'sensitive' || category === 'highrisk' || category === 'personal') {
      return BRAIN_BY_CATEGORY[category];
    }
    if (has(s, /\b(resumir|resumo|resuma|sintetizar|sumarizar|summarize|summarise)\b/)) {
      return ['Defina o que é importante antes de resumir', 'Antes de pedir um resumo, formule o que precisa descobrir. Compare datas, números e conclusões com o original. Se o objetivo for aprender o conteúdo, tente explicá-lo sozinho depois.'];
    }
    if (has(s, /\b(e mail|email|gmail|outlook|correio eletronico)\b/)) {
      if (has(s, /\b(escrever|redigir|responder|resposta|preparar|compose|write|reply|answer)\b/)) {
        return ['Escreva a primeira versão. Deixe a IA revisar.', 'Pense no que quer comunicar e escreva um rascunho com suas palavras (ou comece por um rascunho seu já existente). Depois, peça à IA sugestões de clareza, tom, gramática e concisão. Decida o que aceitar e confira fatos, anexos, destinatários e compromissos antes de enviar.'];
      }
      return ['Decida o que importa na comunicação', 'Defina você a intenção, o tom e os compromissos. Use IA para organizar ou revisar mensagens, sem delegar a decisão sobre o que enviar.'];
    }
    if (has(s, /\b(whatsapp|mensagem|mensagens|sms|direct|dm)\b/) && has(s, /\b(escrever|redigir|responder|enviar|preparar)\b/)) {
      return ['Escreva sua mensagem e depois peça revisão', 'Defina você o objetivo e escreva a mensagem. Use a IA para melhorar clareza e tom, sem transferir a responsabilidade pelo que será enviado em seu nome.'];
    }
    if (has(s, /\b(fotos|fotografias|galeria|google photos|google fotos|imagens)\b/)) {
      return ['Estabeleça seus critérios de organização', 'Decida quais fotos têm valor, o que deve ser privado e o que pode ser descartado. Confira as sugestões antes de mover, compartilhar ou excluir.'];
    }
    if (has(s, /\b(pastas|arquivos|downloads|documentos|drive|onedrive|dropbox)\b/)) {
      return ['Crie a regra de organização', 'Defina nomes e critérios de classificação. Revise uma amostra antes de mover ou renomear em massa e mantenha uma forma de desfazer mudanças.'];
    }
    if (has(s, /\b(artigos cientificos|pubmed|referencias|bibliografia|literatura cientifica|papers)\b/)) {
      return ['Formule a pergunta científica', 'Decida palavras-chave, critérios de inclusão e o que a evidência realmente responderia. Use IA para encontrar pistas, mas confira DOI, métodos e conclusões nos estudos.'];
    }
    if (has(s, /\b(codigo|python|javascript|programacao|programar|sql|debug|depurar)\b/)) {
      return ['Entenda o código que você entrega', 'Defina o comportamento esperado e os testes. Deixe a IA propor mudanças, mas saiba explicar a solução e confira seus efeitos antes de integrar.'];
    }
    return BRAIN_BY_CATEGORY[category] || BRAIN_BY_CATEGORY.routine;
  }
  function assess(task, result, evid) {
    const s = norm(task), cat = result.category || 'routine', profile = evid.profileKey || 'everyday';
    const mathematics = has(s, /\b(matematica|estatistica|algebra|geometria|equacao|fracoes|aritmetica|calculo|trigonometria|exercicios|problemas matematicos)\b/);
    const stories = has(s, /\b(contos?|historias?|narrativas?|ficcao|creative writing)\b/);
    let item;
    if (RULES[cat]) item = {...RULES[cat]};
    else if (cat === 'learn') {
      item = mathematics ? {
        grade:'Moderada',method:'Experimento de IA + estudos de aprendizagem em matemática',
        supports:'Em matemática escolar, um experimento randomizado encontrou pior resultado posterior sem IA quando o acesso foi irrestrito. Trabalhos de “falha produtiva” apoiam a tentativa inicial.',
        uncertainty:'Não é evidência de perda de QI ou efeito duradouro; nem demonstra que toda forma de tutoria por IA atrapalha a aprendizagem.'
      } : {
        grade:'Limitada',method:'Extrapolação de experimentos educacionais',
        supports:'A necessidade de recuperar e praticar conhecimentos é sustentada por estudos de aprendizagem, e há um ensaio específico de IA em matemática.',
        uncertainty:'A evidência citada não testou esta habilidade em particular. Tutores bem desenhados também podem ajudar a aprender.'
      };
    } else if (cat === 'creative') {
      item = {...DIRECT.creative};
      if (stories) {
        item.grade = 'Moderada';
        item.method = 'Experimento diretamente em histórias curtas';
        item.uncertainty = 'O resultado foi observado em produção de histórias; “primeiro humano, depois IA” continua sendo uma proposta prudencial, não uma intervenção testada no estudo.';
      }
    } else if (cat === 'routine') {
      item = {...(DIRECT[profile] || DIRECT.everyday)};
      if (profile === 'business' && has(s, /\b(atendimento|suporte|clientes|clientela|customer service)\b/)) {
        item.grade = 'Moderada';
        item.method = 'Experimento de campo em atendimento e apoio profissional';
      }
    } else item = {...DIRECT.everyday};
    if (result.uncertain && !RULES[cat]) {
      item = {...item,grade:'Baixa para esta busca',method:'Objetivo ou correspondência pouco claros',
        uncertainty:'Não foi possível inferir bem o objetivo desta descrição. A recomendação e os estudos podem não corresponder ao que você quer fazer. ' + item.uncertainty};
    }
    const [brainTitle,brainAction] = brainFor(s,cat);
    return {
      grade:item.grade,method:item.method,supports:item.supports,uncertainty:item.uncertainty,
      brainTitle,brainAction,
      cognition:cat==='learn' ? LEARNING_NOTE : IQ_NOTE
    };
  }
  window.UYB_EVIDENCE = Object.freeze({assess});
})();