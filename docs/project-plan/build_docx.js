// Build the Project Plan .docx from docs/project-plan/project_plan.md (simple markdown subset).
// Usage: npm install docx && node build_docx.js project_plan.md Project_Plan.docx  (then: soffice --headless --convert-to pdf Project_Plan.docx)
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  AlignmentType, WidthType, ShadingType, BorderStyle, LevelFormat, HeadingLevel,
  Footer, PageNumber, TableLayoutType,
} = require("docx");

const MD = process.argv[2];
const OUT = process.argv[3];
const mdDir = path.dirname(MD);
const lines = fs.readFileSync(MD, "utf8").split("\n");

const FONT = "Calibri";
const BODY = 21;   // half-points (10.5 pt)
const SMALL = 17;  // 8.5 pt for tables
const PAGE_W = 11906, PAGE_H = 16838, MARGIN = 1080; // A4, 0.75"
const CONTENT_W = PAGE_W - 2 * MARGIN;

// Inline markdown: **bold**, *italic*, \* escapes.
function runs(text, base = {}) {
  const out = [];
  text = text.replace(/\\\*/g, "\u0000");
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  const push = (s, o) => { if (s) out.push(new TextRun({ text: s.replace(/\u0000/g, "*"), font: FONT, size: BODY, ...base, ...o })); };
  while ((m = re.exec(text))) {
    push(text.slice(last, m.index), {});
    const tok = m[0];
    if (tok.startsWith("**")) push(tok.slice(2, -2), { bold: true });
    else push(tok.slice(1, -1), { italics: true });
    last = m.index + tok.length;
  }
  push(text.slice(last), {});
  return out;
}

function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20), data: b };
}

const children = [];
let i = 0;
let inRefs = false;
const border = { style: BorderStyle.SINGLE, size: 4, color: "A6A6A6" };
const cellBorders = { top: border, bottom: border, left: border, right: border };

function tableFrom(rows) {
  const header = rows[0];
  const body = rows.slice(2); // skip |---|
  const n = header.length;
  // column widths: proportional to max text length, clamped
  const lens = header.map((_, c) => Math.max(...[header, ...body].map(r => (r[c] || "").length)));
  const preset = { "Part": [15, 12, 45, 28], "Week": [7, 15, 60, 18], "Member": [9, 61, 30] }[header[0].trim()];
  const weights = preset || lens.map(l => Math.min(Math.max(l, 6), 90));
  const sum = weights.reduce((a, b) => a + b, 0);
  let widths = weights.map(w => Math.floor(CONTENT_W * w / sum));
  widths[n - 1] += CONTENT_W - widths.reduce((a, b) => a + b, 0);
  const mkRow = (cells, isHeader) => new TableRow({
    tableHeader: isHeader,
    children: cells.map((txt, c) => new TableCell({
      width: { size: widths[c], type: WidthType.DXA },
      borders: cellBorders,
      shading: isHeader ? { fill: "E7EEF7", type: ShadingType.CLEAR, color: "auto" } : undefined,
      margins: { top: 40, bottom: 40, left: 80, right: 80 },
      children: [new Paragraph({ spacing: { before: 0, after: 0, line: 240 }, children: runs(txt.trim(), { size: SMALL, bold: isHeader || undefined }) })],
    })),
  });
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: widths,
    layout: TableLayoutType.FIXED,
    rows: [mkRow(header, true), ...body.map(r => mkRow(r, false))],
  });
}

while (i < lines.length) {
  const line = lines[i];
  if (!line.trim()) { i++; continue; }

  if (line.startsWith("# ")) {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [new TextRun({ text: line.slice(2), bold: true, font: FONT, size: 30 })] }));
    i++; continue;
  }
  if (line.startsWith("COMP1110")) {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      children: [new TextRun({ text: line, font: FONT, size: BODY, color: "404040" })] }));
    i++; continue;
  }
  if (line.startsWith("## ")) {
    inRefs = line.includes("References");
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 200, after: 80 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "1F4E79", space: 2 } },
      children: [new TextRun({ text: line.slice(3), bold: true, font: FONT, size: 25, color: "1F4E79" })] }));
    i++; continue;
  }
  if (line.startsWith("> ")) {
    children.push(new Paragraph({ indent: { left: 400, right: 400 }, spacing: { before: 60, after: 60 },
      shading: { fill: "F2F2F2", type: ShadingType.CLEAR, color: "auto" },
      border: { left: { style: BorderStyle.SINGLE, size: 18, color: "1F4E79", space: 8 } },
      children: runs(line.slice(2), { size: 22 }) }));
    i++; continue;
  }
  if (line.startsWith("|")) {
    const rows = [];
    while (i < lines.length && lines[i].startsWith("|")) {
      rows.push(lines[i].trim().replace(/^\||\|$/g, "").split("|"));
      i++;
    }
    children.push(tableFrom(rows));
    children.push(new Paragraph({ spacing: { after: 40 }, children: [] }));
    continue;
  }
  if (line.startsWith("- ")) {
    children.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 40, line: 252 },
      children: runs(line.slice(2)) }));
    i++; continue;
  }
  const img = line.match(/^!\[.*\]\((.*)\)$/);
  if (img) {
    const file = path.resolve(mdDir, img[1]);
    const { w, h, data } = pngSize(file);
    const width = 500;
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60, after: 0 },
      children: [new ImageRun({ type: "png", data, transformation: { width, height: Math.round(width * h / w) } })] }));
    i++; continue;
  }
  if (inRefs) {
    children.push(new Paragraph({ indent: { left: 360, hanging: 360 }, spacing: { after: 50, line: 240 },
      children: runs(line, { size: 19 }) }));
    i++; continue;
  }
  const isCaption = line.startsWith("*Figure");
  children.push(new Paragraph({ alignment: isCaption ? AlignmentType.CENTER : AlignmentType.JUSTIFIED,
    spacing: { after: isCaption ? 100 : 80, line: 252 },
    children: runs(line, isCaption ? { size: 18 } : {}) }));
  i++;
}

const doc = new Document({
  creator: "COMP1110 Group",
  title: "Project Plan",
  styles: { default: { document: { run: { font: FONT, size: BODY } } } },
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•",
    alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18, color: "808080" })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log("wrote", OUT); });
