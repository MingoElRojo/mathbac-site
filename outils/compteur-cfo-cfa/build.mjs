/* Construit les trois cibles depuis src/app.src.html :
   - outils/compteur-cfo-cfa/index.html  : scripts pdf.js en fichiers séparés (site)
   - dist/compteur-legendes-cfo-cfa.html : fichier unique, tout embarqué (e-mail, clé USB)
   - .../build/artifact.html             : corps seul, tout embarqué (page publiée)
   Usage : node outils/compteur-cfo-cfa/build.mjs            */
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(import.meta.dirname, "../..");
const HERE = path.join(ROOT, "outils/compteur-cfo-cfa");
const TOKEN = "<!--PDFJS_LOADER-->";

const src = fs.readFileSync(path.join(HERE, "src/app.src.html"), "utf8");
if (!src.includes(TOKEN)) throw new Error("Jeton " + TOKEN + " absent de la source");

const cut = src.indexOf("</style>") + "</style>".length;
const head = src.slice(0, cut).trim();
const body = src.slice(cut).trim();

const pdfMain = fs.readFileSync(path.join(HERE, "vendor/pdf.min.js"), "utf8");
const pdfWork = fs.readFileSync(path.join(HERE, "vendor/pdf.worker.min.js"), "utf8");

/* `</script` dans du code embarqué fermerait la balise : on le neutralise. */
const safe = (s) => s.replace(/<\/script/gi, "<\\/script");
const S = "scr" + "ipt";

const loaderInline =
  `<${S}>` + safe(pdfMain) + `</${S}>\n` +
  `<${S}>window.__PDFJS_WORKER_TEXT=` + safe(JSON.stringify(pdfWork)) + `;</${S}>`;

const loaderVendor =
  `<${S} src="./vendor/pdf.min.js"></${S}>\n` +
  `<${S}>window.__PDFJS_WORKER_SRC="./vendor/pdf.worker.min.js";</${S}>`;

const DESC = "Compter les occurrences des symboles et libellés d'une légende sur un plan PDF " +
             "CFO / CFA, puis exporter en CSV ou en DXF AutoCAD. Tout le traitement reste sur le poste.";

function fullDoc(bodyHtml) {
  return `<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="${DESC}">
<style>
:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
html,body{margin:0}
body{font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;background:#f7f7f6}
img{max-width:100%}
[hidden]{display:none!important}
</style>
${head}
</head>
<body>
${bodyHtml}
</body>
</html>
`;
}

const targets = [
  ["outils/compteur-cfo-cfa/index.html", fullDoc(body.replace(TOKEN, loaderVendor))],
  ["dist/compteur-legendes-cfo-cfa.html", fullDoc(body.replace(TOKEN, loaderInline))],
  ["outils/compteur-cfo-cfa/build/artifact.html", head + "\n" + body.replace(TOKEN, loaderInline) + "\n"],
];

for (const [rel, text] of targets) {
  const out = path.join(ROOT, rel);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, text);
  console.log(String(Math.round(text.length / 1024)).padStart(6) + " ko  " + rel);
}
