// node web/build.js [outfile]  ->  single-file page with core.js inlined (default web/dist/index.html)
const fs = require("fs"), path = require("path");
const out = process.argv[2] || path.join(__dirname, "dist", "index.html");
const core = fs.readFileSync(path.join(__dirname, "core.js"), "utf8");
if (core.includes("</script")) throw new Error("core.js must not contain </script");
const html = fs.readFileSync(path.join(__dirname, "app.template.html"), "utf8").replace("/*CORE*/", () => core);
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, html);
console.log("wrote", out, Math.round(html.length / 1024) + " KB");
