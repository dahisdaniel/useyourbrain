import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {runInNewContext,Script} from 'node:vm';
const base=new URL('../',import.meta.url);
const read=async path=>readFile(new URL(path,base),'utf8');
const [html,studiesPage,studiesData,studiesUI,localization,autocomplete,build]=await Promise.all([
  read('index.html'),read('estudos.html'),read('studies-data.js'),read('studies-ui.js'),
  read('localization.js'),read('autocomplete.js'),read('scripts/build.mjs')
]);
for(const [name,source] of [['main script',html.match(/<script>\s*([\s\S]*?)<\/script>/)?.[1]||''],['studies data',studiesData],['studies UI',studiesUI],['localization',localization],['autocomplete',autocomplete]]) {
  assert.ok(source.length>0,name+' missing');
  assert.doesNotThrow(()=>new Script(source,{filename:name}),name+' has JS syntax error');
}
const context={window:{}};
runInNewContext(studiesData,context);
const items=context.window.UYB_STUDIES;
assert.equal(items.length,24,'Expected 24 curated references');
assert.equal(new Set(items.map(x=>x.id)).size,24);
for(const p of items){
  assert.ok(/^https:\/\/(doi\.org\/|www\.)/.test(p.url),p.id+' link');
  assert.ok(p.method.pt && p.method.en && p.findings.pt && p.findings.en && p.limitations.pt && p.limitations.en && p.application.pt && p.application.en,p.id+' translation');
  assert.ok(p.topic && p.year>=2000 && p.year<=2026,p.id+' metadata');
}
assert.ok(items.some(x=>x.topic==='critical'));
assert.ok(items.some(x=>x.topic==='memory'));
assert.ok(items.some(x=>x.topic==='language'));
assert.ok(items.some(x=>x.topic==='creativity'));
assert.ok(items.some(x=>x.topic==='productivity'));
assert.ok(studiesPage.includes('id="library"')&&studiesPage.includes('/studies-ui.js'));
assert.ok(html.includes('Devo usar IA ou não?') && localization.includes('Should I use IA or not?'));
assert.ok(html.includes('id="nav-studies"') && html.includes('id="lang-en"'));
assert.ok(html.includes('localizeResult({task,analysisTask,result,policy,assessment,evid,hybrid})'));
assert.ok(build.includes("'estudos.html'") && build.includes("'studies-data.js'") && build.includes("'localization.js'"));
assert.ok(!localization.includes('fetch(') && !studiesUI.includes('fetch('));
function localeContext(search){
  const nodes=new Map();
  const makeNode=()=>({textContent:'',innerHTML:'',href:'',content:'',placeholder:'',classList:{toggle(){},add(){},remove(){}},setAttribute(){},lastChild:{nodeType:0}});
  const doc={
    documentElement:{lang:'pt-BR'},
    title:'',
    querySelector:()=>makeNode(),
    querySelectorAll:()=>[],
    getElementById(id){if(!nodes.has(id))nodes.set(id,makeNode());return nodes.get(id)}
  };
  const w={UYB_SEARCH:{search(q){return []}},UYB_STUDIES:items};
  runInNewContext(localization,{window:w,document:doc,location:{search},URLSearchParams});
  return {w,doc};
}
const english=localeContext('?lang=en');
assert.equal(english.w.UYB_L10N.lang,'en');
assert.equal(english.doc.documentElement.lang,'en');
assert.match(english.w.UYB_L10N.forAnalysis('Write an email'),/e-mail/);
assert.match(english.w.UYB_L10N.forAnalysis('Learn Python'),/programar/i);
assert.match(english.w.UYB_L10N.forAnalysis('Summarize a scientific paper and its limitations'),/limita/i);
const pt=localeContext('?lang=pt');
assert.equal(pt.w.UYB_L10N.lang,'pt');
assert.equal(pt.w.UYB_L10N.forAnalysis('Escrever um e-mail'),'Escrever um e-mail');
console.log('Bilingual UI and 24 study records: PT/EN, routes, links, source fields and syntax OK.');
