(() => {
  'use strict';
  const params=new URLSearchParams(location.search);
  const lang=params.get('lang')==='en'?'en':'pt';
  const en=lang==='en';
  document.documentElement.lang=en?'en':'pt-BR';
  const $=id=>document.getElementById(id);
  const data=Array.isArray(window.UYB_STUDIES)?window.UYB_STUDIES:[];
  const topicNames={
    all:['Todos os temas','All topics'],
    learning:['Aprendizagem','Learning'],
    critical:['Pensamento crítico','Critical thinking'],
    language:['Linguagem','Language'],
    memory:['Memória','Memory'],
    creativity:['Criatividade','Creativity'],
    productivity:['Produtividade','Productivity'],
    reliability:['Confiabilidade e fontes','Reliability and sources']
  };
  const typeNames={
    all:['Todos os desenhos','All study designs'],
    experiment:['Experimento','Experiment'],
    review:['Revisão','Review'],
    meta:['Metanálise','Meta-analysis'],
    observational:['Observacional / quase-experimento','Observational / quasi-experiment'],
    benchmark:['Benchmark / avaliação','Benchmark / evaluation'],
    guideline:['Diretriz','Guideline']
  };
  const strengthNames={
    direct:['Evidência diretamente relevante','Directly relevant evidence'],
    contextual:['Evidência contextual / indireta','Contextual / indirect evidence'],
    preliminary:['Resultado preliminar','Preliminary result'],
    normative:['Diretriz, não experimento','Guideline, not experiment']
  };
  const text={
    pt:{brand:'Devo usar IA ou não?',tool:'Ferramenta',studies:'Estudos',eyebrow:'BIBLIOTECA CIENTÍFICA',
      title:'O que a ciência diz <em>sobre IA e cognição?</em>',
      intro:'Explore pesquisas sobre aprendizagem, pensamento crítico, memória, linguagem, criatividade e produtividade — com explicações do método, resultados e limitações.',
      note:'<strong>Leitura crítica:</strong> esta é uma seleção de estudos centrais, não uma revisão sistemática de toda a literatura. Um estudo que demonstra produtividade não comprova preservação cognitiva; uma associação não prova causalidade.',
      search:'Encontrar um estudo',placeholder:'Tema, autor, método ou palavra-chave...',topic:'Tema',type:'Tipo de pesquisa',clear:'Limpar filtros',
      count:n=>n+' de '+data.length+' referências',empty:'Nenhum estudo encontrado. Experimente outro termo ou limpe os filtros.',
      expand:'Ver método, resultados e limitações',method:'COMO FOI FEITO',finding:'O QUE FOI ENCONTRADO',
      limit:'LIMITAÇÕES',application:'O QUE ISSO SIGNIFICA PARA O USO DA IA',read:'Abrir estudo original',
      footer:'Ciência para pensar melhor — com e sem inteligência artificial.',titleTab:'Estudos | Devo usar IA ou não?',desc:'Estudos sobre IA, aprendizagem, pensamento crítico, memória, linguagem e criatividade, com método, resultados, limitações e fontes.'},
    en:{brand:'Should I use IA or not?',tool:'Decision tool',studies:'Studies',eyebrow:'RESEARCH LIBRARY',
      title:'What does research say <em>about AI and cognition?</em>',
      intro:'Explore studies on learning, critical thinking, memory, language, creativity and productivity — with clear methods, findings and limitations.',
      note:'<strong>Read critically:</strong> this is a curated selection of important references, not an exhaustive systematic review. A productivity study does not establish cognitive preservation; correlation does not establish causality.',
      search:'Find a study',placeholder:'Topic, author, design or keyword...',topic:'Topic',type:'Study design',clear:'Clear filters',
      count:n=>n+' of '+data.length+' references',empty:'No matching studies. Try another search or clear the filters.',
      expand:'View methods, results and limitations',method:'HOW IT WAS STUDIED',finding:'MAIN FINDINGS',
      limit:'LIMITATIONS',application:'WHAT THIS MEANS FOR AI USE',read:'Open original study',
      footer:'Science for better thinking — with and without artificial intelligence.',titleTab:'Studies | Should I use IA or not?',desc:'Studies on AI, learning, critical thinking, memory, language and creativity with methods, findings, limitations and original sources.'}
  }[lang];
  const pick=pair=>pair?.[lang]||'';
  const name=arr=>arr?.[en?1:0]||'';
  $('brand').querySelector('span').textContent=text.brand;
  $('home-link').textContent=text.tool;
  $('home-link').href=en?'/?lang=en':'/?lang=pt';
  $('studies-link').textContent=text.studies;
  $('studies-link').href=en?'/estudos.html?lang=en':'/estudos.html?lang=pt';
  $('language-pt').classList.toggle('active',!en);
  $('language-en').classList.toggle('active',en);
  $('language-pt').setAttribute('aria-current',en?'false':'page');
  $('language-en').setAttribute('aria-current',en?'page':'false');
  $('eyebrow').textContent=text.eyebrow;
  $('title').innerHTML=text.title;
  $('intro').textContent=text.intro;
  $('method-note').innerHTML=text.note;
  $('query-label').textContent=text.search;
  $('search').placeholder=text.placeholder;
  $('topic-label').textContent=text.topic;
  $('type-label').textContent=text.type;
  $('clear').textContent=text.clear;
  $('footer-brand').textContent=text.brand;
  $('footer-note').textContent=text.footer;
  document.title=text.titleTab;
  document.querySelector('meta[name="description"]').content=text.desc;
  document.querySelector('meta[property="og:title"]').content=text.titleTab;
  document.querySelector('meta[property="og:description"]').content=text.desc;
  function option(select,value,label){const opt=document.createElement('option');opt.value=value;opt.textContent=label;select.append(opt);}
  for(const [k,v] of Object.entries(topicNames))option($('topic'),k,name(v));
  for(const [k,v] of Object.entries(typeNames))option($('design'),k,name(v));
  const norm=s=>String(s||'').toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();
  const add=(tag,className,content)=>{const x=document.createElement(tag);if(className)x.className=className;if(content!==undefined)x.textContent=content;return x;};
  const results=$('library');
  function paper(record){
    const details=document.createElement('details');details.className='paper';details.id='study-'+record.id;
    const summary=document.createElement('summary');
    const meta=add('div','paper-top');
    meta.append(add('span','tag',name(topicNames[record.topic])),add('span','tag secondary',name(typeNames[record.type])),add('span','year',String(record.year)));
    const title=add('h2','paper-title',record.title);
    const citation=add('p','paper-meta',record.authors+' · '+record.source);
    const teaser=add('p','paper-teaser',pick(record.findings));
    const expand=add('div','paper-more',text.expand);
    summary.append(meta,title,citation,teaser,expand);
    details.append(summary);
    const inner=add('div','expanded');
    const grid=add('div','study-grid');
    const fields=[[text.method,pick(record.method)],[text.finding,pick(record.findings)],[text.limit,pick(record.limitations)],[text.application,pick(record.application)]];
    fields.forEach(([label,body])=>{
      const section=add('div','finding');section.append(add('h3','',label),add('p','',body));grid.append(section);
    });
    inner.append(grid);
    const links=add('div','reading');
    const link=add('a','',text.read+' ↗');link.href=record.url;link.target='_blank';link.rel='noopener noreferrer';
    links.append(link);
    if(record.doi)links.append(add('span','doi','DOI: '+record.doi));
    const strength=add('span','tag secondary',name(strengthNames[record.strength]));
    links.append(strength);
    inner.append(links);details.append(inner);
    return details;
  }
  function render(){
    const query=norm($('search').value);
    const topic=$('topic').value;
    const type=$('design').value;
    const filtered=data.filter(p=>(topic==='all'||p.topic===topic)&&(type==='all'||p.type===type)&&(!query||norm([p.title,p.authors,p.source,p.year,name(topicNames[p.topic]),name(typeNames[p.type]),p.method.pt,p.method.en,p.findings.pt,p.findings.en,p.limitations.pt,p.limitations.en,p.application.pt,p.application.en].join(' ')).includes(query)));
    filtered.sort((a,b)=>b.year-a.year||a.title.localeCompare(b.title));
    $('count').textContent=text.count(filtered.length);
    results.replaceChildren();
    if(!filtered.length){results.append(add('p','empty',text.empty));return;}
    const frag=document.createDocumentFragment();
    for(const p of filtered)frag.append(paper(p));
    results.append(frag);
  }
  $('search').addEventListener('input',render);
  $('topic').addEventListener('change',render);
  $('design').addEventListener('change',render);
  $('clear').addEventListener('click',()=>{
    $('search').value='';$('topic').value='all';$('design').value='all';render();$('search').focus();
  });
  render();
  window.UYB_STUDIES_UI={lang,filter:render,count:()=>data.length};
})();