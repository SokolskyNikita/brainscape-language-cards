import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';

const root = path.dirname(new URL(import.meta.url).pathname);
const plan = JSON.parse(await fs.readFile(path.join(root, 'xlsx_plan.json'), 'utf8'));
// Historical plans store absolute paths; use the deck filename in this checkout.
for (const job of plan) {
  const pack = path.basename(path.dirname(job.path));
  assert.ok(['spanish_english_fixed', 'english_spanish_fixed'].includes(pack));
  job.path = path.join(root, '..', pack, path.basename(job.path));
}
const mode = process.argv[2] || 'inspect';
const out = path.join(root, 'xlsx_updated');
const previews = path.join(root, 'xlsx_previews');
await fs.mkdir(previews, { recursive: true });
await fs.mkdir(out, { recursive: true });
for (const job of plan) {
  const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(job.path));
  const sheet = wb.worksheets.getItem(job.sheet);
  if (mode === 'help') {
    console.log(wb.help('workbook.render', { include: 'index,examples,notes', maxChars: 5000 }).ndjson);
    break;
  }
  const r = job.updates[0].row;
  const view = `A${Math.max(1,r-1)}:B${r+1}`;
  if (mode === 'inspect') {
    console.log(JSON.stringify({deckId: job.deckId, inspection: await wb.inspect({kind:'region', sheetId:job.sheet, range:view, maxChars:1200})}));
    const preview = await wb.render({sheetName:job.sheet, range:view, scale:1.3, format:'png'});
    await fs.writeFile(path.join(previews, `before_${job.deckId}.png`), new Uint8Array(await preview.arrayBuffer()));
    continue;
  }
  assert.equal(mode, 'edit');
  for (const change of job.updates) {
    const cell = sheet.getCell(change.row-1, change.col-1);
    assert.equal(cell.values[0][0], change.before);
    cell.values = [[change.after]];
  }
  wb.recalculate();
  for (const change of job.updates) assert.equal(sheet.getCell(change.row-1,change.col-1).values[0][0], change.after);
  console.log(JSON.stringify({deckId: job.deckId, updatedCells:job.updates.length, inspection:await wb.inspect({kind:'region',sheetId:job.sheet,range:view,maxChars:1000})}));
  const preview = await wb.render({sheetName:job.sheet,range:view,scale:1.3,format:'png'});
  await fs.writeFile(path.join(previews, `after_${job.deckId}.png`), new Uint8Array(await preview.arrayBuffer()));
  const exported = await SpreadsheetFile.exportXlsx(wb);
  await exported.save(path.join(out, path.basename(job.path)));
}
