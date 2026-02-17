const logEl = document.getElementById("log");
const btnClear = document.getElementById("btnClear");

function writeLog(msg) {
  const t = new Date().toLocaleTimeString();
  logEl.textContent = `[${t}] ${msg}\n` + logEl.textContent;
}

async function setLed(led, value) {
  try {
    const r = await fetch("/set_led", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ led, value })
    });

    const j = await r.json();
    if (j.ok) writeLog(`${j.cmd} -> ${j.resp}`);
    else writeLog(`ERROR -> ${j.error || j.resp}`);
  } catch (e) {
    writeLog("ERROR -> sin conexión");
  }
}

function setDot(led, value) {
  const d = document.getElementById("d" + led);
  if (!d) return;
  d.style.background = (value > 0) ? "rgba(122,168,255,.95)" : "rgba(255,255,255,.18)";
  d.style.boxShadow = (value > 0) ? "0 0 0 4px rgba(122,168,255,.18)" : "0 0 0 4px rgba(255,255,255,.05)";
}

function bindSlider(sliderId, valueId, led) {
  const s = document.getElementById(sliderId);
  const v = document.getElementById(valueId);

  let timer = null;

  const onMove = () => {
    const val = parseInt(s.value, 10);
    v.textContent = val;
    setDot(led, val);

    if (timer) clearTimeout(timer);
    timer = setTimeout(() => setLed(led, val), 60);
  };

  s.addEventListener("input", onMove);
  onMove();
}

bindSlider("s1", "v1", 1);
bindSlider("s2", "v2", 2);
bindSlider("s3", "v3", 3);
bindSlider("s4", "v4", 4);

if (btnClear) {
  btnClear.addEventListener("click", () => {
    logEl.textContent = "Listo.\n";
  });
}
