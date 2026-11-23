import {readFile,copyFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
const root=resolve(import.meta.dirname,'..');
const files=['index.html','estudos.html','favicon.svg','catalogo-loader.js','search-engine.js','autocomplete.js','evidence-strength.js','hybrid-guidance.js','cognitive-policy.js','studies-data.js','studies-ui.js','localization.js'];
const html=await readFile(resolve(root,'index.html'),'utf8');
if(!html.includes('classifyWithCatalog')||!html.includes('50.000')||!html.includes('EVIDENCE_PROFILES')||!html.includes('<script src="evidence-strength.js"></script>')||!html.includes('<script src="hybrid-guidance.js"></script>')||!html.includes('<script src="cognitive-policy.js"></script>')||!html.includes('/localization.js')||!html.includes('Devo usar IA ou não?')||!html.includes('/estudos.html'))throw Error('Estrutura principal ou suporte PT/EN ausente');
const library=await readFile(resolve(root,'estudos.html'),'utf8');
const studies=await readFile(resolve(root,'studies-data.js'),'utf8');
if(!library.includes('id="library"')||!library.includes('/studies-ui.js')||!studies.includes('window.UYB_STUDIES'))throw Error('Biblioteca de pesquisas ausente');
const shards=Array.from({length:10},(_,i)=>`catalogo/parte-${String(i).padStart(2,'0')}.js`);
let count=0;
const packed=[];
for(const [i,shard] of shards.entries()){
 const data=await readFile(resolve(root,shard),'utf8');
 const n=(data.match(/\["c\d{5}",/g)||[]).length;
 if(n!==5000)throw Error(`${shard}: registros ${n} (esperado 5000)`);
 const match=data.match(/window\.UYB_PACKED\.push\(\.\.\.(\[[\s\S]*\])\);/);
 if(!match)throw Error('Não foi possível extrair '+shard);
 packed.push(...JSON.parse(match[1]));
 count+=n;
 if(!html.includes(`<script src="${shard}"></script>`))throw Error(`Script ${shard} sem referência`);
}
if(count!==50000)throw Error(`Número inválido: ${count}`);
const dist=resolve(root,'dist');
await mkdir(resolve(dist,'data'),{recursive:true});
await mkdir(resolve(dist,'catalogo'),{recursive:true});
await Promise.all([...files,...shards].map(p=>copyFile(resolve(root,p),resolve(dist,p))));
const catalogLoader=await readFile(resolve(root,'catalogo-loader.js'),'utf8');
const dictMatch=catalogLoader.match(/window\.UYB_DICTIONARIES=(\{[^;]*\});/);
if(!dictMatch)throw Error('Dicionário de profissões não encontrado');
const d=JSON.parse(dictMatch[1]);
const csvFields=['id','task','category','profession','sector','sourceGroup','intent','priority','aliases'];
const escape=value=>{const text=String(value??'');return /[\r\n,\"]/.test(text)?'\"'+text.replace(/\"/g,'\"\"')+'\"':text;};
const csv=[csvFields.join(',')];
for(const r of packed){csv.push([r[0],r[1],d.categories[r[2]],d.professions[r[3]],d.sectors[r[4]],d.sources[r[5]],d.intents[r[6]],r[7]?'essencial':'contextual',(r[8]||[]).join(' | ')].map(escape).join(','));}
await writeFile(resolve(dist,'data/catalogo-50000.csv'),'\uFEFF'+csv.join('\n')+'\n','utf8');
await writeFile(resolve(dist,'_headers'),'/catalogo/*\n  Cache-Control: public, max-age=86400\n', 'utf8');
console.log(`Build concluído: ${count} situações, 10 arquivos locais; sem API de IA.`);