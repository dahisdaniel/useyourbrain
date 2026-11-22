/* Busca local por tarefa e ocupação. 10.000 cenários editoriais, nenhuma API. */
(() => {
  'use strict';
  const input = document.getElementById('task');
  const tray = document.getElementById('task-suggestions');
  const list = document.getElementById('suggestions-list');
  const label = document.getElementById('suggestions-label');
  const status = document.getElementById('suggestions-status');
  if (!input || !tray || !list || !label || !status) return;
  const CAT_LABEL={
    authorship:'Autoria acadêmica',learn:'Aprender primeiro',creative:'Criar primeiro',
    routine:'IA com revisão',highrisk:'Decisão de risco',sensitive:'Privacidade',
    personal:'Voz pessoal',noai:'Não usar IA'
  };
  const raw = Array.isArray(window.ANTES_TASKS) ? window.ANTES_TASKS : [];
  const indexed = raw.map(row => ({
    ...row,
    norm:normalize(row.task),
    tt:tokens(row.task),
    pt:tokens(row.profession||''),
    st:tokens(row.sector||'')
  }));
  const freq=Object.create(null);
  indexed.forEach(row=>{for(const t of new Set([...row.tt,...row.pt]))freq[t]=(freq[t]||0)+1;});
  let suggestions=[],active=-1,debounce=0;
  const maxTasks=6;

  const termMatch=(term, arr)=>{
    if(arr.includes(term))return 1;
    if(term.length>=3&&arr.some(t=>t.startsWith(term)))return .78;
    if(term.length>=4&&arr.some(t=>term.startsWith(t)&&t.length>=4))return .48;
    return 0;
  };

  function similarTasks(query,limit=maxTasks){
    const norm=normalize(query);
    if(norm.length<3||!indexed.length)return [];
    const q=tokens(query);
    if(!q.length)return [];
    const weights=q.map(t=>Math.log(1+indexed.length/(1+(freq[t]||0))));
    const total=weights.reduce((s,n)=>s+n,0)||1;
    const candidates=[];
    const privacyIntent=/identificav|prontuario|sigil|confidenc|dados pessoais/.test(norm);
    for(const row of indexed){
      let weight=0, hits=0, taskHits=0;
      for(let i=0;i<q.length;i++){
        const inTask=termMatch(q[i],row.tt);
        const inMeta=Math.max(termMatch(q[i],row.pt),termMatch(q[i],row.st));
        const strength=Math.max(inTask,inMeta*.50);
        if(strength){weight+=weights[i]*strength;hits++;if(inTask)taskHits++;}
      }
      if(!hits)continue;
      let score=.79*weight/total +.08*taskHits/Math.max(row.tt.length,1);
      if(row.norm.startsWith(norm))score+=.13;
      else if(row.norm.includes(norm))score+=.07;
      if(row.norm===norm)score=2;
      if(row.priority==='ancora')score+=.16;
      if(privacyIntent && row.category==='sensitive')score+=.16;
      if(privacyIntent && /sistema clinico aprovado/.test(row.norm))score-=.24;
      if(hits===q.length)score+=.10;
      // Long, generic descriptions should not drown out specific matches.
      if(taskHits===0)score-=.10;
      if(score<.22)continue;
      candidates.push({...row,score});
    }
    candidates.sort((a,b)=>b.score-a.score||a.task.length-b.task.length||a.id.localeCompare(b.id));
    const results=[], professions=new Map();
    for(const item of candidates){
      const count=professions.get(item.profession)||0;
      if(count>=2)continue;
      professions.set(item.profession,count+1);
      results.push(item);
      if(results.length>=Math.max(1,Math.min(limit,12)))break;
    }
    return results;
  }

  function hide(){
    window.clearTimeout(debounce);debounce=0;
    tray.hidden=true;input.setAttribute('aria-expanded','false');
    input.removeAttribute('aria-activedescendant');list.replaceChildren();suggestions=[];active=-1;
  }
  function activate(index){
    if(!suggestions.length)return;
    active=(index+suggestions.length)%suggestions.length;
    [...list.children].forEach((el,i)=>{
      el.classList.toggle('is-active',active===i);
      el.setAttribute('aria-selected',String(active===i));
    });
    const item=list.children[active];
    if(item){input.setAttribute('aria-activedescendant',item.id);item.scrollIntoView({block:'nearest'});}
  }
  function selectTask(task){
    window.__selectedTask=task;
    input.value=task.task;
    document.getElementById('charcount').textContent=`${input.value.length} / 700`;
    document.getElementById('error').textContent='';
    hide();
    document.getElementById('task-form').requestSubmit();
  }
  function update(){
    debounce=0;
    const value=input.value.trim();
    if(value.length<3){hide();return;}
    suggestions=similarTasks(value,maxTasks);active=-1;
    list.replaceChildren();tray.hidden=false;
    input.setAttribute('aria-expanded','true');input.removeAttribute('aria-activedescendant');
    if(!suggestions.length){
      label.textContent='Nenhum caso semelhante';
      const msg=document.createElement('p');msg.className='suggestions-empty';
      msg.textContent='Você pode continuar descrevendo e clicar em “Analisar tarefa”.';
      list.append(msg);status.textContent='Nenhuma correspondência próxima';return;
    }
    label.textContent=`${suggestions.length} tarefas relacionadas`;
    status.textContent=`${suggestions.length} sugestões. Use as setas e Enter para selecionar.`;
    suggestions.forEach((item,i)=>{
      const button=document.createElement('button');
      button.type='button';button.id=`suggestion-${i}`;button.className='suggestion';
      button.setAttribute('role','option');button.setAttribute('aria-selected','false');button.tabIndex=-1;
      const main=document.createElement('span');main.className='suggestion-text';main.textContent=item.task;
      const meta=document.createElement('span');meta.className='suggestion-category';
      meta.textContent=`${item.profession} · ${CAT_LABEL[item.category]||'Tarefa'}`;
      const arrow=document.createElement('span');arrow.className='suggestion-arrow';
      arrow.setAttribute('aria-hidden','true');arrow.textContent='↗';
      button.append(main,meta,arrow);
      button.addEventListener('mouseenter',()=>activate(i));
      button.addEventListener('click',()=>selectTask(item));
      list.append(button);
    });
  }
  input.setAttribute('role','combobox');input.setAttribute('aria-autocomplete','list');
  input.setAttribute('aria-controls','suggestions-list');input.setAttribute('aria-expanded','false');
  input.addEventListener('input',()=>{
    window.__selectedTask=null;
    window.clearTimeout(debounce);
    debounce=window.setTimeout(update,85);
  });
  input.addEventListener('focus',()=>{if(input.value.trim().length>=3&&tray.hidden){window.clearTimeout(debounce);debounce=window.setTimeout(update,40);}});
  input.addEventListener('keydown',event=>{
    if(event.isComposing||event.keyCode===229)return;
    if(event.key==='Escape'){hide();return;}
    if((event.key==='ArrowDown'||event.key==='ArrowUp')&&!tray.hidden&&suggestions.length){
      event.preventDefault();activate(active+(event.key==='ArrowDown'?1:-1));return;
    }
    if(event.key==='Enter'&&!event.shiftKey){
      event.preventDefault();
      if(!tray.hidden&&suggestions.length)selectTask(suggestions[active<0?0:active]);
      else document.getElementById('task-form').requestSubmit();
    }
  });
  document.getElementById('task-form').addEventListener('submit',hide);
  document.addEventListener('pointerdown',e=>{if(!document.getElementById('task-form').contains(e.target))hide();});
  window.__suggestTasks=similarTasks;
})();
