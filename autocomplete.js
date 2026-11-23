/* Busca local por tarefa e ocupação. 50.000 cenários editoriais, nenhuma API. */
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
  let suggestions=[],active=-1,debounce=0;
  const maxTasks=6;
  function similarTasks(query,limit=maxTasks){
    const locale=window.UYB_L10N;
    return locale?.isEnglish()
      ? locale.suggestionsEnglish(query,limit)
      : (window.UYB_SEARCH?.search(query,limit)||[]);
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
    input.value=window.UYB_L10N?.isEnglish() ? (task.displayTask||task.task) : task.task;
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
      label.textContent=window.UYB_L10N?.strings.emptySuggestions||'Nenhum caso semelhante';
      const msg=document.createElement('p');msg.className='suggestions-empty';
      msg.textContent=window.UYB_L10N?.strings.choose||'Você pode continuar descrevendo e clicar em “Analisar tarefa”.';
      list.append(msg);status.textContent=window.UYB_L10N?.strings.emptySuggestions||'Nenhuma correspondência próxima';return;
    }
    label.textContent=window.UYB_L10N?.strings.similar(suggestions.length)||`${suggestions.length} tarefas relacionadas`;
    status.textContent=window.UYB_L10N?.isEnglish()?`${suggestions.length} suggestions. Use arrows and Enter to select.`:`${suggestions.length} sugestões. Use as setas e Enter para selecionar.`;
    suggestions.forEach((item,i)=>{
      const button=document.createElement('button');
      button.type='button';button.id=`suggestion-${i}`;button.className='suggestion';
      button.setAttribute('role','option');button.setAttribute('aria-selected','false');button.tabIndex=-1;
      const main=document.createElement('span');main.className='suggestion-text';main.textContent=window.UYB_L10N?.isEnglish()?(item.displayTask||item.task):item.task;
      const meta=document.createElement('span');meta.className='suggestion-category';
      meta.textContent=window.UYB_L10N?.isEnglish()
        ? ({learn:'Learn actively',routine:'AI with review',authorship:'Human authorship',creative:'Creative work',highrisk:'High-stakes',sensitive:'Privacy',noai:'No AI',personal:'Personal expression'}[item.category]||'Task')
        : `${item.profession} · ${CAT_LABEL[item.category]||'Tarefa'}`;
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