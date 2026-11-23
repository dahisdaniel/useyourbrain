import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {runInNewContext} from 'node:vm';

const base = new URL('../', import.meta.url);
const policySource = await readFile(new URL('cognitive-policy.js',base),'utf8');
const html = await readFile(new URL('index.html',base),'utf8');
const build = await readFile(new URL('scripts/build.mjs',base),'utf8');
const context = {window:{}};
runInNewContext(policySource,context,{filename:'cognitive-policy.js'});
const assess = context.window.UYB_COGNITION.assess;
const checks = [
  ['Escrever um e-mail profissional','routine','linguistic'],
  ['Responder um e-mail para um colega','routine','linguistic'],
  ['Responder 500 emails de confirmação automática','routine','routine'],
  ['Revisar um texto que já escrevi','routine','review'],
  ['Preparar uma apresentação oral','routine','spoken'],
  ['Falar em público sobre meu projeto','routine','spoken'],
  ['Resumir um e-mail recebido','routine','summary'],
  ['Organizar meus arquivos de trabalho','routine','routine'],
  ['Organizar fotos do Google Fotos','routine','routine'],
  ['Transcrever gravação de reunião','routine','routine'],
  ['Aprender inglês','learn','learn_language'],
  ['Aprender espanhol','learn','learn_language'],
  ['Aprender a programar','learn','learn_code'],
  ['Aprender Python','learn','learn_code'],
  ['Aprender a tocar piano','learn','learn_any'],
  ['Aprender a escrever e-mails','learn','learn_any'],
  ['Escrever minha tese de doutorado','authorship','authored'],
  ['Criar um roteiro original','creative','creative'],
  ['Criar hipóteses originais','creative','creative'],
  ['Interpretar resultados de um estudo','routine','critical'],
  ['Comparar dados de um experimento','routine','critical'],
  ['Avaliar a originalidade de um artigo','routine','critical'],
  ['Resumir artigo científico apontando limitações','routine','critical'],
  ['Debater argumentos em um estudo','routine','critical'],
  ['Diagnosticar um paciente','highrisk','highstakes'],
  ['Tomar uma decisão de alto risco','highrisk','highstakes'],
  ['Analisar prontuário confidencial','sensitive','restricted'],
  ['Fazer uma prova que proíbe IA','noai','restricted']
];
for (const [task, category, expected] of checks) {
  const result = assess(task,{category,uncertain:false});
  assert.equal(result.mode,expected,task+': '+result.mode+' vs '+expected);
  assert.ok(result.keep?.length>15 && result.delegate?.length>15 && result.check?.length>15);
  assert.ok(result.domains?.length>0);
}
const authored = assess('Escrever minha tese',{category:'authorship'});
assert.ok(authored.domains.includes('Pensamento crítico'));
assert.ok(authored.domains.includes('Linguagem'));
const writing = assess('Escrever um e-mail',{category:'routine'});
assert.match(writing.evidence.grade,/produtividade.*preservar/i);
const personal = assess('Escrever carta pessoal',{category:'personal'});
assert.equal(personal.evidence,null);
const prohibit = assess('Fazer prova sem IA',{category:'noai'});
assert.match(prohibit.title,/não use IA/i);
assert.ok(html.includes('<script src="cognitive-policy.js"></script>'));
assert.ok(build.includes("'cognitive-policy.js'"));
for(const id of ['cognitive-focus','cognitive-delegate','cognitive-check'])assert.ok(html.includes('id="'+id+'"'));
assert.ok(!html.includes('Não é uma medida de QI'));
console.log('Cognitive policy: '+checks.length+' task cases + safety, evidence and UI checks passed.');
