from Grabber import api
from fastapi.responses import HTMLResponse

@api.get("/eval", response_class=HTMLResponse)
async def hime():
    html_body = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hime • Telegram JS Playground</title>
<style>
  :root{--bg:#0b1020;--panel:#101828;--card:#0f1626;--muted:#9aa4b2;--fg:#e6f0ff}
  *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--fg);font-family:ui-sans-serif,system-ui,Segoe UI,Roboto,Ubuntu,Arial}
  .wrap{max-width:1100px;margin:0 auto;padding:18px}
  header{display:flex;gap:12px;align-items:center;justify-content:space-between;margin-bottom:12px}
  .title{font-weight:700;font-size:18px}
  .tg-badge{background:#1a2338;border:1px solid #223053;padding:6px 10px;border-radius:10px;color:var(--muted)}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  .card{background:var(--card);border:1px solid #1c2742;border-radius:14px;overflow:hidden}
  .card h3{margin:0;padding:10px 12px;border-bottom:1px solid #1c2742;font-size:14px;color:#b7c3d7}
  #editor{width:100%;min-height:320px;resize:vertical;padding:12px;background:#0a1222;color:#eafffb;border:none;outline:none;font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;border-bottom-left-radius:14px;border-bottom-right-radius:14px}
  .toolbar{display:flex;gap:8px;padding:10px;border-bottom:1px solid #1c2742;background:#0f1626}
  button{cursor:pointer;border:none;border-radius:10px;padding:8px 12px;background:#1b63ff;color:white;font-weight:600}
  button:disabled{opacity:.6;cursor:not-allowed}
  #console{height:340px;overflow:auto;background:#070d1a;padding:10px;font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
  .log{white-space:pre-wrap;word-wrap:break-word;margin:0 0 8px}
  .log.info{color:#d9f99d} .log.warn{color:#fde68a} .log.error{color:#fecaca}
  .pill{display:inline-flex;gap:6px;align-items:center;background:#12203a;border:1px solid #1d2b48;color:#bcd0ff;padding:6px 10px;border-radius:999px;font-size:12px}
  .row{display:flex;gap:10px;flex-wrap:wrap;padding:10px}
  .mono{font:12px/1.4 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:#c7e0ff}
</style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="title">Hime — Telegram JS Playground</div>
      <div id="tg-status" class="tg-badge">Detecting Telegram WebApp…</div>
    </header>

    <div class="grid">
      <!-- Editor -->
      <div class="card">
        <h3>Editor</h3>
        <div class="toolbar">
          <button id="runBtn">Run ▶</button>
          <button id="clearBtn">Clear Console</button>
          <button id="sampleBtn">Load Sample</button>
        </div>
        <textarea id="editor" spellcheck="false">// You can use:
//  - tg  → window.Telegram.WebApp (if available)
//  - $, $$ → query helpers
//  - http(url, opts) → fetch helper (returns text)
//  - print(...args) → console + on-screen log
// Examples:

print("Hello from Hime!");
print("tg available?", !!tg);

if (tg) {
  tg.ready();
  print("user id:", tg.initDataUnsafe?.user?.id);
  print("initData:", tg.initData?.slice(0,120) + "...");
  tg.HapticFeedback?.impactOccurred?.("soft");
}

// Try Telegram UI buttons
// if (tg?.MainButton) { tg.MainButton.setText("Click Me"); tg.MainButton.show(); tg.onEvent("mainButtonClicked", ()=>print("MainButton clicked")); }
</textarea>
      </div>

      <!-- Console + Info -->
      <div class="card">
        <h3>Console</h3>
        <div id="console"></div>
        <div class="row">
          <div class="pill"><span>initData</span><span id="init-len" class="mono">—</span></div>
          <div class="pill"><span>User</span><span id="user-id" class="mono">—</span></div>
          <div class="pill"><span>Platform</span><span id="platform" class="mono">—</span></div>
        </div>
      </div>
    </div>
  </div>

<script>
(function(){
  // --- Console mirror ---
  const con = document.getElementById('console');
  function push(type, args){
    const el = document.createElement('div'); el.className = 'log ' + type;
    try { el.textContent = args.map(a => {
      if (typeof a === 'string') return a;
      return JSON.stringify(a, null, 2);
    }).join(' ');
    } catch(e){ el.textContent = args.join(' '); }
    con.appendChild(el); con.scrollTop = con.scrollHeight;
  }
  const orig = { log: console.log, warn: console.warn, error: console.error };
  console.log = (...a)=>{ orig.log(...a); push('info', a); };
  console.warn = (...a)=>{ orig.warn(...a); push('warn', a); };
  console.error = (...a)=>{ orig.error(...a); push('error', a); };

  // --- Helpers available to user code ---
  const $ = (sel, root=document)=>root.querySelector(sel);
  const $$ = (sel, root=document)=>Array.from(root.querySelectorAll(sel));
  async function http(url, opts){ const r = await fetch(url, opts); return r.text(); }
  function print(...args){ console.log(...args); }

  // --- Telegram detection ---
  const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;
  const badge = document.getElementById('tg-status');
  const initLen = document.getElementById('init-len');
  const userId = document.getElementById('user-id');
  const platform = document.getElementById('platform');

  if (tg) {
    try { tg.ready(); } catch(_) {}
    badge.textContent = "Telegram WebApp detected ✅";
    initLen.textContent = (tg.initData || '').length + " chars";
    userId.textContent = tg.initDataUnsafe?.user?.id ?? "—";
    platform.textContent = tg.platform ?? "—";
  } else {
    badge.textContent = "Telegram WebApp not found ❌ (open inside Telegram)";
    initLen.textContent = "—";
    userId.textContent = "—";
    platform.textContent = navigator.userAgent;
  }

  // --- Run button: execute user code with tg in scope ---
  const runBtn = document.getElementById('runBtn');
  const clearBtn = document.getElementById('clearBtn');
  const sampleBtn = document.getElementById('sampleBtn');
  const editor = document.getElementById('editor');

  runBtn.addEventListener('click', ()=>{
    try {
      // new Function gets helpers + tg
      const fn = new Function('tg','$','$$','http','print', editor.value);
      Promise.resolve(fn(tg,$,$$,http,print)).catch(e=>console.error(e));
    } catch(e) { console.error(e); }
  });

  clearBtn.addEventListener('click', ()=>{ con.innerHTML=''; });
  sampleBtn.addEventListener('click', ()=>{
    editor.value = `print("Hime sample running…");
print("tg available?", !!tg);
if (tg){ tg.ready(); print("user:", tg.initDataUnsafe?.user); }
const txt = await http("https://httpbin.org/get");
print("http result (first 120):", txt.slice(0,120)+"…");`;
  });
})();
</script>
</body>
</html>"""
    return HTMLResponse(content=html_body, status_code=200)

