/* ============================================================
   main.js — 交互逻辑
   模块：① 章节切分与折叠 ② 目录生成与滚动高亮
        ③ 移动端抽屉 ④ 阅读进度条与返回顶部 ⑤ 顶栏阴影
   依赖：原生 API（IntersectionObserver），无第三方库
   ============================================================ */
(function () {
  "use strict";

  var main = document.getElementById("main");

  /* ---------- ① 章节切分与折叠 ----------
     将 main 内每个 <h1> 及其后继内容包成一张 article 卡片；
     点击章标题切换折叠（凸起卡片保留，内容收起）。 */
  function initSections() {
    var kids = [].slice.call(main.children);
    var wrap = document.createDocumentFragment();
    var cur = null;

    kids.forEach(function (el) {
      if (el.tagName === "H1") {
        cur = document.createElement("article");

        var chip = document.createElement("span");
        chip.className = "chip";
        chip.textContent = "章节";

        var arr = document.createElement("span");
        arr.className = "arr";
        arr.textContent = "▾ 收起";

        el.insertBefore(chip, el.firstChild);
        el.appendChild(arr);
        cur.appendChild(el);

        var sec = document.createElement("div");
        sec.className = "sec";
        cur.appendChild(sec);
        cur._sec = sec;
        wrap.appendChild(cur);

        el.addEventListener("click", function () {
          cur.classList.toggle("folded");
          arr.textContent = cur.classList.contains("folded") ? "▸ 展开" : "▾ 收起";
        });
      } else if (cur) {
        cur._sec.appendChild(el);
      } else {
        wrap.appendChild(el);   /* hero 区在 h1 之前，原样保留 */
      }
    });

    main.innerHTML = "";
    main.appendChild(wrap);
  }

  /* ---------- ② 目录生成与滚动高亮 ----------
     从章节卡片标题生成侧栏链接；
     IntersectionObserver 监听章节进入视口中部时高亮对应链接。 */
  function initToc() {
    var toc = document.getElementById("toc");
    var arts = [].slice.call(document.querySelectorAll("main > article"));
    var links = arts.map(function (art, i) {
      var h = art.querySelector("h1");
      var t = h
        ? h.textContent.replace("章节", "").replace(/[▾▸]\s*收起|▸\s*展开/, "").trim()
        : "章节 " + (i + 1);
      var a = document.createElement("a");
      a.href = "#";
      a.textContent = t;
      a.addEventListener("click", function (e) {
        e.preventDefault();
        art.scrollIntoView({ behavior: "smooth" });
        if (window.innerWidth <= 960) toggleNav(false);  // 移动端点击后收起抽屉
      });
      toc.appendChild(a);
      return a;
    });

    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (en) {
            if (!en.isIntersecting) return;
            links.forEach(function (l) { l.classList.remove("on"); });
            var i = arts.indexOf(en.target);
            if (links[i]) links[i].classList.add("on");
          });
        },
        { rootMargin: "-20% 0px -70% 0px" }
      );
      arts.forEach(function (a) { io.observe(a); });
    }
  }

  /* ---------- ③ 移动端抽屉 ---------- */
  var nav = document.getElementById("sidebar");
  var menuBtn = document.getElementById("menuBtn");

  function toggleNav(force) {
    var open = typeof force === "boolean" ? force : !nav.classList.contains("open");
    nav.classList.toggle("open", open);
    menuBtn.textContent = open ? "✕" : "☰";
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function initDrawer() {
    menuBtn.addEventListener("click", function () { toggleNav(); });
    document.addEventListener("click", function (e) {
      if (window.innerWidth <= 960 &&
          nav.classList.contains("open") &&
          !nav.contains(e.target) && e.target !== menuBtn) {
        toggleNav(false);
      }
    });
  }

  /* ---------- ④ 进度条 + 返回顶部 ---------- */
  function initScrollUI() {
    var bar = document.getElementById("progress");
    var backtop = document.getElementById("backtop");

    window.addEventListener("scroll", function () {
      var h = document.documentElement;
      var ratio = h.scrollTop / (h.scrollHeight - h.clientHeight);
      bar.style.width = (ratio * 100).toFixed(2) + "%";
      backtop.classList.toggle("show", h.scrollTop > 600);
      document.querySelector(".topbar").classList.toggle("scrolled", h.scrollTop > 8);
    }, { passive: true });

    backtop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------- 启动 ---------- */
  initSections();
  initToc();
  initDrawer();
  initScrollUI();
})();
