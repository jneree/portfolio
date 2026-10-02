(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Top bar border once scrolled
  const top = $(".top");
  const onScroll = () => top && top.classList.toggle("scrolled", scrollY > 8);
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Mobile menu
  const menuBtn = $(".menu-btn");
  const setMenu = (open) => {
    top.classList.toggle("open", open);
    menuBtn.setAttribute("aria-expanded", String(open));
  };
  menuBtn?.addEventListener("click", () => setMenu(!top.classList.contains("open")));
  $$(".nav a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
  document.addEventListener("click", (e) => { if (!top.contains(e.target)) setMenu(false); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });
  matchMedia("(min-width: 901px)").addEventListener("change", (e) => { if (e.matches) setMenu(false); });

  // Highlight the current section in the nav
  const links = new Map($$(".nav a").map((a) => [a.hash.slice(1), a]));
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      links.forEach((a) => a.classList.remove("on"));
      links.get(e.target.id)?.classList.add("on");
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  $$("[data-section]").forEach((s) => spy.observe(s));

  // Looping videos: load and play only while visible
  const loops = new IntersectionObserver((entries) => {
    entries.forEach(({ target: v, isIntersecting }) => {
      if (isIntersecting) {
        if (!v.src) v.src = v.dataset.src;
        if (!reduceMotion) v.play().catch(() => {});
      } else {
        v.pause();
      }
    });
  }, { rootMargin: "200px 0px" });
  $$("video.loop").forEach((v) => loops.observe(v));

  // Strip arrows
  $$(".strip-wrap").forEach((wrap) => {
    const strip = $(".strip", wrap);
    const prev = $(".prev", wrap);
    const next = $(".next", wrap);
    const update = () => {
      prev.disabled = strip.scrollLeft < 8;
      next.disabled = strip.scrollLeft + strip.clientWidth >= strip.scrollWidth - 8;
    };
    const step = (dir) => strip.scrollBy({ left: dir * strip.clientWidth * 0.8, behavior: reduceMotion ? "auto" : "smooth" });
    prev.addEventListener("click", () => step(-1));
    next.addEventListener("click", () => step(1));
    strip.addEventListener("scroll", update, { passive: true });
    addEventListener("resize", update);
    update();
  });

  // "What I do" filter
  const chips = $$(".chip");
  const bar = $(".filterbar");
  const setFilter = (key) => {
    const body = document.body;
    const chip = chips.find((c) => c.dataset.filter === key);
    chips.forEach((c) => c.setAttribute("aria-pressed", String(c === chip && !!key)));
    $$(".match").forEach((el) => el.classList.remove("match"));
    if (!key) {
      delete body.dataset.filter;
      bar.hidden = true;
      return;
    }
    body.dataset.filter = key;
    $$(`.row[data-cat~="${key}"]`).forEach((r) => {
      r.classList.add("match");
      r.closest(".phase")?.classList.add("match");
      r.closest(".co")?.classList.add("match");
    });
    $(".fb-name", bar).textContent = $("span", chip).textContent;
    bar.hidden = false;
    const first = $(".co.match");
    if (first) requestAnimationFrame(() => first.scrollIntoView({ behavior: "auto", block: "start" }));
  };
  chips.forEach((c) => {
    c.setAttribute("aria-pressed", "false");
    c.addEventListener("click", () => {
      const key = c.dataset.filter;
      if (key === "photo") {
        setFilter(null);
        $("#photography").scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
        return;
      }
      setFilter(c.getAttribute("aria-pressed") === "true" ? null : key);
    });
  });
  $(".fb-clear")?.addEventListener("click", () => {
    setFilter(null);
    $(".index").scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
  });

  // YouTube: load the player only on click
  $$(".yt-play").forEach((b) => {
    b.addEventListener("click", () => {
      const f = document.createElement("div");
      f.className = "yt-frame";
      f.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${b.dataset.yt}?autoplay=1&rel=0" title="${b.getAttribute("aria-label")}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`;
      b.replaceWith(f);
    });
  });

  // Lightbox
  const lb = $(".lb");
  if (!lb) return;
  const stage = $(".lb-stage", lb);
  let group = [];
  let idx = 0;

  const show = (i) => {
    idx = (i + group.length) % group.length;
    const d = group[idx].dataset;
    stage.innerHTML = "";
    let el;
    if (d.lb === "vid") {
      el = document.createElement("video");
      Object.assign(el, { src: d.src, poster: d.poster, controls: true, loop: true, muted: true, playsInline: true, autoplay: true });
    } else {
      el = document.createElement("img");
      el.src = d.src;
      el.srcset = d.srcset;
      el.sizes = "100vw";
      el.width = +d.w;
      el.height = +d.h;
      el.alt = d.cap || "";
    }
    stage.append(el);
    $(".lb-t", lb).textContent = d.cap || "";
    $(".lb-n", lb).textContent = group.length > 1 ? `${idx + 1} / ${group.length}` : "";
    lb.classList.toggle("single", group.length < 2);
  };

  document.addEventListener("click", (e) => {
    const z = e.target.closest(".zoom");
    if (!z) return;
    const gallery = z.closest("[data-gallery]");
    group = gallery ? $$(".zoom", gallery) : [z];
    lb.showModal();
    show(group.indexOf(z));
  });
  $(".lb-close", lb).addEventListener("click", () => lb.close());
  $(".lb-prev", lb).addEventListener("click", () => show(idx - 1));
  $(".lb-next", lb).addEventListener("click", () => show(idx + 1));
  lb.addEventListener("click", (e) => { if (e.target === lb || e.target === stage) lb.close(); });
  lb.addEventListener("close", () => { stage.innerHTML = ""; });
  lb.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") show(idx - 1);
    if (e.key === "ArrowRight") show(idx + 1);
  });
  let x0 = null;
  lb.addEventListener("pointerdown", (e) => { x0 = e.clientX; });
  lb.addEventListener("pointerup", (e) => {
    if (x0 === null) return;
    const dx = e.clientX - x0;
    x0 = null;
    if (Math.abs(dx) > 50 && group.length > 1) show(idx + (dx < 0 ? 1 : -1));
  });
})();
