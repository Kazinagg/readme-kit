// ==============================================================================
// THEME STUDIO & COLOR HARMONIZER MODULE
// Dynamic palette creation, WCAG contrast calculation, and preset management
// ==============================================================================

let cachedThemesData = null;
let currentGeneratedTheme = null;

async function loadDynamicPresets() {
  try {
    const resp = await fetch("/api/themes");
    if (!resp.ok) return;
    cachedThemesData = await resp.json();

    // 1. Merge server-side style themes mapping if available
    if (cachedThemesData.style_themes && window.STYLE_THEMES_MAP) {
      Object.assign(window.STYLE_THEMES_MAP, cachedThemesData.style_themes);
    }

    // 2. Update PRESET_COLORS in global scope
    if (cachedThemesData.themes) {
      window.PRESET_COLORS = window.PRESET_COLORS || {};
      for (const [slug, data] of Object.entries(cachedThemesData.themes)) {
        if (data.dark) {
          window.PRESET_COLORS[slug] = {
            primary: data.dark.primary || "#00c8d7",
            accent: data.dark.accent || "#a855f7",
            tertiary: data.dark.tertiary || "#ff0055",
          };
        }
      }
    }

    // 3. Keep active style & theme dropdown in sync
    const selGlobalStyle = document.getElementById("sel-global-style");
    const activeStyle = selGlobalStyle ? selGlobalStyle.value : "pixel";
    if (typeof selectTopNavStyle === "function") {
      selectTopNavStyle(activeStyle);
    }
  } catch (err) {
    console.warn("Could not load dynamic presets:", err);
  }
}

function openThemeStudio() {
  let modal = document.getElementById("theme-studio-modal");
  if (!modal) {
    modal = createThemeStudioModal();
    document.body.appendChild(modal);
  }
  modal.style.display = "flex";

  // Match target style in studio with current selected global style
  const selGlobalStyle = document.getElementById("sel-global-style");
  const tsStyle = document.getElementById("ts-style");
  if (selGlobalStyle && tsStyle) {
    tsStyle.value = selGlobalStyle.value;
  }

  syncThemeStudioColor("picker");
  generateHarmoniousTheme();
}

function closeThemeStudio() {
  const modal = document.getElementById("theme-studio-modal");
  if (modal) {
    modal.style.display = "none";
  }
}

function createThemeStudioModal() {
  const backdrop = document.createElement("div");
  backdrop.id = "theme-studio-modal";
  backdrop.className = "theme-studio-backdrop";
  backdrop.style.cssText = `
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(15, 23, 42, 0.72);
    backdrop-filter: blur(8px);
    z-index: 9999;
    align-items: center;
    justify-content: center;
    padding: 20px;
  `;

  backdrop.innerHTML = `
    <div class="theme-studio-window" style="
      background: var(--studio-elevated);
      border: 1px solid var(--studio-panel-border);
      border-radius: 8px;
      width: 100%;
      max-width: 680px;
      box-shadow: 0 20px 48px rgba(0, 0, 0, 0.35);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      font-family: var(--studio-font-mono);
      color: var(--studio-text);
    ">
      <div class="theme-studio-header" style="
        background: var(--studio-surface);
        border-bottom: 1px solid var(--studio-panel-border);
        padding: 12px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      ">
        <div style="font-family:var(--studio-font-mono); font-weight:700; font-size:12px; color:var(--signal-teal); letter-spacing:0.5px;">
          THEME STUDIO // PALETTE HARMONIZER & PRESETS
        </div>
        <button onclick="closeThemeStudio()" style="
          background: transparent;
          border: 1px solid var(--studio-panel-border);
          color: var(--studio-text-muted);
          cursor: pointer;
          font-family: var(--studio-font-mono);
          padding: 4px 10px;
          border-radius: 4px;
          font-size: 11px;
        " onmouseover="this.style.borderColor='var(--studio-danger)';this.style.color='var(--studio-danger)'" onmouseout="this.style.borderColor='var(--studio-panel-border)';this.style.color='var(--studio-text-muted)'">[ CLOSE ]</button>
      </div>

      <div class="theme-studio-body" style="padding: 20px; overflow-y: auto; max-height: 80vh;">
        <!-- Inputs Row 1: Target Style + Strategy -->
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px;">
          <div>
            <label style="font-size:11px; color:var(--studio-text-muted); display:block; margin-bottom:5px; font-weight:600;">TARGET STYLE PARADIGM</label>
            <select id="ts-style" style="
              width: 100%; background: var(--studio-surface); border: 1px solid var(--studio-panel-border);
              color: var(--studio-text); padding: 7px 10px; border-radius: 4px; font-family: var(--studio-font-mono); font-size: 12px;
            ">
              <option value="pixel">Pixel / Retro-Tech</option>
              <option value="modern">Modern Clean Vector</option>
              <option value="sketch">Hand-Drawn Sketch</option>
            </select>
          </div>
          <div>
            <label style="font-size:11px; color:var(--studio-text-muted); display:block; margin-bottom:5px; font-weight:600;">HARMONIZATION STRATEGY</label>
            <select id="ts-strategy" style="
              width: 100%; background: var(--studio-surface); border: 1px solid var(--studio-panel-border);
              color: var(--studio-text); padding: 7px 10px; border-radius: 4px; font-family: var(--studio-font-mono); font-size: 12px;
            " onchange="generateHarmoniousTheme()">
              <option value="triadic">Triadic (Balanced High Contrast)</option>
              <option value="complementary">Complementary (Dual Dynamic)</option>
              <option value="analogous">Analogous (Harmonious Gradient)</option>
            </select>
          </div>
        </div>

        <!-- Inputs Row 2: Theme Name -->
        <div style="margin-bottom: 14px;">
          <label style="font-size:11px; color:var(--studio-text-muted); display:block; margin-bottom:5px; font-weight:600;">PRESET SLUG / NAME</label>
          <input type="text" id="ts-theme-name" value="Neon Matrix" style="
            width: 100%; background: var(--studio-surface); border: 1px solid var(--studio-panel-border);
            color: var(--studio-text); padding: 7px 10px; border-radius: 4px; font-family: var(--studio-font-mono); font-size: 12px;
          " oninput="debounceThemeStudioGenerate()">
        </div>

        <!-- Inputs Row 3: Primary Brand Color -->
        <div style="margin-bottom: 20px;">
          <label style="font-size:11px; color:var(--studio-text-muted); display:block; margin-bottom:5px; font-weight:600;">PRIMARY BRAND COLOR (HEX)</label>
          <div style="display:flex; gap:10px; align-items:center;">
            <input type="color" id="ts-picker-primary" value="#00e5b0" style="
              width: 44px; height: 34px; background: transparent; border: 1px solid var(--studio-panel-border); cursor: pointer; border-radius:4px;
            " oninput="syncThemeStudioColor('picker')">
            <input type="text" id="ts-inp-primary" value="#00e5b0" style="
              flex: 1; background: var(--studio-surface); border: 1px solid var(--studio-panel-border);
              color: var(--signal-teal); font-weight: bold; padding: 7px 10px; border-radius: 4px; font-family: var(--studio-font-mono); font-size: 12px;
            " oninput="syncThemeStudioColor('text')">
            <button onclick="generateHarmoniousTheme()" style="
              background: rgba(13, 148, 136, 0.12); border: 1px solid var(--signal-teal);
              color: var(--signal-teal); padding: 7px 16px; border-radius: 4px; cursor: pointer; font-weight: 600; font-size: 11px;
            ">[ HARMONIZE ]</button>
          </div>
        </div>

        <!-- Palette Preview Swatches -->
        <div style="background: var(--studio-surface); border: 1px solid var(--studio-panel-border); border-radius:6px; padding:15px; margin-bottom:18px;">
          <div style="font-size:11px; color:var(--signal-teal); font-weight:600; margin-bottom:12px; letter-spacing:0.5px;">
            DERIVED HARMONIZED SWATCHES
          </div>
          <div id="ts-swatches-grid" style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
            <!-- Generated dynamically -->
          </div>
        </div>

        <!-- Live Component Mini Preview -->
        <div style="background: var(--studio-surface); border: 1px solid var(--studio-panel-border); border-radius:6px; padding:15px; margin-bottom:20px;">
          <div style="font-size:11px; color:var(--studio-text-muted); margin-bottom:10px; font-weight:600;">COMPONENT PREVIEW (SVG CHIP & FRAME)</div>
          <div id="ts-preview-mount" style="display:flex; flex-direction:column; gap:10px; align-items:center;">
            <div id="ts-chip-preview" style="display:flex; gap:10px;"></div>
          </div>
        </div>

        <!-- Action Row -->
        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--studio-panel-border); padding-top:15px;">
          <button onclick="applyCurrentThemeLocally()" style="
            background: rgba(124, 58, 237, 0.12); border: 1px solid var(--signal-violet);
            color: var(--signal-violet); padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: 600; font-size: 11px;
          ">[ APPLY SESSION ]</button>
          <button onclick="saveCurrentCustomTheme()" style="
            background: rgba(13, 148, 136, 0.12); border: 1px solid var(--signal-teal);
            color: var(--signal-teal); padding: 8px 20px; border-radius: 4px; cursor: pointer; font-weight: 600; font-size: 11px;
          ">[ SAVE PRESET ] (*.json)</button>
        </div>
      </div>
    </div>
  `;

  return backdrop;
}

let tsTimer = null;
function debounceThemeStudioGenerate() {
  if (tsTimer) clearTimeout(tsTimer);
  tsTimer = setTimeout(generateHarmoniousTheme, 300);
}

function syncThemeStudioColor(from) {
  const picker = document.getElementById("ts-picker-primary");
  const text = document.getElementById("ts-inp-primary");
  if (!picker || !text) return;
  if (from === "picker") {
    text.value = picker.value;
  } else {
    if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) {
      picker.value = text.value;
    }
  }
  debounceThemeStudioGenerate();
}

async function generateHarmoniousTheme() {
  const primInput = document.getElementById("ts-inp-primary");
  const nameInput = document.getElementById("ts-theme-name");
  const stratSelect = document.getElementById("ts-strategy");
  if (!primInput) return;

  const prim = primInput.value.trim() || "#00e5b0";
  const name = nameInput ? nameInput.value.trim() : "Custom Theme";
  const strategy = stratSelect ? stratSelect.value : "triadic";

  try {
    const resp = await fetch("/api/themes/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ primary: prim, name: name, strategy: strategy })
    });
    if (!resp.ok) return;
    const data = await resp.json();
    currentGeneratedTheme = data.theme;

    renderSwatchesGrid(currentGeneratedTheme);
    renderMiniComponents(currentGeneratedTheme);
  } catch (e) {
    console.error("Theme generation error:", e);
  }
}

function renderSwatchesGrid(themeData) {
  const container = document.getElementById("ts-swatches-grid");
  if (!container || !themeData) return;

  const preset = themeData.preset || {};
  const swatches = [
    { label: "PRIMARY", color: preset.primary },
    { label: "ACCENT", color: preset.secondary },
    { label: "TERTIARY", color: preset.accent },
    { label: "STATUS / OK", color: preset.success || "#00D26A" },
    { label: "WARNING", color: preset.warning || "#F59E0B" },
    { label: "BG GLASS", color: preset.bg_glass, isGlass: true },
    { label: "BORDER", color: preset.border_subtle, isGlass: true },
    { label: "TEXT MAIN", color: "#F8F8F2" },
  ];

  container.innerHTML = swatches.map(s => `
    <div style="background: var(--studio-elevated); border: 1px solid var(--studio-panel-border); border-radius:4px; padding:8px;">
      <div style="
        height: 28px; border-radius: 3px; background: ${s.color};
        border: 1px solid var(--studio-panel-border); margin-bottom: 6px;
      "></div>
      <div style="font-size:9.5px; color:var(--studio-text-muted);">${s.label}</div>
      <div style="font-size:10px; font-weight:bold; color:var(--studio-text); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
        ${s.color}
      </div>
    </div>
  `).join("");
}

function renderMiniComponents(themeData) {
  const container = document.getElementById("ts-chip-preview");
  if (!container || !themeData) return;

  const preset = themeData.preset || {};
  container.innerHTML = `
    <div style="
      background: ${preset.bg_glass || 'rgba(13,18,28,0.85)'};
      border: 1px solid ${preset.primary || '#00e5b0'};
      padding: 6px 14px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: bold;
      color: ${preset.primary || '#00e5b0'};
    ">
      ${preset.name || 'THEME'} // ACTIVE
    </div>
    <div style="
      background: ${preset.bg_glass || 'rgba(13,18,28,0.85)'};
      border: 1px solid ${preset.secondary || '#a855f7'};
      padding: 6px 14px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: bold;
      color: ${preset.secondary || '#a855f7'};
    ">
      ACCENT // PASS
    </div>
  `;
}

function applyCurrentThemeLocally() {
  if (!currentGeneratedTheme) return;
  const p = currentGeneratedTheme.preset;
  if (!p) return;

  const tsStyle = document.getElementById("ts-style");
  const targetStyle = tsStyle ? tsStyle.value : "pixel";

  if (typeof selectTopNavStyle === "function") {
    selectTopNavStyle(targetStyle);
  }

  const globalPreset = document.getElementById("sel-global-preset");
  const primInput = document.getElementById("inp-global-primary");
  const primPicker = document.getElementById("picker-global-primary");
  const accInput = document.getElementById("inp-global-accent");
  const accPicker = document.getElementById("picker-global-accent");
  const tertInput = document.getElementById("inp-global-tertiary");
  const tertPicker = document.getElementById("picker-global-tertiary");

  if (globalPreset) globalPreset.value = "custom";
  if (primInput) primInput.value = p.primary;
  if (primPicker) primPicker.value = p.primary;
  if (accInput) accInput.value = p.secondary;
  if (accPicker) accPicker.value = p.secondary;
  if (tertInput) tertInput.value = p.accent;
  if (tertPicker) tertPicker.value = p.accent;

  closeThemeStudio();
  if (typeof applyGlobalThemeToAllBlocks === "function") {
    applyGlobalThemeToAllBlocks(true);
  }
}

async function saveCurrentCustomTheme() {
  if (!currentGeneratedTheme) return;
  const p = currentGeneratedTheme.preset;
  if (!p) return;

  const tsStyle = document.getElementById("ts-style");
  const targetStyle = tsStyle ? tsStyle.value : "pixel";

  try {
    const resp = await fetch("/api/themes/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: p.name,
        slug: p.theme,
        style: targetStyle,
        preset: Object.assign({}, p, { style: targetStyle }),
        dark: currentGeneratedTheme.dark,
        light: currentGeneratedTheme.light,
      })
    });
    if (!resp.ok) {
      alert("Failed to save theme to presets: " + await resp.text());
      return;
    }
    const data = await resp.json();
    alert(`[OK] Theme successfully saved to presets/${data.slug}.json!`);
    await loadDynamicPresets();
    closeThemeStudio();
  } catch (e) {
    alert("Error saving theme: " + e);
  }
}

// Auto-initialize presets on DOM ready
window.addEventListener("DOMContentLoaded", () => {
  loadDynamicPresets();
});
