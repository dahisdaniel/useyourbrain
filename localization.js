/* Portuguese / English static UI + evidence-aware localized answers. No external API. */
(() => {
  'use strict';
  const lang=new URLSearchParams(location.search).get('lang')==='en'?'en':'pt';
  const en=lang==='en';
  const $=id=>document.getElementById(id);
  const norm=v=>String(v||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();
  const label=(selector,value,asHTML=false)=>{const el=document.querySelector(selector);if(el){if(asHTML)el.innerHTML=value;else el.textContent=value;}};
  const set=(id,value,asHTML=false)=>{const el=$(id);if(el){if(asHTML)el.innerHTML=value;else el.textContent=value;}};
  const phrases={
    pt:{name:'Devo usar IA ou não?',study:'Estudos',tool:'Ferramenta',how:'Como funciona'},
    en:{name:'Should I use IA or not?',study:'Studies',tool:'Decision tool',how:'How it works'}
  };
  const WORDS={
    learning:'Learning',language:'Language',critical:'Critical thinking',memory:'Memory',creativity:'Creativity',productivity:'Productivity',reliability:'Reliability',
    'Aprendizagem':'Learning','Linguagem':'Language','Pensamento crítico':'Critical thinking','Criatividade':'Creativity',
    'Execução e checagem':'Execution and checking','Autonomia e responsabilidade':'Agency and responsibility'
  };
  const modeEn={
    restricted:{tag:'Not authorized',title:'Do not use an unauthorized AI tool for this task.',
      summary:'Rules, confidential information and permissions take priority over convenience.',
      brain:'Respect the limits of the activity',action:'Identify which tools are allowed and what information must remain private.',
      delegate:'Only the help explicitly permitted by the activity or organization.',check:'Follow the rules and confirm where data would go.'},
    highstakes:{tag:'Human judgment required',title:'Use AI as support, not as the final decision-maker.',
      summary:'Form your own assessment of risks and options, then consult AI to find questions you might have missed. Verify with reliable sources and qualified people.',
      brain:'Keep your critical judgment',action:'Define the question, evidence, assumptions and consequences. Challenge AI claims and verify high-impact conclusions.',
      delegate:'Preliminary organization, alternative perspectives and questions for experts.',check:'Could you justify the decision with independent evidence?'},
    learn_language:{tag:'Learning · language',title:'Speak and write yourself. Use AI for conversation practice.',
      summary:'Form your own sentences before accepting feedback. Use AI to practice dialogue and pronunciation, then try again without help and with real people.',
      brain:'Practice producing language',action:'Speak or write your answer before seeing a model answer. Ask for explanations of errors, then repeat unaided.',
      delegate:'Conversation prompts, feedback and graded practice.',check:'Can you sustain a short conversation without auto-translation?'},
    learn_code:{tag:'Learning · programming',title:'Write the code first. Ask AI for hints, not a finished answer.',
      summary:'Attempt the algorithm and debug it yourself. Get progressively stronger hints when needed, then solve a similar problem without AI.',
      brain:'Practice algorithmic thinking',action:'Sketch the logic, write a partial solution and test it before asking for help.',
      delegate:'Specific explanations, incremental clues and review of tests.',check:'Can you explain and reconstruct the solution without AI?'},
    learn_any:{tag:'Active learning',title:'Learn actively. Use AI as a tutor, not a substitute.',
      summary:'Try, make mistakes, retrieve what you learned and ask for targeted hints. Test your understanding without assistance.',
      brain:'Preserve the learning effort',action:'Explain or solve something yourself, then ask for feedback and try a new example.',
      delegate:'Practice problems, examples and feedback.',check:'Can you do something new without copying the AI answer?'},
    authored:{tag:'Human authorship',title:'Keep the argument yours. Use AI as a critical editor.',
      summary:'Develop your own questions, interpretation and argument. Ask AI for counterarguments and clarity checks while following authorship rules.',
      brain:'Own the reasoning and interpretation',action:'Write your position first and verify every claim against the original sources.',
      delegate:'Language editing, organization and counterarguments.',check:'Can you defend your conclusions without the AI draft?'},
    linguistic:{tag:'Language · write first',title:'Draft it yourself. Let AI review it.',
      summary:'Choose what to say and write your first version. Then ask AI for clarity, grammar, tone and concision suggestions; accept only changes that reflect your intent.',
      brain:'Preserve your writing skills',action:'Formulate the message in your own words before using automatic suggestions.',
      delegate:'Grammar, tone, concision and clarity suggestions.',check:'Could you explain or rewrite the final message in your own words?'},
    spoken:{tag:'Spoken language',title:'Prepare your ideas. Practice speaking in your own words.',
      summary:'Organize the points and rehearse without reading AI-generated prose. Use AI to simulate questions and highlight confusing sections.',
      brain:'Keep your ability to explain',action:'Practice speaking without relying on a finished AI script.',
      delegate:'Mock Q&A, structural feedback and clarity checks.',check:'Could you deliver the message aloud without a generated script?'},
    critical:{tag:'Critical thinking · AI as challenger',title:'Form your interpretation. Use AI to challenge it.',
      summary:'Analyze evidence and alternatives yourself. Then ask AI for objections and blind spots, and verify consequential claims in original sources.',
      brain:'Make your own critical assessment',action:'Write your initial reasoning and what evidence would change your mind, then test it against counterarguments.',
      delegate:'Alternative hypotheses, critiques and ways to organize evidence.',check:'Can you justify the conclusion using original sources?'},
    creative:{tag:'Creativity · original ideas',title:'Start with your own ideas. Use AI as a counterpoint.',
      summary:'Generate your own possibilities before looking at AI suggestions. Use it to test assumptions and explore genuinely different alternatives.',
      brain:'Keep your own creative direction',action:'Sketch several options before asking for AI suggestions, including one surprising idea.',
      delegate:'Criticism, analogies and contrasting approaches.',check:'Which creative decisions were yours, and why?'},
    summary:{tag:'Summarization · verify',title:'AI can summarize. You decide what matters.',
      summary:'AI can draft a summary to save time. Define your question and verify facts, numbers, negations and commitments against the original.',
      brain:'Choose what deserves attention',action:'Decide why you are reading the material and which details cannot be lost.',
      delegate:'Initial outline, topic extraction and first-pass summary.',check:'Compare the result with the original for omissions or errors.'},
    routine:{tag:'Automation · human oversight',title:'Automate repetitive work. Keep control.',
      summary:'Use AI for repetitive, checkable work. Set the rules and review important or irreversible actions.',
      brain:'Set the quality criteria',action:'Define organization, privacy and success criteria before delegating.',
      delegate:'Sorting, formatting, transcription and repeatable operations.',check:'Review a sample and preserve a way to undo changes.'},
    review:{tag:'AI as editor',title:'Let AI review. You decide what to change.',
      summary:'When the material is already yours, request editing suggestions and compare them with your intent.',
      brain:'Keep the meaning yours',action:'Review suggestions rather than accepting everything automatically.',
      delegate:'Proofreading, structure and fluency corrections.',check:'Does every accepted change still mean what you intended?'},
    unclear:{tag:'Clarify the purpose',title:'Define your goal before you delegate.',
      summary:'The same task can be done to learn or simply to save time. State which matters, then decide what to outsource.',
      brain:'Decide what the task is for',action:'Ask whether you need to develop the skill or just complete the task.',
      delegate:'Simple preliminary organization if appropriate.',check:'Can you say what you wish to learn or accomplish?'}
  };
  const evidenceEn={
    restricted:['Rule or safety guideline','The decision follows restrictions or privacy requirements, not a trial of this exact task.','Neither blanket bans on AI nor universal data exposure are established by these sources.'],
    highstakes:['Guidance and indirect evidence','Risk-management frameworks recommend human review, verification and proportionate safeguards.','These studies do not prove that AI performs worse than professionals in every high-stakes task.'],
    learn_language:['Moderate for English learning; indirect elsewhere','A meta-analysis of English-learning interventions found average benefits, although results varied widely.','This does not prove the same benefits for every language or that AI should replace teachers.'],
    learn_code:['Limited; programming experiments','In specific programming courses, hints-based assistants supported test gains while unrestricted assistance improved output without equal gains in understanding.','Effects depend on the setting and model; no universal cognitive decline is shown.'],
    learn_any:['Limited for this specific skill','Retrieval practice and productive failure research support active learning, alongside narrower AI education experiments.','The evidence may not test the skill you entered or compare all possible AI-tutoring designs.'],
    authored:['Editorial guidance + indirect evidence','Publication guidelines keep authors accountable for original arguments, accuracy and source checking.','This is not an experiment proving that AI editing causes loss of authorship skills.'],
    linguistic:['Moderate for productivity; limited for skill preservation','Randomized writing experiments found faster, better-rated output with AI, and a small quasi-experimental study examined unaided writing after different types of assistance.','The exact workflow of human draft first, AI review second has not been proven to preserve long-term language ability.'],
    spoken:['Indirect evidence for oral skills','Results from writing and educational studies offer plausible reasons to practice independently.','There is no direct test here showing how AI affects long-term public-speaking ability.'],
    critical:['Limited or indirect evidence','Observational research and reliability studies support checking AI claims and preserving independent judgment.','The human-first sequence has not been validated as superior for every intellectual task.'],
    creative:['Direct for short stories; indirect elsewhere','An experiment found better-rated individual stories but greater similarity across AI-assisted authors.','It did not test all creative fields or prove that creating first prevents homogenization.'],
    summary:['Limited; reliability benchmarks','Benchmarks identify fabricated or distorted content in model-generated summaries.','They do not establish the error rate of your specific tool or a decline in your memory.'],
    routine:['Indirect for this exact operation','Real-world studies show AI productivity benefits in selected tasks, making supervised automation plausible.','Not every file operation or workflow has been experimentally evaluated.'],
    review:['Productivity studies; limited for retention','AI assistance can improve some writing outputs. Reviewing the suggestion keeps responsibility with the human.','No direct proof that the suggested review sequence protects independent writing in the long term.'],
    unclear:['Insufficient task-specific evidence','The description does not clarify whether the goal is learning, creative work or execution.','A single evidence grade would overstate our certainty.']
  };
  const hybridEn={
    'scientific-critique':['Read and critique first. Use AI as a second opinion.','Identify the study question, design, results and limitations yourself; then ask AI to challenge your assessment. Verify every claim against the paper.'],
    'scientific-summary':['Use AI to synthesize. Check the original study yourself.','Read the key methods and results before trusting a generated summary. Verify numbers, study design and limitations.'],
    'literature-search':['Use AI to suggest search terms. You select the papers.','Define your scientific question and inclusion criteria. Verify titles, DOIs, eligibility and methods in the original sources.'],
    'study-design':['Form your hypothesis. Ask AI to try to refute it.','Write the hypothesis, endpoints and controls first; ask for alternative explanations and confounders, and validate them.'],
    'authored-scholarship':['Your scholarship needs your judgment. Use AI as an editor.','Define the research question, reasoning and conclusions yourself. Use AI for objections and language review, with disclosure as needed.'],
    'data-interpretation':['Interpret the data first. Use AI to challenge your analysis.','State assumptions and your interpretation before asking for alternative models; verify calculations with reliable tools.'],
    'code-review':['Let AI review code. You must still understand and test it.','Define expected behavior, write tests and inspect proposed changes. Do not merge code you cannot explain.'],
    'engineering-review':['Own the engineering. Use AI to flag blind spots.','Set specifications, units, safety margins and tests. Check every safety-critical claim against standards and validated tools.'],
    'clinical-reasoning':['AI may support review; clinical decisions require accountability.','Do not delegate diagnosis or treatment. Validate sources, protect patient data and retain qualified clinical review.'],
    'legal-reasoning':['Build your legal reasoning. Use AI for a verified second pass.','Check the law, jurisdiction, precedents and citations yourself.'],
    'financial-judgment':['Set your financial criteria. Use AI to explore scenarios.','Define risk tolerance, assumptions and horizons, then verify calculations and primary information.'],
    'business-strategy':['Set the criteria. Ask AI to challenge the strategy.','Write down trade-offs and assumptions; use AI to generate objections, then verify decisions with evidence.'],
    'hiring-appraisal':['Use explicit fair criteria. Do not outsource judgments about people.','Use AI to structure questions, not for unchecked automatic hiring decisions.'],
    'teaching-and-assessment':['Define learning objectives yourself. Let AI expand examples.','Choose what students must learn and demonstrate; then review the generated teaching materials.'],
    'creative-authorship':['Start with your own concept. Use AI to expand rather than homogenize.','Draft ideas without AI, then critically review suggested alternatives.']
  };
  const refSummaries={
    openaiusage:'Observed common uses of conversational AI, including writing, research and practical assistance; usage frequency does not establish benefits.',
    researchsurvey:'Surveyed how researchers use and evaluate AI throughout research workflows; adoption does not establish methodological validity.',
    ama2026:'Medical professionals report AI use for literature, drafting and documentation, but adoption does not establish clinical safety.',
    googlephotos:'Product documentation describes capabilities for finding and managing photos; it is not an independent clinical or cognitive experiment.',
    nist:'Technical guidance describes errors, privacy exposure and risk controls for generative AI.',
    anthropicindex:'Occupational data describe where models are used; they do not independently validate output quality.',
    icmje:'Editorial guidance keeps authors accountable for accuracy, originality, citations and disclosure.',
    riskbias:'AI-produced methodological assessments may contain plausible judgments without fully supported rationales.',
    languageChat:'Review of second-language chatbots describes opportunities for practice and feedback with important pedagogical limitations.'
  };
  const origToEnglish=[
    ['Escrever um e-mail profissional','Write a professional email'],
    ['Responder a um e-mail recebido','Reply to an email'],
    ['Organizar minhas fotos do Google Fotos','Organize my Google Photos'],
    ['Organizar pastas no computador','Organize computer folders'],
    ['Buscar artigos científicos no PubMed','Find scientific papers on PubMed'],
    ['Escrever minha tese de doutorado','Write my doctoral thesis'],
    ['Aprender uma língua estrangeira','Learn a foreign language'],
    ['Aprender a programar','Learn to code'],
    ['Aprender algo novo','Learn something new'],
    ['Resumir texto','Summarize text'],
    ['Resumir e-mail','Summarize an email'],
    ['Resumir um artigo científico','Summarize a scientific paper'],
    ['Resumir artigo científico apontando limitações','Summarize a scientific paper and its limitations'],
    ['Aprender Python','Learn Python'],
    ['Aprender inglês','Learn English'],
    ['Aprender espanhol','Learn Spanish'],
    ['Praticar conversação em inglês','Practice English conversation'],
    ['Criar uma hipótese original para investigar uma doença','Develop an original scientific hypothesis'],
    ['Revisar código Python','Review Python code'],
    ['Interpretar resultados estatísticos','Interpret statistical results'],
    ['Preparar uma apresentação oral','Prepare a presentation'],
    ['Revisar um contrato','Review a contract'],
    ['Avaliar paciente para diagnóstico','Evaluate a patient for diagnosis'],
    ['Resumir um PDF','Summarize a PDF'],
    ['Organizar arquivos','Organize files'],
    ['Aprender a usar planilhas Excel','Learn Excel']
  ];
  const originalMap=new Map(origToEnglish.map(([pt,enTitle])=>[norm(pt),enTitle]));
  const englishSamples=new Map(origToEnglish.map(([pt,translation])=>[norm(translation),pt]));
  const KEYWORDS=[
    [/learn|study|practice|memorize|improve.*skill/,q=>/program|code|python|javascript|sql|software/.test(q)?'Aprender a programar':/spanish/.test(q)?'Aprender espanhol':/english|language|speak|conversation|vocabulary|grammar/.test(q)?'Aprender uma língua estrangeira':'Aprender algo novo'],
    [/summari[sz]e|summary|outline|condense/,q=>/scientific|research|paper|study/.test(q)?(/limitations|bias|methods|critique|critical/.test(q)?'Resumir artigo científico apontando limitações':'Resumir um artigo científico'):/email|e mail|inbox/.test(q)?'Resumir e-mail':'Resumir texto'],
    [/scientific|research|pubmed|literature/,q=>/critique|limitations|bias|methodolog|apprais|evaluate|review/.test(q)?'Resumir artigo científico apontando limitações':'Buscar artigos científicos no PubMed'],
    [/program|code|debug|python|javascript/,q=>/learn|study|practice/.test(q)?'Aprender a programar':'Revisar código Python'],
    [/email|e mail|inbox/,q=>/summari[sz]e/.test(q)?'Resumir e-mail':/reply|respond|answer/.test(q)?'Responder a um e-mail recebido':'Escrever um e-mail profissional'],
    [/thesis|dissertation|academic manuscript/,()=> 'Escrever minha tese de doutorado'],
    [/photos?|pictures?|albums?|gallery/,()=> 'Organizar minhas fotos do Google Fotos'],
    [/folders?|files?|directories|documents/,()=> 'Organizar pastas no computador'],
    [/contract|agreement|legal/,()=> 'Revisar um contrato'],
    [/diagnos|patient|medical decision/,()=> 'Avaliar paciente para diagnóstico'],
    [/hypothes|creative ideas/,()=> 'Criar uma hipótese original para investigar uma doença'],
    [/presentation|public speaking/,()=> 'Preparar uma apresentação oral']
  ];
  function forAnalysis(value){
    if(!en)return value;
    const q=norm(value);
    if(englishSamples.has(q))return englishSamples.get(q);
    for(const [test,translate] of KEYWORDS)if(test.test(q))return translate(q);
    return value;
  }
  function suggestionLabel(task){
    if(!en)return task;
    if(originalMap.has(norm(task)))return originalMap.get(norm(task));
    const t=norm(task);
    if(t.startsWith('aprender ')){const noun=task.slice(task.indexOf(' ')+1);if(/python|excel|sql|java/i.test(noun))return 'Learn '+noun;return 'Learn a new skill';}
    if(t.startsWith('resumir '))return 'Summarize a document';
    if(t.startsWith('organizar '))return 'Organize files or information';
    if(t.startsWith('escrever '))return 'Draft a text';
    if(t.startsWith('buscar artigos'))return 'Find research papers';
    return 'Related catalog task';
  }
  function suggestionsEnglish(query,limit=6){
    const q=norm(query);
    if(q.length<2)return [];
    const chosen=forAnalysis(query);
    const base=window.UYB_SEARCH?.search(chosen,limit*3)||[];
    const out=[],used=new Set();
    for(const row of base){
      const displayed=suggestionLabel(row.task);
      if(used.has(displayed))continue;
      used.add(displayed);out.push({...row,displayTask:displayed});
      if(out.length>=limit)break;
    }
    return out;
  }
  const findStudyByUrl=url=>(window.UYB_STUDIES||[]).find(x=>x.url===url);
  function translateLabel(value){return WORDS[value]||value;}
  function localizeResult(ctx){
    if(!en)return;
    const {task,policy,evid,assessment,hybrid,result}=ctx;
    const m=modeEn[policy.mode]||modeEn.unclear;
    const h=hybridEn[hybrid?.id];
    set('res-category',m.tag);
    set('res-title',h?h[0]:m.title);
    set('res-summary',h?h[1]:m.summary);
    set('res-task',task);
    const custom=evidenceEn[policy.mode]||evidenceEn.unclear;
    set('res-evidence-quick','STRENGTH OF EVIDENCE: '+custom[0]);
    set('brain-title',m.brain);
    set('brain-action',h?h[1]:m.action);
    set('cognitive-focus',policy.domains.map(translateLabel).join(' · '));
    set('cognitive-delegate',m.delegate);
    set('cognitive-check',m.check);
    set('res-reason','WHY THIS APPROACH: '+(h?'This task requires careful human judgment, an AI second opinion and independent verification.':policy.reason==='O objetivo é desenvolver uma capacidade, e não apenas entregar um produto.'?'The goal is to develop a skill, not just complete an output.':'Our recommendation weighs learning, language, critical thinking, responsibility and verifiability.'));
    set('reason-pill','Evidence selected by task; interpret the limitations below');
    set('evidence-grade',custom[0]);
    set('evidence-method',assessment.method==='Juízo ético, não resultado experimental'?'Ethical judgment rather than experimental evidence':'Task-relevant studies and documented limitations; not a validated clinical evidence scale');
    set('evidence-support',custom[1]);
    set('evidence-uncertainty',custom[2]);
    set('evidence-cognition','ON COGNITION: These studies do not establish that this specific use of AI permanently lowers general intelligence.');
    set('res-limitation','LIMITATION: '+custom[2]+' The site uses editorial rules; its decision algorithm has not been independently validated.');
    document.querySelectorAll('.evidence-item').forEach(node=>{
      const lbl=node.querySelector('.ev-label'),p=node.querySelector('p'),a=node.querySelector('a');
      if(lbl)lbl.textContent='Original research / reference · '+(lbl.textContent.match(/20\d\d|19\d\d/)||[])[0];
      if(a){
        const study=findStudyByUrl(a.href);
        if(study&&p)p.textContent=study.authors+' · '+study.source+'. '+study.findings.en;
        else if(p){
          const original=p.textContent;
          const author=original.split(' · ')[0];
          const url=a.href.toLowerCase();
          const key=Object.keys(refSummaries).find(k=>url.includes(k));
          p.textContent=author+' · '+(key?refSummaries[key]:'See the original publication for design, findings and limitations.');
        }
        a.textContent='Read original source ↗';
      }
    });
  }
  function applyStatic(){
    document.documentElement.lang=en?'en':'pt-BR';
    const n=phrases[lang];
    document.title=n.name+' — Use Your Brain';
    document.querySelector('meta[property="og:title"]').content=n.name+' — Use Your Brain';
    document.querySelector('meta[name="description"]').content=en?
      'Describe your task and learn when to use AI, when to think independently, and what the scientific evidence really shows.':
      'Descreva sua tarefa e descubra quando usar IA — e quando pensar por conta própria, com referências científicas.';
    document.querySelector('meta[property="og:description"]').content=document.querySelector('meta[name="description"]').content;
    label('.brand span',n.name);label('.footer-brand span',n.name);
    set('nav-tool',n.tool);set('nav-studies',n.study);set('nav-science',n.how);
    const studies=document.getElementById('nav-studies');if(studies)studies.href='/estudos.html?lang='+lang;
    const seeAll=$('all-studies-link');if(seeAll){seeAll.href='/estudos.html?lang='+lang;seeAll.textContent=en?'Browse research library ↗':'Ver biblioteca de estudos ↗';}
    $('lang-pt')?.classList.toggle('active',!en);$('lang-en')?.classList.toggle('active',en);
    if(!en)return;
    label('.site-status','50,000 TASKS · NO API');
    label('.hero .eyebrow','AN EXPERIMENT IN INTELLECTUAL AUTONOMY');
    set('hero-title','Should I use <em>IA or not?</em>',true);
    label('.hero-description','Not everything that can be automated <strong>should be automated.</strong><br>Describe your task to see when AI helps — and when thinking for yourself is worth preserving.',true);
    const task=$('task');if(task)task.placeholder='What are you thinking of doing?\nE.g., I want to learn how to code...';
    label('label[for="task"]','What task do you want to complete?');
    set('task-help','Tell us whether you want to learn or simply finish the task.');
    set('analyze','Analyze task ↗');
    label('.suggestions-heading small','Select a task to see the recommendation');
    label('.examples-title','Try');
    const examples=['Write email','Reply to email','Google Photos','Organize files','Find research','Write thesis','Learn languages','Learn to code','Learn something new'];
    document.querySelectorAll('button.sample').forEach((b,i)=>{b.textContent=examples[i]||b.textContent;});
    const privacy=document.querySelector('.privacy');if(privacy&&privacy.lastChild?.nodeType===3)privacy.lastChild.textContent=' Your task is analyzed in your browser and is not sent to our server.';
    label('.custom-details>summary','Adjust context (optional)');
    label('label[for="goal"]','What is your main goal?');
    label('.custom-body .field-hint','Choose an option to improve the recommendation.');
    const opt=['Let the tool interpret','Learn or develop a skill','Create something original','Complete a task efficiently','Make an important decision','Write original academic work','Express something personal'];
    document.querySelectorAll('#goal option').forEach((x,i)=>x.textContent=opt[i]||x.textContent);
    document.querySelectorAll('.custom-body .field-title').forEach(x=>{if(x.textContent==='Cuidados especiais')x.textContent='Special considerations';});
    const ch=['Includes private or confidential data','An error could have serious consequences','AI help is not allowed for this task'];
    document.querySelectorAll('.checkbox-line span').forEach((x,i)=>x.textContent=ch[i]||x.textContent);
    label('.section-top .mono','01 / YOUR RECOMMENDATION');
    label('.section-top small','Local search in 50,000 examples + transparent rules · no AI API calls');
    label('.result-task b','YOUR TASK');
    label('.brain-recommendation-label .mono','USE YOUR BRAIN');
    label('.cognitive-focus-label','SKILLS TO EXERCISE');
    label('.cognitive-guidance p:nth-child(1) strong','AI can help:');
    label('.cognitive-guidance p:nth-child(2) strong','Independence check:');
    label('.brain-recommendation-copy>small','The goal is to preserve intellectual practice while using technology wisely.');
    label('.evidence-section .overline','02 / WHAT THE EVIDENCE SAYS');
    set('science-title','What does the research actually show?');
    label('.assessment-heading','STRENGTH OF EVIDENCE');
    label('.assessment-text:nth-of-type(2) strong','What supports this suggestion:');
    label('.assessment-text:nth-of-type(3) strong','What has not been demonstrated:');
    label('.evidence-heading','Research and sources');
    const spans=document.querySelectorAll('.science-heading span');if(spans[0])spans[0].textContent='WHY THIS TOOL EXISTS';if(spans[1])spans[1].textContent='CRITICAL THINKING × TECHNOLOGY';
    set('science-main-title','Not every difficulty needs to <em>disappear.</em>',true);
    const intro=document.querySelectorAll('.science-intro');
    if(intro[0])intro[0].textContent='Some tasks consume time without helping us grow. Others are exactly the practice that develops our ability to think, create and learn.';
    if(intro[1])intro[1].innerHTML='The goal is not to oppose AI. There is no proof that using AI necessarily reduces general intelligence. Critical thinking, writing in our own words and actively learning still matter. The question is when to <strong>delegate</strong>, <strong>collaborate</strong> or <strong>preserve human effort</strong>.';
    const info=[
      ['Learning means more than reaching the answer.','Assisted task performance can differ from later independent learning.'],
      ['Better ideas can become more alike.','In some tasks AI raises individual quality while reducing diversity across outputs.'],
      ['Saving effort is valuable too.','Experiments find real productivity gains in instrumental work.'],
      ['Risk changes the decision.','Privacy, security and the consequences of errors matter.']
    ];
    document.querySelectorAll('.science-point').forEach((node,i)=>{if(info[i]){node.querySelector('h3').textContent=info[i][0];node.querySelector('p').textContent=info[i][1];}});
    label('.disclosure-details summary','How does the site make recommendations?');
    label('.disclosure','This tool runs locally in your browser, without sending your task to a paid AI model. It compares your task with 50,000 editorially constructed examples and transparent rules for learning goals, language, critical thinking, originality, privacy and verification. These are not 50,000 observed popular user searches. Its recommendations are educational judgments, not validated cognitive measurements. The research supports specific findings about productivity, learning and reliability; no study establishes that AI necessarily lowers intelligence in every setting.');
    label('.footer-credit','An educational initiative about science and intellectual autonomy.');
  }
  applyStatic();
  window.UYB_L10N=Object.freeze({
    lang,isEnglish:()=>en,forAnalysis,suggestionsEnglish,suggestionLabel,localizeResult,
    strings:{emptySuggestions:en?'No similar tasks found':'Nenhuma tarefa semelhante',similar:n=>en?n+' related tasks':n+' tarefas relacionadas',
      choose:en?'Pick a suggestion or analyze your own description.':'Selecione uma sugestão ou analise sua descrição.',
      minWords:en?'Describe your task using a few more words.':'Descreva a tarefa com pelo menos algumas palavras.'}
  });
})();
