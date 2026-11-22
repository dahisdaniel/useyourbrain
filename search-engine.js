/* Indexação lexical privada: 50 mil cenários, sinônimos PT/EN, sem API remota. */
(()=>{
'use strict';
const entries=Array.isArray(window.ANTES_TASKS)?window.ANTES_TASKS:[];
const normalize=text=>String(text||'').toLocaleLowerCase('pt-BR')
 .normalize('NFD').replace(/[\u0300-\u036f]/g,'')
 .replace(/\be[\s-]?mails?\b/g,' email ').replace(/\bwhats\s?app\b/g,' whatsapp ')
 .replace(/\bgoogle\s+photos\b/g,' google fotos ')
 .replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();
const stop=new Set('a o as os um uma uns umas de da do dos das no na nos nas em para por com que eu voce tu me meu minha meus minhas sua seu sua seus suas nosso nossos quero preciso gostaria vou gostaria como tambem até ate mais menos coisa fazer preciso eu gostaria the a an to for of in on with my your at and or do me please want need i we you be can can i will'.split(' '));
const equiv={
 emails:'email',mails:'email',mail:'email',correo:'email',correio:'email',eletronico:'email',eletronica:'email',
 escrever:'escrever',escrevendo:'escrever',redigir:'escrever',redacao:'escrever',redija:'escrever',compose:'escrever',write:'escrever',writing:'escrever',draft:'escrever',criar:'criar',fazer:'criar',produzir:'criar',montar:'criar',create:'criar',generate:'criar',
 resposta:'responder',respostas:'responder',respondo:'responder',respondendo:'responder',retornar:'responder',responda:'responder',responder:'responder',reply:'responder',answer:'responder',replies:'responder',
 organizar:'organizar',organizando:'organizar',arrumar:'organizar',arrumando:'organizar',ordenar:'organizar',sort:'organizar',sorting:'organizar',organize:'organizar',organise:'organizar',classificacao:'classificar',
 resumir:'resumir',sumarizar:'resumir',sumario:'resumir',resumo:'resumir',summarize:'resumir',summary:'resumir',sumarize:'resumir',sintetizar:'resumir',
 procurar:'buscar',encontrar:'buscar',localizar:'buscar',pesquisar:'buscar',achar:'buscar',busca:'buscar',search:'buscar',find:'buscar',look:'buscar',looking:'buscar',
 fotos:'foto',fotografias:'foto',fotografia:'foto',photos:'foto',photo:'foto',pictures:'foto',picture:'foto',imagem:'foto',imagens:'foto',
 pastas:'pasta',folders:'pasta',folder:'pasta',diretorios:'pasta',diretorio:'pasta',arquivos:'arquivo',files:'arquivo',file:'arquivo',
 documentos:'documento',docs:'documento',document:'documento',pdfs:'pdf',
 inbox:'inbox',caixa:'caixa',entrada:'entrada',
 cientificos:'cientifico',cientificas:'cientifico',cientifica:'cientifico',papers:'artigo',paper:'artigo',artigos:'artigo',
 estudos:'estudo',literatura:'literatura',bibliografica:'bibliografia',bibliografico:'bibliografia',
 tesis:'tese',thesis:'tese',dissertation:'tese',dissertacao:'tese',
 medicos:'medico',medical:'medico',clinica:'clinico',clinical:'clinico',clinicas:'clinico',pacientes:'paciente',patients:'paciente',
 aprender:'aprender',estudar:'aprender',estudos:'estudo',learning:'aprender',learn:'aprender',study:'aprender',
 planilhas:'planilha',spreadsheets:'planilha',spreadsheet:'planilha',excel:'excel',
 organizacao:'organizar',pessoal:'pessoal',pessoais:'pessoal',
 reunioes:'reuniao',meetings:'reuniao',meeting:'reuniao',
 pagamentos:'pagamento',contas:'conta',faturas:'fatura',
 scripts:'script',codes:'codigo',coding:'codigo',code:'codigo',programar:'codigo',
 relatos:'relato',relatorios:'relatorio',contratos:'contrato',
 traduzir:'traduzir',translate:'traduzir',translation:'traduzir',
 corrigir:'corrigir',correcao:'corrigir',revisar:'revisar',review:'revisar',
 duplicadas:'duplicado',duplicados:'duplicado',duplicates:'duplicado',
 mensagens:'mensagem',mensajes:'mensagem',messages:'mensagem',message:'mensagem',
 google:'google',gmail:'gmail',outlook:'outlook',drive:'drive',icloud:'icloud',whatsapp:'whatsapp',
 paperwriting:'tese'
};
function toks(s){return [...new Set(normalize(s).split(' ').filter(w=>w.length>1&&!stop.has(w)).map(w=>equiv[w]||w))];}
let docs,posting,vocabulary,df;
function prepare(){
 if(docs)return;
 const local=[];const map=new Map();const freq=new Map();
 for(let i=0;i<entries.length;i++){
  const row=entries[i];
  const terms=new Set(toks(row.task));
  const aliasTexts=(row.aliases||[]).map(normalize);
  const aliasSet=new Set(aliasTexts.flatMap(toks));
  const metadata=new Set(toks(`${row.profession} ${row.sector}`));
  const all=new Set([...terms,...aliasSet,...metadata]);
  const item={row,normal:normalize(row.task),aliasTexts,terms,aliasSet,metadata,wordCount:terms.size};
  local.push(item);
  for(const w of all){let ids=map.get(w);if(!ids){ids=[];map.set(w,ids);}ids.push(i);freq.set(w,(freq.get(w)||0)+1);}
 }
 docs=local;posting=map;df=freq;vocabulary=[...map.keys()];
}
function search(query,limit=6,preferred=null){
 if(normalize(query).length<2)return [];
 prepare();
 let q=toks(query);if(!q.length)return [];
 if(q.length>20)q=q.slice(0,20);
 const queryNorm=normalize(query);
 const ids=new Set();const resolved=[];
 for(const term of q){
  const candidates=[];
  if(posting.has(term))candidates.push([term,1]);
  // partial typing, including profession names, with bounded vocabulary expansion
  if(term.length>=3){
   let count=0;
   for(const word of vocabulary){
    if(word!==term&&word.startsWith(term)){candidates.push([word,.72]);if(++count===24)break;}
   }
  }
  resolved.push(candidates);
  for(const [word] of candidates)for(const id of posting.get(word)||[])ids.add(id);
 }
 if(!ids.size)return [];
 const weights=q.map(term=>Math.log(2+entries.length/(1+(df.get(term)||2))));
 const denominator=weights.reduce((a,b)=>a+b,0)||1;
 const ranked=[];
 for(const id of ids){
  const d=docs[id];if(preferred&&d.row.category!==preferred)continue;
  let score=0,hits=0,taskhits=0;
  for(let j=0;j<q.length;j++){
   let mx=0;
   for(const [term,quality] of resolved[j]){
    if(d.terms.has(term))mx=Math.max(mx,quality);
    else if(d.aliasSet.has(term))mx=Math.max(mx,quality*.96);
    else if(d.metadata.has(term))mx=Math.max(mx,quality*.24);
   }
   if(mx){score+=weights[j]*mx;hits++;if(mx>=.70)taskhits++;}
  }
  if(!hits)continue;
  score=score/denominator;
  if(hits===q.length)score+=.11;
  // Prefer the exact action/object rather than 10-context generic work scenarios.
  score+=Math.min(.18,.18/(1+d.wordCount/6));
  if(d.normal.startsWith(queryNorm))score+=.23;
  else if(d.normal.includes(queryNorm))score+=.12;
  if(d.normal===queryNorm)score+=1.6;
  if(d.aliasTexts.includes(queryNorm))score+=1.55;
  if(d.row.priority==='essencial')score+=.25;
  if(q.length>1&&taskhits===1)score-=.12;
  if(score<.22)continue;
  ranked.push({row:d.row,score,action:toks(d.row.task)[0]||''});
 }
 ranked.sort((a,b)=>b.score-a.score||a.row.task.length-b.row.task.length);
 const output=[];const perAction=new Map(),perProfession=new Map();
 for(const hit of ranked){
  const verb=hit.action,prof=hit.row.profession;
  if(perAction.get(verb)>=2&&limit<=10)continue;
  if(perProfession.get(prof)>=4&&limit<=10)continue;
  perAction.set(verb,(perAction.get(verb)||0)+1);perProfession.set(prof,(perProfession.get(prof)||0)+1);
  output.push({...hit.row,score:Math.min(1,hit.score/1.3)});
  if(output.length>=limit)break;
 }
 // For exact sentence, ensure the closest match isn't suppressed by diversity.
 return output;
}
window.UYB_SEARCH={normalize,tokens:toks,search,nearest:(query,preferred)=>search(query,1,preferred)[0]||null,ready:()=>Boolean(docs),count:()=>entries.length};
if(typeof requestIdleCallback==='function')requestIdleCallback(()=>prepare(),{timeout:2000});
else setTimeout(prepare,300);
})();