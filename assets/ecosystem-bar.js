(function () {
  if (document.getElementById("artelligence-ecosystem-bar")) return;

  const scriptEl = document.currentScript;
  const position = (scriptEl && scriptEl.getAttribute("data-position")) || "bottom";
  const isEn = (document.documentElement.lang || "ar").toLowerCase().startsWith("en");

  const LINKS = [
    { key: "portfolio", labelAr: "البورتفوليو", labelEn: "Portfolio", href: "https://ahmedissamramadan.github.io/portfolio/" },
    { key: "artelligence", labelAr: "Artelligence", labelEn: "Artelligence", href: "https://ahmedissamramadan.github.io/artelligence/" },
    { key: "artelligence-os", labelAr: "Artelligence OS", labelEn: "Artelligence OS", href: "https://ahmedissamramadan.github.io/Artelligence-OS/" },
    { key: "ai-pyramid", labelAr: "هرم الـ AI", labelEn: "AI Pyramid", href: "https://ahmedissamramadan.github.io/ai-pyramid/" },
    { key: "air", labelAr: "حاسبة الجاهزية", labelEn: "AIR Calculator", href: "https://ahmedissamramadan.github.io/air/" },
    { key: "transformation", labelAr: "تحوّل الأعمال", labelEn: "Transformation", href: "https://ahmedissamramadan.github.io/ai-business-transformation/" },
    { key: "content-system", labelAr: "منظومة 84 يوماً", labelEn: "84-Day System", href: "https://ahmedissamramadan.github.io/ai-business-transformation/content-system/" },
    { key: "wasl", labelAr: "WASL Network", labelEn: "WASL Network", href: "https://wasl-network.com" },
    { key: "campaign", labelAr: "احجز مكالمة", labelEn: "Book Call", href: "https://ahmedissamramadan.github.io/ai-business-transformation/campaign/?utm_source=ecosystem_bar&utm_medium=" + position, cta: true }
  ];

  const currentUrl = window.location.href.toLowerCase();
  const currentPath = window.location.pathname.toLowerCase();

  const style = document.createElement("style");
  style.textContent = `
    #artelligence-ecosystem-bar {
      width: 100%;
      background: #0A0A0A;
      color: #FAFAFA;
      border-bottom: 1px solid rgba(250, 250, 250, 0.14);
      border-top: 1px solid rgba(250, 250, 250, 0.14);
      font-family: 'Cairo', 'Inter', system-ui, -apple-system, sans-serif;
      font-size: 12px;
      line-height: 1.4;
      z-index: 60;
    }
    #artelligence-ecosystem-bar .eco-inner {
      max-width: 1120px;
      margin: 0 auto;
      padding: 8px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }
    #artelligence-ecosystem-bar .eco-brand {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-weight: 800;
      letter-spacing: 0.08em;
      font-size: 11px;
      color: #A1A1AA;
      white-space: nowrap;
    }
    #artelligence-ecosystem-bar .eco-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #FAFAFA;
      display: inline-block;
    }
    #artelligence-ecosystem-bar .eco-links {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }
    #artelligence-ecosystem-bar a {
      color: #D4D4D8;
      text-decoration: none;
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid transparent;
      font-weight: 600;
      transition: all 0.15s ease;
      white-space: nowrap;
    }
    #artelligence-ecosystem-bar a:hover {
      color: #FAFAFA;
      border-color: rgba(250, 250, 250, 0.25);
    }
    #artelligence-ecosystem-bar a.eco-active {
      color: #FAFAFA;
      border-color: rgba(250, 250, 250, 0.4);
      background: rgba(250, 250, 250, 0.08);
    }
    #artelligence-ecosystem-bar a.eco-cta {
      background: #FAFAFA;
      color: #0A0A0A;
      font-weight: 700;
    }
    #artelligence-ecosystem-bar a.eco-cta:hover {
      opacity: 0.88;
      border-color: #FAFAFA;
    }
  `;
  document.head.appendChild(style);

  const bar = document.createElement("nav");
  bar.id = "artelligence-ecosystem-bar";
  bar.setAttribute("aria-label", "Artelligence Ecosystem");
  bar.setAttribute("dir", isEn ? "ltr" : "rtl");

  const inner = document.createElement("div");
  inner.className = "eco-inner";

  const brand = document.createElement("div");
  brand.className = "eco-brand";
  brand.innerHTML = `<span class="eco-dot"></span><span>${isEn ? "ARTELLIGENCE ECOSYSTEM" : "منظومة ARTELLIGENCE"}</span>`;

  const linksWrap = document.createElement("div");
  linksWrap.className = "eco-links";

  LINKS.forEach((item) => {
    const a = document.createElement("a");
    a.href = item.href;
    a.textContent = isEn ? item.labelEn : item.labelAr;
    if (item.href.startsWith("https://wasl-network.com")) {
      a.target = "_blank";
      a.rel = "noopener noreferrer";
    }
    if (item.cta) {
      a.className = "eco-cta";
    } else if (
      (item.key === "portfolio" && currentPath.startsWith("/portfolio")) ||
      (item.key === "artelligence" && currentPath.startsWith("/artelligence/")) ||
      (item.key === "artelligence-os" && currentPath.startsWith("/artelligence-os")) ||
      (item.key === "ai-pyramid" && currentPath.startsWith("/ai-pyramid")) ||
      (item.key === "air" && currentPath.startsWith("/air")) ||
      (item.key === "content-system" && currentUrl.includes("/content-system")) ||
      (item.key === "transformation" && currentUrl.includes("/ai-business-transformation") && !currentUrl.includes("/content-system") && !currentUrl.includes("/campaign"))
    ) {
      a.className = "eco-active";
    }
    linksWrap.appendChild(a);
  });

  inner.appendChild(brand);
  inner.appendChild(linksWrap);
  bar.appendChild(inner);

  if (position === "top") {
    document.body.insertBefore(bar, document.body.firstChild);
  } else {
    document.body.appendChild(bar);
  }
})();
