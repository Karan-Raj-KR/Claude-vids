/* Shared, seek-safe motion helpers for the 20 s reel. Every helper adds
   fromTo/set tweens at explicit times on the scene's paused timeline. */
window.R = (function () {
  const BEAT = 0.4; // 150 BPM
  const P = () => !!document.querySelector('[data-width="1080"]');
  function seeded(i) { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }

  // Fit a single-line element to a target width (layout constant, measured once at setup).
  function fit(el, maxW, maxSize) {
    // Measure an attached, unconstrained clone (the scene may not be in the DOM yet).
    const probe = el.cloneNode(true);
    probe.removeAttribute("id");
    probe.style.cssText += ";position:absolute;left:-99999px;top:0;visibility:hidden;white-space:nowrap;font-size:100px;display:inline-block;width:auto;transform:none;";
    document.body.appendChild(probe);
    const w = probe.offsetWidth || probe.scrollWidth || 1;
    if (window.__fitDebug) window.__fitDebug.push([el.id, w, probe.getBoundingClientRect().width]);
    probe.remove();
    const size = Math.min(maxSize || 9999, (100 * maxW) / w);
    el.style.fontSize = size + "px";
    return size;
  }
  function fitAll(root, W) {
    root.querySelectorAll("[data-fit]").forEach((el) => {
      const frac = Number(el.dataset.fit) || 0.86;
      fit(el, W * frac, Number(el.dataset.max) || undefined);
    });
  }
  // Hard cut: shot visible only inside [at, at + dur).
  function cut(tl, el, at, dur) {
    tl.set(el, { visibility: "visible" }, at);
    if (dur != null) tl.set(el, { visibility: "hidden" }, at + dur);
  }
  // Scale-down slam with blur; lands in ~0.18 s.
  function slam(tl, el, at, from = 1.7, rot = 0) {
    tl.fromTo(el, { scale: from, opacity: 0, filter: "blur(14px)", rotation: rot },
      { scale: 1, opacity: 1, filter: "blur(0px)", rotation: 0, duration: 0.2, ease: "expo.out" }, at);
  }
  // Whip in from a side with motion blur.
  function whip(tl, el, at, dir = 1, dist = 1.2, dur = 0.22) {
    tl.fromTo(el, { xPercent: dir * dist * 100, filter: "blur(18px)", opacity: 1 },
      { xPercent: 0, filter: "blur(0px)", duration: dur, ease: "expo.out" }, at);
  }
  function whipV(tl, el, at, dir = 1, dist = 1.2, dur = 0.22) {
    tl.fromTo(el, { yPercent: dir * dist * 100, filter: "blur(18px)" },
      { yPercent: 0, filter: "blur(0px)", duration: dur, ease: "expo.out" }, at);
  }
  // Leave fast with blur (exit before a cut).
  function whipOut(tl, el, at, dir = -1, dur = 0.16) {
    tl.to(el, { xPercent: dir * 120, filter: "blur(18px)", duration: dur, ease: "power3.in" }, at);
  }
  function punch(tl, el, at, amt = 1.08) {
    tl.fromTo(el, { scale: amt }, { scale: 1, duration: 0.3, ease: "expo.out", immediateRender: false }, at);
  }
  function pop(tl, el, at, dist = 500, dur = 0.32) {
    tl.fromTo(el, { y: dist, rotation: -6 }, { y: 0, rotation: 0, duration: dur, ease: "back.out(1.6)" }, at);
  }
  function flash(tl, el, at, peak = 0.85) {
    tl.fromTo(el, { opacity: peak }, { opacity: 0, duration: 0.14, ease: "power2.out", immediateRender: false }, at);
  }
  // Registry camera-shake, kept on a short leash: capped overscan and a hard
  // reset when the hit is over so the frame never stays zoomed.
  function shake(tl, rig, at, dur = 0.5, intensity = 2.2) {
    if (!window.cameraShake) return;
    window.cameraShake(tl, rig, { profile: "handheld-normal-strong", intensity: Math.min(intensity, 2.2) * 0.9,
      frequency: 2.6, duration: dur, at, fps: 60, overscan: 1.08, rotation: false });
    const rest = { x: 0, y: 0, rotation: 0, rotationX: 0, rotationY: 0, scale: 1 };
    gsap.set(rig, rest);                 // undo the library's set-up frame
    tl.set(rig, rest, 0);                // and keep the frame still before the hit
    tl.set(rig, rest, at + dur);         // and after it
  }
  // Infinite-feeling marquee: one long row translated across the window.
  function marquee(tl, el, at, dur, from, to) {
    tl.fromTo(el, { x: from }, { x: to, duration: dur, ease: "none" }, at);
  }
  // Stud particles bursting from a point (seeded, deterministic).
  function burst(tl, host, at, n, cx, cy, spread, colors, size = 26) {
    for (let i = 0; i < n; i++) {
      const d = document.createElement("i");
      d.className = "r-sq";
      const s = size * (0.6 + seeded(i + 3) * 0.9);
      d.style.cssText = `width:${s}px;height:${s}px;left:${cx - s / 2}px;top:${cy - s / 2}px;background:${colors[i % colors.length]};opacity:0;`;
      host.appendChild(d);
      const a = seeded(i) * Math.PI * 2, r = spread * (0.35 + seeded(i + 9) * 0.65);
      tl.fromTo(d, { x: 0, y: 0, opacity: 1, rotation: 0, scale: 1 },
        { x: Math.cos(a) * r, y: Math.sin(a) * r + spread * 0.25, rotation: (seeded(i + 1) - 0.5) * 540, scale: 0.4, opacity: 0,
          duration: 0.9 + seeded(i + 5) * 0.4, ease: "power3.out" }, at);
    }
  }
  function ready() {
    return Promise.all([
      document.fonts.load('900 100px "Archivo"'),
      document.fonts.load('750 40px "Archivo"'),
      document.fonts.load('700 40px "JetBrains Mono"'),
    ]).catch(() => null);
  }
  // Async fit: probes are attached first so the real face is requested, then
  // we wait for fonts and measure (layout constants, computed once at setup).
  async function fitAllAsync(root) {
    const W = Number(root.getAttribute("data-width"));
    const els = Array.from(root.querySelectorAll("[data-fit]"));
    const probes = els.map((el) => {
      const p = el.cloneNode(true); p.removeAttribute("id");
      p.style.cssText += ";position:absolute;left:-99999px;top:0;white-space:nowrap;font-size:100px;display:inline-block;width:auto;transform:none;filter:none;";
      document.body.appendChild(p); return p;
    });
    // Force layout (this is what requests the real face), then wait until the
    // measured widths stop changing, i.e. the webfont has replaced the fallback.
    let prev = probes.map((p) => p.offsetWidth);
    for (let k = 0; k < 40; k++) {
      await document.fonts.ready;
      await new Promise((r) => setTimeout(r, 40));
      const cur = probes.map((p) => p.offsetWidth);
      const stable = cur.every((w, i) => Math.abs(w - prev[i]) < 0.5);
      prev = cur;
      if (stable && k >= 2 && document.fonts.check('900 100px "Archivo"')) break;
    }
    els.forEach((el, i) => {
      const w = probes[i].offsetWidth || 1;
      const portrait = Number(root.getAttribute("data-height")) > W;
      const frac = Number((portrait && el.dataset.fitv) || el.dataset.fit) || 0.86;
      el.style.fontSize = Math.min(Number(el.dataset.max) || 9999, (100 * W * frac) / w) + "px";
      probes[i].remove();
    });
  }
  return { fitAllAsync, ready, BEAT, P, seeded, fit, fitAll, cut, slam, whip, whipV, whipOut, punch, pop, flash, shake, marquee, burst };
})();
