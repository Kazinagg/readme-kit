// Pixel Readme Kit Studio Core JavaScript
    let renderTimer = null;
    let sseSource = null;
    let debugMode = false;
    let editorMode = 'edit';
    let templateBlocks = [];
    let currentEditingBlockId = null;
    let currentEditingBlockOriginal = null;
    let targetInsertAfterId = -1;
    let isParsingRaw = false;
    let activePreviewTheme = 'dark';

    const PRESET_COLORS = {
      cyberpunk:        { primary: "#00c8d7", accent: "#a855f7", tertiary: "#ff0055" },
      "neon-matrix":    { primary: "#00ff66", accent: "#79ffe1", tertiary: "#00dd44" },
      matrix:           { primary: "#00ff66", accent: "#79ffe1", tertiary: "#00dd44" },
      synthwave:        { primary: "#ff71ce", accent: "#01cdfe", tertiary: "#05ffa1" },
      amber:            { primary: "#ffb000", accent: "#ffe57f", tertiary: "#ff8800" },
      tactical:         { primary: "#f59e0b", accent: "#ea580c", tertiary: "#ef4444" },
      minimal:          { primary: "#4f8bff", accent: "#a855f7", tertiary: "#06b6d4" },
      tokyo:            { primary: "#7aa2f7", accent: "#7dcfff", tertiary: "#bb9af7" },
      "clean-mono":     { primary: "#e2e8f0", accent: "#94a3b8", tertiary: "#cbd5e1" },
      "slate-dark":     { primary: "#38bdf8", accent: "#818cf8", tertiary: "#06b6d4" },
      "modern-clean":   { primary: "#38bdf8", accent: "#818cf8", tertiary: "#06b6d4" },
      "nordic-frost":   { primary: "#e0f2fe", accent: "#38bdf8", tertiary: "#7dd3fc" },
      "linear-violet":  { primary: "#8b5cf6", accent: "#c084fc", tertiary: "#a855f7" },
      "emerald-clean":  { primary: "#10b981", accent: "#34d399", tertiary: "#059669" },
      "modern-slate":   { primary: "#2dd4bf", accent: "#a78bfa", tertiary: "#f43f5e" },
      "rough-doodle":   { primary: "#4f46e5", accent: "#059669", tertiary: "#d97706" },
      "excali-dark":    { primary: "#a78bfa", accent: "#6ee7b7", tertiary: "#fde047" },
      whiteboard:       { primary: "#38bdf8", accent: "#f87171", tertiary: "#fbbf24" },
      "notebook-graph": { primary: "#f3f4f6", accent: "#facc15", tertiary: "#fb923c" },
      "blueprint-sketch":{ primary: "#f8fafc", accent: "#38bdf8", tertiary: "#7dd3fc" }
    };

    function toggleInspector() {
      const panel = document.getElementById("inspector-panel");
      panel.classList.toggle("collapsed");
      const btn = document.getElementById("btn-toggle-inspector");
      if (panel.classList.contains("collapsed")) {
        btn.classList.remove("active-btn");
      } else {
        btn.classList.add("active-btn");
      }
    }

    function openInspector() {
      const panel = document.getElementById("inspector-panel");
      panel.classList.remove("collapsed");
      document.getElementById("btn-toggle-inspector").classList.add("active-btn");
    }

    function toggleDebugMode() {
      debugMode = !debugMode;
      const box = document.getElementById("live-svg-box");
      const btn = document.getElementById("btn-debug");
      const body = document.body;

      if (debugMode) {
        box.classList.add("debug-active");
        body.classList.add("debug-active");
        btn.classList.add("active-btn");
        btn.style.background = "var(--studio-amber)";
        btn.style.color = "#000";
        btn.style.borderColor = "var(--studio-amber)";
      } else {
        box.classList.remove("debug-active");
        body.classList.remove("debug-active");
        btn.classList.remove("active-btn");
        btn.style.background = "";
        btn.style.color = "";
        btn.style.borderColor = "";
      }
    }

    // --- Global Studio Theme Controller (Auto / Dark / Light) ---
    let currentStudioThemeMode = "dark";
    const studioSystemThemeMedia = window.matchMedia("(prefers-color-scheme: light)");

    function applyStudioTheme(isLight) {
      if (isLight) {
        document.documentElement.setAttribute("data-theme", "light");
      } else {
        document.documentElement.setAttribute("data-theme", "dark");
      }
    }

    function handleStudioSystemThemeChange(e) {
      if (currentStudioThemeMode === "auto") {
        applyStudioTheme(e.matches);
        switchPreviewTheme(e.matches ? "light" : "dark");
      }
    }
    if (studioSystemThemeMedia.addEventListener) {
      studioSystemThemeMedia.addEventListener("change", handleStudioSystemThemeChange);
    } else if (studioSystemThemeMedia.addListener) {
      studioSystemThemeMedia.addListener(handleStudioSystemThemeChange);
    }

    function setStudioTheme(mode) {
      currentStudioThemeMode = mode;
      try { localStorage.setItem("prk_studio_theme", mode); } catch (_) {}

      const btnAuto = document.getElementById("btn-studio-theme-auto");
      const btnDark = document.getElementById("btn-studio-theme-dark");
      const btnLight = document.getElementById("btn-studio-theme-light");
      if (btnAuto) btnAuto.classList.toggle("active", mode === "auto");
      if (btnDark) btnDark.classList.toggle("active", mode === "dark");
      if (btnLight) btnLight.classList.toggle("active", mode === "light");

      const isLight = (mode === "auto") ? studioSystemThemeMedia.matches : (mode === "light");
      applyStudioTheme(isLight);
      if (activePreviewTheme === "sync") {
        switchPreviewTheme("sync");
      } else {
        updateCatalogPreviews(true);
      }
    }

    function switchPreviewTheme(theme) {
      activePreviewTheme = theme;
      try { localStorage.setItem("pk_preview_theme", theme); } catch (_) {}
      const scrollArea = document.getElementById("preview-scroll-area");
      const mdBody = document.getElementById("readme-preview-content");
      const tabSync = document.getElementById("tab-preview-sync");
      const tabDark = document.getElementById("tab-dark");
      const tabLight = document.getElementById("tab-light");
      const liveBox = document.getElementById("live-svg-box");

      if (tabSync) tabSync.classList.toggle("active", theme === "sync");
      if (tabDark) tabDark.classList.toggle("active", theme === "dark");
      if (tabLight) tabLight.classList.toggle("active", theme === "light");

      let effectiveTheme = theme;
      if (theme === "sync") {
        const isStudioLight = (currentStudioThemeMode === "auto")
          ? studioSystemThemeMedia.matches
          : (currentStudioThemeMode === "light");
        effectiveTheme = isStudioLight ? "light" : "dark";
      }

      const readmeWrapper = document.querySelector(".gh-readme-wrapper");
      if (effectiveTheme === "light") {
        if (scrollArea) {
          scrollArea.classList.remove("dark-theme");
          scrollArea.classList.add("light-theme");
          scrollArea.setAttribute("data-color-mode", "light");
          scrollArea.setAttribute("data-theme", "light");
        }
        if (readmeWrapper) {
          readmeWrapper.classList.remove("dark-theme");
          readmeWrapper.classList.add("light-theme");
          readmeWrapper.setAttribute("data-color-mode", "light");
          readmeWrapper.setAttribute("data-theme", "light");
        }
        if (mdBody) {
          mdBody.setAttribute("data-color-mode", "light");
          mdBody.setAttribute("data-theme", "light");
        }
        if (liveBox) liveBox.classList.add("light-preview");
      } else {
        if (scrollArea) {
          scrollArea.classList.remove("light-theme");
          scrollArea.classList.add("dark-theme");
          scrollArea.setAttribute("data-color-mode", "dark");
          scrollArea.setAttribute("data-theme", "dark");
        }
        if (readmeWrapper) {
          readmeWrapper.classList.remove("light-theme");
          readmeWrapper.classList.add("dark-theme");
          readmeWrapper.setAttribute("data-color-mode", "dark");
          readmeWrapper.setAttribute("data-theme", "dark");
        }
        if (mdBody) {
          mdBody.setAttribute("data-color-mode", "dark");
          mdBody.setAttribute("data-theme", "dark");
        }
        if (liveBox) liveBox.classList.remove("light-preview");
      }
      const catSidebar = document.getElementById("catalog-sidebar");
      if (catSidebar) {
        catSidebar.classList.toggle("light-catalog", effectiveTheme === "light");
      }
      document.querySelectorAll(".catalog-card-preview").forEach(el => {
        el.classList.toggle("light-preview", effectiveTheme === "light");
      });
      loadCompiledPreview();
      renderCurrentBlock(false);
      updateCatalogPreviews(true);
    }

    // --- View Mode vs Edit Mode Logic ---
    let currentStudioMode = "edit";
    let cachedEditHtml = "";
    let cachedViewHtml = "";

    function setStudioMode(mode) {
      currentStudioMode = mode;
      try { localStorage.setItem("pk_studio_mode", mode); } catch (_) {}
      const editTab = document.getElementById("tab-mode-edit");
      const viewTab = document.getElementById("tab-mode-view");
      const previewArea = document.getElementById("readme-preview-content");

      if (mode === "view") {
        if (editTab) editTab.classList.remove("active");
        if (viewTab) viewTab.classList.add("active");
        if (previewArea) {
          previewArea.classList.add("view-mode");
          if (cachedViewHtml) {
            previewArea.innerHTML = cachedViewHtml;
          }
        }
      } else {
        if (editTab) editTab.classList.add("active");
        if (viewTab) viewTab.classList.remove("active");
        if (previewArea) {
          previewArea.classList.remove("view-mode");
          if (cachedEditHtml) {
            previewArea.innerHTML = cachedEditHtml;
          }
          if (currentEditingBlockId !== null) {
            highlightBlockInPreview(currentEditingBlockId);
          }
        }
      }
    }

    // --- 3-Tier Architecture: Style (3) -> Theme (5) -> Color Preset ---
    const STYLE_CANONICAL_THEMES_MAP = {
      pixel: ["cyberpunk", "tactical", "minimal"],
      modern: ["modern-clean"],
      sketch: ["rough-doodle"]
    };

    const THEME_PRESETS_MAP = {
      "cyberpunk": ["cyberpunk", "neon-matrix", "matrix", "synthwave", "amber"],
      "tactical": ["tactical", "amber"],
      "minimal": ["minimal", "tokyo", "clean-mono"],
      "modern-clean": ["slate-dark", "nordic-frost", "linear-violet", "emerald-clean", "modern-slate", "clean-mono"],
      "rough-doodle": ["excali-dark", "whiteboard", "notebook-graph", "blueprint-sketch"]
    };

    // Backward-compatible alias for existing extensions
    const STYLE_THEMES_MAP = {
      pixel: ["cyberpunk", "tactical", "minimal", "amber", "tokyo", "matrix"],
      modern: ["modern-clean", "slate-dark", "nordic-frost", "linear-violet", "emerald-clean"],
      sketch: ["rough-doodle", "excali-dark", "whiteboard", "notebook-graph", "blueprint-sketch"]
    };

    window.STYLE_CANONICAL_THEMES_MAP = STYLE_CANONICAL_THEMES_MAP;
    window.THEME_PRESETS_MAP = THEME_PRESETS_MAP;
    window.STYLE_THEMES_MAP = STYLE_THEMES_MAP;

    function getStyleAndThemeForPreset(preset) {
      if (!preset) return { style: "pixel", theme: "cyberpunk" };
      for (const [theme, pList] of Object.entries(THEME_PRESETS_MAP)) {
        if (pList.includes(preset) || theme === preset) {
          for (const [st, thList] of Object.entries(STYLE_CANONICAL_THEMES_MAP)) {
            if (thList.includes(theme)) {
              return { style: st, theme: theme };
            }
          }
        }
      }
      return { style: "pixel", theme: "cyberpunk" };
    }

    function getStyleForPreset(preset) {
      return getStyleAndThemeForPreset(preset).style;
    }

    function updateThemeOptions(selectEl, style, selectedTheme = null) {
      if (!selectEl) return;
      const themes = STYLE_CANONICAL_THEMES_MAP[style] || STYLE_CANONICAL_THEMES_MAP.pixel;
      selectEl.innerHTML = "";
      themes.forEach(t => {
        const opt = document.createElement("option");
        opt.value = t;
        opt.textContent = t.replace(/-/g, " ").toUpperCase();
        selectEl.appendChild(opt);
      });
      if (selectedTheme && themes.includes(selectedTheme)) {
        selectEl.value = selectedTheme;
      } else {
        selectEl.value = themes[0];
      }
    }

    function updatePresetOptions(selectEl, theme, includeCustom = false, selectedPreset = null) {
      if (!selectEl) return;
      const presets = THEME_PRESETS_MAP[theme] || (THEME_PRESETS_MAP["cyberpunk"]);
      selectEl.innerHTML = "";
      presets.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p;
        opt.textContent = p.replace(/-/g, " ").toUpperCase();
        selectEl.appendChild(opt);
      });
      if (includeCustom) {
        const customOpt = document.createElement("option");
        customOpt.value = "custom";
        customOpt.textContent = "CUSTOM (HEX PICKERS)";
        selectEl.appendChild(customOpt);
      }
      if (selectedPreset && (presets.includes(selectedPreset) || (includeCustom && selectedPreset === "custom"))) {
        selectEl.value = selectedPreset;
      } else {
        selectEl.value = presets[0];
      }
    }

    // 3-Tier Controls in Top Navbar
    function selectTopNavStyle(style) {
      // 1. Update Top Nav segmented buttons
      ["pixel", "modern", "sketch"].forEach(s => {
        const btn = document.getElementById(`btn-top-style-${s}`);
        if (btn) {
          if (s === style) btn.classList.add("active");
          else btn.classList.remove("active");
        }
      });

      // 2. Sync Inspector Global Style selector
      const selGlobalStyle = document.getElementById("sel-global-style");
      if (selGlobalStyle && selGlobalStyle.value !== style) {
        selGlobalStyle.value = style;
      }

      // 3. Update Theme options for Top Nav and Inspector
      const topNavThemeSelect = document.getElementById("top-nav-theme-select");
      const selGlobalTheme = document.getElementById("sel-global-theme");
      const currTheme = selGlobalTheme ? selGlobalTheme.value : null;

      updateThemeOptions(topNavThemeSelect, style, currTheme);
      updateThemeOptions(selGlobalTheme, style, currTheme);

      const activeTheme = selGlobalTheme ? selGlobalTheme.value : STYLE_CANONICAL_THEMES_MAP[style][0];

      // 4. Update Preset options for Top Nav and Inspector
      const topNavPresetSelect = document.getElementById("top-nav-preset-select");
      const selGlobalPreset = document.getElementById("sel-global-preset");
      const currPreset = (selGlobalPreset && selGlobalPreset.value !== "custom") ? selGlobalPreset.value : null;

      updatePresetOptions(topNavPresetSelect, activeTheme, false, currPreset);
      updatePresetOptions(selGlobalPreset, activeTheme, true, currPreset);

      onGlobalPresetChange();
    }

    function onTopNavThemeChange() {
      const topNavThemeSelect = document.getElementById("top-nav-theme-select");
      const selGlobalTheme = document.getElementById("sel-global-theme");
      if (topNavThemeSelect && selGlobalTheme) {
        selGlobalTheme.value = topNavThemeSelect.value;
      }
      const activeTheme = topNavThemeSelect ? topNavThemeSelect.value : "cyberpunk";

      const topNavPresetSelect = document.getElementById("top-nav-preset-select");
      const selGlobalPreset = document.getElementById("sel-global-preset");
      updatePresetOptions(topNavPresetSelect, activeTheme, false);
      updatePresetOptions(selGlobalPreset, activeTheme, true);

      onGlobalPresetChange();
    }

    function onTopNavPresetChange() {
      const topNavPresetSelect = document.getElementById("top-nav-preset-select");
      const selGlobalPreset = document.getElementById("sel-global-preset");
      if (topNavPresetSelect && selGlobalPreset) {
        selGlobalPreset.value = topNavPresetSelect.value;
        onGlobalPresetChange();
      }
    }

    function onGlobalStyleChange() {
      const selGlobalStyle = document.getElementById("sel-global-style");
      if (selGlobalStyle) {
        selectTopNavStyle(selGlobalStyle.value);
      }
    }

    function onGlobalThemeChange() {
      const selGlobalTheme = document.getElementById("sel-global-theme");
      const topNavThemeSelect = document.getElementById("top-nav-theme-select");
      if (selGlobalTheme && topNavThemeSelect) {
        topNavThemeSelect.value = selGlobalTheme.value;
      }
      const activeTheme = selGlobalTheme ? selGlobalTheme.value : "cyberpunk";

      const topNavPresetSelect = document.getElementById("top-nav-preset-select");
      const selGlobalPreset = document.getElementById("sel-global-preset");
      updatePresetOptions(topNavPresetSelect, activeTheme, false);
      updatePresetOptions(selGlobalPreset, activeTheme, true);

      onGlobalPresetChange();
    }

    function onBlockStyleChange() {
      const selStyle = document.getElementById("sel-style");
      const selTheme = document.getElementById("sel-theme");
      const selPreset = document.getElementById("sel-preset");
      if (selStyle && selTheme) {
        updateThemeOptions(selTheme, selStyle.value);
        const activeTheme = selTheme.value;
        if (selPreset) {
          updatePresetOptions(selPreset, activeTheme, false);
        }
        onBlockPresetChange();
      }
    }

    function onBlockThemeChange() {
      const selTheme = document.getElementById("sel-theme");
      const selPreset = document.getElementById("sel-preset");
      if (selTheme && selPreset) {
        updatePresetOptions(selPreset, selTheme.value, false);
        onBlockPresetChange();
      }
    }

    function onBlockPresetChange() {
      const selPreset = document.getElementById("sel-preset");
      const preset = selPreset ? selPreset.value : "cyberpunk";
      if (PRESET_COLORS[preset]) {
        document.getElementById("inp-primary").value = PRESET_COLORS[preset].primary;
        document.getElementById("picker-primary").value = PRESET_COLORS[preset].primary;
        document.getElementById("inp-accent").value = PRESET_COLORS[preset].accent;
        document.getElementById("picker-accent").value = PRESET_COLORS[preset].accent;
        if (document.getElementById("inp-tertiary")) {
          document.getElementById("inp-tertiary").value = PRESET_COLORS[preset].tertiary || "#ff0055";
          document.getElementById("picker-tertiary").value = PRESET_COLORS[preset].tertiary || "#ff0055";
        }
      }
      debounceRender();
    }

    // --- Global Theme Logic ---
    function onGlobalPresetChange() {
      const selGlobalPreset = document.getElementById("sel-global-preset");
      const preset = selGlobalPreset ? selGlobalPreset.value : "cyberpunk";
      const primPicker = document.getElementById("picker-global-primary");
      const primText = document.getElementById("inp-global-primary");
      const accPicker = document.getElementById("picker-global-accent");
      const accText = document.getElementById("inp-global-accent");
      const tertPicker = document.getElementById("picker-global-tertiary");
      const tertText = document.getElementById("inp-global-tertiary");

      // Keep top nav preset select in sync if not custom
      const topNavPresetSelect = document.getElementById("top-nav-preset-select");
      if (topNavPresetSelect && preset !== "custom") {
        topNavPresetSelect.value = preset;
      }

      if (preset === "custom") {
        primPicker.style.boxShadow = "0 0 6px var(--studio-teal)";
        accPicker.style.boxShadow = "0 0 6px var(--studio-purple)";
        if (tertPicker) tertPicker.style.boxShadow = "0 0 6px #ff0055";
        return;
      }
      primPicker.style.boxShadow = "none";
      accPicker.style.boxShadow = "none";
      if (tertPicker) tertPicker.style.boxShadow = "none";

      if (PRESET_COLORS[preset]) {
        primPicker.value = PRESET_COLORS[preset].primary;
        primText.value = PRESET_COLORS[preset].primary;
        accPicker.value = PRESET_COLORS[preset].accent;
        accText.value = PRESET_COLORS[preset].accent;
        if (tertPicker && tertText) {
          tertPicker.value = PRESET_COLORS[preset].tertiary || "#ff0055";
          tertText.value = PRESET_COLORS[preset].tertiary || "#ff0055";
        }
      }
      if (typeof updateCatalogPreviews === "function") {
        updateCatalogPreviews();
      }
    }

    function onGlobalModeChange() {
      if (typeof updateCatalogPreviews === "function") {
        updateCatalogPreviews();
      }
    }

    function syncGlobalColor(type, from) {
      const picker = document.getElementById(`picker-global-${type}`);
      const text = document.getElementById(`inp-global-${type}`);
      if (from === "picker") {
        text.value = picker.value;
      } else {
        if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) {
          picker.value = text.value;
        }
      }
      const selPreset = document.getElementById("sel-global-preset");
      if (selPreset && selPreset.value !== "custom") {
        selPreset.value = "custom";
        onGlobalPresetChange();
      } else if (typeof updateCatalogPreviews === "function") {
        updateCatalogPreviews();
      }
    }

    async function applyGlobalThemeToAllBlocks(force = false) {
      const activeStyleBtn = document.querySelector(".style-switch-group .seg-btn.active");
      const gStyle = activeStyleBtn ? (activeStyleBtn.id.replace("btn-top-style-", "") || "pixel") : (document.getElementById("sel-global-style") ? document.getElementById("sel-global-style").value : "pixel");
      const gTheme = document.getElementById("top-nav-theme-select") ? document.getElementById("top-nav-theme-select").value : (document.getElementById("sel-global-theme") ? document.getElementById("sel-global-theme").value : "cyberpunk");
      const gPreset = document.getElementById("top-nav-preset-select") ? document.getElementById("top-nav-preset-select").value : (document.getElementById("sel-global-preset") ? document.getElementById("sel-global-preset").value : "cyberpunk");
      const gMode = document.getElementById("sel-global-mode") ? document.getElementById("sel-global-mode").value : "auto";
      const gPrim = document.getElementById("inp-global-primary").value.trim();
      const gAcc = document.getElementById("inp-global-accent").value.trim();
      const gTert = document.getElementById("inp-global-tertiary") ? document.getElementById("inp-global-tertiary").value.trim() : "";

      try {
        const resp = await fetch("/api/template/apply_global_theme", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            style: gStyle,
            theme: gTheme,
            preset: gPreset,
            mode: gMode,
            primary: gPrim,
            accent: gAcc,
            tertiary: gTert,
            force: !!force
          })
        });
        if (resp.ok) {
          const msg = force ? "[OK] FORCE OVERRIDE APPLIED TO ALL BLOCKS" : "[OK] SOFT APPLY COMPLETED (ACCENTS PRESERVED)";
          flashNotification(msg, "var(--studio-green)");
          await loadTemplateBlocks(currentEditingBlockId);
          await loadCompiledPreview();
        } else {
          const err = await resp.text();
          alert("Failed to apply global theme: " + err);
        }
      } catch (err) {
        console.error("Error applying global theme:", err);
        alert("Error applying global theme: " + err);
      }
    }

    // --- Block Level Theme & Preset / Custom Hex Interaction ---
    function onInheritThemeToggle() {
      const inherit = document.getElementById("chk-inherit-theme").checked;
      const overrideBox = document.getElementById("block-theme-override-controls");
      if (inherit) {
        overrideBox.style.display = "none";
      } else {
        overrideBox.style.display = "block";
      }
      debounceRender();
    }

    function onBlockColorModeToggle() {
      const isCustom = document.getElementById("rad-custom").checked;
      const row = document.getElementById("row-custom-colors");
      if (isCustom) {
        row.style.opacity = "1";
        row.style.pointerEvents = "auto";
      } else {
        row.style.opacity = "0.4";
        row.style.pointerEvents = "none";
        onBlockPresetChange();
      }
      debounceRender();
    }

    function syncBlockColor(type, from) {
      document.getElementById("rad-custom").checked = true;
      document.getElementById("row-custom-colors").style.opacity = "1";
      document.getElementById("row-custom-colors").style.pointerEvents = "auto";

      const picker = document.getElementById(`picker-${type}`);
      const text = document.getElementById(`inp-${type}`);
      if (from === "picker") {
        text.value = picker.value;
      } else {
        if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) {
          picker.value = text.value;
        }
      }
      debounceRender();
    }

    const GITHUB_ALERT_COLORS = {
      NOTE: "#2f81f7",
      TIP: "#238636",
      IMPORTANT: "#8957e5",
      WARNING: "#d29922",
      CAUTION: "#f85149",
      CRITICAL: "#f85149",
      SUCCESS: "#238636",
      INFO: "#8957e5"
    };

    function onQuoteBadgeChange() {
      const badge = document.getElementById("sel-quote-badge").value.toUpperCase();
      const isCustom = document.getElementById("chk-quote-custom-badge").checked;
      if (!isCustom && GITHUB_ALERT_COLORS[badge]) {
        document.getElementById("picker-quote-badge-color").value = GITHUB_ALERT_COLORS[badge];
        document.getElementById("inp-quote-badge-color").value = GITHUB_ALERT_COLORS[badge];
      }
      debounceRender();
    }

    function onQuoteCustomBadgeToggle() {
      const isCustom = document.getElementById("chk-quote-custom-badge").checked;
      document.getElementById("quote-badge-color-group").style.display = isCustom ? "block" : "none";
      if (!isCustom) {
        const badge = document.getElementById("sel-quote-badge").value.toUpperCase();
        if (GITHUB_ALERT_COLORS[badge]) {
          document.getElementById("picker-quote-badge-color").value = GITHUB_ALERT_COLORS[badge];
          document.getElementById("inp-quote-badge-color").value = GITHUB_ALERT_COLORS[badge];
        }
      }
      updateContextualVisibility();
      debounceRender();
    }

    function syncQuoteBadgeColor(from) {
      const picker = document.getElementById("picker-quote-badge-color");
      const text = document.getElementById("inp-quote-badge-color");
      if (from === "picker") {
        text.value = picker.value;
      } else {
        if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) picker.value = text.value;
      }
      debounceRender();
    }

    function onCalloutTypeChange() {
      const ctype = document.getElementById("sel-callout-type").value.toUpperCase();
      const isCustom = document.getElementById("chk-callout-custom-badge").checked;
      if (!isCustom && GITHUB_ALERT_COLORS[ctype]) {
        document.getElementById("picker-callout-badge-color").value = GITHUB_ALERT_COLORS[ctype];
        document.getElementById("inp-callout-badge-color").value = GITHUB_ALERT_COLORS[ctype];
      }
      debounceRender();
    }

    function onCalloutCustomBadgeToggle() {
      const isCustom = document.getElementById("chk-callout-custom-badge").checked;
      document.getElementById("callout-badge-color-group").style.display = isCustom ? "block" : "none";
      if (!isCustom) {
        const ctype = document.getElementById("sel-callout-type").value.toUpperCase();
        if (GITHUB_ALERT_COLORS[ctype]) {
          document.getElementById("picker-callout-badge-color").value = GITHUB_ALERT_COLORS[ctype];
          document.getElementById("inp-callout-badge-color").value = GITHUB_ALERT_COLORS[ctype];
        }
      }
      updateContextualVisibility();
      debounceRender();
    }

    function syncCalloutBadgeColor(from) {
      const picker = document.getElementById("picker-callout-badge-color");
      const text = document.getElementById("inp-callout-badge-color");
      if (from === "picker") {
        text.value = picker.value;
      } else {
        if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) picker.value = text.value;
      }
      debounceRender();
    }

    function syncProgressInput(from) {
      const rng = document.getElementById("rng-progress-val");
      const num = document.getElementById("inp-progress-val");
      const lbl = document.getElementById("lbl-progress-num");
      if (from === "range") {
        num.value = rng.value;
      } else {
        rng.value = num.value;
      }
      lbl.innerText = `${rng.value}%`;
      debounceRender();
    }

    function addSampleMilestone() {
      const area = document.getElementById("inp-timeline-milestones");
      const count = area.value.split("\n").filter(l => l.trim()).length + 1;
      const sample = `milestone title="PHASE ${count}: MILESTONE" date="2026-Q${count % 4 + 1}" status="PLANNED" desc="Milestone deliverables and specification"`;
      if (area.value.trim()) {
        area.value = area.value.trim() + "\n" + sample;
      } else {
        area.value = sample;
      }
      debounceRender();
    }

    function updateContextualVisibility() {
      const btype = document.getElementById("sel-type").value;
      if (btype === "chip") {
        const ct = document.getElementById("sel-chip-type").value;
        const gh = document.getElementById("sel-chip-gh").value;
        const gDecay = document.getElementById("group-decay-dir");
        const rChipForm = document.getElementById("row-chip-form");
        if (gDecay) {
          const isDecay = (ct === "decay");
          gDecay.style.display = isDecay ? "flex" : "none";
          if (rChipForm) rChipForm.style.gridTemplateColumns = isDecay ? "1fr 1fr" : "1fr";
        }
        const gRepo = document.getElementById("group-chip-repo");
        const rChipGh = document.getElementById("row-chip-gh");
        if (gRepo) {
          const hasGh = (gh !== "");
          gRepo.style.display = hasGh ? "flex" : "none";
          if (rChipGh) rChipGh.style.gridTemplateColumns = hasGh ? "1fr 1fr" : "1fr";
        }
      } else if (btype === "header") {
        const isCompact = document.getElementById("chk-compact").checked;
        const gSpecs = document.getElementById("group-header-specs");
        if (gSpecs) {
          gSpecs.style.display = isCompact ? "none" : "flex";
        }
      } else if (btype === "frame") {
        const fType = document.getElementById("sel-frame-type").value;
        const isBottom = (fType === "bottom");
        const gTag = document.getElementById("group-frame-tag");
        const rCap = document.getElementById("row-frame-cap");
        const gTitle = document.getElementById("group-frame-title");
        const gTagUrl = document.getElementById("group-frame-tag-url");
        const rLinks = document.getElementById("row-frame-links");

        if (gTag) gTag.style.display = isBottom ? "none" : "flex";
        if (rCap) rCap.style.gridTemplateColumns = isBottom ? "1fr" : "1fr 1fr";
        if (gTitle) gTitle.style.display = isBottom ? "none" : "flex";
        if (gTagUrl) gTagUrl.style.display = isBottom ? "none" : "flex";
        if (rLinks) rLinks.style.gridTemplateColumns = isBottom ? "1fr" : "1fr 1fr";
      } else if (btype === "quote") {
        const isCustom = document.getElementById("chk-quote-custom-badge").checked;
        const rBadge = document.getElementById("row-quote-badge");
        if (rBadge) rBadge.style.gridTemplateColumns = isCustom ? "1fr 1fr" : "1fr";
      } else if (btype === "callout") {
        const isCustom = document.getElementById("chk-callout-custom-badge").checked;
        const rBadge = document.getElementById("row-callout-badge");
        if (rBadge) rBadge.style.gridTemplateColumns = isCustom ? "1fr 1fr" : "1fr";
      }
    }

    function selectBlockFromPreview(blockId, event) {
      if (event) event.stopPropagation();
      openInspector();
      switchEditorMode('edit');

      const foundIdx = templateBlocks.findIndex(b => b.id === blockId);
      if (foundIdx !== -1) {
        document.getElementById("sel-existing-block").value = foundIdx;
        onSelectExistingBlock();
      }
      highlightBlockInPreview(blockId);
    }

    function highlightBlockInPreview(blockId) {
      document.querySelectorAll(".pk-block-wrapper").forEach(el => {
        el.classList.remove("selected-block");
      });
      const el = document.getElementById(`pk-block-${blockId}`);
      if (el) {
        el.classList.add("selected-block");
      }
    }

    function openInsertAt(afterId, event) {
      if (event) event.stopPropagation();
      targetInsertAfterId = afterId;
      openInspector();
      switchEditorMode('insert');

      const heading = document.getElementById("lbl-inspector-heading");
      heading.innerText = (afterId === -1) ? "Insert Block at Top" : `Insert Block after #${afterId}`;

      document.getElementById("sel-type").value = "header";
      onTypeChange(true);
      document.getElementById("inp-title").value = "NEW PIXEL SECTION";
      document.getElementById("inp-subtitle").value = "SECTION DESCRIPTION // SUBTITLE";
      document.getElementById("inp-tag").value = "STATUS_OK";
      renderCurrentBlock();
    }

    function cancelInsertMode() {
      switchEditorMode('edit');
      if (templateBlocks.length > 0) {
        onSelectExistingBlock();
      } else {
        const emptyState = document.getElementById("inspector-empty-state");
        const editorContainer = document.getElementById("block-editor-container");
        if (emptyState) emptyState.style.display = "flex";
        if (editorContainer) editorContainer.style.display = "none";
      }
    }

    function switchEditorMode(mode) {
      editorMode = mode;
      const grpExisting = document.getElementById("group-existing-blocks");
      const editActions = document.getElementById("edit-mode-actions");
      const insertActions = document.getElementById("insert-mode-actions");
      const heading = document.getElementById("lbl-inspector-heading");
      const selType = document.getElementById("sel-type");
      const badgeLock = document.getElementById("badge-lock-type");
      const emptyState = document.getElementById("inspector-empty-state");
      const editorContainer = document.getElementById("block-editor-container");

      if (mode === "edit") {
        grpExisting.style.display = "flex";
        editActions.style.display = "grid";
        insertActions.style.display = "none";
        heading.innerText = "Block Parameters";
        selType.disabled = true;
        selType.title = "Block type cannot be changed after creation. To use another type, insert a new block.";
        if (badgeLock) badgeLock.style.display = "inline-block";
        if (templateBlocks.length === 0 || currentEditingBlockId === null) {
          if (emptyState) emptyState.style.display = "flex";
          if (editorContainer) editorContainer.style.display = "none";
        } else {
          if (emptyState) emptyState.style.display = "none";
          if (editorContainer) {
            editorContainer.style.display = "flex";
            editorContainer.style.flexDirection = "column";
          }
        }
      } else {
        grpExisting.style.display = "none";
        editActions.style.display = "none";
        insertActions.style.display = "grid";
        selType.disabled = false;
        selType.title = "";
        if (badgeLock) badgeLock.style.display = "none";
        if (emptyState) emptyState.style.display = "none";
        if (editorContainer) {
          editorContainer.style.display = "flex";
          editorContainer.style.flexDirection = "column";
        }
      }
    }

    async function loadTemplateBlocks(preferredId = null) {
      try {
        const resp = await fetch("/api/template/blocks");
        if (resp.ok) {
          const data = await resp.json();
          templateBlocks = data.blocks || [];
          const sel = document.getElementById("sel-existing-block");
          sel.innerHTML = "";

          const badge = document.getElementById("block-counter-badge");
          if (badge) badge.innerText = `${templateBlocks.length} blocks`;

          const emptyState = document.getElementById("inspector-empty-state");
          const editorContainer = document.getElementById("block-editor-container");

          if (templateBlocks.length === 0) {
            sel.innerHTML = "<option value=''>No blocks found</option>";
            currentEditingBlockId = null;
            if (emptyState) emptyState.style.display = "flex";
            if (editorContainer) editorContainer.style.display = "none";
            return;
          }

          templateBlocks.forEach((blk, idx) => {
            const opt = document.createElement("option");
            opt.value = idx;
            const btype = blk.type.toUpperCase();
            const title = blk.attrs.title || blk.attrs.text || blk.attrs.label || blk.attrs.status || (blk.type === "divider" ? "DIVIDER" : "");
            const displayTitle = title ? ` // ${title.slice(0, 30)}` : "";
            opt.innerText = `#${blk.id} ${btype}${displayTitle}`;
            sel.appendChild(opt);
          });

          let targetIndex = 0;
          if (preferredId !== null) {
            const foundIdx = templateBlocks.findIndex(b => b.id === preferredId);
            if (foundIdx !== -1) targetIndex = foundIdx;
          }
          sel.value = targetIndex;
          if (editorMode === "edit" && templateBlocks[targetIndex]) {
            onSelectExistingBlock();
          }
        }
      } catch (e) {
        console.error("Failed to load template blocks:", e);
      }
    }

    function onSelectExistingBlock() {
      const sel = document.getElementById("sel-existing-block");
      const idx = parseInt(sel.value, 10);
      const emptyState = document.getElementById("inspector-empty-state");
      const editorContainer = document.getElementById("block-editor-container");

      if (isNaN(idx) || !templateBlocks[idx]) {
        currentEditingBlockId = null;
        if (emptyState) emptyState.style.display = "flex";
        if (editorContainer) editorContainer.style.display = "none";
        return;
      }

      if (emptyState) emptyState.style.display = "none";
      if (editorContainer) {
        editorContainer.style.display = "flex";
        editorContainer.style.flexDirection = "column";
      }

      const blk = templateBlocks[idx];
      currentEditingBlockId = blk.id;
      currentEditingBlockOriginal = blk;

      const heading = document.getElementById("lbl-inspector-heading");
      heading.innerText = `#${blk.id} ${blk.type.toUpperCase()}`;

      const selType = document.getElementById("sel-type");
      selType.value = blk.type;
      onTypeChange(false);

      const attrs = blk.attrs || {};

      // Check whether this block uses custom theme overrides or inherits
      const hasCustomStyle = !!attrs.style;
      const hasCustomTheme = !!attrs.theme;
      const hasCustomPreset = !!attrs.preset;
      const hasCustomColors = !!(attrs.primary || attrs.accent || attrs.tertiary);
      const isCustomOverride = hasCustomStyle || hasCustomTheme || hasCustomPreset || hasCustomColors;

      const chkInherit = document.getElementById("chk-inherit-theme");
      chkInherit.checked = !isCustomOverride;
      onInheritThemeToggle();

      const resolved = getStyleAndThemeForPreset(attrs.preset);
      const blockStyle = attrs.style || resolved.style || "pixel";
      const blockTheme = attrs.theme || resolved.theme || "cyberpunk";

      const selStyle = document.getElementById("sel-style");
      if (selStyle) selStyle.value = blockStyle;
      const selTheme = document.getElementById("sel-theme");
      if (selTheme) updateThemeOptions(selTheme, blockStyle, blockTheme);
      const selPreset = document.getElementById("sel-preset");
      if (selPreset) {
        updatePresetOptions(selPreset, blockTheme, false, attrs.preset);
      }
      if (attrs.mode) document.getElementById("sel-mode").value = attrs.mode;

      if (hasCustomColors) {
        document.getElementById("rad-custom").checked = true;
        document.getElementById("row-custom-colors").style.opacity = "1";
        document.getElementById("row-custom-colors").style.pointerEvents = "auto";
        if (attrs.primary) {
          document.getElementById("inp-primary").value = attrs.primary;
          if (/^#[0-9A-Fa-f]{6}$/.test(attrs.primary)) document.getElementById("picker-primary").value = attrs.primary;
        }
        if (attrs.accent) {
          document.getElementById("inp-accent").value = attrs.accent;
          if (/^#[0-9A-Fa-f]{6}$/.test(attrs.accent)) document.getElementById("picker-accent").value = attrs.accent;
        }
        if (attrs.tertiary) {
          document.getElementById("inp-tertiary").value = attrs.tertiary;
          if (/^#[0-9A-Fa-f]{6}$/.test(attrs.tertiary)) document.getElementById("picker-tertiary").value = attrs.tertiary;
        }
      } else {
        document.getElementById("rad-preset").checked = true;
        document.getElementById("row-custom-colors").style.opacity = "0.4";
        document.getElementById("row-custom-colors").style.pointerEvents = "none";
        onBlockPresetChange();
      }

      // 1. Header
      document.getElementById("inp-title").value = attrs.title || attrs.text || attrs.label || attrs.status || "";
      document.getElementById("inp-subtitle").value = attrs.subtitle || attrs.sub || "";
      document.getElementById("inp-tag").value = attrs.tag || "";
      document.getElementById("inp-spec1").value = attrs.spec1 || "";
      document.getElementById("inp-spec2").value = attrs.spec2 || "";
      document.getElementById("inp-spec3").value = attrs.spec3 || "";
      document.getElementById("inp-tag-url").value = attrs.tag_url || attrs.tag_href || "";
      document.getElementById("inp-close-url").value = attrs.close_url || attrs.close_href || "";
      document.getElementById("chk-compact").checked = (attrs.compact === "true" || attrs.compact === "1");

      // 2. Timeline
      document.getElementById("inp-timeline-milestones").value = blk.body || "";

      // 3. Window
      document.getElementById("inp-window-title").value = attrs.title || "SYSTEM.WINDOW";
      document.getElementById("inp-window-tag").value = attrs.tag || "[SYS_LOG]";
      document.getElementById("inp-window-tag-url").value = attrs.tag_url || "";
      document.getElementById("inp-window-close-url").value = attrs.close_url || "";

      // 4. Terminal
      document.getElementById("inp-terminal-title").value = attrs.title || "HUD.TERMINAL";
      document.getElementById("sel-terminal-state").value = (attrs.state && attrs.state.toLowerCase() === "closed") ? "closed" : "open";

      // 5. Quote
      document.getElementById("inp-quote-title").value = attrs.title || "SPECIFICATION NOTICE";
      document.getElementById("inp-quote-sub").value = attrs.subtitle || "";
      const qBadgeVal = (attrs.badge || "NOTE").toUpperCase();
      document.getElementById("sel-quote-badge").value = qBadgeVal;
      if (attrs.badge_color) {
        document.getElementById("chk-quote-custom-badge").checked = true;
        document.getElementById("quote-badge-color-group").style.display = "block";
        document.getElementById("picker-quote-badge-color").value = attrs.badge_color;
        document.getElementById("inp-quote-badge-color").value = attrs.badge_color;
      } else {
        document.getElementById("chk-quote-custom-badge").checked = false;
        document.getElementById("quote-badge-color-group").style.display = "none";
        const defCol = GITHUB_ALERT_COLORS[qBadgeVal] || "#2f81f7";
        document.getElementById("picker-quote-badge-color").value = defCol;
        document.getElementById("inp-quote-badge-color").value = defCol;
      }

      // 6. Chip
      document.getElementById("inp-chip-text").value = attrs.text || attrs.title || "CHIP";
      if (attrs.type) document.getElementById("sel-chip-type").value = attrs.type;
      if (attrs.decay_dir) document.getElementById("sel-decay-dir").value = attrs.decay_dir;
      if (attrs.github) document.getElementById("sel-chip-gh").value = attrs.github;
      if (attrs.repo) document.getElementById("inp-chip-repo").value = attrs.repo;
      document.getElementById("inp-chip-width").value = attrs.width || "";
      document.getElementById("inp-chip-url").value = attrs.url || attrs.href || "";

      // 7. Metrics
      document.getElementById("inp-metrics-items").value = attrs.items || blk.body || "";
      document.getElementById("inp-metrics-label").value = attrs.label || attrs.title || "";
      document.getElementById("inp-metrics-val").value = attrs.value || attrs.subtitle || "";
      document.getElementById("inp-metrics-delta").value = attrs.delta || attrs.tag || "";
      document.getElementById("inp-metrics-status").value = attrs.status || "";

      // 8. Progress
      const pVal = parseInt(attrs.value || attrs.tag || "75", 10) || 75;
      document.getElementById("rng-progress-val").value = pVal;
      document.getElementById("inp-progress-val").value = pVal;
      document.getElementById("lbl-progress-num").innerText = `${pVal}%`;
      document.getElementById("inp-progress-label").value = attrs.label || attrs.title || "PROGRESS";
      document.getElementById("inp-progress-sub").value = attrs.sub || attrs.subtitle || "";

      // 9. Techstack
      document.getElementById("inp-techstack-items").value = attrs.items || attrs.subtitle || "python,cpp,docker,git";
      document.getElementById("inp-techstack-cols").value = attrs.columns || attrs.tag || "5";

      // 10. Callout
      const cTypeVal = (attrs.type || "note").toLowerCase();
      document.getElementById("sel-callout-type").value = cTypeVal;
      document.getElementById("inp-callout-title").value = attrs.title || "SYSTEM SPECIFICATION";
      document.getElementById("inp-callout-sub").value = attrs.subtitle || "";
      document.getElementById("chk-callout-quote").checked = (attrs.quote === "true" || attrs.quote === "1");
      if (attrs.badge_color) {
        document.getElementById("chk-callout-custom-badge").checked = true;
        document.getElementById("callout-badge-color-group").style.display = "block";
        document.getElementById("picker-callout-badge-color").value = attrs.badge_color;
        document.getElementById("inp-callout-badge-color").value = attrs.badge_color;
      } else {
        document.getElementById("chk-callout-custom-badge").checked = false;
        document.getElementById("callout-badge-color-group").style.display = "none";
        const defCol = GITHUB_ALERT_COLORS[cTypeVal.toUpperCase()] || "#2f81f7";
        document.getElementById("picker-callout-badge-color").value = defCol;
        document.getElementById("inp-callout-badge-color").value = defCol;
      }

      // 11. Frame
      if (attrs.type) document.getElementById("sel-frame-type").value = attrs.type;
      document.getElementById("inp-frame-title").value = attrs.title || "SYSTEM.CORE";
      document.getElementById("inp-frame-tag").value = attrs.tag || "[OPEN_HUD]";
      document.getElementById("inp-frame-tag-url").value = attrs.tag_url || "";
      document.getElementById("inp-frame-close-url").value = attrs.close_url || "";

      // 13. Splitter
      document.getElementById("inp-splitter-label").value = attrs.label || attrs.title || "[SUB_MODULE]";

      // 14. Footer
      document.getElementById("inp-footer-status").value = attrs.status || attrs.title || "SESSION_ACTIVE // STANDBY";
      document.getElementById("inp-footer-nav").value = attrs.nav || attrs.tag || "^ RETURN TO TOP";
      document.getElementById("inp-footer-sub").value = attrs.sub || attrs.subtitle || "";

      // 15. Social
      document.getElementById("inp-social-title").value = attrs.title || "PIXEL README KIT";
      document.getElementById("inp-social-sub").value = attrs.subtitle || "";
      document.getElementById("inp-social-repo").value = attrs.repo || "Kazinagg/pixel-readme-kit";
      document.getElementById("inp-social-tags").value = attrs.tags || attrs.tag || "PYTHON,SVG";

      // Generic container body
      document.getElementById("inp-body").value = blk.body || "";

      highlightBlockInPreview(blk.id);
      updateContextualVisibility();
      renderCurrentBlock();
    }

    function onTypeChange(resetValues = true) {
      const type = document.getElementById("sel-type").value;

      const sections = {
        header: document.getElementById("section-header"),
        timeline: document.getElementById("section-timeline"),
        window: document.getElementById("section-window"),
        terminal: document.getElementById("section-terminal"),
        quote: document.getElementById("section-quote"),
        chip: document.getElementById("section-chip"),
        metrics: document.getElementById("section-metrics"),
        progress: document.getElementById("section-progress"),
        techstack: document.getElementById("section-techstack"),
        callout: document.getElementById("section-callout"),
        frame: document.getElementById("section-frame"),
        divider: document.getElementById("section-divider"),
        splitter: document.getElementById("section-splitter"),
        footer: document.getElementById("section-footer"),
        social: document.getElementById("section-social"),
        body: document.getElementById("section-body")
      };

      for (let k in sections) {
        if (sections[k]) sections[k].style.display = "none";
      }

      if (sections[type]) {
        sections[type].style.display = "flex";
      }

      if (type === "header" || type === "starchart" || type === "profile") {
        if (sections.header) sections.header.style.display = "flex";
      }

      // Container markdown body section
      if (type === "window" || type === "terminal" || type === "quote") {
        sections.body.style.display = "flex";
      }

      updateCharCounters();
      updateContextualVisibility();
      renderCurrentBlock();
    }

    function generateDirectiveCode() {
      const btype = document.getElementById("sel-type").value;
      const inheritTheme = document.getElementById("chk-inherit-theme").checked;

      let style = document.getElementById("sel-global-style").value;
      let theme = document.getElementById("sel-global-theme") ? document.getElementById("sel-global-theme").value : "cyberpunk";
      let preset = document.getElementById("sel-global-preset").value;
      let mode = document.getElementById("sel-global-mode").value;
      let isCustomColors = false;
      let prim = "";
      let acc = "";
      let tert = "";

      if (!inheritTheme) {
        style = document.getElementById("sel-style").value;
        theme = document.getElementById("sel-theme") ? document.getElementById("sel-theme").value : "cyberpunk";
        preset = document.getElementById("sel-preset").value;
        mode = document.getElementById("sel-mode").value;
        isCustomColors = document.getElementById("rad-custom").checked;
        if (isCustomColors) {
          prim = document.getElementById("inp-primary").value.trim();
          acc = document.getElementById("inp-accent").value.trim();
          tert = document.getElementById("inp-tertiary") ? document.getElementById("inp-tertiary").value.trim() : "";
        }
      }

      const origAttrs = (currentEditingBlockOriginal && currentEditingBlockOriginal.attrs) ? currentEditingBlockOriginal.attrs : {};

      let opening = `<!-- pixel-kit:${btype}`;
      if (!inheritTheme) {
        if (style) opening += ` style="${style}"`;
        if (theme) opening += ` theme="${theme}"`;
        if (preset) opening += ` preset="${preset}"`;
        if (mode && mode !== "auto") opening += ` mode="${mode}"`;
        if (isCustomColors && prim) opening += ` primary="${prim}"`;
        if (isCustomColors && acc) opening += ` accent="${acc}"`;
        if (isCustomColors && tert) opening += ` tertiary="${tert}"`;
      }

      let innerBody = "";

      if (btype === "header") {
        const title = document.getElementById("inp-title").value.trim();
        const sub = document.getElementById("inp-subtitle").value.trim();
        const tag = document.getElementById("inp-tag").value.trim();
        const s1 = document.getElementById("inp-spec1").value.trim();
        const s2 = document.getElementById("inp-spec2").value.trim();
        const s3 = document.getElementById("inp-spec3").value.trim();
        const tUrl = document.getElementById("inp-tag-url").value.trim();
        const cUrl = document.getElementById("inp-close-url").value.trim();
        const compact = document.getElementById("chk-compact").checked;

        if (title) opening += ` title="${title}"`;
        if (sub) opening += ` subtitle="${sub}"`;
        if (tag) opening += ` tag="${tag}"`;
        if (!compact && s1) opening += ` spec1="${s1}"`;
        if (!compact && s2) opening += ` spec2="${s2}"`;
        if (!compact && s3) opening += ` spec3="${s3}"`;
        if (tUrl) opening += ` tag_url="${tUrl}"`;
        if (cUrl) opening += ` close_url="${cUrl}"`;
        if (compact) opening += ` compact="true"`;
      } else if (btype === "timeline") {
        innerBody = document.getElementById("inp-timeline-milestones").value.trim();
      } else if (btype === "window") {
        const title = document.getElementById("inp-window-title").value.trim();
        const tag = document.getElementById("inp-window-tag").value.trim();
        const tUrl = document.getElementById("inp-window-tag-url").value.trim();
        const cUrl = document.getElementById("inp-window-close-url").value.trim();
        if (title) opening += ` title="${title}"`;
        if (tag) opening += ` tag="${tag}"`;
        if (tUrl) opening += ` tag_url="${tUrl}"`;
        if (cUrl) opening += ` close_url="${cUrl}"`;
        innerBody = document.getElementById("inp-body").value;
      } else if (btype === "terminal") {
        const title = document.getElementById("inp-terminal-title").value.trim();
        const state = document.getElementById("sel-terminal-state").value;
        if (title) opening += ` title="${title}"`;
        if (state) opening += ` state="${state}"`;
        innerBody = document.getElementById("inp-body").value;
      } else if (btype === "quote") {
        const title = document.getElementById("inp-quote-title").value.trim();
        const sub = document.getElementById("inp-quote-sub").value.trim();
        const badge = document.getElementById("sel-quote-badge").value;
        const isCustomBadge = document.getElementById("chk-quote-custom-badge").checked;
        const bCol = document.getElementById("inp-quote-badge-color").value.trim();
        if (title) opening += ` title="${title}"`;
        if (sub) opening += ` subtitle="${sub}"`;
        if (badge) opening += ` badge="${badge}"`;
        if (isCustomBadge && bCol) opening += ` badge_color="${bCol}"`;
        innerBody = document.getElementById("inp-body").value;
      } else if (btype === "chip") {
        const text = document.getElementById("inp-chip-text").value.trim();
        const ctype = document.getElementById("sel-chip-type").value;
        const decay = document.getElementById("sel-decay-dir").value;
        const gh = document.getElementById("sel-chip-gh").value;
        const repo = document.getElementById("inp-chip-repo").value.trim();
        const w = document.getElementById("inp-chip-width").value.trim();
        const url = document.getElementById("inp-chip-url").value.trim();

        if (text) opening += ` text="${text}"`;
        if (ctype && ctype !== "closed") opening += ` type="${ctype}"`;
        if (ctype === "decay" && decay && decay !== "right") opening += ` decay_dir="${decay}"`;
        if (gh) opening += ` github="${gh}"`;
        if (gh && repo) opening += ` repo="${repo}"`;
        if (w) opening += ` width="${w}"`;
        if (url) opening += ` url="${url}"`;
      } else if (btype === "metrics") {
        const items = document.getElementById("inp-metrics-items").value.trim();
        const lbl = document.getElementById("inp-metrics-label").value.trim();
        const val = document.getElementById("inp-metrics-val").value.trim();
        const delta = document.getElementById("inp-metrics-delta").value.trim();
        const st = document.getElementById("inp-metrics-status").value.trim();

        if (items.includes("\n") || items.startsWith("-")) {
          innerBody = items;
        } else if (items) {
          opening += ` items="${items}"`;
        } else {
          if (lbl) opening += ` label="${lbl}"`;
          if (val) opening += ` value="${val}"`;
          if (delta) opening += ` delta="${delta}"`;
          if (st) opening += ` status="${st}"`;
        }
      } else if (btype === "progress") {
        const val = document.getElementById("inp-progress-val").value;
        const lbl = document.getElementById("inp-progress-label").value.trim();
        const sub = document.getElementById("inp-progress-sub").value.trim();
        opening += ` value="${val}" label="${lbl}"`;
        if (sub) opening += ` sub="${sub}"`;
      } else if (btype === "techstack") {
        const items = document.getElementById("inp-techstack-items").value.trim();
        const cols = document.getElementById("inp-techstack-cols").value.trim();
        opening += ` items="${items}" columns="${cols}"`;
      } else if (btype === "callout") {
        const ctype = document.getElementById("sel-callout-type").value;
        const title = document.getElementById("inp-callout-title").value.trim();
        const sub = document.getElementById("inp-callout-sub").value.trim();
        const quote = document.getElementById("chk-callout-quote").checked;
        const isCustomBadge = document.getElementById("chk-callout-custom-badge").checked;
        const bCol = document.getElementById("inp-callout-badge-color").value.trim();
        opening += ` type="${ctype}" title="${title}"`;
        if (sub) opening += ` subtitle="${sub}"`;
        if (quote) opening += ` quote="true"`;
        if (isCustomBadge && bCol) opening += ` badge_color="${bCol}"`;
      } else if (btype === "frame") {
        const ftype = document.getElementById("sel-frame-type").value;
        const title = document.getElementById("inp-frame-title").value.trim();
        const tag = document.getElementById("inp-frame-tag").value.trim();
        const tUrl = document.getElementById("inp-frame-tag-url").value.trim();
        const cUrl = document.getElementById("inp-frame-close-url").value.trim();
        if (ftype === "bottom") {
          opening += ` type="bottom"`;
          if (cUrl) opening += ` close_url="${cUrl}"`;
        } else {
          opening += ` type="top" title="${title}" tag="${tag}"`;
          if (tUrl) opening += ` tag_url="${tUrl}"`;
          if (cUrl) opening += ` close_url="${cUrl}"`;
        }
      } else if (btype === "splitter") {
        const lbl = document.getElementById("inp-splitter-label").value.trim();
        opening += ` label="${lbl}"`;
      } else if (btype === "footer") {
        const st = document.getElementById("inp-footer-status").value.trim();
        const nav = document.getElementById("inp-footer-nav").value.trim();
        const sub = document.getElementById("inp-footer-sub").value.trim();
        opening += ` status="${st}" nav="${nav}"`;
        if (sub) opening += ` sub="${sub}"`;
      } else if (btype === "social") {
        const title = document.getElementById("inp-social-title").value.trim();
        const sub = document.getElementById("inp-social-sub").value.trim();
        const repo = document.getElementById("inp-social-repo").value.trim();
        const tags = document.getElementById("inp-social-tags").value.trim();
        opening += ` title="${title}" subtitle="${sub}" repo="${repo}" tags="${tags}"`;
      } else if (btype === "starchart") {
        const repo = document.getElementById("inp-title").value.trim() || "Kazinagg/pixel-readme-kit";
        opening += ` repo="${repo}" points="15,65,190,480,950,1650" current="1,650" delta="+78% past 6m" title="STAR GROWTH TRAJECTORY"`;
      } else if (btype === "profile") {
        const name = document.getElementById("inp-title").value.trim() || "ALEX DEVELOPER";
        const role = document.getElementById("inp-subtitle").value.trim() || "FULLSTACK & SYSTEMS ARCHITECT";
        opening += ` name="${name}" role="${role}" bio="Building high-performance runtimes and resilient developer tooling." status="AVAILABLE FOR HIRE" location="REMOTE" badge="LEVEL_99"`;
      }

      if (origAttrs.out) opening += ` out="${origAttrs.out}"`;
      opening += ` -->`;

      const isContainerType = (btype === "window" || btype === "terminal" || btype === "quote" || btype === "timeline" || (btype === "metrics" && innerBody));
      if (isContainerType) {
        return `${opening}\n${innerBody}\n<!-- /pixel-kit:${btype} -->`;
      }
      return opening;
    }

    function onRawDirectiveManualEdit() {
      if (isParsingRaw) return;
      const raw = document.getElementById("txt-raw-directive").value;
      const m = raw.match(/<!--\s*pixel-kit:([a-zA-Z0-9_\-]+)\b([\s\S]*?)-->/i);
      if (!m) return;

      isParsingRaw = true;
      try {
        const btype = m[1].toLowerCase();
        const attrStr = m[2];
        const selType = document.getElementById("sel-type");
        if (editorMode === "insert" && selType.querySelector(`option[value="${btype}"]`)) {
          selType.value = btype;
          onTypeChange(false);
        }

        const attrRegex = /([\w\-]+)=(?:"([^"]*)"|'([^']*)'|([^\s>]+))/g;
        let match;
        const parsed = {};
        while ((match = attrRegex.exec(attrStr)) !== null) {
          const key = match[1].toLowerCase();
          const val = match[2] !== undefined ? match[2] : (match[3] !== undefined ? match[3] : match[4]);
          parsed[key] = val;
        }

        const hasCustom = parsed.style || parsed.theme || parsed.preset || parsed.primary || parsed.accent;
        document.getElementById("chk-inherit-theme").checked = !hasCustom;
        onInheritThemeToggle();

        const resolved = getStyleAndThemeForPreset(parsed.preset);
        const blockStyle = parsed.style || resolved.style || "pixel";
        const blockTheme = parsed.theme || resolved.theme || "cyberpunk";

        const selStyle = document.getElementById("sel-style");
        if (selStyle) selStyle.value = blockStyle;
        const selTheme = document.getElementById("sel-theme");
        if (selTheme) updateThemeOptions(selTheme, blockStyle, blockTheme);
        const selPreset = document.getElementById("sel-preset");
        if (selPreset) {
          updatePresetOptions(selPreset, blockTheme, false, parsed.preset);
        }
        if (parsed.mode) document.getElementById("sel-mode").value = parsed.mode;
        if (parsed.primary || parsed.accent) {
          document.getElementById("rad-custom").checked = true;
          document.getElementById("row-custom-colors").style.opacity = "1";
          document.getElementById("row-custom-colors").style.pointerEvents = "auto";
          if (parsed.primary) {
            document.getElementById("inp-primary").value = parsed.primary;
            if (/^#[0-9A-Fa-f]{6}$/.test(parsed.primary)) document.getElementById("picker-primary").value = parsed.primary;
          }
          if (parsed.accent) {
            document.getElementById("inp-accent").value = parsed.accent;
            if (/^#[0-9A-Fa-f]{6}$/.test(parsed.accent)) document.getElementById("picker-accent").value = parsed.accent;
          }
        }

        if (parsed.title) document.getElementById("inp-title").value = parsed.title;
        if (parsed.subtitle) document.getElementById("inp-subtitle").value = parsed.subtitle;
        if (parsed.tag) document.getElementById("inp-tag").value = parsed.tag;
        if (parsed.spec1) document.getElementById("inp-spec1").value = parsed.spec1;
        if (parsed.spec2) document.getElementById("inp-spec2").value = parsed.spec2;
        if (parsed.spec3) document.getElementById("inp-spec3").value = parsed.spec3;
        if (parsed.compact !== undefined) document.getElementById("chk-compact").checked = (parsed.compact === "true" || parsed.compact === "1");

        updateCharCounters();
        updateContextualVisibility();
        renderCurrentBlock(false);
      } finally {
        isParsingRaw = false;
      }
    }

    function updateCharCounters() {
      const title = document.getElementById("inp-title").value || "";
      const sub = document.getElementById("inp-subtitle").value || "";
      const s1 = document.getElementById("inp-spec1").value || "";
      const s2 = document.getElementById("inp-spec2").value || "";
      const s3 = document.getElementById("inp-spec3").value || "";

      const bTitle = document.getElementById("badge-title-budget");
      const bSub = document.getElementById("badge-sub-budget");
      const bS1 = document.getElementById("badge-spec1-budget");
      const bS2 = document.getElementById("badge-spec2-budget");
      const bS3 = document.getElementById("badge-spec3-budget");

      if (bTitle) {
        const len = title.length;
        bTitle.innerText = `${len} chars`;
        bTitle.className = "char-badge " + (len <= 14 ? "badge-optimal" : (len <= 20 ? "badge-warning" : "badge-danger"));
      }
      if (bSub) {
        const len = sub.length;
        bSub.innerText = `${len} chars`;
        bSub.className = "char-badge " + (len <= 45 ? "badge-optimal" : "badge-warning");
      }
      if (bS1) {
        const len = s1.length;
        bS1.innerText = `${len} chars`;
        bS1.className = "char-badge " + (len <= 32 ? "badge-optimal" : "badge-warning");
      }
      if (bS2) {
        const len = s2.length;
        bS2.innerText = `${len} chars`;
        bS2.className = "char-badge " + (len <= 32 ? "badge-optimal" : "badge-warning");
      }
      if (bS3) {
        const len = s3.length;
        bS3.innerText = `${len} chars`;
        bS3.className = "char-badge " + (len <= 32 ? "badge-optimal" : "badge-warning");
      }
    }

    function debounceRender() {
      updateCharCounters();
      if (!isParsingRaw) {
        const rawCode = generateDirectiveCode();
        document.getElementById("txt-raw-directive").value = rawCode;
      }
      clearTimeout(renderTimer);
      renderTimer = setTimeout(renderCurrentBlock, 60);
    }

    async function renderCurrentBlock(updateRaw = true) {
      const t0 = performance.now();
      const btype = document.getElementById("sel-type").value;
      const inheritTheme = document.getElementById("chk-inherit-theme").checked;

      let style = document.getElementById("sel-global-style").value;
      let theme = document.getElementById("sel-global-theme") ? document.getElementById("sel-global-theme").value : "cyberpunk";
      let preset = document.getElementById("sel-global-preset").value;
      let mode = document.getElementById("sel-global-mode").value;
      let prim = "";
      let acc = "";
      let tert = "";

      if (!inheritTheme) {
        style = document.getElementById("sel-style").value;
        theme = document.getElementById("sel-theme") ? document.getElementById("sel-theme").value : "cyberpunk";
        preset = document.getElementById("sel-preset").value;
        mode = document.getElementById("sel-mode").value;
        if (document.getElementById("rad-custom").checked) {
          prim = document.getElementById("inp-primary").value.trim();
          acc = document.getElementById("inp-accent").value.trim();
          tert = document.getElementById("inp-tertiary") ? document.getElementById("inp-tertiary").value.trim() : "";
        }
      }

      // If mode is auto, force the current preview theme mode so the user sees the SVG in chosen theme
      let effectiveRenderMode = mode;
      if (mode === "auto") {
        effectiveRenderMode = activePreviewTheme;
      }

      if (updateRaw && !isParsingRaw) {
        const rawCode = generateDirectiveCode();
        document.getElementById("txt-raw-directive").value = rawCode;
      }

      const params = new URLSearchParams({
        block_type: btype,
        style: style,
        theme: theme,
        preset: preset,
        mode: effectiveRenderMode
      });
      if (prim) params.set("primary", prim);
      if (acc) params.set("accent", acc);
      if (tert) params.set("tertiary", tert);

      if (btype === "header") {
        params.set("title", document.getElementById("inp-title").value);
        params.set("subtitle", document.getElementById("inp-subtitle").value);
        params.set("tag", document.getElementById("inp-tag").value);
        params.set("spec1", document.getElementById("inp-spec1").value);
        params.set("spec2", document.getElementById("inp-spec2").value);
        params.set("spec3", document.getElementById("inp-spec3").value);
        params.set("tag_url", document.getElementById("inp-tag-url").value);
        params.set("close_url", document.getElementById("inp-close-url").value);
        params.set("compact", document.getElementById("chk-compact").checked ? "true" : "false");
      } else if (btype === "timeline") {
        params.set("body", document.getElementById("inp-timeline-milestones").value);
      } else if (btype === "window") {
        params.set("title", document.getElementById("inp-window-title").value);
        params.set("tag", document.getElementById("inp-window-tag").value);
      } else if (btype === "terminal") {
        params.set("title", document.getElementById("inp-terminal-title").value);
      } else if (btype === "quote") {
        params.set("title", document.getElementById("inp-quote-title").value);
        params.set("subtitle", document.getElementById("inp-quote-sub").value);
        const qBadge = document.getElementById("sel-quote-badge").value;
        params.set("badge", qBadge);
        if (document.getElementById("chk-quote-custom-badge").checked) {
          const bCol = document.getElementById("inp-quote-badge-color").value.trim();
          if (bCol) params.set("badge_color", bCol);
        } else if (GITHUB_ALERT_COLORS[qBadge.toUpperCase()]) {
          params.set("badge_color", GITHUB_ALERT_COLORS[qBadge.toUpperCase()]);
        }
      } else if (btype === "chip") {
        params.set("title", document.getElementById("inp-chip-text").value);
        params.set("type", document.getElementById("sel-chip-type").value);
        params.set("decay_dir", document.getElementById("sel-decay-dir").value);
        params.set("github", document.getElementById("sel-chip-gh").value);
        params.set("repo", document.getElementById("inp-chip-repo").value);
        params.set("width", document.getElementById("inp-chip-width").value);
      } else if (btype === "metrics") {
        params.set("items", document.getElementById("inp-metrics-items").value);
        params.set("title", document.getElementById("inp-metrics-label").value);
        params.set("subtitle", document.getElementById("inp-metrics-val").value);
        params.set("delta", document.getElementById("inp-metrics-delta").value);
        params.set("status", document.getElementById("inp-metrics-status").value);
      } else if (btype === "progress") {
        params.set("value", document.getElementById("inp-progress-val").value);
        params.set("title", document.getElementById("inp-progress-label").value);
        params.set("sub", document.getElementById("inp-progress-sub").value);
      } else if (btype === "techstack") {
        params.set("items", document.getElementById("inp-techstack-items").value);
        params.set("columns", document.getElementById("inp-techstack-cols").value);
      } else if (btype === "callout") {
        const cType = document.getElementById("sel-callout-type").value;
        params.set("type", cType);
        params.set("title", document.getElementById("inp-callout-title").value);
        params.set("subtitle", document.getElementById("inp-callout-sub").value);
        params.set("quote", document.getElementById("chk-callout-quote").checked ? "true" : "false");
        if (document.getElementById("chk-callout-custom-badge").checked) {
          const bCol = document.getElementById("inp-callout-badge-color").value.trim();
          if (bCol) params.set("badge_color", bCol);
        } else if (GITHUB_ALERT_COLORS[cType.toUpperCase()]) {
          params.set("badge_color", GITHUB_ALERT_COLORS[cType.toUpperCase()]);
        }
      } else if (btype === "frame") {
        params.set("type", document.getElementById("sel-frame-type").value);
        params.set("title", document.getElementById("inp-frame-title").value);
        params.set("tag", document.getElementById("inp-frame-tag").value);
        params.set("tag_url", document.getElementById("inp-frame-tag-url").value);
        params.set("close_url", document.getElementById("inp-frame-close-url").value);
      } else if (btype === "splitter") {
        params.set("title", document.getElementById("inp-splitter-label").value);
      } else if (btype === "footer") {
        params.set("status", document.getElementById("inp-footer-status").value);
        params.set("nav", document.getElementById("inp-footer-nav").value);
        params.set("sub", document.getElementById("inp-footer-sub").value);
      } else if (btype === "social") {
        params.set("title", document.getElementById("inp-social-title").value);
        params.set("subtitle", document.getElementById("inp-social-sub").value);
        params.set("repo", document.getElementById("inp-social-repo").value);
        params.set("tags", document.getElementById("inp-social-tags").value);
      } else if (btype === "starchart") {
        params.set("repo", document.getElementById("inp-title").value || "Kazinagg/pixel-readme-kit");
        params.set("title", "STAR GROWTH TRAJECTORY");
        params.set("points", "15,65,190,480,950,1650");
        params.set("current", "1,650");
        params.set("delta", "+78% past 6m");
      } else if (btype === "profile") {
        params.set("name", document.getElementById("inp-title").value || "ALEX DEVELOPER");
        params.set("role", document.getElementById("inp-subtitle").value || "FULLSTACK & SYSTEMS ARCHITECT");
        params.set("status", "AVAILABLE FOR HIRE");
        params.set("location", "REMOTE // UTC+3");
        params.set("badge", "LEVEL_99");
      }

      try {
        const resp = await fetch(`/api/render?${params.toString()}`);
        if (resp.ok) {
          const svgText = await resp.text();
          const mount = document.getElementById("svg-render-mount");
          // Use Shadow DOM to prevent any <style>:root in SVG from leaking into Studio UI
          if (!mount.shadowRoot) {
            mount.attachShadow({ mode: "open" });
          }
          mount.shadowRoot.innerHTML = svgText;
          const dt = Math.round(performance.now() - t0);
          document.getElementById("render-latency").innerText = `${dt}ms`;
        }
      } catch (err) {
        console.error("Render block error:", err);
      }
    }

    async function saveExistingBlockChanges() {
      if (currentEditingBlockId === null) {
        alert("No block selected to update.");
        return;
      }
      const newRaw = document.getElementById("txt-raw-directive").value.trim() || generateDirectiveCode();
      try {
        const resp = await fetch("/api/template/update_block", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            id: currentEditingBlockId,
            directive_raw: newRaw
          })
        });
        if (resp.ok) {
          flashNotification("[OK] BLOCK SAVED & RECOMPILED", "var(--studio-green)");
          markDraftDirty();
          const keepId = currentEditingBlockId;
          await loadTemplateBlocks(keepId);
          await loadCompiledPreview();
          highlightBlockInPreview(keepId);
        } else {
          const err = await resp.text();
          alert("Failed to update block: " + err);
        }
      } catch (e) {
        alert("Error saving block: " + e);
      }
    }

    async function executeInsertBlock() {
      const newRaw = document.getElementById("txt-raw-directive").value.trim() || generateDirectiveCode();
      try {
        const resp = await fetch("/api/template/insert_block", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            after_id: targetInsertAfterId,
            directive_raw: newRaw
          })
        });
        if (resp.ok) {
          flashNotification("[OK] NEW BLOCK INSERTED", "var(--studio-green)");
          markDraftDirty();
          switchEditorMode('edit');
          await loadTemplateBlocks();
          await loadCompiledPreview();
        } else {
          const err = await resp.text();
          alert("Failed to insert block: " + err);
        }
      } catch (e) {
        alert("Error inserting block: " + e);
      }
    }

    function confirmDeleteBlock(blockId, event) {
      if (event) event.stopPropagation();
      currentEditingBlockId = blockId;
      deleteExistingBlock();
    }

    async function deleteExistingBlock() {
      if (currentEditingBlockId === null) return;
      if (!confirm(`Delete block #${currentEditingBlockId} from template?`)) return;
      try {
        const resp = await fetch("/api/template/delete_block", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ id: currentEditingBlockId })
        });
        if (resp.ok) {
          flashNotification("[OK] BLOCK REMOVED", "var(--studio-amber)");
          markDraftDirty();
          currentEditingBlockId = null;
          currentEditingBlockOriginal = null;
          await loadTemplateBlocks(0);
          await loadCompiledPreview();
        } else {
          const err = await resp.text();
          alert("Failed to delete block: " + err);
        }
      } catch (e) {
        alert("Error deleting block: " + e);
      }
    }

    function copyDirective() {
      const code = document.getElementById("txt-raw-directive").value;
      navigator.clipboard.writeText(code).then(() => {
        flashNotification("[OK] COPIED TO CLIPBOARD", "var(--studio-cyan)");
      });
    }

    function flashNotification(text, color) {
      const s = document.getElementById("sse-status");
      if (s) {
        const oldText = s.innerText;
        const oldColor = s.style.color;
        s.innerText = text;
        s.style.color = color;
        setTimeout(() => {
          s.innerText = oldText;
          s.style.color = oldColor;
        }, 2500);
      }
    }

    async function pushReadmeToGit() {
      const btn = document.getElementById("btn-git-push");
      if (!btn) return;
      const originalText = btn.innerText;
      btn.disabled = true;
      btn.innerText = "[ PUSHING... ]";
      flashNotification("SYNCING README & PUSHING TO GIT...", "var(--studio-amber)");

      try {
        const resp = await fetch("/api/git/push_readme", {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        });
        const data = await resp.json();
        if (resp.ok && data.ok) {
          flashNotification(data.committed ? "[OK] README PUSHED TO GITHUB" : "[OK] ALREADY UP TO DATE IN GIT", "var(--studio-green)");
          await loadCompiledPreview();
        } else {
          flashNotification("[ERR] PUSH FAILED: " + (data.error || "Unknown error"), "var(--studio-danger)");
          alert("Git Push Error: " + (data.error || "Failed to push to Git"));
        }
      } catch (err) {
        flashNotification("[ERR] NETWORK ERROR DURING PUSH", "var(--studio-danger)");
        alert("Network / Server error: " + err);
      } finally {
        btn.disabled = false;
        btn.innerText = originalText;
      }
    }

    async function loadCompiledPreview() {
      try {
        const resp = await fetch(`/api/preview?theme=${activePreviewTheme}&t=${Date.now()}`, { cache: "no-store" });
        if (resp.ok) {
          const data = await resp.json();
          const bustTimestamp = Date.now();
          const applyTheme = (htmlStr) => (htmlStr || "").replace(
            /(<img\b[^>]*?\bsrc=")([^"]+)(\")/gi,
            function(match, p1, p2, p3) {
              const cleanUrl = p2.split("?")[0];
              return `${p1}${cleanUrl}?theme=${activePreviewTheme}&t=${bustTimestamp}${p3}`;
            }
          );
          cachedEditHtml = applyTheme(data.html || "");
          cachedViewHtml = applyTheme(data.view_html || data.html || "");

          const previewArea = document.getElementById("readme-preview-content");
          if (previewArea) {
            if (currentStudioMode === "view") {
              previewArea.innerHTML = cachedViewHtml;
            } else {
              previewArea.innerHTML = cachedEditHtml;
            }
          }
          document.getElementById("template-filename").innerText = data.filename || "README.template.md";
          if (data.lines) document.getElementById("gh-stats-lines").innerText = `${data.lines} lines`;
          if (data.bytes) {
            const kb = (data.bytes / 1024).toFixed(1);
            document.getElementById("gh-stats-bytes").innerText = `${kb} KB`;
          }
          if (currentStudioMode !== "view" && currentEditingBlockId !== null) {
            highlightBlockInPreview(currentEditingBlockId);
          }
        }
      } catch (e) {
        console.error("Load preview error:", e);
      }
    }

    function attachPreviewClickInterceptor() {
      const container = document.getElementById("readme-preview-content");
      if (!container) return;
      container.addEventListener("click", function(e) {
        if (currentStudioMode === "view") return;
        const link = e.target.closest("a");
        if (link && !e.target.closest(".pk-block-hud-bar")) {
          e.preventDefault();
          e.stopPropagation();
        }
        const wrapper = e.target.closest(".pk-block-wrapper");
        if (wrapper && !e.target.closest(".pk-hud-actions")) {
          const blkId = parseInt(wrapper.getAttribute("data-pk-id"), 10);
          if (!isNaN(blkId)) {
            selectBlockFromPreview(blkId, e);
          }
        }
      });
    }

    let sseReloadTimer = null;
    function initSSE() {
      if (sseSource) sseSource.close();
      sseSource = new EventSource("/events");
      sseSource.addEventListener("reload", () => {
        if (sseReloadTimer) clearTimeout(sseReloadTimer);
        sseReloadTimer = setTimeout(() => {
          loadTemplateBlocks(currentEditingBlockId);
          loadCompiledPreview();
        }, 200);
      });
      sseSource.onopen = () => {
        const el = document.getElementById("sse-status");
        if (el) { el.innerText = "HUD STUDIO SYNC: ONLINE"; el.style.color = "var(--studio-green)"; }
      };
      sseSource.onerror = () => {
        const el = document.getElementById("sse-status");
        if (el) { el.innerText = "HUD STUDIO SYNC: RECONNECTING..."; el.style.color = "var(--studio-amber)"; }
      };
    }

    // ==============================================================================
    // COMPONENT CATALOG & DRAG AND DROP
    // ==============================================================================
    const COMPONENT_CATALOG = [
      {
        id: "header",
        name: "Header Banner",
        category: "hero",
        catName: "Hero & Banners",
        desc: "Flagship master title banner with telemetry specs, status badge, and radar.",
        snippet: '<!-- readme-kit:header title="READMEKIT // STUDIO" subtitle="Universal Customization System for GitHub" tag="[V5.1]" spec1="PYTHON 3.10+" spec2="100% SVG" spec3="NOMINAL" -->'
      },
      {
        id: "window",
        name: "Window Frame Monolith",
        category: "containers",
        catName: "Containers",
        desc: "Seamless table container wrapper with 45° chamfers and status header.",
        snippet: '<!-- readme-kit:window title="CORE // ARCHITECTURE" tag="[SYS_LOG]" -->\n\n| MODULE | STATUS | DESCRIPTION |\n| :--- | :--- | :--- |\n| Core Runtime | Online | Standard library architecture |\n\n<!-- /readme-kit:window -->'
      },
      {
        id: "terminal",
        name: "Terminal Shell",
        category: "containers",
        catName: "Containers",
        desc: "Interactive details/summary terminal console for deployment commands and logs.",
        snippet: '<!-- readme-kit:terminal title="BASH // PRODUCTION_DEPLOY" tag="[ONLINE]" -->\n\n```bash\n$ python -m generator.cli compile --clean-assets\n$ pytest tests/\n```\n\n<!-- /readme-kit:terminal -->'
      },
      {
        id: "frame",
        name: "Window Cap (Top/Bottom)",
        category: "containers",
        catName: "Containers",
        desc: "Standalone top or bottom cap plate for enclosing custom tables.",
        snippet: '<!-- readme-kit:frame frame_type="top" title="SYSTEM.CORE" tag="[OPEN_HUD]" -->'
      },
      {
        id: "quote",
        name: "Architectural Quote",
        category: "content",
        catName: "Callouts & Content",
        desc: "Markdown-friendly quote box with 45° rail, dashed bottom, and alert badge.",
        snippet: '<!-- readme-kit:quote title="ARCHITECTURAL NOTICE" subtitle="Component standard guarantees deterministic SVG rendering across modes." badge="NOTE" -->'
      },
      {
        id: "callout",
        name: "Alert Callout",
        category: "content",
        catName: "Callouts & Content",
        desc: "Autonomous alert card with GitHub standard alert levels (NOTE, TIP, WARNING).",
        snippet: '<!-- readme-kit:callout title="SECURITY ADVISORY" subtitle="Update dependency versions to latest patch to ensure integrity." callout_type="warning" -->'
      },
      {
        id: "footer",
        name: "Closing Footer Plate",
        category: "navigation",
        catName: "Navigation",
        desc: "Monumental closing tray with session status, build info, and return-to-top button.",
        snippet: '<!-- readme-kit:footer status="SYSTEM NOMINAL // ALL TESTS GREEN" nav_text="BACK TO TOP [^]" sub_text="BUILD 2026.10" -->'
      },
      {
        id: "divider",
        name: "Chapter Divider",
        category: "navigation",
        catName: "Navigation",
        desc: "Vector chapter boundary line with grid ornaments and style accents.",
        snippet: '<!-- readme-kit:divider -->'
      },
      {
        id: "splitter",
        name: "Sub-Module Splitter",
        category: "navigation",
        catName: "Navigation",
        desc: "In-window section splitter line with centered telemetry badge.",
        snippet: '<!-- readme-kit:splitter label="SECTION // TELEMETRY METRICS" -->'
      },
      {
        id: "chip",
        name: "Status Chip",
        category: "badges",
        catName: "Badges",
        desc: "Holographic status pill badge with decay grid or live GitHub telemetry.",
        snippet: '<!-- readme-kit:chip text="STATUS: 200 OK" type="decay" decay_dir="right" -->'
      },
      {
        id: "metrics",
        name: "Metrics KPI Row",
        category: "metrics",
        catName: "Metrics & Status",
        desc: "Modular 3-metric KPI dashboard card with sparkline and percentage deltas.",
        snippet: '<!-- readme-kit:metrics items="CORE UPTIME: 99.98% | LATENCY: 12ms | BUFFER: 256MB" -->'
      },
      {
        id: "progress",
        name: "Progress HUD Bar",
        category: "metrics",
        catName: "Metrics & Status",
        desc: "Multi-segment progress meter with percentage display and label.",
        snippet: '<!-- readme-kit:progress label="ENGINE CORE UPGRADE" value="78" max_val="100" status="ACTIVE" -->'
      },
      {
        id: "techstack",
        name: "Tech Stack Matrix",
        category: "metrics",
        catName: "Metrics & Status",
        desc: "Visual tech stack badges matrix organized by category.",
        snippet: '<!-- readme-kit:techstack categories="LANGUAGES: Python, Rust, TypeScript | INFRA: Docker, K8s, Linux | FRAMEWORKS: React, FastAPI" -->'
      },
      {
        id: "timeline",
        name: "PCB Timeline / Roadmap",
        category: "metrics",
        catName: "Metrics & Status",
        desc: "Milestone board with circuit traces and chronological phases.",
        snippet: '<!-- readme-kit:timeline body=\'milestone title="ALPHA" date="2026-Q1" status="COMPLETED" desc="Testing"\\nmilestone title="BETA" date="2026-Q2" status="IN_PROGRESS" desc="Launch"\' -->'
      },
      {
        id: "starchart",
        name: "Star Growth Chart",
        category: "social",
        catName: "Profiles & Social",
        desc: "Star history growth trend curve with coordinate grid, peaks, and gain metric.",
        snippet: '<!-- readme-kit:starchart repo="Kazinagg/pixel-readme-kit" points="120, 240, 480, 890, 1450, 2100" labels="Jan, Feb, Mar, Apr, May, Jun" gain="+180%" -->'
      },
      {
        id: "profile",
        name: "Profile Dossier Card",
        category: "social",
        catName: "Profiles & Social",
        desc: "Developer dossier profile card with cyber avatar, status LED, and tech badges.",
        snippet: '<!-- readme-kit:profile name="KAZINAGG" role="SENIOR SYSTEMS ARCHITECT" status="ONLINE" location="TOKYO / BERLIN" badges="PYTHON,RUST,SYSTEMS" bio="Architecting deterministic SVG graphics and resilient systems." -->'
      },
      {
        id: "social",
        name: "OpenGraph Social Card",
        category: "social",
        catName: "Profiles & Social",
        desc: "1280x640 OpenGraph social media preview banner with repo branding.",
        snippet: '<!-- readme-kit:social title="READMEKIT" subtitle="Universal Customization System for GitHub" repo="Kazinagg/pixel-readme-kit" tags="PYTHON,SVG,CYBERPUNK" -->'
      }
    ];

    let activeCatalogCategory = "all";
    let catalogSearchQuery = "";
    let draggedBlockType = null;
    let draftIsDirty = false;

    function toggleCatalogSidebar() {
      const sidebar = document.getElementById("catalog-sidebar");
      const btn = document.getElementById("btn-toggle-catalog");
      if (!sidebar) return;
      sidebar.classList.toggle("collapsed");
      if (btn) btn.classList.toggle("active-btn", !sidebar.classList.contains("collapsed"));
    }

    // Backward-compatible alias
    function toggleCatalogDrawer() {
      toggleCatalogSidebar();
    }

    function getActiveThemeParams() {
      const selStyleBtn = document.querySelector(".style-switch-group .seg-btn.active");
      const style = selStyleBtn ? (selStyleBtn.id.replace("btn-top-style-", "") || "pixel") : "pixel";
      const selTheme = document.getElementById("top-nav-theme-select");
      const theme = selTheme ? selTheme.value : "cyberpunk";
      const selPreset = document.getElementById("top-nav-preset-select");
      const preset = selPreset ? selPreset.value : "cyberpunk";
      const selMode = document.getElementById("sel-global-mode");
      const mode = selMode ? selMode.value : "dark";
      const prim = (document.getElementById("inp-global-primary") || {}).value || "";
      const acc = (document.getElementById("inp-global-accent") || {}).value || "";
      const tert = (document.getElementById("inp-global-tertiary") || {}).value || "";
      return { style, theme, preset, mode, primary: prim, accent: acc, tertiary: tert };
    }

    function getBlockPreviewUrl(blockId, blockName) {
      const p = getActiveThemeParams();
      let effectiveMode = p.mode;
      if (p.mode === "auto") {
        let isLight = false;
        if (activePreviewTheme === "light") {
          isLight = true;
        } else if (activePreviewTheme === "sync") {
          isLight = (currentStudioThemeMode === "auto")
            ? studioSystemThemeMedia.matches
            : (currentStudioThemeMode === "light");
        }
        effectiveMode = isLight ? "light" : "dark";
      }
      let query = `block_type=${encodeURIComponent(blockId)}&style=${encodeURIComponent(p.style)}&theme=${encodeURIComponent(p.theme)}&preset=${encodeURIComponent(p.preset)}&mode=${encodeURIComponent(effectiveMode)}&width=280&title=${encodeURIComponent(blockName)}`;
      if (p.primary && /^#[0-9A-Fa-f]{6}$/.test(p.primary)) query += `&primary=${encodeURIComponent(p.primary)}`;
      if (p.accent && /^#[0-9A-Fa-f]{6}$/.test(p.accent)) query += `&accent=${encodeURIComponent(p.accent)}`;
      if (p.tertiary && /^#[0-9A-Fa-f]{6}$/.test(p.tertiary)) query += `&tertiary=${encodeURIComponent(p.tertiary)}`;
      return `/api/render?${query}`;
    }

    let catalogPreviewDebounce = null;
    function updateCatalogPreviews(immediate = false) {
      if (catalogPreviewDebounce) clearTimeout(catalogPreviewDebounce);
      if (immediate) {
        doUpdateCatalogPreviews();
      } else {
        catalogPreviewDebounce = setTimeout(doUpdateCatalogPreviews, 120);
      }
    }

    function doUpdateCatalogPreviews() {
      COMPONENT_CATALOG.forEach(b => {
        const img = document.getElementById(`cat-thumb-${b.id}`);
        if (img) {
          img.src = getBlockPreviewUrl(b.id, b.name);
        }
      });
    }

    function renderCatalogDrawer() {
      const listEl = document.getElementById("catalog-blocks-list");
      if (!listEl) return;
      const filtered = COMPONENT_CATALOG.filter(b => {
        const matchCat = activeCatalogCategory === "all" || b.category === activeCatalogCategory;
        const q = catalogSearchQuery.toLowerCase().trim();
        const matchSearch = !q || b.name.toLowerCase().includes(q) || b.id.toLowerCase().includes(q) || b.desc.toLowerCase().includes(q);
        return matchCat && matchSearch;
      });

      const badge = document.getElementById("catalog-count-badge");
      if (badge) badge.innerText = `${filtered.length} BLOCKS`;

      listEl.innerHTML = "";
      filtered.forEach(b => {
        const card = document.createElement("div");
        card.className = "catalog-card";
        card.setAttribute("draggable", "true");
        card.setAttribute("data-block-id", b.id);
        const thumbUrl = getBlockPreviewUrl(b.id, b.name);
        card.innerHTML = `
          <div class="catalog-card-header">
            <span class="catalog-card-name">
              <svg viewBox="0 0 16 16" width="12" height="12" fill="var(--studio-cyan)"><path d="M7.75 2a.75.75 0 0 1 .75.75V7h4.25a.75.75 0 0 1 0 1.5H8.5v4.25a.75.75 0 0 1-1.5 0V8.5H2.75a.75.75 0 0 1 0-1.5H7V2.75A.75.75 0 0 1 7.75 2Z"/></svg>
              ${b.name}
            </span>
            <span class="catalog-card-cat">${b.catName}</span>
          </div>
          <div class="catalog-card-desc">${b.desc}</div>
          <div class="${(activePreviewTheme === 'light' || (activePreviewTheme === 'sync' && ((currentStudioThemeMode === 'auto') ? studioSystemThemeMedia.matches : (currentStudioThemeMode === 'light')))) ? 'catalog-card-preview light-preview' : 'catalog-card-preview'}" title="Live SVG preview in active theme">
            <img id="cat-thumb-${b.id}" src="${thumbUrl}" alt="${b.name}" loading="lazy" />
          </div>
          <div class="catalog-card-footer">
            <span class="catalog-card-pill">drag or click &rarr;</span>
            <button class="catalog-card-btn" onclick="insertBlockFromCatalog('${b.id}', -1, event)">+ Add</button>
          </div>
        `;
        card.addEventListener("dragstart", (e) => onBlockDragStart(e, b.id));
        card.addEventListener("dragend", onBlockDragEnd);
        listEl.appendChild(card);
      });
    }

    async function fetchTemplatesList() {
      const sel = document.getElementById("sel-template-file");
      if (!sel) return;
      try {
        const res = await fetch("/api/templates");
        if (!res.ok) return;
        const data = await res.json();
        sel.innerHTML = "";
        (data.templates || []).forEach(t => {
          const opt = document.createElement("option");
          opt.value = t.path;
          opt.textContent = t.name;
          if (t.is_active) opt.selected = true;
          sel.appendChild(opt);
        });
        if (data.current) {
          const filename = data.current.split("/").pop().split("\\").pop();
          const lbl = document.getElementById("template-filename");
          if (lbl) lbl.textContent = filename;
        }
      } catch (err) {
        console.error("Failed to fetch templates:", err);
      }
    }

    async function onTemplateFileSelect() {
      const sel = document.getElementById("sel-template-file");
      if (!sel || !sel.value) return;
      const newPath = sel.value;
      try {
        const res = await fetch("/api/template/switch", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ file: newPath, path: newPath })
        });
        if (res.ok) {
          const filename = newPath.split("/").pop().split("\\").pop();
          flashNotification(`Active file: ${filename}`, "var(--studio-green)");
          const lbl = document.getElementById("template-filename");
          if (lbl) lbl.textContent = filename;
          clearDraftDirty();
          await loadTemplateBlocks();
          await loadCompiledPreview();
        } else {
          const err = await res.text();
          alert("Failed to switch template: " + err);
        }
      } catch (err) {
        alert("Error switching template: " + err);
      }
    }

    function filterCatalogBlocks() {
      const inp = document.getElementById("catalog-search-inp");
      catalogSearchQuery = inp ? inp.value : "";
      renderCatalogDrawer();
    }

    function filterCatalogCategory(cat) {
      activeCatalogCategory = cat;
      document.querySelectorAll(".cat-tag-btn").forEach(btn => {
        btn.classList.toggle("active", btn.getAttribute("data-cat") === cat);
      });
      renderCatalogDrawer();
    }

    function onBlockDragStart(e, blockType) {
      draggedBlockType = blockType;
      e.dataTransfer.setData("text/plain", blockType);
      e.dataTransfer.effectAllowed = "copy";
      e.currentTarget.classList.add("dragging");
      document.querySelectorAll(".pk-insert-divider").forEach(d => {
        d.classList.add("drop-target-active");
      });
    }

    function onBlockDragEnd(e) {
      draggedBlockType = null;
      document.querySelectorAll(".catalog-card").forEach(c => c.classList.remove("dragging"));
      document.querySelectorAll(".pk-insert-divider").forEach(d => {
        d.classList.remove("drop-target-active", "drag-over");
      });
    }

    function onDividerDragOver(e) {
      e.preventDefault();
      e.dataTransfer.dropEffect = "copy";
      e.currentTarget.classList.add("drag-over");
    }

    function onDividerDragLeave(e) {
      e.currentTarget.classList.remove("drag-over");
    }

    async function onDividerDrop(e, afterId) {
      e.preventDefault();
      e.currentTarget.classList.remove("drag-over");
      const blockType = e.dataTransfer.getData("text/plain") || draggedBlockType;
      if (!blockType) return;
      await insertBlockFromCatalog(blockType, afterId);
    }

    async function insertBlockFromCatalog(blockType, afterId = -1, event = null) {
      if (event) event.stopPropagation();
      const item = COMPONENT_CATALOG.find(b => b.id === blockType);
      if (!item) return;

      const p = getActiveThemeParams();
      const curStyle = p.style;
      const curTheme = p.theme;

      let directive = item.snippet;
      if (!directive.includes('style="')) {
        directive = item.snippet.replace(`<!-- readme-kit:${item.id}`, `<!-- readme-kit:${item.id} style="${curStyle}" theme="${curTheme}"`);
      }

      try {
        const resp = await fetch("/api/template/insert_block", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            after_id: afterId,
            directive_raw: directive
          })
        });
        if (resp.ok) {
          flashNotification(`Added ${item.name}`, "var(--studio-green)");
          markDraftDirty();
          await loadTemplateBlocks();
          await loadCompiledPreview();
        } else {
          const err = await resp.text();
          alert("Failed to insert block: " + err);
        }
      } catch (e) {
        alert("Error inserting block: " + e);
      }
    }

    function markDraftDirty() {
      draftIsDirty = true;
      const badge = document.getElementById("draft-dirty-badge");
      const revBtn = document.getElementById("btn-revert-file");
      if (badge) badge.style.display = "inline-flex";
      if (revBtn) revBtn.style.display = "inline-flex";
    }

    function clearDraftDirty() {
      draftIsDirty = false;
      const badge = document.getElementById("draft-dirty-badge");
      const revBtn = document.getElementById("btn-revert-file");
      if (badge) badge.style.display = "none";
      if (revBtn) revBtn.style.display = "none";
    }

    async function saveTemplateToFile() {
      try {
        const resp = await fetch("/api/recompile", { method: "POST" });
        if (resp.ok) {
          flashNotification("[OK] TEMPLATE & README SAVED TO DISK", "var(--studio-green)");
          clearDraftDirty();
          await loadTemplateBlocks(currentEditingBlockId);
          await loadCompiledPreview();
        } else {
          alert("Recompile failed");
        }
      } catch (e) {
        alert("Save failed: " + e);
      }
    }

    async function revertDraftChanges() {
      if (!confirm("Revert unsaved draft changes and reload template from disk?")) return;
      clearDraftDirty();
      await loadTemplateBlocks();
      await loadCompiledPreview();
      flashNotification("[OK] REVERTED TO DISK VERSION", "var(--studio-amber)");
    }

    // Global Keyboard Shortcuts
    document.addEventListener("keydown", function(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === "s") {
        e.preventDefault();
        if (editorMode === "edit") {
          saveExistingBlockChanges();
        } else {
          executeInsertBlock();
        }
      }
    });

    window.addEventListener("DOMContentLoaded", () => {
      try {
        const savedMode = localStorage.getItem("pk_studio_mode");
        if (savedMode === "view") {
          setStudioMode("view");
        }
        const savedTheme = localStorage.getItem("pk_preview_theme") || "dark";
        switchPreviewTheme(savedTheme);
        const savedStudioTheme = localStorage.getItem("prk_studio_theme") || "dark";
        setStudioTheme(savedStudioTheme);
      } catch (_) {}
      selectTopNavStyle("pixel");
      onBlockStyleChange();
      renderCatalogDrawer();
      fetchTemplatesList();
      loadTemplateBlocks();
      loadCompiledPreview();
      updateCatalogPreviews(true);
      attachPreviewClickInterceptor();
      initSSE();
    });
