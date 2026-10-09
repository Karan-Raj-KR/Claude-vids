"""Writes compositions/step1..back.html. Edit the scene markup here or in the
generated HTML directly (the HTML is the source of truth once written)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def chrome(sid, page, step):
    rail = "".join(f'<i class="{"on" if k < step else ""}"></i>' for k in range(6))
    return f'''<div class="m-chrome m-mono" id="{sid}-chrome"><span>Builder Set No. 2026 · Karan Raj KR</span><span>Instructions · {page}/7</span></div>
    <div class="m-rail m-mono" id="{sid}-rail">{rail}<span>{step}/6 built</span></div>'''

def step_head(sid, n, title):
    return f'''<div class="st-head" id="{sid}-head">
      <div class="m-step m-x st-badge" id="{sid}-badge">{n}</div>
      <div class="m-mask"><div class="m-x st-title" id="{sid}-title">{title}</div></div>
    </div>'''

COMMON_CSS = '''
  .st-head { position: absolute; left: 140px; top: 150px; display: flex; align-items: center; gap: 34px; }
  .st-badge { width: 150px; height: 150px; font-size: 104px; }
  .st-title { font-size: 104px; }
  .callout { padding: 22px 28px; display: flex; align-items: center; gap: 22px; }
  .qty { font-size: 44px; color: var(--red-ink); }
  [data-width="1080"] .st-head { left: 72px; top: 270px; gap: 26px; }[data-width="1080"] .st-badge { width: 120px; height: 120px; font-size: 84px; }[data-width="1080"] .st-title { font-size: 74px; }
  
'''

def write(sid, css, body, js, dur):
    html = f'''<!doctype html>
<html><head><meta charset="UTF-8" /></head>
<body>
<template>
<style>
  #{sid}-root {{ position: absolute; inset: 0; }}
{COMMON_CSS}
{css}
</style>
<div id="{sid}-root" data-composition-id="{sid}" data-width="1920" data-height="1080">
  <div class="m-page"><div class="m-dots" id="{sid}-dots" data-layout-allow-overflow></div>
{body}
  </div>
</div>
<script>
(function () {{
  const tl = gsap.timeline({{ paused: true }});
  const P = !!document.querySelector('[data-width="1080"]');
  const rise = (sel, at, d = 0.45) => tl.fromTo(sel, {{ yPercent: 112 }}, {{ yPercent: 0, duration: d, ease: "power4.out" }}, at);
  const snap = (sel, at, from = -520) => tl.fromTo(sel, {{ y: from, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.36, ease: "back.out(1.5)" }}, at);
  const pop = (sel, at) => tl.fromTo(sel, {{ scale: 0.86, opacity: 0, y: 24 }}, {{ scale: 1, opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, at);
  // page enters: camera drop-in from the previous page, then a slow push
  tl.fromTo("#{sid}-root .m-page", {{ yPercent: 9, scale: 1.02 }}, {{ yPercent: 0, scale: 1, duration: 0.5, ease: "expo.out" }}, 0);
  tl.fromTo("#{sid}-dots", {{ x: 0, y: 0 }}, {{ x: -30, y: 20, duration: {dur}, ease: "none" }}, 0);
  if (document.getElementById("{sid}-chrome")) tl.fromTo("#{sid}-chrome", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0.1);
{js}
  window.__timelines["{sid}"] = tl;
}})();
</script>
</template>
</body></html>
'''
    open(os.path.join(ROOT, "compositions", f"{sid}.html"), "w").write(html)

HEAD_JS = lambda sid: f'''  pop("#{sid}-badge", 0.15);
  rise("#{sid}-title", 0.3);'''

# ---------------------------------------------------------------- STEP 1
write("step1", '''
  #step1-fig { position: absolute; left: 230px; bottom: 190px; height: 600px; }
  #step1-slot { position: absolute; left: 150px; bottom: 136px; width: 540px; height: 70px; --stud: 90px; }
  #step1-callout { position: absolute; right: 140px; top: 340px; }
  #step1-callout .brick { width: 300px; height: 96px; display: flex; align-items: center; justify-content: center; font-size: 52px; --stud: 75px; }
  #step1-lines { position: absolute; left: 820px; top: 530px; width: 960px; }
  #step1-l1 { font-size: 120px; }
  #step1-l2 { font-size: 56px; margin-top: 30px; }
  #step1-l3 { font-size: 30px; color: var(--muted); margin-top: 24px; }
  #step1-arrow { position: absolute; right: 290px; top: 330px; width: 120px; height: 90px; }
  [data-width="1080"] #step1-callout { right: 72px; top: 450px; }[data-width="1080"] #step1-arrow { display: none; }[data-width="1080"] #step1-lines { left: 72px; top: 640px; width: 936px; }[data-width="1080"] #step1-l1 { font-size: 96px; }[data-width="1080"] #step1-l2 { font-size: 48px; }[data-width="1080"] #step1-fig { left: 50%; margin-left: -200px; bottom: 260px; height: 560px; }[data-width="1080"] #step1-slot { left: 50%; margin-left: -270px; bottom: 210px; }
  
''', f'''    {chrome("step1", 2, 1)}
    {step_head("step1", 1, "Start a company")}
    <div class="m-callout callout" id="step1-callout"><span class="m-mono qty">1x</span><div class="brick b-red m-x" id="step1-brick">KĀRYO</div></div>
    <div class="brick b-red" id="step1-slot"></div>
    <img id="step1-fig" src="assets/karan/three-quarter.png" alt="" />
    <div id="step1-lines">
      <div class="m-mask"><div class="m-x" id="step1-l1">Founder, KĀRYO</div></div>
      <div class="m-mask"><div class="m-n" id="step1-l2">6-figure revenue from products &amp; agencies</div></div>
      <div class="m-mask"><div class="m-mono" id="step1-l3">B.Tech CSE (AI/ML) · NIAT–S-VYASA University</div></div>
    </div>''', HEAD_JS("step1") + '''
  pop("#step1-callout", 0.5);
  tl.fromTo("#step1-fig", { y: 90, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }, 0.35);
  snap("#step1-slot", 1.0, -700);
  rise("#step1-l1", 1.0, 0.5);
  rise("#step1-l2", 1.5);
  rise("#step1-l3", 2.0);
  tl.to("#step1-fig", { y: -6, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }, 1.36);''', 4)

# ---------------------------------------------------------------- STEP 2
products = [("School ERP", "Live · 41 tables · ~45 routes", "b-red"), ("ClinicDesk", "Dental clinic system", "b-yellow"),
            ("Eligent", "Finds it, checks eligibility, fills the form", "b-ink"), ("FormPilot", "AI Chrome extension", "b-white")]
pb = "\n".join(f'''      <div class="brick {c} s2-brick" id="step2-p{i}"><div class="m-x s2-name">{n}</div><div class="m-n s2-line">{l}</div></div>''' for i, (n, l, c) in enumerate(products))
write("step2", '''
  #step2-plate { position: absolute; left: 140px; right: 140px; top: 360px; height: 470px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 34px 40px; align-content: start; }
  .s2-brick { height: 180px; padding: 26px 32px 0; --stud: 70px; border: 4px solid var(--ink); }
  .s2-name { font-size: 64px; }
  .s2-line { font-size: 34px; margin-top: 16px; }
  #step2-prs { position: absolute; left: 140px; bottom: 112px; display: flex; align-items: center; gap: 26px; padding: 18px 30px; }
  #step2-num { font-size: 120px; color: var(--red-ink); line-height: 1; }
  #step2-num .hf-number-wheel-digit { height: 1em; }
  #step2-prs .m-mono { font-size: 30px; line-height: 1.35; }
  #step2-fig { position: absolute; right: 150px; bottom: 0; height: 300px; }
  [data-width="1080"] #step2-plate { left: 72px; right: 72px; top: 470px; grid-template-columns: 1fr; gap: 34px; height: auto; }[data-width="1080"] .s2-brick { height: 170px; }[data-width="1080"] .s2-name { font-size: 58px; }[data-width="1080"] .s2-line { font-size: 32px; }[data-width="1080"] #step2-prs { right: 72px; left: 72px; bottom: auto; top: 1310px; }[data-width="1080"] #step2-fig { right: 50px; bottom: 0; height: 330px; }
  
''', f'''    {chrome("step2", 3, 2)}
    {step_head("step2", 2, "Ship products")}
    <div id="step2-plate">
{pb}
    </div>
    <div class="m-callout" id="step2-prs"><span class="m-x" id="step2-num"><span class="hf-number-wheel" data-value="18"></span></span><span class="m-mono">x merged PRs · GSSoC 2026<br />Maintainer · crewai-recipes</span></div>
    <img id="step2-fig" src="assets/karan/explaining.png" alt="" />''', HEAD_JS("step2") + '''
  // number wheel (registry component): build the digit strips
  document.querySelectorAll("#step2-root .hf-number-wheel").forEach((el) => {
    if (el.dataset.ready) return;
    const v = el.dataset.value; el.textContent = "";
    for (const ch of v) { const f = document.createElement("span"); f.className = "hf-number-wheel-digit"; f.style.cssText = "display:inline-block;height:1em;overflow:hidden;";
      const s = document.createElement("span"); s.className = "hf-number-wheel-strip"; s.style.display = "grid"; s.dataset.target = (-100 * (10 + Number(ch))) / (11 + Number(ch));
      for (let i = 0; i <= 10 + Number(ch); i++) { const d = document.createElement("span"); d.style.cssText = "height:1em;line-height:1em;"; d.textContent = String(i % 10); s.appendChild(d); }
      f.appendChild(s); el.appendChild(f); }
    el.dataset.ready = "1";
  });
  [0, 1, 2, 3].forEach((i) => snap("#step2-p" + i, 0.5 + i * 0.5, -600));
  pop("#step2-prs", 2.75);
  gsap.utils.toArray("#step2-root .hf-number-wheel-strip").forEach((s, i) => {
    tl.fromTo(s, { yPercent: 0 }, { yPercent: Number(s.dataset.target), duration: 1.0, ease: "power3.out" }, 2.85 + i * 0.08);
  });
  tl.fromTo("#step2-fig", { y: 300 }, { y: 0, duration: 0.45, ease: "power3.out" }, 3.0);
  tl.to("#step2-plate", { scale: 1.02, duration: 3, ease: "sine.inOut", transformOrigin: "50% 50%" }, 2.6);''', 6)

# ---------------------------------------------------------------- STEP 3
studs = "".join(f'<i class="s3-stud{" win" if k == 60 else ""}"></i>' for k in range(121))
awards = [("GRIT Awards 2026", "Winner · Content", "b-red"), ("GRIT Awards 2026", "Winner · Hackathons", "b-yellow"),
          ("HackBLR 2026", "Top 40 of 2,500+ teams", "b-white"), ("Technology Innovators Award", "August 2026", "b-ink"),
          ("IIT Alumni Incubation", "Selected · Cohort 2.0", "b-red"), ("Smart India Hackathon 2026", "Leading a team of 6", "b-yellow")]
tower = "\n".join(f'''        <div class="brick {c} s3-award" id="step3-a{i}"><span class="m-x">{n}</span><span class="m-mono">{d}</span></div>''' for i, (n, d, c) in enumerate(awards))
write("step3", '''
  #step3-a { position: absolute; inset: 0; }
  #step3-plate { position: absolute; right: 140px; top: 330px; width: 620px; height: 620px; display: grid; grid-template-columns: repeat(11, 1fr); gap: 12px; padding: 22px; background: #c9d4db; border-radius: 18px; border: 4px solid var(--ink); }
  .s3-stud { display: block; border-radius: 50%; background: #9aa7b0; box-shadow: inset 0 -5px 0 rgba(0,0,0,.18); }
  .s3-stud.win { background: var(--red); }
  #step3-res { position: absolute; left: 140px; top: 360px; width: 1000px; }
  #step3-first { font-size: 300px; color: var(--red-ink); line-height: 0.85; }
  #step3-of { font-size: 56px; margin-top: 18px; }
  #step3-meta { font-size: 32px; margin-top: 18px; color: var(--muted); }
  #step3-bars { margin-top: 34px; display: grid; gap: 14px; width: 760px; }
  .s3-bar { display: grid; grid-template-columns: 210px 1fr 90px; align-items: center; gap: 18px; font-size: 30px; }
  .s3-bar i { display: block; height: 30px; border-radius: 6px; background: var(--ink); transform-origin: 0 50%; }
  .s3-bar.us i { background: var(--red); }
  .s3-bar b { font-size: 46px; }
  #step3-b { position: absolute; inset: 0; }
  #step3-tower { position: absolute; left: 140px; bottom: 120px; width: 1100px; display: flex; flex-direction: column-reverse; gap: 18px; }
  .s3-award { height: 80px; display: flex; align-items: center; justify-content: space-between; padding: 0 30px; border: 4px solid var(--ink); --stud: 66px; }
  .s3-award .m-x { font-size: 40px; }
  .s3-award .m-mono { font-size: 28px; }
  #step3-fig { position: absolute; right: 150px; bottom: 0; height: 520px; }
  [data-width="1080"] #step3-plate { right: 140px; left: 140px; top: 440px; width: 800px; height: 800px; }[data-width="1080"] #step3-res { left: 72px; top: 1290px; width: 936px; }[data-width="1080"] #step3-first { font-size: 200px; }[data-width="1080"] #step3-of { font-size: 44px; }[data-width="1080"] #step3-bars { width: 936px; }[data-width="1080"] #step3-tower { left: 72px; right: 72px; width: auto; bottom: 640px; }[data-width="1080"] .s3-award { height: 120px; flex-direction: column; align-items: flex-start; justify-content: center; gap: 6px; }[data-width="1080"] .s3-award .m-x { font-size: 38px; }[data-width="1080"] .s3-award .m-mono { font-size: 26px; }[data-width="1080"] #step3-fig { right: 50%; margin-right: -220px; bottom: 100px; height: 440px; }
  
''', f'''    {chrome("step3", 4, 3)}
    {step_head("step3", 3, "Compete")}
    <div id="step3-a">
      <div id="step3-plate">{studs}</div>
      <div id="step3-res">
        <div class="m-mask"><div class="m-x" id="step3-first">1st</div></div>
        <div class="m-mask"><div class="m-x" id="step3-of">of 121 teams · Open Loop 2026</div></div>
        <div class="m-mask"><div class="m-mono" id="step3-meta">FormPilot · ₹20,000 prize · 309 people · 109 colleges · 14 states</div></div>
        <div id="step3-bars" class="m-mono">
          <div class="s3-bar us"><span>Our score</span><i id="step3-us"></i><b class="m-x">80</b></div>
          <div class="s3-bar"><span>Runner-up</span><i id="step3-ru"></i><b class="m-x">60</b></div>
        </div>
      </div>
    </div>
    <div id="step3-b">
      <div id="step3-tower">
{tower}
      </div>
      <img id="step3-fig" src="assets/karan/happy.png" alt="" />
    </div>''', HEAD_JS("step3") + '''
  const studs = gsap.utils.toArray("#step3-plate .s3-stud");
  studs.forEach((s, k) => {
    const r = Math.floor(k / 11), c = k % 11, d = Math.hypot(r - 5, c - 5);
    tl.fromTo(s, { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.25, ease: "power3.out" }, 0.3 + d * 0.035);
    if (k !== 60) tl.to(s, { opacity: 0.28, duration: 0.25, ease: "power2.out" }, 1.0 + d * 0.03);
  });
  tl.fromTo(studs[60], { scale: 1 }, { scale: 1.9, duration: 0.3, ease: "back.out(2)" }, 1.45);
  tl.to(studs[60], { scale: 1.35, duration: 0.3, ease: "power2.out" }, 1.75);
  rise("#step3-first", 1.5, 0.5);
  rise("#step3-of", 1.75);
  rise("#step3-meta", 2.0);
  tl.fromTo("#step3-us", { scaleX: 0 }, { scaleX: 0.8, duration: 0.6, ease: "power3.out" }, 2.2);
  tl.fromTo("#step3-ru", { scaleX: 0 }, { scaleX: 0.6, duration: 0.6, ease: "power3.out" }, 2.3);
  // whip to the trophy tower on the bar line (local 4.0 = 20.0 s)
  tl.fromTo("#step3-a", { yPercent: 0 }, { yPercent: -110, duration: 0.4, ease: "power3.in" }, 3.75);
  tl.fromTo("#step3-b", { yPercent: 110 }, { yPercent: 0, duration: 0.45, ease: "expo.out" }, 4.0);
  [0, 1, 2, 3, 4, 5].forEach((i) => snap("#step3-a" + i, 4.25 + i * 0.5, -700));
  tl.fromTo("#step3-fig", { y: 520 }, { y: 0, duration: 0.5, ease: "power3.out" }, 4.3);
  tl.to("#step3-fig", { rotation: 4, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: 5, transformOrigin: "50% 100%" }, 6.3);''', 8)

# ---------------------------------------------------------------- STEP 4
events = [("IPL Auction", "b-red"), ("30-Min Build + Pitch", "b-yellow"), ("Every Team Sponsored", "b-white"), ("Debate &amp; Rebrand", "b-ink")]
eb = "\n".join(f'''      <div class="brick {c} s4-ev" id="step4-e{i}"><span class="m-mono">0{i+1}</span><span class="m-x">{n}</span></div>''' for i, (n, c) in enumerate(events))
crowd = "".join(f'<i class="s4-p{" r" if (k * 37) % 9 == 0 else ""}"></i>' for k in range(120))
write("step4", '''
  #step4-events { position: absolute; left: 140px; right: 140px; top: 340px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 26px; }
  .s4-ev { height: 190px; padding: 20px 24px; display: flex; flex-direction: column; justify-content: space-between; border: 4px solid var(--ink); --stud: 64px; }
  .s4-ev .m-x { font-size: 36px; line-height: 1; }
  .s4-ev .m-mono { font-size: 26px; }
  #step4-crowd { position: absolute; right: 140px; bottom: 140px; width: 760px; display: grid; grid-template-columns: repeat(20, 1fr); gap: 7px; }
  .s4-p { display: block; aspect-ratio: 1; border-radius: 8px; background: var(--ink); box-shadow: inset 0 -5px 0 rgba(0,0,0,.25); }
  .s4-p.r { background: var(--red); }
  #step4-count { position: absolute; left: 140px; bottom: 270px; display: flex; align-items: flex-end; }
  #step4-num { font-size: 260px; color: var(--red-ink); line-height: 0.85; }
  #step4-plus { font-size: 260px; color: var(--red-ink); line-height: 0.85; }
  #step4-cap { position: absolute; left: 140px; bottom: 140px; width: 780px; }
  #step4-cap1 { font-size: 52px; }
  #step4-cap2 { font-size: 40px; margin-top: 8px; }
  [data-width="1080"] #step4-events { left: 72px; right: 72px; top: 450px; grid-template-columns: repeat(2, 1fr); gap: 22px 22px; }[data-width="1080"] .s4-ev { height: 170px; }[data-width="1080"] .s4-ev .m-x { font-size: 38px; }[data-width="1080"] #step4-crowd { left: 72px; right: 72px; width: auto; bottom: auto; top: 1080px; grid-template-columns: repeat(15, 1fr); }[data-width="1080"] #step4-count { left: 72px; bottom: auto; top: 850px; }[data-width="1080"] #step4-num, [data-width="1080"] #step4-plus { font-size: 200px; }[data-width="1080"] #step4-cap { left: 72px; bottom: auto; top: 1620px; width: 936px; }[data-width="1080"] #step4-cap1 { font-size: 48px; }
  
''', f'''    {chrome("step4", 5, 4)}
    {step_head("step4", 4, "Bring people in")}
    <div id="step4-events">
{eb}
    </div>
    <div id="step4-count"><span class="m-x" id="step4-num"><span class="hf-number-wheel" data-value="120"></span></span><span class="m-x" id="step4-plus">+</span></div>
    <div id="step4-crowd">{crowd}</div>
    <div id="step4-cap">
      <div class="m-mask"><div class="m-x" id="step4-cap1">at our biggest event</div></div>
      <div class="m-mask"><div class="m-n" id="step4-cap2">— and teams kept building after.</div></div>
    </div>''', HEAD_JS("step4") + '''
  document.querySelectorAll("#step4-root .hf-number-wheel").forEach((el) => {
    if (el.dataset.ready) return;
    const v = el.dataset.value; el.textContent = "";
    for (const ch of v) { const f = document.createElement("span"); f.style.cssText = "display:inline-block;height:1em;overflow:hidden;";
      const s = document.createElement("span"); s.className = "hf-number-wheel-strip"; s.style.display = "grid"; s.dataset.target = (-100 * (10 + Number(ch))) / (11 + Number(ch));
      for (let i = 0; i <= 10 + Number(ch); i++) { const d = document.createElement("span"); d.style.cssText = "height:1em;line-height:1em;"; d.textContent = String(i % 10); s.appendChild(d); }
      f.appendChild(s); el.appendChild(f); }
    el.dataset.ready = "1";
  });
  [0, 1, 2, 3].forEach((i) => snap("#step4-e" + i, 0.5 + i * 0.25, -500));
  const ppl = gsap.utils.toArray("#step4-crowd .s4-p");
  ppl.forEach((p, k) => {
    const cols = P ? 15 : 20, r = Math.floor(k / cols), c = k % cols;
    const d = Math.hypot(r - (P ? 4 : 3), c - cols / 2);
    tl.fromTo(p, { scale: 0.5, opacity: 0, y: -30 }, { scale: 1, opacity: 1, y: 0, duration: 0.22, ease: "power3.out" }, 2.0 + d * 0.11);
  });
  gsap.utils.toArray("#step4-root .hf-number-wheel-strip").forEach((s, i) => {
    tl.fromTo(s, { yPercent: 0 }, { yPercent: Number(s.dataset.target), duration: 1.6, ease: "power2.out" }, 2.0 + i * 0.06);
  });
  tl.fromTo("#step4-count", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 1.9);
  tl.fromTo("#step4-plus", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 3.6);
  rise("#step4-cap1", 3.2);
  rise("#step4-cap2", 3.6);''', 6)

# ---------------------------------------------------------------- COMPLETE
podium = [("KĀRYO", "b-red"), ("Products", "b-yellow"), ("Wins", "b-ink"), ("Community", "b-white")]
pod = "\n".join(f'''        <div class="brick {c} cp-pb" id="complete-pb{i}"><span class="m-mono">{n}</span></div>''' for i, (n, c) in enumerate(podium))
pledges = [("1x", "Campus hackathon this year, then a national one"), ("1x", "Internships through my company"), ("12x", "Build &amp; pitch nights — one every month")]
pl = "\n".join(f'''        <div class="m-callout cp-pl" id="complete-pl{i}"><span class="m-mono qty">{q}</span><span class="m-n">{t}</span></div>''' for i, (q, t) in enumerate(pledges))
write("complete", '''
  #complete-head { position: absolute; left: 140px; top: 150px; display: flex; align-items: center; gap: 30px; }
  #complete-check { width: 150px; height: 150px; border-radius: 22px; background: var(--red); }
  #complete-title { font-size: 104px; }
  #complete-model { position: absolute; left: 160px; bottom: 110px; width: 560px; display: flex; flex-direction: column; align-items: center; }
  #complete-fig { height: 400px; margin-bottom: -6px; position: relative; z-index: 2; }
  #complete-pod { width: 100%; display: flex; flex-direction: column; gap: 14px; }
  .cp-pb { height: 56px; display: flex; align-items: center; justify-content: center; font-size: 24px; border: 3px solid var(--ink); --stud: 56px; }
  #complete-next { position: absolute; left: 820px; top: 360px; width: 960px; }
  #complete-nt { font-size: 92px; }
  #complete-nt b { color: var(--red-ink); }
  #complete-pls { display: grid; gap: 22px; margin-top: 40px; }
  .cp-pl { display: flex; align-items: center; gap: 24px; padding: 22px 28px; font-size: 40px; }
  .cp-pl .qty { min-width: 80px; }
  [data-width="1080"] #complete-head { left: 72px; top: 270px; }[data-width="1080"] #complete-check { width: 120px; height: 120px; }[data-width="1080"] #complete-title { font-size: 74px; }[data-width="1080"] #complete-model { left: 50%; margin-left: -230px; width: 460px; bottom: 800px; }[data-width="1080"] #complete-fig { height: 340px; }[data-width="1080"] .cp-pb { height: 44px; }[data-width="1080"] #complete-next { left: 72px; top: auto; bottom: 200px; width: 936px; }[data-width="1080"] #complete-nt { font-size: 80px; }[data-width="1080"] .cp-pl { font-size: 34px; }
  
''', f'''    {chrome("complete", 6, 6)}
    <div id="complete-head">
      <svg id="complete-check" viewBox="0 0 150 150"><rect width="150" height="150" rx="22" fill="#ff4a1c"/><path id="complete-tick" d="M38 78 L64 104 L114 46" fill="none" stroke="#141414" stroke-width="16" stroke-linecap="square"/></svg>
      <div class="m-mask"><div class="m-x" id="complete-title">Build complete</div></div>
    </div>
    <div id="complete-model">
      <img id="complete-fig" src="assets/karan/front.png" alt="" />
      <div id="complete-pod">
{pod}
      </div>
    </div>
    <div id="complete-next">
      <div class="m-mask"><div class="m-x" id="complete-nt">Next build: <b>EDC</b></div></div>
      <div id="complete-pls">
{pl}
      </div>
    </div>''', '''
  tl.fromTo("#complete-check", { scale: 0.85, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "power3.out" }, 0.15);
  const tick = document.getElementById("complete-tick"); const len = 140;
  tick.style.strokeDasharray = len;
  tl.fromTo(tick, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }, 0.4);
  rise("#complete-title", 0.3);
  [3, 2, 1, 0].forEach((i, k) => snap("#complete-pb" + i, 0.5 + k * 0.25, -400));
  tl.fromTo("#complete-fig", { y: -500, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.4)" }, 1.5);
  rise("#complete-nt", 2.5, 0.5);
  [0, 1, 2].forEach((i) => pop("#complete-pl" + i, 3.0 + i * 0.5));
  tl.to("#complete-model", { scale: 1.03, duration: 4, ease: "sine.inOut", transformOrigin: "50% 100%" }, 2);''', 6)

# ---------------------------------------------------------------- BACK
write("back", '''
  #back-card { position: absolute; left: 190px; top: 130px; width: 1540px; height: 840px; background: var(--red); border: 6px solid var(--ink); border-radius: 30px; box-shadow: 18px 18px 0 rgba(20,20,20,.16); overflow: hidden; }
  #back-text { position: absolute; left: 70px; top: 90px; width: 900px; }
  #back-n1, #back-n2 { font-size: 178px; }
  #back-tag { font-size: 60px; margin-top: 26px; }
  #back-links { position: absolute; left: 70px; bottom: 70px; font-size: 40px; background: var(--page); border: 5px solid var(--ink); border-radius: 16px; padding: 18px 28px; }
  #back-fig { position: absolute; right: 90px; bottom: -8px; height: 640px; }
  #back-small { position: absolute; right: 70px; top: 54px; font-size: 26px; }
  [data-width="1080"] #back-card { left: 60px; top: 300px; width: 960px; height: 1380px; }[data-width="1080"] #back-text { left: 50px; top: 120px; width: 860px; }[data-width="1080"] #back-n1, [data-width="1080"] #back-n2 { font-size: 144px; }[data-width="1080"] #back-tag { font-size: 54px; }[data-width="1080"] #back-links { left: 50px; right: 50px; bottom: 600px; font-size: 34px; }[data-width="1080"] #back-fig { right: 50%; margin-right: -230px; height: 560px; }[data-width="1080"] #back-small { right: 50px; top: 40px; }
  
''', '''    <div id="back-card">
      <div id="back-small" class="m-mono">Builder Set No. 2026</div>
      <div id="back-text">
        <div class="m-mask"><div class="m-x" id="back-n1">Karan</div></div>
        <div class="m-mask"><div class="m-x" id="back-n2">Raj KR</div></div>
        <div class="m-mask"><div class="m-n" id="back-tag">Founder, KĀRYO</div></div>
      </div>
      <div id="back-links" class="m-mono">karanrajkr.com · @karan.rajkr</div>
      <img id="back-fig" src="assets/karan/happy.png" alt="" />
    </div>''', '''
  tl.fromTo("#back-card", { rotationY: 90, opacity: 0.6, transformPerspective: 1600 }, { rotationY: 0, opacity: 1, duration: 0.55, ease: "power3.out" }, 0);
  rise("#back-n1", 0.35, 0.5);
  rise("#back-n2", 0.45, 0.5);
  rise("#back-tag", 0.7);
  tl.fromTo("#back-fig", { y: 420 }, { y: 0, duration: 0.5, ease: "power3.out" }, 0.6);
  pop("#back-links", 1.0);
  tl.fromTo("#back-small", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.2);
  tl.to("#back-card", { scale: 1.025, duration: 3, ease: "sine.inOut" }, 1);''', 4)
print("ok")
