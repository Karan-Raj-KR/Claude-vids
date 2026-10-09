"""Writes compositions/<section>.html for the 20 s reel (16:9 originals).
Then run tools/make_vertical.py for the 9:16 copies."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def scene(sid, markup, js, css=""):
    html = f'''<!doctype html>
<html><head><meta charset="UTF-8" /></head>
<body>
<template>
<style>
  #{sid}-root {{ position: absolute; inset: 0; }}
{css}
</style>
<div id="{sid}-root" data-composition-id="{sid}" data-width="1920" data-height="1080">
  <div class="r-stage" id="{sid}-stage"><div class="r-rig" id="{sid}-rig">
{markup}
  </div><div class="r-flash" id="{sid}-flash"></div></div>
</div>
<script>
R.ready().then(() => R.fitAllAsync(document.getElementById("{sid}-root"))).then(function () {{
  const root = document.getElementById("{sid}-root");
  const W = Number(root.getAttribute("data-width")), H = Number(root.getAttribute("data-height")), V = H > W;
  const $ = (s) => root.querySelector(s), $$ = (s) => Array.from(root.querySelectorAll(s));
  const tl = gsap.timeline({{ paused: true }});
  const FL = $("#{sid}-flash"), RIG = $("#{sid}-rig");
{js}
  window.__timelines["{sid}"] = tl;
}});
</script>
</template>
</body></html>
'''
    open(os.path.join(ROOT, "compositions", f"{sid}.html"), "w").write(html)

K = lambda pose: f"assets/karan/{pose}.png"

# ------------------------------------------------------------------ S1 HOOK 0–2.4
scene("hook", f'''
    <div class="r-shot bg-ink" id="h1"><div class="X fit" data-fit="0.8" id="h1t">Don’t</div></div>
    <div class="r-shot bg-yellow" id="h2"><div class="X fit" data-fit="0.82" id="h2t">just</div></div>
    <div class="r-shot bg-red" id="h3"><div style="position:relative"><div class="X fit c-ink" data-fit="0.84" id="h3t">talk.</div><i id="h3s" style="position:absolute;left:-4%;right:-4%;top:46%;height:9%;background:#f2ede3;transform-origin:0 50%;display:block"></i></div></div>
    <div class="r-shot bg-paper" id="h4">
      <div class="r-row X c-ink" id="h4m1" style="top:4%;opacity:.13">Karan Raj KR · Founder, KĀRYO · Karan Raj KR · Founder, KĀRYO · Karan Raj KR · Founder, KĀRYO ·</div>
      <div class="r-row X c-ink" id="h4m2" style="bottom:4%;opacity:.13">Builds · Ships · Wins · Builds · Ships · Wins · Builds · Ships · Wins · Builds · Ships ·</div>
      <div class="X fit c-red" data-fit="0.92" id="h4t">Build.</div>
      <div id="h4burst" style="position:absolute;inset:0"></div>
      <img class="r-kar" id="h4k" src="{K('front')}" />
      <div class="r-chip bg-ink M" id="h4tag" style="position:absolute;font-size:34px">Karan Raj KR · Founder, KĀRYO</div>
    </div>''', '''
  [["#h4m1"], ["#h4m2"]].forEach(([s]) => { $(s).style.fontSize = (V ? 120 : 150) + "px"; });
  const kH = V ? 980 : 760; const k = $("#h4k"); k.style.height = kH + "px"; k.style.left = (W / 2 - kH * 0.306) + "px"; k.style.top = (H * (V ? 0.88 : 0.97) - kH) + "px";
  const tag = $("#h4tag"); tag.style.left = "50%"; tag.style.bottom = (V ? 170 : 60) + "px"; tag.style.transform = "translateX(-50%)";
  R.cut(tl, "#h1", 0, 0.4); R.slam(tl, "#h1t", 0, 2.2);
  R.cut(tl, "#h2", 0.4, 0.4); R.whip(tl, "#h2t", 0.4, 1);
  R.cut(tl, "#h3", 0.8, 0.4); R.slam(tl, "#h3t", 0.8, 0.6); tl.fromTo("#h3s", { scaleX: 0 }, { scaleX: 1, duration: 0.12, ease: "expo.out" }, 1.0);
  R.cut(tl, "#h4", 1.2, 1.2); R.slam(tl, "#h4t", 1.2, 2.4, -6);
  R.marquee(tl, "#h4m1", 1.2, 1.2, 0, -900); R.marquee(tl, "#h4m2", 1.2, 1.2, -1400, -500);
  tl.fromTo(k, { y: -H * 1.2 }, { y: 0, duration: 0.3, ease: "back.out(1.3)" }, 1.4);
  R.burst(tl, $("#h4burst"), 1.66, 26, W / 2, H * (V ? 0.86 : 0.93), V ? 520 : 700, ["#ff4a1c", "#ffc629", "#121212"]);
  R.flash(tl, FL, 1.2, 0.6);
  R.shake(tl, RIG, 1.66, 0.4, 2.4);
  tl.fromTo(tag, { yPercent: 160, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.2, ease: "expo.out" }, 1.8);
  R.punch(tl, "#h4t", 1.66, 1.06);
  tl.to("#h4 > *", { xPercent: -30, filter: "blur(16px)", duration: 0.16, ease: "power3.in" }, 2.24);''')

# ------------------------------------------------------------------ S2 BUILDS 2.4–6.4
prods = [("School ERP", "Live · 41 tables · ~45 routes", "bg-red", "c-ink"), ("ClinicDesk", "Dental clinic system", "bg-yellow", "c-ink"),
         ("Eligent", "Finds it · checks eligibility · fills the form", "bg-paper", "c-ink"), ("FormPilot", "AI Chrome extension", "bg-ink", "c-red")]
pm = "\n".join(f'''    <div class="r-shot {bg}" id="p{i}"><div class="r-col" id="p{i}c">
      <div class="M" style="font-size:30px;opacity:.75">01 — Builds · {i+1}/4</div>
      <div class="X fit {fc}" data-fit="0.9" id="p{i}t">{n}</div>
      <div class="N" style="font-size:44px;margin-top:22px">{l}</div></div>
      <div class="ui" id="p{i}u"><b></b><b></b><b></b><b></b><b></b></div>
    </div>''' for i, (n, l, bg, fc) in enumerate(prods))
scene("builds", f'''
    <div class="r-shot bg-ink" id="b1">
      <div class="r-col" id="b1c"><div class="X fit c-paper" data-fit="0.62" id="b1t">I ship</div><div class="X fit c-red" data-fit="0.62" id="b1u">products.</div></div>
      <img class="r-kar" id="b1k" src="{K('three-quarter')}" />
      <div class="r-row M c-paper" id="b1m" style="bottom:5%;font-size:40px;opacity:.5">School ERP · ClinicDesk · Eligent · FormPilot · School ERP · ClinicDesk · Eligent · FormPilot · School ERP · ClinicDesk ·</div>
    </div>
{pm}
    <div class="r-shot bg-paper" id="b6"><div class="r-col">
      <div class="X fit c-ink" data-fit="0.8" id="b6a">6-figure</div>
      <div class="X fit c-redink" data-fit="0.8" id="b6b">revenue</div>
      <div class="M" style="font-size:38px;margin-top:26px" id="b6c">Products &amp; agencies</div></div></div>
    <div class="r-shot bg-red" id="b7">
      <div class="r-col" id="b7c"><div class="X c-ink fit" data-fit="0.42" data-max="560" id="b7n" style="line-height:.8">18</div>
      <div class="X fit c-ink" data-fit="0.5" id="b7t">merged PRs</div>
      <div class="M c-ink" style="font-size:36px;margin-top:20px">GSSoC 2026 · Maintainer, crewai-recipes</div></div>
      <img class="r-kar" id="b7k" src="{K('explaining')}" />
    </div>''', '''
  const kq = $("#b1k"); const kqH = V ? 760 : 820; kq.style.height = kqH + "px"; kq.style.left = (V ? W / 2 - kqH * 0.28 : W - kqH * 0.62) + "px"; kq.style.top = (H - kqH - (V ? 60 : 20)) + "px";
  if (!V) { $("#b1c").style.marginRight = "520px"; $("#b1c").style.alignItems = "flex-start"; } else { $("#b1c").style.marginTop = "-760px"; }
  R.cut(tl, "#b1", 0, 0.8); R.whip(tl, "#b1t", 0, -1); R.whip(tl, "#b1u", 0.08, 1); R.pop(tl, kq, 0.12, 700);
  R.marquee(tl, "#b1m", 0, 0.8, 0, -700); R.shake(tl, RIG, 0.0, 0.3, 1.6);
  [0, 1, 2, 3].forEach((i) => {
    const at = 0.8 + i * 0.4, dir = i % 2 ? -1 : 1;
    R.cut(tl, "#p" + i, at, 0.4);
    R.whip(tl, "#p" + i + "c", at, dir, 1.0, 0.2);
    tl.fromTo("#p" + i + "u", { rotationY: dir * 70, rotationX: 18, opacity: 0, transformPerspective: 1200 }, { rotationY: dir * -14, rotationX: 8, opacity: 1, duration: 0.36, ease: "expo.out" }, at + 0.04);
    $$("#p" + i + "u b").forEach((b, j) => tl.fromTo(b, { scaleX: 0 }, { scaleX: 1, duration: 0.18, ease: "expo.out" }, at + 0.08 + j * 0.035));
    R.punch(tl, "#p" + i + "t", at + 0.2, 1.04);
  });
  R.cut(tl, "#b6", 2.4, 0.8); R.slam(tl, "#b6a", 2.4, 2.0); R.slam(tl, "#b6b", 2.6, 2.0, 4); tl.fromTo("#b6c", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.2 }, 2.8);
  R.flash(tl, FL, 2.6, 0.45); R.shake(tl, RIG, 2.6, 0.35, 2);
  R.cut(tl, "#b7", 3.2, 0.8);
  const n = { v: 0 }; const nEl = $("#b7n");
  tl.fromTo(n, { v: 0 }, { v: 18, duration: 0.45, ease: "power3.out", onUpdate: () => { nEl.textContent = Math.round(n.v); } }, 3.2);
  tl.fromTo(nEl, { filter: "blur(16px)", scale: 1.3 }, { filter: "blur(0px)", scale: 1, duration: 0.45, ease: "power3.out" }, 3.2);
  R.slam(tl, "#b7t", 3.4, 1.6);
  const ke = $("#b7k"); const keH = V ? 520 : 560; ke.style.height = keH + "px"; ke.style.left = (V ? W - keH * 1.0 : W - keH * 1.1) + "px"; ke.style.top = (H - keH + 6) + "px";
  R.pop(tl, ke, 3.45, 600);
  tl.to("#b7c", { xPercent: -40, filter: "blur(20px)", duration: 0.16, ease: "power3.in" }, 3.84);''', css='''
  #builds-root .ui { position: absolute; right: 7%; bottom: 9%; width: 380px; padding: 26px; background: #121212; border-radius: 18px; display: grid; gap: 14px; box-shadow: 14px 14px 0 rgba(0,0,0,.25); }
  #builds-root .bg-ink .ui { background: #2a2a2a; }
  #builds-root .ui b { display: block; height: 22px; border-radius: 6px; background: #ff4a1c; transform-origin: 0 50%; }
  #builds-root .ui b:nth-child(2n) { background: #f2ede3; width: 72%; }
  #builds-root .ui b:nth-child(3n) { background: #ffc629; width: 54%; }
  #builds-root .r-col { position: relative; z-index: 2; }
  [data-width="1080"] #builds-root .ui { right: auto; left: 50%; margin-left: -190px; bottom: 7%; }''')

# ------------------------------------------------------------------ S3 WINS 6.4–12.0
awards = [("GRIT Awards ×2", "Winner · Content + Hackathons", "bg-yellow", "c-ink"), ("HackBLR 2026", "Top 40 of 2,500+ teams", "bg-ink", "c-paper"),
          ("Tech Innovators", "Technology Innovators Award · Aug 2026", "bg-paper", "c-red"), ("IIT Alumni", "Incubation · selected · Cohort 2.0", "bg-red", "c-ink"),
          ("SIH 2026", "Smart India Hackathon · leading a team of 6", "bg-ink", "c-yellow")]
am = "\n".join(f'''    <div class="r-shot {bg}" id="a{i}"><div class="r-col" id="a{i}c"><div class="X fit {fc}" data-fit="0.9" id="a{i}t">{n}</div>
      <div class="M" style="font-size:38px;margin-top:24px">{d}</div></div></div>''' for i, (n, d, bg, fc) in enumerate(awards))
studs = "".join('<i class="w-st"></i>' for _ in range(121))
rows = " · ".join(a[0] for a in awards)
scene("wins", f'''
    <div class="r-shot bg-ink" id="w1"><div id="w1g">{studs}</div>
      <div class="M c-paper" id="w1l" style="position:absolute;left:6%;top:7%;font-size:36px">Open Loop 2026 · 121 teams</div></div>
    <div class="r-shot bg-red" id="w2">
      <div class="r-col" id="w2c"><div class="X c-ink fit" data-fit="0.66" data-max="640" id="w2t" style="line-height:.78">1st</div>
      <div class="M c-ink" style="font-size:40px;margin-top:10px">Open Loop 2026 · with FormPilot</div></div>
      <div id="w2burst" style="position:absolute;inset:0"></div>
      <img class="r-kar" id="w2k" src="{K('happy')}" />
    </div>
    <div class="r-shot bg-ink" id="w3"><div id="w3c" style="width:80%">
      <div class="M c-red" style="font-size:36px">Our score</div><div class="w-bar"><i id="w3a" style="background:#ff4a1c"></i><span class="X c-red" id="w3an">80</span></div>
      <div class="M c-paper" style="font-size:36px;margin-top:28px;opacity:.6">Runner-up</div><div class="w-bar"><i id="w3b" style="background:#5a5a5a"></i><span class="X c-paper" id="w3bn" style="opacity:.6">60</span></div>
      <div class="X c-yellow fit" data-fit="0.5" data-max="140" id="w3p" style="margin-top:40px">₹20,000</div></div></div>
{am}
    <div class="r-shot bg-paper" id="w9">
      <div class="r-row X c-ink" id="w9r1" style="top:6%">{rows} · {rows} ·</div>
      <div class="r-row X c-red" id="w9r2" style="top:38%">{rows} · {rows} ·</div>
      <div class="r-row X c-ink" id="w9r3" style="top:70%">{rows} · {rows} ·</div>
      <img class="r-kar" id="w9k" src="{K('neutral')}" />
    </div>''', '''
  // 121-team grid: camera starts on the winning stud and pulls out, then the rest drop away.
  const g = $("#w1g"), cell = V ? 70 : 64, gap = V ? 14 : 12, size = 11 * cell + 10 * gap;
  g.style.cssText = `position:absolute;left:${(W - size) / 2}px;top:${(H - size) / 2}px;width:${size}px;height:${size}px;display:grid;grid-template-columns:repeat(11,1fr);gap:${gap}px;transform-origin:50% 50%`;
  const st = $$("#w1g .w-st");
  st.forEach((s, k) => { s.style.cssText = `display:block;border-radius:50%;background:${k === 60 ? "#ff4a1c" : "#3c3c3c"}`; });
  R.cut(tl, "#w1", 0, 1.2);
  tl.fromTo(g, { scale: 9 }, { scale: 1, duration: 0.75, ease: "expo.inOut" }, 0);
  st.forEach((s, k) => { if (k === 60) return; const r = Math.floor(k / 11), c = k % 11;
    tl.to(s, { y: H, rotation: (R.seeded(k) - 0.5) * 120, duration: 0.42, ease: "power2.in" }, 0.78 + R.seeded(k + 2) * 0.22); });
  tl.to(st[60], { scale: 2.4, duration: 0.25, ease: "back.out(2)" }, 1.0);
  tl.fromTo("#w1l", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.2 }, 0.2);
  // 1ST slam
  R.cut(tl, "#w2", 1.2, 0.8);
  const t1 = $("#w2t");
  R.slam(tl, t1, 1.2, 3.2, -10); R.flash(tl, FL, 1.2, 0.9); R.shake(tl, RIG, 1.2, 0.5, 3);
  R.burst(tl, $("#w2burst"), 1.24, 34, W / 2, H / 2, V ? 620 : 820, ["#121212", "#ffc629", "#f2ede3"]);
  const kh = $("#w2k"); const khH = V ? 520 : 560; kh.style.height = khH + "px"; kh.style.left = (W - khH * 0.95) + "px"; kh.style.top = (H - khH + 6) + "px";
  R.pop(tl, kh, 1.36, 600);
  // score race
  R.cut(tl, "#w3", 2.0, 0.8);
  tl.fromTo("#w3a", { scaleX: 0 }, { scaleX: 0.8, duration: 0.45, ease: "expo.out" }, 2.04);
  tl.fromTo("#w3b", { scaleX: 0 }, { scaleX: 0.6, duration: 0.45, ease: "expo.out" }, 2.1);
  R.slam(tl, "#w3p", 2.4, 1.8);
  // award rapid-fire: one per beat, alternating whip directions
  [0, 1, 2, 3, 4].forEach((i) => { const at = 2.8 + i * 0.4; R.cut(tl, "#a" + i, at, 0.4);
    if (i % 2) R.whipV(tl, "#a" + i + "c", at, i % 4 === 1 ? 1 : -1, 1.1, 0.2); else R.whip(tl, "#a" + i + "c", at, i % 4 === 0 ? 1 : -1, 1.1, 0.2);
    R.punch(tl, "#a" + i + "t", at + 0.2, 1.05); });
  R.shake(tl, RIG, 2.8, 2.0, 0.9);
  // recap wall
  R.cut(tl, "#w9", 4.8, 0.8);
  ["#w9r1", "#w9r2", "#w9r3"].forEach((s, i) => { $(s).style.fontSize = (V ? 150 : 200) + "px"; R.marquee(tl, s, 4.8, 0.8, i % 2 ? -2600 : 0, i % 2 ? -1600 : -1000); });
  const k9 = $("#w9k"); const k9H = V ? 760 : 820; k9.style.height = k9H + "px"; k9.style.left = (W / 2 - k9H * 0.41) + "px"; k9.style.top = (H - k9H + 6) + "px";
  R.pop(tl, k9, 4.84, 800, 0.3); R.flash(tl, FL, 4.8, 0.5);''', css='''
  #wins-root .w-bar { display: flex; align-items: center; gap: 26px; margin-top: 12px; }
  #wins-root .w-bar i { display: block; flex: 1; height: 70px; border-radius: 10px; transform-origin: 0 50%; }
  #wins-root .w-bar span { font-size: 110px; }''')

# ------------------------------------------------------------------ S4 PEOPLE 12.0–14.8
ev = [("IPL Auction", "#ff4a1c"), ("30-min Build + Pitch", "#ffc629"), ("Every Team Sponsored", "#f2ede3"), ("Debate & Rebrand", "#3a3a3a")]
cards = "\n".join(f'''      <div class="pe-card" id="e{i}" style="background:{c};color:{'#f2ede3' if c=='#3a3a3a' else '#121212'}"><span class="M" style="font-size:30px">0{i+1}</span><span class="X" style="font-size:52px;white-space:normal;line-height:.95">{n.replace('&','&amp;')}</span></div>''' for i, (n, c) in enumerate(ev))
crowd = "".join('<i class="pe-p"></i>' for _ in range(120))
scene("people", f'''
    <div class="r-shot bg-ink" id="e">
      <div class="X fit c-paper" data-fit="0.84" id="et" style="position:absolute;top:9%">Co-led 4+ events</div>
      <div id="ecards">
{cards}
      </div></div>
    <div class="r-shot bg-paper" id="c">
      <div id="cgrid">{crowd}</div>
      <div class="r-col" id="cc" style="position:relative;z-index:2"><div class="X c-redink fit" data-fit="0.62" data-max="420" id="cn" style="line-height:.8">120+</div>
      <div class="X fit c-ink" data-fit="0.7" id="cl">at our biggest event</div>
      <div class="N" style="font-size:44px;margin-top:16px">and teams kept building after.</div></div>
    </div>''', '''
  const cw = V ? 440 : 400, ch = V ? 330 : 300;
  $$(".pe-card").forEach((c, i) => {
    const col = V ? i % 2 : i, row = V ? Math.floor(i / 2) : 0, n = V ? 2 : 4;
    const totalW = n * cw + (n - 1) * 30;
    c.style.cssText += `;position:absolute;width:${cw}px;height:${ch}px;left:${(W - totalW) / 2 + col * (cw + 30)}px;top:${(V ? 560 : 430) + row * (ch + 30)}px;border-radius:18px;padding:26px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:12px 12px 0 rgba(0,0,0,.35)`;
  });
  R.cut(tl, "#e", 0, 1.2); R.whip(tl, "#et", 0, -1);
  [0, 1, 2, 3].forEach((i) => tl.fromTo("#e" + i, { y: H, rotation: (i - 1.5) * 24, scale: 0.8 }, { y: 0, rotation: (i - 1.5) * 2.5, scale: 1, duration: 0.3, ease: "back.out(1.4)" }, 0.12 + i * 0.2));
  R.shake(tl, RIG, 0.12, 0.8, 0.8);
  // crowd: 120 squares explode from the centre into a grid behind the counter
  R.cut(tl, "#c", 1.2, 1.6);
  const cols = V ? 10 : 15, cs = V ? 74 : 92, gp = V ? 12 : 14;
  const gw = cols * cs + (cols - 1) * gp, rowsN = Math.ceil(120 / cols), gh = rowsN * cs + (rowsN - 1) * gp;
  const grid = $("#cgrid"); grid.style.cssText = `position:absolute;left:${(W - gw) / 2}px;top:${(H - gh) / 2}px;width:${gw}px;height:${gh}px`;
  $$(".pe-p").forEach((p, k) => {
    const r = Math.floor(k / cols), c = k % cols, x = c * (cs + gp), y = r * (cs + gp);
    p.style.cssText = `position:absolute;left:${x}px;top:${y}px;width:${cs}px;height:${cs}px;border-radius:12px;background:${k % 7 === 3 ? "#ff4a1c" : "#121212"};opacity:.14`;
    tl.fromTo(p, { x: gw / 2 - x - cs / 2, y: gh / 2 - y - cs / 2, scale: 0.2, rotation: (R.seeded(k) - 0.5) * 360 }, { x: 0, y: 0, scale: 1, rotation: 0, duration: 0.5, ease: "expo.out" }, 1.2 + R.seeded(k + 4) * 0.45);
  });
  const cn = $("#cn"); const cv = { v: 0 };
  tl.fromTo(cv, { v: 0 }, { v: 120, duration: 0.7, ease: "power2.out", onUpdate: () => { cn.textContent = Math.round(cv.v) + (cv.v >= 119.5 ? "+" : ""); } }, 1.2);
  tl.fromTo(cn, { scale: 0.6, filter: "blur(12px)" }, { scale: 1, filter: "blur(0px)", duration: 0.7, ease: "power2.out" }, 1.2);
  R.punch(tl, cn, 1.9, 1.15); R.flash(tl, FL, 1.9, 0.5); R.shake(tl, RIG, 1.9, 0.35, 2.2);
  R.slam(tl, "#cl", 2.0, 1.6);''', css='''
  #people-root #ecards { position: absolute; inset: 0; }''')

# ------------------------------------------------------------------ S5 FINALE 14.8–20.0
pl = [("Hackathons", "Campus this year · then national", "bg-yellow", "c-ink"), ("Internships", "For students, through my company", "bg-paper", "c-red"),
      ("Build & Pitch", "Every month · ideas into products", "bg-red", "c-ink")]
plm = "\n".join(f'''    <div class="r-shot {bg}" id="f{i+2}"><div class="r-col" id="f{i+2}c"><div class="M" style="font-size:36px">Promise {i+1}/3</div><div class="X fit {fc}" data-fit="0.88" id="f{i+2}t">{n.replace('&','&amp;')}</div>
      <div class="N" style="font-size:46px;margin-top:20px">{d}</div></div></div>''' for i, (n, d, bg, fc) in enumerate(pl))
scene("finale", f'''
    <div class="r-shot bg-ink" id="f0"><div class="X fit c-paper" data-fit="0.8" id="f0t">Next build:</div></div>
    <div class="r-shot bg-red" id="f1"><div class="X c-ink fit" data-fit="0.8" data-max="720" id="f1t" style="line-height:.8">EDC</div></div>
{plm}
    <div class="r-shot bg-ink" id="f9">
      <div class="r-row X c-paper" id="f9m1" style="top:3%;opacity:.12">Builds · Ships · Wins · Brings people in · Builds · Ships · Wins · Brings people in ·</div>
      <div id="f9burst" style="position:absolute;inset:0"></div>
      <div class="r-col" id="f9c" style="position:relative;z-index:3">
        <div class="X fit c-paper" data-fit="0.5" data-fitv="0.86" id="f9a">Karan</div>
        <div class="X fit c-red" data-fit="0.5" data-fitv="0.86" id="f9b">Raj KR</div>
        <div class="r-chip bg-red M" id="f9tag" style="font-size:38px;margin-top:26px;color:#121212">Founder, KĀRYO</div>
        <div class="M c-paper" id="f9l" style="font-size:40px;margin-top:22px">karanrajkr.com · @karan.rajkr</div>
      </div>
      <img class="r-kar" id="f9k" src="{K('happy')}" />
    </div>''', '''
  R.cut(tl, "#f0", 0, 0.4); R.whip(tl, "#f0t", 0, -1);
  R.cut(tl, "#f1", 0.4, 0.4); const e = $("#f1t"); R.slam(tl, e, 0.4, 3, 8); R.flash(tl, FL, 0.4, 0.9); R.shake(tl, RIG, 0.4, 0.4, 3);
  [2, 3, 4].forEach((i, k) => { const at = 0.8 + k * 0.4; R.cut(tl, "#f" + i, at, 0.4); if (k === 1) R.whipV(tl, "#f" + i + "c", at, -1, 1.1, 0.2); else R.whip(tl, "#f" + i + "c", at, k ? -1 : 1, 1.1, 0.2); R.punch(tl, "#f" + i + "t", at + 0.2, 1.05); });
  // lockup: zoom-through into the name, burst, then hold
  R.cut(tl, "#f9", 2.0, null);
  $("#f9m1").style.fontSize = (V ? 120 : 160) + "px";
  if (!V) { $("#f9c").style.alignItems = "flex-start"; $("#f9c").style.marginRight = "640px"; } else { $("#f9c").style.marginTop = "-720px"; }
  tl.fromTo("#f9c", { scale: 4, filter: "blur(30px)", opacity: 0 }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.45, ease: "expo.out" }, 2.0);
  R.flash(tl, FL, 2.0, 0.9); R.shake(tl, RIG, 2.0, 0.6, 2.6);
  R.burst(tl, $("#f9burst"), 2.05, 40, W / 2, H / 2, V ? 700 : 950, ["#ff4a1c", "#ffc629", "#f2ede3"], 30);
  const kf = $("#f9k"); const kfH = V ? 700 : 760; kf.style.height = kfH + "px"; kf.style.left = (V ? W / 2 - kfH * 0.455 : W - kfH * 1.0) + "px"; kf.style.top = (H - kfH + 6) + "px";
  R.pop(tl, kf, 2.2, 900, 0.36);
  tl.fromTo("#f9tag", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(2)" }, 2.4);
  tl.fromTo("#f9l", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25 }, 2.6);
  R.marquee(tl, "#f9m1", 2.0, 3.2, 0, -900);
  tl.to("#f9c", { y: -10, duration: 2.6, ease: "sine.inOut" }, 2.6);
  tl.fromTo(kf, { rotation: 0 }, { rotation: 3, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 5, transformOrigin: "50% 100%" }, 2.8);''')
print("ok")
