import { mkdir, copyFile, readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
const root = resolve(import.meta.dirname, '..');
const index = await readFile(resolve(root, 'index.html'), 'utf8');
const data = await readFile(resolve(root, 'catalogo-3000.js'), 'utf8');
const autocomplete = await readFile(resolve(root, 'autocomplete.js'), 'utf8');
const n = (data.match(/"id":/g) || []).length;
if (n !== 3000 || !index.includes('classifyWithCatalog') || !index.includes('autocomplete.js')) {
  throw new Error(`Build invalido: ${n} casos ou algoritmo ausente`);
}
await mkdir(resolve(root, 'dist'), { recursive: true });
// Embutir o catálogo no HTML gerado evita erro de caminho/bloqueio do arquivo no Worker.
const bundled = index
  .replace('<script src="catalogo-3000.js"></script>', `<script>\n${data}\n</script>`)
  .replace('<script src="autocomplete.js"></script>', `<script>\n${autocomplete}\n</script>`);
if (bundled === index || bundled.includes('src="catalogo-3000.js"') || bundled.includes('src="autocomplete.js"')) {
  throw new Error('Nao foi possivel embutir os scripts de busca no HTML');
}
await writeFile(resolve(root, 'dist/index.html'), bundled, 'utf8');
await copyFile(resolve(root, 'catalogo-3000.js'), resolve(root, 'dist/catalogo-3000.js'));
await copyFile(resolve(root, 'autocomplete.js'), resolve(root, 'dist/autocomplete.js'));
console.log('Build concluído: dist/ contém o site estático e 3.000 tarefas.');