import { mkdir, copyFile, readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
const root = resolve(import.meta.dirname, '..');
const index = await readFile(resolve(root, 'index.html'), 'utf8');
const data = await readFile(resolve(root, 'catalogo-3000.js'), 'utf8');
const n = (data.match(/"id":/g) || []).length;
if (n !== 3000 || !index.includes('classifyWithCatalog')) {
  throw new Error(`Build invalido: ${n} casos ou algoritmo ausente`);
}
await mkdir(resolve(root, 'dist'), { recursive: true });
await copyFile(resolve(root, 'index.html'), resolve(root, 'dist/index.html'));
await copyFile(resolve(root, 'catalogo-3000.js'), resolve(root, 'dist/catalogo-3000.js'));
console.log('Build concluído: dist/ contém o site estático e 3.000 tarefas.');