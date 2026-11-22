/* Explorador sem rede: filtros de área/profissão/estratégia e CSV completo. */
(() => {
 'use strict';
 const items=Array.isArray(window.ANTES_TASKS)?window.ANTES_TASKS:[];
 const $=id=>document.getElementById(id);
 const sector=$('sector-filter'),profession=$('profession-filter'),strategy=$('strategy-filter'),list=$('explore-tasks');
 if(!sector||!profession||!strategy||!list)return;
 const count=$('explore-count'),more=$('explore-more');
 const sectors=[...new Set(items.map(x=>x.sector))].sort((a,b)=>a.localeCompare(b,'pt-BR'));
 for(const name of sectors){const opt=document.createElement('option');opt.value=name;opt.textContent=name;sector.append(opt);}
 function populateProfessions(){
  const selected=profession.value;
  profession.replaceChildren();
  const all=document.createElement('option');all.value='';all.textContent='Todas as profissões';profession.append(all);
  const names=[...new Set(items.filter(x=>!sector.value||x.sector===sector.value).map(x=>x.profession))].sort((a,b)=>a.localeCompare(b,'pt-BR'));
  for(const name of names){const opt=document.createElement('option');opt.value=name;opt.textContent=name;profession.append(opt);}
  if(names.includes(selected))profession.value=selected;
 }
 let eligible=[],limit=12;
 function refresh(reset=true){
  if(reset)limit=12;
  eligible=items.filter(x=>(!sector.value||x.sector===sector.value)&&(!profession.value||x.profession===profession.value)&&(!strategy.value||x.category===strategy.value));
  // Prefer examples of typical productive work; avoid showing 12 nearly identical cases from one occupation.
  const chosen=[],perProfession=new Map();
  for(const item of eligible){
   const n=perProfession.get(item.profession)||0;
   if(!profession.value&&n>=Math.max(2,Math.ceil(limit/5)))continue;
   perProfession.set(item.profession,n+1);
   chosen.push(item);
   if(chosen.length>=limit)break;
  }
  list.replaceChildren();
  for(const item of chosen){
   const b=document.createElement('button');b.type='button';b.className='explore-item';
   const words=document.createElement('span');const title=document.createElement('strong');title.textContent=item.task;
   const meta=document.createElement('small');meta.textContent=`${item.profession} · ${item.sector}`;
   const arrow=document.createElement('b');arrow.textContent='↗';arrow.setAttribute('aria-hidden','true');
   words.append(title,meta);b.append(words,arrow);
   b.addEventListener('click',()=>{
     window.__selectedTask=item;
     $('task').value=item.task;
     $('charcount').textContent=`${item.task.length} / 700`;
     $('goal').value='auto';
     $('sensitive').checked=false;$('stakes').checked=false;$('prohibited').checked=false;
     $('task-form').requestSubmit();
   });
   list.append(b);
  }
  count.textContent=`${eligible.length.toLocaleString('pt-BR')} tarefa${eligible.length===1?'':'s'} neste filtro · mostrando ${chosen.length.toLocaleString('pt-BR')}`;
  more.hidden=eligible.length<=chosen.length;
 }
 sector.addEventListener('change',()=>{populateProfessions();refresh();});
 profession.addEventListener('change',()=>refresh());
 strategy.addEventListener('change',()=>refresh());
 more.addEventListener('click',()=>{limit+=12;refresh(false);});
 populateProfessions();refresh();
 window.__browseCount=()=>eligible.length;
})();
