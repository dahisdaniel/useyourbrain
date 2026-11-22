import {mkdir, copyFile, readFile, writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
const root=resolve(import.meta.dirname,'..');
const index=await readFile(resolve(root,'index.html'),'utf8');
const data=await readFile(resolve(root,'catalogo-10000.js'),'utf8');
const autocomplete=await readFile(resolve(root,'autocomplete.js'),'utf8');
const explore=await readFile(resolve(root,'explore.js'),'utf8');
const n=(data.match(/"id":"u\d+"/g)||[]).length;
if(n!==10000||!index.includes('classifyWithCatalog')||!index.includes('catalogo-10000.js')||!index.includes('explore.js'))throw new Error(`Build inválido: ${n} registros ou scripts ausentes`);
const dist=resolve(root,'dist');
await mkdir(resolve(dist,'data'),{recursive:true});
// Worker com ativos estáticos: embute busca e dados para impedir falhas de paths.
const embed=(html,source,content)=>{
 const tag=`<script src="${source}"></script>`;
 if(!html.includes(tag))throw new Error(`Script ${source} não foi encontrado`);
 return html.replace(tag,`<script>\n${content}\n</script>`);
};
let bundled=embed(index,'catalogo-10000.js',data);
bundled=embed(bundled,'autocomplete.js',autocomplete);
bundled=embed(bundled,'explore.js',explore);
await writeFile(resolve(dist,'index.html'),bundled,'utf8');
await copyFile(resolve(root,'data/catalogo-10000.csv'),resolve(dist,'data/catalogo-10000.csv'));
await copyFile(resolve(root,'catalogo-10000.js'),resolve(dist,'catalogo-10000.js'));
console.log(`Build: ${n} casos locais; HTML pronto para Cloudflare Worker/Pages`);
