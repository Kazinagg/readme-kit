"""
Generates the 4 test cases for GitHub Theme Switching and Transparency:
1. #gh-dark-mode-only (header-gh-dark.svg)
   #gh-light-mode-only (header-gh-light.svg)
2. <picture> (header-pic-dark.svg, header-pic-light.svg)
3. Internal CSS @media (prefers-color-scheme: dark) (header-adaptive-internal.svg)
4. 100% Transparent background (header-transparent.svg)
"""

import os
import xml.etree.ElementTree as ET
from generator.font_engine import render_3d_text, calculate_px_size
from generator.engine import validate_svg

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "theme-tests")
os.makedirs(ASSETS_DIR, exist_ok=True)

def save_svg(filename, content):
    validate_svg(content)
    filepath = os.path.join(ASSETS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Saved & validated: {filename} ({len(content)} bytes)")


# ==============================================================================
# TEST 1: GitHub Mode Anchors (#gh-dark-mode-only & #gh-light-mode-only)
# ==============================================================================

def make_gh_dark_header():
    width = 850
    height = 260
    prim = "#00C8D7"
    acc = "#A855F7"
    bg = "rgba(10, 14, 23, 0.85)"
    mid_shadow = "#006b74"
    dark_shadow = "#002b2f"

    grid_lines = []
    for x in range(0, width + 1, 20):
        grid_lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="{prim}" stroke-width="1"/>')
    for y in range(0, height + 1, 20):
        grid_lines.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="{prim}" stroke-width="1"/>')

    pixel_markup, _, _ = render_3d_text(
        "CYBERPUNK // DARK", x=42, y=62, px_size=5,
        front_color=prim, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
        spacing=2, max_width=520
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
      @keyframes ledFlicker {{ 0%, 100% {{ fill: #00D26A; }} 50% {{ fill: #005511; }} }}
      @keyframes crtScanline {{
        0% {{ transform: translateY(0px); opacity: 0; }}
        20% {{ opacity: 0.35; }}
        80% {{ opacity: 0.35; }}
        100% {{ transform: translateY({height}px); opacity: 0; }}
      }}
      @keyframes waveBar1 {{ 0%, 100% {{ height: 6px; y: 198px; }} 50% {{ height: 20px; y: 184px; }} }}
      @keyframes waveBar2 {{ 0%, 100% {{ height: 18px; y: 186px; }} 50% {{ height: 8px; y: 196px; }} }}
      @keyframes waveBar3 {{ 0%, 100% {{ height: 12px; y: 192px; }} 50% {{ height: 22px; y: 182px; }} }}
      @keyframes waveBar4 {{ 0%, 100% {{ height: 22px; y: 182px; }} 50% {{ height: 10px; y: 194px; }} }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      .cursor-blink {{ animation: blink 1s infinite steps(1); }}
      .status-led {{ animation: ledFlicker 1.8s infinite steps(1); }}
      .scan-line {{ animation: crtScanline 6s linear infinite; }}
      .w1 {{ animation: waveBar1 1.1s infinite ease-in-out; }}
      .w2 {{ animation: waveBar2 0.8s infinite ease-in-out; }}
      .w3 {{ animation: waveBar3 1.3s infinite ease-in-out; }}
      .w4 {{ animation: waveBar4 0.9s infinite ease-in-out; }}
    </style>
  </defs>

  <!-- 1. DARK GLASS BACKGROUND -->
  <rect x="0" y="0" width="{width}" height="{height}" fill="{bg}"/>

  <!-- 2. MATRIX RETRO GRID -->
  <g opacity="0.08">
    {''.join(grid_lines)}
  </g>

  <!-- 3. ANIMATED SCANLINE -->
  <line x1="0" y1="0" x2="{width}" y2="0" stroke="{prim}" stroke-width="2" class="scan-line"/>

  <!-- 4. CHASSIS -->
  <rect x="6" y="6" width="{width-12}" height="{height-12}" fill="none" stroke="rgba(30, 41, 59, 0.85)" stroke-width="2"/>
  <rect x="12" y="12" width="{width-24}" height="{height-24}" fill="none" stroke="{prim}" stroke-width="2" opacity="0.85"/>

  <!-- CORNER BRACKETS -->
  <rect x="6" y="6" width="24" height="6" fill="{prim}"/>
  <rect x="6" y="6" width="6" height="24" fill="{prim}"/>
  <rect x="{width-30}" y="6" width="24" height="6" fill="{prim}"/>
  <rect x="{width-12}" y="6" width="6" height="24" fill="{prim}"/>
  <rect x="6" y="{height-12}" width="24" height="6" fill="{prim}"/>
  <rect x="6" y="{height-30}" width="6" height="24" fill="{prim}"/>
  <rect x="{width-30}" y="{height-12}" width="24" height="6" fill="{prim}"/>
  <rect x="{width-12}" y="{height-30}" width="6" height="24" fill="{prim}"/>

  <!-- STATUS BAR -->
  <rect x="14" y="14" width="{width-28}" height="22" fill="rgba(15, 23, 38, 0.85)"/>
  <line x1="14" y1="36" x2="{width-14}" y2="36" stroke="{prim}" stroke-width="1.5" opacity="0.6"/>
  <circle cx="28" cy="25" r="4" fill="#00D26A" class="status-led"/>
  <text x="38" y="29" fill="#00D26A" font-size="11" font-weight="bold" class="font-mono">GITHUB: DARK MODE DETECTED</text>
  <rect x="250" y="19" width="2" height="12" fill="rgba(30, 41, 59, 0.85)"/>
  <text x="262" y="29" fill="#94A3B8" font-size="11" class="font-mono">SELECTOR: #gh-dark-mode-only</text>
  <rect x="520" y="19" width="2" height="12" fill="rgba(30, 41, 59, 0.85)"/>
  <text x="532" y="29" fill="#F59E0B" font-size="11" font-weight="bold" class="font-mono">NEON_CYAN // PURPLE</text>

  <!-- WINDOW CONTROLS -->
  <rect x="{width-85}" y="19" width="16" height="12" fill="rgba(30, 41, 59, 0.85)"/>
  <text x="{width-80}" y="28" fill="#94A3B8" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-63}" y="19" width="16" height="12" fill="rgba(30, 41, 59, 0.85)"/>
  <text x="{width-59}" y="29" fill="#94A3B8" font-size="11" font-weight="bold" class="font-mono">□</text>
  <rect x="{width-41}" y="19" width="16" height="12" fill="#FF0055"/>
  <text x="{width-37}" y="29" fill="#FFFFFF" font-size="11" font-weight="bold" class="font-mono">×</text>

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUB-BADGE -->
  <g transform="translate(42, 128)">
    <rect x="0" y="0" width="460" height="26" fill="rgba(15, 23, 38, 0.85)" stroke="{acc}" stroke-width="2"/>
    <rect x="-2" y="-2" width="6" height="6" fill="{acc}"/>
    <rect x="456" y="-2" width="6" height="6" fill="{acc}"/>
    <rect x="-2" y="22" width="6" height="6" fill="{acc}"/>
    <rect x="456" y="22" width="6" height="6" fill="{acc}"/>
    <text x="12" y="18" fill="#F8F8F2" font-size="11" font-weight="bold" letter-spacing="1" class="font-mono">
      ⚡ GITHUB DARK THEME ACTIVE (#gh-dark-mode-only)
    </text>
  </g>

  <!-- TELEMETRY -->
  <g>
    <text x="42" y="180" fill="#00D26A" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="180" fill="#F8F8F2" font-size="11" class="font-mono">TRIGGER:</text>
    <text x="170" y="180" fill="{prim}" font-size="11" font-weight="bold" class="font-mono">URL Fragment #gh-dark-mode-only</text>

    <text x="42" y="200" fill="#00D26A" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="200" fill="#F8F8F2" font-size="11" class="font-mono">STATUS:</text>
    <text x="170" y="200" fill="{acc}" font-size="11" font-weight="bold" class="font-mono">Visible only in GitHub Dark Mode</text>

    <text x="42" y="220" fill="#00D26A" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="220" fill="#F8F8F2" font-size="11" class="font-mono">CONTRAST:</text>
    <text x="170" y="220" fill="#00D26A" font-size="11" font-weight="bold" class="font-mono">Optimized for dark background #0d1117</text>
    <rect x="490" y="210" width="8" height="12" fill="{prim}" class="cursor-blink"/>
  </g>

  <!-- MINI EQUALIZER -->
  <g transform="translate(515, 10)">
    <rect x="0" y="198" width="5" height="6" fill="{prim}" class="w1"/>
    <rect x="8" y="186" width="5" height="18" fill="{acc}" class="w2"/>
    <rect x="16" y="192" width="5" height="12" fill="#FF0055" class="w3"/>
    <rect x="24" y="182" width="5" height="22" fill="#F59E0B" class="w4"/>
  </g>

  <!-- 360° RADAR -->
  <g transform="translate({width-220}, 60)">
    <rect x="0" y="0" width="170" height="140" fill="rgba(15, 23, 38, 0.85)" stroke="rgba(30, 41, 59, 0.85)" stroke-width="2"/>
    <rect x="4" y="4" width="162" height="132" fill="none" stroke="{prim}" stroke-width="1" opacity="0.6"/>
    <circle cx="85" cy="70" r="50" fill="none" stroke="{prim}" stroke-width="1" stroke-dasharray="3,3" opacity="0.4"/>
    <circle cx="85" cy="70" r="35" fill="none" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <circle cx="85" cy="70" r="18" fill="none" stroke="{prim}" stroke-width="1" opacity="0.25"/>
    <line x1="85" y1="15" x2="85" y2="125" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <line x1="30" y1="70" x2="140" y2="70" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <g>
      <line x1="85" y1="70" x2="85" y2="20" stroke="#00D26A" stroke-width="2.5" opacity="0.9"/>
      <circle cx="85" cy="35" r="3.5" fill="#F59E0B"/>
      <animateTransform attributeName="transform" type="rotate" from="0 85 70" to="360 85 70" dur="4s" repeatCount="indefinite"/>
    </g>
    <circle cx="110" cy="50" r="3" fill="#FF0055">
      <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="85" y="132" fill="#00D26A" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">DARK RADAR // 360°</text>
  </g>

  <!-- BOTTOM STATUS LINE -->
  <line x1="14" y1="{height-26}" x2="{width-14}" y2="{height-26}" stroke="rgba(30, 41, 59, 0.85)" stroke-width="1"/>
  <text x="24" y="{height-15}" fill="#94A3B8" font-size="9" class="font-mono">THEME_PROFILE: GITHUB_DARK // CAMO_COMPAT: 100%</text>
  <text x="{width-24}" y="{height-15}" fill="{prim}" font-size="9" font-weight="bold" text-anchor="end" class="font-mono">MODE: DARK_ACTIVE</text>
</svg>"""
    return svg

def make_gh_light_header():
    width = 850
    height = 260
    prim = "#0969DA"        # High contrast tech blue
    acc = "#8250DF"         # GitHub deep purple
    bg = "#F6F8FA"          # GitHub light background
    mid_shadow = "#0550ae"
    dark_shadow = "#033d8b"

    grid_lines = []
    for x in range(0, width + 1, 20):
        grid_lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="{prim}" stroke-width="1"/>')
    for y in range(0, height + 1, 20):
        grid_lines.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="{prim}" stroke-width="1"/>')

    pixel_markup, _, _ = render_3d_text(
        "CYBERPUNK // LIGHT", x=42, y=62, px_size=5,
        front_color=prim, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
        spacing=2, max_width=520
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
      @keyframes ledFlicker {{ 0%, 100% {{ fill: #1a7f37; }} 50% {{ fill: #4ac26b; }} }}
      @keyframes crtScanline {{
        0% {{ transform: translateY(0px); opacity: 0; }}
        20% {{ opacity: 0.25; }}
        80% {{ opacity: 0.25; }}
        100% {{ transform: translateY({height}px); opacity: 0; }}
      }}
      @keyframes waveBar1 {{ 0%, 100% {{ height: 6px; y: 198px; }} 50% {{ height: 20px; y: 184px; }} }}
      @keyframes waveBar2 {{ 0%, 100% {{ height: 18px; y: 186px; }} 50% {{ height: 8px; y: 196px; }} }}
      @keyframes waveBar3 {{ 0%, 100% {{ height: 12px; y: 192px; }} 50% {{ height: 22px; y: 182px; }} }}
      @keyframes waveBar4 {{ 0%, 100% {{ height: 22px; y: 182px; }} 50% {{ height: 10px; y: 194px; }} }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      .cursor-blink {{ animation: blink 1s infinite steps(1); }}
      .status-led {{ animation: ledFlicker 1.8s infinite steps(1); }}
      .scan-line {{ animation: crtScanline 6s linear infinite; }}
      .w1 {{ animation: waveBar1 1.1s infinite ease-in-out; }}
      .w2 {{ animation: waveBar2 0.8s infinite ease-in-out; }}
      .w3 {{ animation: waveBar3 1.3s infinite ease-in-out; }}
      .w4 {{ animation: waveBar4 0.9s infinite ease-in-out; }}
    </style>
  </defs>

  <!-- 1. LIGHT SOLID BACKGROUND -->
  <rect x="0" y="0" width="{width}" height="{height}" fill="{bg}" stroke="#D0D7DE" stroke-width="2"/>

  <!-- 2. RETRO GRID -->
  <g opacity="0.10">
    {''.join(grid_lines)}
  </g>

  <!-- 3. ANIMATED SCANLINE -->
  <line x1="0" y1="0" x2="{width}" y2="0" stroke="{prim}" stroke-width="2" class="scan-line"/>

  <!-- 4. CHASSIS -->
  <rect x="6" y="6" width="{width-12}" height="{height-12}" fill="none" stroke="#D0D7DE" stroke-width="2"/>
  <rect x="12" y="12" width="{width-24}" height="{height-24}" fill="none" stroke="{prim}" stroke-width="2" opacity="0.85"/>

  <!-- CORNER BRACKETS -->
  <rect x="6" y="6" width="24" height="6" fill="{prim}"/>
  <rect x="6" y="6" width="6" height="24" fill="{prim}"/>
  <rect x="{width-30}" y="6" width="24" height="6" fill="{prim}"/>
  <rect x="{width-12}" y="6" width="6" height="24" fill="{prim}"/>
  <rect x="6" y="{height-12}" width="24" height="6" fill="{prim}"/>
  <rect x="6" y="{height-30}" width="6" height="24" fill="{prim}"/>
  <rect x="{width-30}" y="{height-12}" width="24" height="6" fill="{prim}"/>
  <rect x="{width-12}" y="{height-30}" width="6" height="24" fill="{prim}"/>

  <!-- STATUS BAR -->
  <rect x="14" y="14" width="{width-28}" height="22" fill="#EAEFF5"/>
  <line x1="14" y1="36" x2="{width-14}" y2="36" stroke="{prim}" stroke-width="1.5" opacity="0.6"/>
  <circle cx="28" cy="25" r="4" fill="#1A7F37" class="status-led"/>
  <text x="38" y="29" fill="#1A7F37" font-size="11" font-weight="bold" class="font-mono">GITHUB: LIGHT MODE DETECTED</text>
  <rect x="250" y="19" width="2" height="12" fill="#D0D7DE"/>
  <text x="262" y="29" fill="#57606A" font-size="11" class="font-mono">SELECTOR: #gh-light-mode-only</text>
  <rect x="520" y="19" width="2" height="12" fill="#D0D7DE"/>
  <text x="532" y="29" fill="#8250DF" font-size="11" font-weight="bold" class="font-mono">TECH_BLUE // VIOLET</text>

  <!-- WINDOW CONTROLS -->
  <rect x="{width-85}" y="19" width="16" height="12" fill="#D0D7DE"/>
  <text x="{width-80}" y="28" fill="#57606A" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-63}" y="19" width="16" height="12" fill="#D0D7DE"/>
  <text x="{width-59}" y="29" fill="#57606A" font-size="11" font-weight="bold" class="font-mono">□</text>
  <rect x="{width-41}" y="19" width="16" height="12" fill="#CF222E"/>
  <text x="{width-37}" y="29" fill="#FFFFFF" font-size="11" font-weight="bold" class="font-mono">×</text>

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUB-BADGE -->
  <g transform="translate(42, 128)">
    <rect x="0" y="0" width="460" height="26" fill="#FFFFFF" stroke="{acc}" stroke-width="2"/>
    <rect x="-2" y="-2" width="6" height="6" fill="{acc}"/>
    <rect x="456" y="-2" width="6" height="6" fill="{acc}"/>
    <rect x="-2" y="22" width="6" height="6" fill="{acc}"/>
    <rect x="456" y="22" width="6" height="6" fill="{acc}"/>
    <text x="12" y="18" fill="#1F2328" font-size="11" font-weight="bold" letter-spacing="1" class="font-mono">
      ⚡ GITHUB LIGHT THEME ACTIVE (#gh-light-mode-only)
    </text>
  </g>

  <!-- TELEMETRY -->
  <g>
    <text x="42" y="180" fill="#1A7F37" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="180" fill="#1F2328" font-size="11" class="font-mono">TRIGGER:</text>
    <text x="170" y="180" fill="{prim}" font-size="11" font-weight="bold" class="font-mono">URL Fragment #gh-light-mode-only</text>

    <text x="42" y="200" fill="#1A7F37" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="200" fill="#1F2328" font-size="11" class="font-mono">STATUS:</text>
    <text x="170" y="200" fill="{acc}" font-size="11" font-weight="bold" class="font-mono">Visible only in GitHub Light Mode</text>

    <text x="42" y="220" fill="#1A7F37" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="220" fill="#1F2328" font-size="11" class="font-mono">CONTRAST:</text>
    <text x="170" y="220" fill="#1A7F37" font-size="11" font-weight="bold" class="font-mono">High-contrast daytime clarity (11:1)</text>
    <rect x="490" y="210" width="8" height="12" fill="{prim}" class="cursor-blink"/>
  </g>

  <!-- MINI EQUALIZER -->
  <g transform="translate(515, 10)">
    <rect x="0" y="198" width="5" height="6" fill="{prim}" class="w1"/>
    <rect x="8" y="186" width="5" height="18" fill="{acc}" class="w2"/>
    <rect x="16" y="192" width="5" height="12" fill="#CF222E" class="w3"/>
    <rect x="24" y="182" width="5" height="22" fill="#9A6700" class="w4"/>
  </g>

  <!-- 360° RADAR -->
  <g transform="translate({width-220}, 60)">
    <rect x="0" y="0" width="170" height="140" fill="#FFFFFF" stroke="#D0D7DE" stroke-width="2"/>
    <rect x="4" y="4" width="162" height="132" fill="none" stroke="{prim}" stroke-width="1" opacity="0.6"/>
    <circle cx="85" cy="70" r="50" fill="none" stroke="{prim}" stroke-width="1" stroke-dasharray="3,3" opacity="0.4"/>
    <circle cx="85" cy="70" r="35" fill="none" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <circle cx="85" cy="70" r="18" fill="none" stroke="{prim}" stroke-width="1" opacity="0.25"/>
    <line x1="85" y1="15" x2="85" y2="125" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <line x1="30" y1="70" x2="140" y2="70" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <g>
      <line x1="85" y1="70" x2="85" y2="20" stroke="#1A7F37" stroke-width="2.5" opacity="0.9"/>
      <circle cx="85" cy="35" r="3.5" fill="#9A6700"/>
      <animateTransform attributeName="transform" type="rotate" from="0 85 70" to="360 85 70" dur="4s" repeatCount="indefinite"/>
    </g>
    <circle cx="110" cy="50" r="3" fill="#CF222E">
      <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="85" y="132" fill="#1A7F37" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">LIGHT RADAR // 360°</text>
  </g>

  <!-- BOTTOM STATUS LINE -->
  <line x1="14" y1="{height-26}" x2="{width-14}" y2="{height-26}" stroke="#D0D7DE" stroke-width="1"/>
  <text x="24" y="{height-15}" fill="#57606A" font-size="9" class="font-mono">THEME_PROFILE: GITHUB_LIGHT // CAMO_COMPAT: 100%</text>
  <text x="{width-24}" y="{height-15}" fill="{prim}" font-size="9" font-weight="bold" text-anchor="end" class="font-mono">MODE: LIGHT_ACTIVE</text>
</svg>"""
    return svg


# ==============================================================================
# TEST 2: HTML5 <picture> (header-pic-dark.svg & header-pic-light.svg)
# ==============================================================================

def make_pic_dark_header():
    width = 850
    height = 220
    prim = "#F59E0B"        # Tactical Amber
    acc = "#EA580C"
    bg = "rgba(10, 14, 23, 0.88)"
    mid_shadow = "#92400e"
    dark_shadow = "#451a03"

    pixel_markup, _, _ = render_3d_text(
        "PICTURE // DARK", x=42, y=52, px_size=5,
        front_color=prim, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
        spacing=2, max_width=520
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      @keyframes targetScan {{
        0% {{ transform: translateX(0px); opacity: 0; }}
        15% {{ opacity: 0.8; }}
        85% {{ opacity: 0.8; }}
        100% {{ transform: translateX({width-100}px); opacity: 0; }}
      }}
      @keyframes pulseLock {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.4; transform: scale(0.96); }}
      }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      .laser-scan {{ animation: targetScan 4s ease-in-out infinite; }}
      .reticle-pulse {{ transform-origin: 750px 105px; animation: pulseLock 2s infinite ease-in-out; }}
    </style>
  </defs>

  <!-- 45° CHAMFERED CHASSIS -->
  <polygon points="20 4, {width-20} 4, {width-4} 20, {width-4} {height-20}, {width-20} {height-4}, 20 {height-4}, 4 {height-20}, 4 20"
           fill="{bg}" stroke="rgba(50, 36, 16, 0.85)" stroke-width="2"/>
  <polygon points="24 10, {width-24} 10, {width-10} 24, {width-10} {height-24}, {width-24} {height-10}, 24 {height-10}, 10 {height-24}, 10 24"
           fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.75"/>

  <!-- CORNER ACCENTS -->
  <polygon points="20 4, 35 4, 4 35, 4 20" fill="{prim}"/>
  <polygon points="{width-20} 4, {width-35} 4, {width-4} 35, {width-4} 20" fill="{prim}"/>
  <polygon points="20 {height-4}, 35 {height-4}, 4 {height-35}, 4 {height-20}" fill="{prim}"/>
  <polygon points="{width-20} {height-4}, {width-35} {height-4}, {width-4} {height-35}, {width-4} {height-20}" fill="{prim}"/>

  <!-- TOP BAR -->
  <text x="35" y="24" fill="{prim}" font-size="10" font-weight="bold" class="font-mono">▲ HTML5 &lt;picture&gt; CONTAINER</text>
  <text x="270" y="24" fill="#94A3B8" font-size="10" class="font-mono">MEDIA: (prefers-color-scheme: dark)</text>
  <text x="{width-35}" y="24" fill="{acc}" font-size="10" font-weight="bold" text-anchor="end" class="font-mono">SYSTEM_THEME // DARK</text>

  <!-- 3D TITLE -->
  {pixel_markup}

  <!-- SUBTITLE -->
  <text x="42" y="115" fill="#F8F8F2" font-size="12" font-weight="bold" class="font-mono">
    ⚡ ADAPTIVE VIA HTML5 &lt;picture&gt; (DARK SCHEME ACTIVE)
  </text>

  <!-- TELEMETRY -->
  <text x="42" y="148" fill="{prim}" font-size="11" class="font-mono">&gt; SOURCE: <tspan fill="#F8F8F2">&lt;source media="(prefers-color-scheme: dark)" ...&gt;</tspan></text>
  <text x="42" y="168" fill="{prim}" font-size="11" class="font-mono">&gt; PALETTE: <tspan fill="{acc}">TACTICAL AMBER // DARK GLASS</tspan></text>
  <text x="42" y="188" fill="{prim}" font-size="11" class="font-mono">&gt; ENGINE: <tspan fill="#00D26A">Client Browser System Theme Switcher</tspan></text>

  <!-- RETICLE HUD -->
  <g class="reticle-pulse">
    <circle cx="750" cy="105" r="42" fill="none" stroke="{prim}" stroke-width="1.5" stroke-dasharray="8,4" opacity="0.75"/>
    <circle cx="750" cy="105" r="22" fill="none" stroke="{acc}" stroke-width="1.5" opacity="0.6"/>
    <circle cx="750" cy="105" r="4" fill="{prim}"/>
    <line x1="750" y1="52" x2="750" y2="158" stroke="{prim}" stroke-width="1" stroke-dasharray="2,2" opacity="0.5"/>
    <line x1="698" y1="105" x2="802" y2="105" stroke="{prim}" stroke-width="1" stroke-dasharray="2,2" opacity="0.5"/>
  </g>
</svg>"""
    return svg

def make_pic_light_header():
    width = 850
    height = 220
    prim = "#B45309"        # High-contrast daytime amber
    acc = "#C2410C"
    bg = "#FFFBEB"          # Soft warm paper background
    mid_shadow = "#78350f"
    dark_shadow = "#451a03"

    pixel_markup, _, _ = render_3d_text(
        "PICTURE // LIGHT", x=42, y=52, px_size=5,
        front_color=prim, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
        spacing=2, max_width=520
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      @keyframes targetScan {{
        0% {{ transform: translateX(0px); opacity: 0; }}
        15% {{ opacity: 0.8; }}
        85% {{ opacity: 0.8; }}
        100% {{ transform: translateX({width-100}px); opacity: 0; }}
      }}
      @keyframes pulseLock {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.4; transform: scale(0.96); }}
      }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      .laser-scan {{ animation: targetScan 4s ease-in-out infinite; }}
      .reticle-pulse {{ transform-origin: 750px 105px; animation: pulseLock 2s infinite ease-in-out; }}
    </style>
  </defs>

  <!-- 45° CHAMFERED CHASSIS -->
  <polygon points="20 4, {width-20} 4, {width-4} 20, {width-4} {height-20}, {width-20} {height-4}, 20 {height-4}, 4 {height-20}, 4 20"
           fill="{bg}" stroke="#FDE68A" stroke-width="2"/>
  <polygon points="24 10, {width-24} 10, {width-10} 24, {width-10} {height-24}, {width-24} {height-10}, 24 {height-10}, 10 {height-24}, 10 24"
           fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.85"/>

  <!-- CORNER ACCENTS -->
  <polygon points="20 4, 35 4, 4 35, 4 20" fill="{prim}"/>
  <polygon points="{width-20} 4, {width-35} 4, {width-4} 35, {width-4} 20" fill="{prim}"/>
  <polygon points="20 {height-4}, 35 {height-4}, 4 {height-35}, 4 {height-20}" fill="{prim}"/>
  <polygon points="{width-20} {height-4}, {width-35} {height-4}, {width-4} {height-35}, {width-4} {height-20}" fill="{prim}"/>

  <!-- TOP BAR -->
  <text x="35" y="24" fill="{prim}" font-size="10" font-weight="bold" class="font-mono">▲ HTML5 &lt;picture&gt; CONTAINER</text>
  <text x="270" y="24" fill="#6B7280" font-size="10" class="font-mono">MEDIA: (prefers-color-scheme: light)</text>
  <text x="{width-35}" y="24" fill="{acc}" font-size="10" font-weight="bold" text-anchor="end" class="font-mono">SYSTEM_THEME // LIGHT</text>

  <!-- 3D TITLE -->
  {pixel_markup}

  <!-- SUBTITLE -->
  <text x="42" y="115" fill="#1F2937" font-size="12" font-weight="bold" class="font-mono">
    ⚡ ADAPTIVE VIA HTML5 &lt;picture&gt; (LIGHT SCHEME ACTIVE)
  </text>

  <!-- TELEMETRY -->
  <text x="42" y="148" fill="{prim}" font-size="11" class="font-mono">&gt; SOURCE: <tspan fill="#1F2937">&lt;source media="(prefers-color-scheme: light)" ...&gt;</tspan></text>
  <text x="42" y="168" fill="{prim}" font-size="11" class="font-mono">&gt; PALETTE: <tspan fill="{acc}">WARM OCHRE // HIGH CONTRAST</tspan></text>
  <text x="42" y="188" fill="{prim}" font-size="11" class="font-mono">&gt; ENGINE: <tspan fill="#15803D">Client Browser System Theme Switcher</tspan></text>

  <!-- RETICLE HUD -->
  <g class="reticle-pulse">
    <circle cx="750" cy="105" r="42" fill="none" stroke="{prim}" stroke-width="1.5" stroke-dasharray="8,4" opacity="0.75"/>
    <circle cx="750" cy="105" r="22" fill="none" stroke="{acc}" stroke-width="1.5" opacity="0.6"/>
    <circle cx="750" cy="105" r="4" fill="{prim}"/>
    <line x1="750" y1="52" x2="750" y2="158" stroke="{prim}" stroke-width="1" stroke-dasharray="2,2" opacity="0.5"/>
    <line x1="698" y1="105" x2="802" y2="105" stroke="{prim}" stroke-width="1" stroke-dasharray="2,2" opacity="0.5"/>
  </g>
</svg>"""
    return svg


# ==============================================================================
# TEST 3: Single SVG with Internal CSS @media (prefers-color-scheme: dark)
# ==============================================================================

def make_internal_adaptive_header():
    width = 850
    height = 260

    # We generate pixel text with CSS classes!
    # front-face, mid-shadow, dark-shadow will have CSS classes
    px_size = 5
    from generator.font_engine import GLYPHS, matrix_to_rects
    text = "ADAPTIVE // SVG"
    
    shadow_dark_rects = []
    shadow_mid_rects = []
    front_rects = []

    curr_x = 42
    y = 62
    for char in text.upper():
        glyph = GLYPHS.get(char, GLYPHS[' '])
        w = len(glyph[0])
        # We pass CSS class placeholders or inline styles with variables!
        shadow_dark_rects.append(matrix_to_rects(glyph, 'X', "var(--title-dark)", px_size, curr_x + int(px_size * 1.2), y + int(px_size * 1.2)))
        shadow_mid_rects.append(matrix_to_rects(glyph, 'X', "var(--title-mid)", px_size, curr_x + int(px_size * 0.6), y + int(px_size * 0.6)))
        front_rects.append(matrix_to_rects(glyph, 'X', "var(--title-front)", px_size, curr_x, y))
        curr_x += (w + 2) * px_size

    pixel_markup = f"""<g class="pixel-text-3d">
  <!-- Shadow Dark -->
  {''.join(shadow_dark_rects)}
  <!-- Shadow Mid -->
  {''.join(shadow_mid_rects)}
  <!-- Front Face -->
  {''.join(front_rects)}
</g>"""

    grid_lines = []
    for x in range(0, width + 1, 20):
        grid_lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="var(--primary)" stroke-width="1"/>')
    for y_line in range(0, height + 1, 20):
        grid_lines.append(f'<line x1="0" y1="{y_line}" x2="{width}" y2="{y_line}" stroke="var(--primary)" stroke-width="1"/>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      :root {{
        --bg-glass: #F6F8FA;
        --border-chassis: #D0D7DE;
        --primary: #0969DA;
        --accent: #8250DF;
        --title-front: #0969DA;
        --title-mid: #0550AE;
        --title-dark: #033D8B;
        --text-main: #1F2328;
        --text-muted: #57606A;
        --status-color: #1A7F37;
        --bar-fill: #EAEFF5;
        --sub-bg: #FFFFFF;
        --sub-border: #8250DF;
        --radar-grid: #0969DA;
        --theme-label: "INTERNAL CSS: LIGHT DETECTED";
      }}

      @media (prefers-color-scheme: dark) {{
        :root {{
          --bg-glass: rgba(10, 14, 23, 0.85);
          --border-chassis: rgba(30, 41, 59, 0.85);
          --primary: #00C8D7;
          --accent: #A855F7;
          --title-front: #00C8D7;
          --title-mid: #006B74;
          --title-dark: #002B2F;
          --text-main: #F8F8F2;
          --text-muted: #94A3B8;
          --status-color: #00D26A;
          --bar-fill: rgba(15, 23, 38, 0.85);
          --sub-bg: rgba(15, 23, 38, 0.85);
          --sub-border: #A855F7;
          --radar-grid: #00C8D7;
          --theme-label: "INTERNAL CSS: DARK DETECTED";
        }}
      }}

      @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
      @keyframes ledFlicker {{ 0%, 100% {{ fill: var(--status-color); }} 50% {{ fill: #004411; }} }}
      @keyframes crtScanline {{
        0% {{ transform: translateY(0px); opacity: 0; }}
        20% {{ opacity: 0.25; }}
        80% {{ opacity: 0.25; }}
        100% {{ transform: translateY({height}px); opacity: 0; }}
      }}
      @keyframes waveBar1 {{ 0%, 100% {{ height: 6px; y: 198px; }} 50% {{ height: 20px; y: 184px; }} }}
      @keyframes waveBar2 {{ 0%, 100% {{ height: 18px; y: 186px; }} 50% {{ height: 8px; y: 196px; }} }}
      @keyframes waveBar3 {{ 0%, 100% {{ height: 12px; y: 192px; }} 50% {{ height: 22px; y: 182px; }} }}
      @keyframes waveBar4 {{ 0%, 100% {{ height: 22px; y: 182px; }} 50% {{ height: 10px; y: 194px; }} }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      .cursor-blink {{ animation: blink 1s infinite steps(1); }}
      .status-led {{ animation: ledFlicker 1.8s infinite steps(1); }}
      .scan-line {{ animation: crtScanline 6s linear infinite; }}
      .w1 {{ animation: waveBar1 1.1s infinite ease-in-out; }}
      .w2 {{ animation: waveBar2 0.8s infinite ease-in-out; }}
      .w3 {{ animation: waveBar3 1.3s infinite ease-in-out; }}
      .w4 {{ animation: waveBar4 0.9s infinite ease-in-out; }}
    </style>
  </defs>

  <!-- 1. DYNAMIC BACKGROUND -->
  <rect x="0" y="0" width="{width}" height="{height}" fill="var(--bg-glass)"/>

  <!-- 2. RETRO GRID -->
  <g opacity="0.08">
    {''.join(grid_lines)}
  </g>

  <!-- 3. ANIMATED SCANLINE -->
  <line x1="0" y1="0" x2="{width}" y2="0" stroke="var(--primary)" stroke-width="2" class="scan-line"/>

  <!-- 4. CHASSIS -->
  <rect x="6" y="6" width="{width-12}" height="{height-12}" fill="none" stroke="var(--border-chassis)" stroke-width="2"/>
  <rect x="12" y="12" width="{width-24}" height="{height-24}" fill="none" stroke="var(--primary)" stroke-width="2" opacity="0.85"/>

  <!-- CORNER BRACKETS -->
  <rect x="6" y="6" width="24" height="6" fill="var(--primary)"/>
  <rect x="6" y="6" width="6" height="24" fill="var(--primary)"/>
  <rect x="{width-30}" y="6" width="24" height="6" fill="var(--primary)"/>
  <rect x="{width-12}" y="6" width="6" height="24" fill="var(--primary)"/>
  <rect x="6" y="{height-12}" width="24" height="6" fill="var(--primary)"/>
  <rect x="6" y="{height-30}" width="6" height="24" fill="var(--primary)"/>
  <rect x="{width-30}" y="{height-12}" width="24" height="6" fill="var(--primary)"/>
  <rect x="{width-12}" y="{height-30}" width="6" height="24" fill="var(--primary)"/>

  <!-- STATUS BAR -->
  <rect x="14" y="14" width="{width-28}" height="22" fill="var(--bar-fill)"/>
  <line x1="14" y1="36" x2="{width-14}" y2="36" stroke="var(--primary)" stroke-width="1.5" opacity="0.6"/>
  <circle cx="28" cy="25" r="4" fill="var(--status-color)" class="status-led"/>
  <text x="38" y="29" fill="var(--status-color)" font-size="11" font-weight="bold" class="font-mono">1 SINGLE SVG: DYNAMIC CSS VARIABLES</text>
  <rect x="330" y="19" width="2" height="12" fill="var(--border-chassis)"/>
  <text x="342" y="29" fill="var(--text-muted)" font-size="11" class="font-mono">CSS: @media (prefers-color-scheme)</text>

  <!-- WINDOW CONTROLS -->
  <rect x="{width-85}" y="19" width="16" height="12" fill="var(--border-chassis)"/>
  <text x="{width-80}" y="28" fill="var(--text-muted)" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-63}" y="19" width="16" height="12" fill="var(--border-chassis)"/>
  <text x="{width-59}" y="29" fill="var(--text-muted)" font-size="11" font-weight="bold" class="font-mono">□</text>
  <rect x="{width-41}" y="19" width="16" height="12" fill="#FF0055"/>
  <text x="{width-37}" y="29" fill="#FFFFFF" font-size="11" font-weight="bold" class="font-mono">×</text>

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUB-BADGE -->
  <g transform="translate(42, 128)">
    <rect x="0" y="0" width="460" height="26" fill="var(--sub-bg)" stroke="var(--sub-border)" stroke-width="2"/>
    <rect x="-2" y="-2" width="6" height="6" fill="var(--sub-border)"/>
    <rect x="456" y="-2" width="6" height="6" fill="var(--sub-border)"/>
    <rect x="-2" y="22" width="6" height="6" fill="var(--sub-border)"/>
    <rect x="456" y="22" width="6" height="6" fill="var(--sub-border)"/>
    <text x="12" y="18" fill="var(--text-main)" font-size="11" font-weight="bold" letter-spacing="1" class="font-mono">
      ⚡ SINGLE FILE: ADAPTS VIA INTERNAL SVG CSS
    </text>
  </g>

  <!-- TELEMETRY -->
  <g>
    <text x="42" y="180" fill="var(--status-color)" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="180" fill="var(--text-main)" font-size="11" class="font-mono">METHOD:</text>
    <text x="170" y="180" fill="var(--primary)" font-size="11" font-weight="bold" class="font-mono">Single SVG with :root &amp; @media inside</text>

    <text x="42" y="200" fill="var(--status-color)" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="200" fill="var(--text-main)" font-size="11" class="font-mono">REPOSITORIES:</text>
    <text x="170" y="200" fill="var(--accent)" font-size="11" font-weight="bold" class="font-mono">Zero asset duplicates (only 1 file stored)</text>

    <text x="42" y="220" fill="var(--status-color)" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="220" fill="var(--text-main)" font-size="11" class="font-mono">SWITCHING:</text>
    <text x="170" y="220" fill="var(--status-color)" font-size="11" font-weight="bold" class="font-mono">Instant live CSS repaint on scheme change</text>
    <rect x="490" y="210" width="8" height="12" fill="var(--primary)" class="cursor-blink"/>
  </g>

  <!-- MINI EQUALIZER -->
  <g transform="translate(515, 10)">
    <rect x="0" y="198" width="5" height="6" fill="var(--primary)" class="w1"/>
    <rect x="8" y="186" width="5" height="18" fill="var(--accent)" class="w2"/>
    <rect x="16" y="192" width="5" height="12" fill="#FF0055" class="w3"/>
    <rect x="24" y="182" width="5" height="22" fill="#F59E0B" class="w4"/>
  </g>

  <!-- 360° RADAR -->
  <g transform="translate({width-220}, 60)">
    <rect x="0" y="0" width="170" height="140" fill="var(--bar-fill)" stroke="var(--border-chassis)" stroke-width="2"/>
    <rect x="4" y="4" width="162" height="132" fill="none" stroke="var(--radar-grid)" stroke-width="1" opacity="0.6"/>
    <circle cx="85" cy="70" r="50" fill="none" stroke="var(--radar-grid)" stroke-width="1" stroke-dasharray="3,3" opacity="0.4"/>
    <circle cx="85" cy="70" r="35" fill="none" stroke="var(--radar-grid)" stroke-width="1" opacity="0.3"/>
    <circle cx="85" cy="70" r="18" fill="none" stroke="var(--radar-grid)" stroke-width="1" opacity="0.25"/>
    <line x1="85" y1="15" x2="85" y2="125" stroke="var(--radar-grid)" stroke-width="1" opacity="0.3"/>
    <line x1="30" y1="70" x2="140" y2="70" stroke="var(--radar-grid)" stroke-width="1" opacity="0.3"/>
    <g>
      <line x1="85" y1="70" x2="85" y2="20" stroke="var(--status-color)" stroke-width="2.5" opacity="0.9"/>
      <circle cx="85" cy="35" r="3.5" fill="#F59E0B"/>
      <animateTransform attributeName="transform" type="rotate" from="0 85 70" to="360 85 70" dur="4s" repeatCount="indefinite"/>
    </g>
    <circle cx="110" cy="50" r="3" fill="#FF0055">
      <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="85" y="132" fill="var(--status-color)" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">ADAPTIVE RADAR</text>
  </g>

  <!-- BOTTOM STATUS LINE -->
  <line x1="14" y1="{height-26}" x2="{width-14}" y2="{height-26}" stroke="var(--border-chassis)" stroke-width="1"/>
  <text x="24" y="{height-15}" fill="var(--text-muted)" font-size="9" class="font-mono">ENGINE: EMBEDDED_CSS_VARIABLES // CAMO_OK</text>
  <text x="{width-24}" y="{height-15}" fill="var(--primary)" font-size="9" font-weight="bold" text-anchor="end" class="font-mono">AUTO_DETECT: PASS</text>
</svg>"""
    return svg


# ==============================================================================
# TEST 4: 100% Transparent Background Cyberpunk Header (Zero Fill)
# ==============================================================================

def make_transparent_header():
    width = 850
    height = 260
    prim = "#00C8D7"
    acc = "#A855F7"
    mid_shadow = "#006b74"
    dark_shadow = "#002b2f"

    grid_lines = []
    for x in range(0, width + 1, 20):
        grid_lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="{prim}" stroke-width="1"/>')
    for y in range(0, height + 1, 20):
        grid_lines.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="{prim}" stroke-width="1"/>')

    pixel_markup, _, _ = render_3d_text(
        "CYBER // ZERO BG", x=42, y=62, px_size=5,
        front_color=prim, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
        spacing=2, max_width=520
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
      @keyframes ledFlicker {{ 0%, 100% {{ fill: #00D26A; }} 50% {{ fill: #005511; }} }}
      @keyframes crtScanline {{
        0% {{ transform: translateY(0px); opacity: 0; }}
        20% {{ opacity: 0.35; }}
        80% {{ opacity: 0.35; }}
        100% {{ transform: translateY({height}px); opacity: 0; }}
      }}
      @keyframes waveBar1 {{ 0%, 100% {{ height: 6px; y: 198px; }} 50% {{ height: 20px; y: 184px; }} }}
      @keyframes waveBar2 {{ 0%, 100% {{ height: 18px; y: 186px; }} 50% {{ height: 8px; y: 196px; }} }}
      @keyframes waveBar3 {{ 0%, 100% {{ height: 12px; y: 192px; }} 50% {{ height: 22px; y: 182px; }} }}
      @keyframes waveBar4 {{ 0%, 100% {{ height: 22px; y: 182px; }} 50% {{ height: 10px; y: 194px; }} }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      .cursor-blink {{ animation: blink 1s infinite steps(1); }}
      .status-led {{ animation: ledFlicker 1.8s infinite steps(1); }}
      .scan-line {{ animation: crtScanline 6s linear infinite; }}
      .w1 {{ animation: waveBar1 1.1s infinite ease-in-out; }}
      .w2 {{ animation: waveBar2 0.8s infinite ease-in-out; }}
      .w3 {{ animation: waveBar3 1.3s infinite ease-in-out; }}
      .w4 {{ animation: waveBar4 0.9s infinite ease-in-out; }}
    </style>
  </defs>

  <!-- 1. ZERO BACKGROUND: RECT OMITTED ENTIRELY, 100% TRANSPARENT -->

  <!-- 2. MATRIX RETRO GRID (OVERLAY DIRECTLY ON GITHUB BACKGROUND) -->
  <g opacity="0.12">
    {''.join(grid_lines)}
  </g>

  <!-- 3. ANIMATED SCANLINE -->
  <line x1="0" y1="0" x2="{width}" y2="0" stroke="{prim}" stroke-width="2" class="scan-line"/>

  <!-- 4. CHASSIS / WIREFRAME (NO GLASS FILL) -->
  <rect x="6" y="6" width="{width-12}" height="{height-12}" fill="none" stroke="{prim}" stroke-width="2"/>
  <rect x="12" y="12" width="{width-24}" height="{height-24}" fill="none" stroke="rgba(0, 200, 215, 0.4)" stroke-width="1.5"/>

  <!-- CORNER BRACKETS -->
  <rect x="6" y="6" width="24" height="6" fill="{prim}"/>
  <rect x="6" y="6" width="6" height="24" fill="{prim}"/>
  <rect x="{width-30}" y="6" width="24" height="6" fill="{prim}"/>
  <rect x="{width-12}" y="6" width="6" height="24" fill="{prim}"/>
  <rect x="6" y="{height-12}" width="24" height="6" fill="{prim}"/>
  <rect x="6" y="{height-30}" width="6" height="24" fill="{prim}"/>
  <rect x="{width-30}" y="{height-12}" width="24" height="6" fill="{prim}"/>
  <rect x="{width-12}" y="{height-30}" width="6" height="24" fill="{prim}"/>

  <!-- TOP WIREFRAME STATUS BAR -->
  <rect x="14" y="14" width="{width-28}" height="22" fill="none" stroke="{prim}" stroke-width="1" opacity="0.7"/>
  <circle cx="28" cy="25" r="4" fill="#00D26A" class="status-led"/>
  <text x="38" y="29" fill="#00D26A" font-size="11" font-weight="bold" class="font-mono">BG_ALPHA: 0.00 // ZERO_FILL</text>
  <line x1="240" y1="19" x2="240" y2="31" stroke="{prim}" stroke-width="1" opacity="0.6"/>
  <text x="252" y="29" fill="{prim}" font-size="11" class="font-mono">TRANSPARENT HOLOGRAPHIC HUD</text>
  <line x1="510" y1="19" x2="510" y2="31" stroke="{prim}" stroke-width="1" opacity="0.6"/>
  <text x="522" y="29" fill="#FF0055" font-size="11" font-weight="bold" class="font-mono">PURE_TRANSPARENCY</text>

  <!-- WINDOW CONTROLS -->
  <rect x="{width-85}" y="19" width="16" height="12" fill="none" stroke="{prim}" stroke-width="1"/>
  <text x="{width-80}" y="28" fill="{prim}" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-63}" y="19" width="16" height="12" fill="none" stroke="{prim}" stroke-width="1"/>
  <text x="{width-59}" y="29" fill="{prim}" font-size="11" font-weight="bold" class="font-mono">□</text>
  <rect x="{width-41}" y="19" width="16" height="12" fill="#FF0055"/>
  <text x="{width-37}" y="29" fill="#FFFFFF" font-size="11" font-weight="bold" class="font-mono">×</text>

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUB-BADGE (TRANSPARENT SKELETON) -->
  <g transform="translate(42, 128)">
    <rect x="0" y="0" width="460" height="26" fill="none" stroke="{acc}" stroke-width="2"/>
    <rect x="-2" y="-2" width="6" height="6" fill="{acc}"/>
    <rect x="456" y="-2" width="6" height="6" fill="{acc}"/>
    <rect x="-2" y="22" width="6" height="6" fill="{acc}"/>
    <rect x="456" y="22" width="6" height="6" fill="{acc}"/>
    <text x="12" y="18" fill="{acc}" font-size="11" font-weight="bold" letter-spacing="1" class="font-mono">
      ⚡ 100% PURE TRANSPARENT BACKGROUND (ZERO GLASS)
    </text>
  </g>

  <!-- TELEMETRY -->
  <g>
    <text x="42" y="180" fill="#00D26A" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="180" fill="#00C8D7" font-size="11" class="font-mono">SURFACE:</text>
    <text x="170" y="180" fill="#FF0055" font-size="11" font-weight="bold" class="font-mono">Takes exact page background of GitHub</text>

    <text x="42" y="200" fill="#00D26A" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="200" fill="#00C8D7" font-size="11" class="font-mono">DARK THEME:</text>
    <text x="170" y="200" fill="#00D26A" font-size="11" font-weight="bold" class="font-mono">Neon lines glow directly on #0d1117</text>

    <text x="42" y="220" fill="#00D26A" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="220" fill="#00C8D7" font-size="11" class="font-mono">LIGHT THEME:</text>
    <text x="170" y="220" fill="#F59E0B" font-size="11" font-weight="bold" class="font-mono">Noticeable decrease in contrast on #FFFFFF!</text>
    <rect x="490" y="210" width="8" height="12" fill="{prim}" class="cursor-blink"/>
  </g>

  <!-- MINI EQUALIZER -->
  <g transform="translate(515, 10)">
    <rect x="0" y="198" width="5" height="6" fill="{prim}" class="w1"/>
    <rect x="8" y="186" width="5" height="18" fill="{acc}" class="w2"/>
    <rect x="16" y="192" width="5" height="12" fill="#FF0055" class="w3"/>
    <rect x="24" y="182" width="5" height="22" fill="#F59E0B" class="w4"/>
  </g>

  <!-- 360° RADAR (TRANSPARENT HOUSING) -->
  <g transform="translate({width-220}, 60)">
    <rect x="0" y="0" width="170" height="140" fill="none" stroke="{prim}" stroke-width="1.5"/>
    <rect x="4" y="4" width="162" height="132" fill="none" stroke="{acc}" stroke-width="1" opacity="0.4"/>
    <circle cx="85" cy="70" r="50" fill="none" stroke="{prim}" stroke-width="1" stroke-dasharray="3,3" opacity="0.5"/>
    <circle cx="85" cy="70" r="35" fill="none" stroke="{prim}" stroke-width="1" opacity="0.4"/>
    <circle cx="85" cy="70" r="18" fill="none" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <line x1="85" y1="15" x2="85" y2="125" stroke="{prim}" stroke-width="1" opacity="0.4"/>
    <line x1="30" y1="70" x2="140" y2="70" stroke="{prim}" stroke-width="1" opacity="0.4"/>
    <g>
      <line x1="85" y1="70" x2="85" y2="20" stroke="#00D26A" stroke-width="2.5" opacity="0.9"/>
      <circle cx="85" cy="35" r="3.5" fill="#F59E0B"/>
      <animateTransform attributeName="transform" type="rotate" from="0 85 70" to="360 85 70" dur="4s" repeatCount="indefinite"/>
    </g>
    <circle cx="110" cy="50" r="3" fill="#FF0055">
      <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="85" y="132" fill="#00D26A" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">WIRE_RADAR // 360°</text>
  </g>

  <!-- BOTTOM STATUS LINE -->
  <line x1="14" y1="{height-26}" x2="{width-14}" y2="{height-26}" stroke="{prim}" stroke-width="1" opacity="0.5"/>
  <text x="24" y="{height-15}" fill="{prim}" font-size="9" class="font-mono">OPACITY: 0% // GLASS_OFF // COMPARISON_SURFACE</text>
  <text x="{width-24}" y="{height-15}" fill="{acc}" font-size="9" font-weight="bold" text-anchor="end" class="font-mono">TEST_FOUR: ACTIVE</text>
</svg>"""
    return svg

def main():
    print("[*] Generating Theme Test SVGs...")
    save_svg("header-gh-dark.svg", make_gh_dark_header())
    save_svg("header-gh-light.svg", make_gh_light_header())
    save_svg("header-pic-dark.svg", make_pic_dark_header())
    save_svg("header-pic-light.svg", make_pic_light_header())
    save_svg("header-adaptive-internal.svg", make_internal_adaptive_header())
    save_svg("header-transparent.svg", make_transparent_header())
    print("[+] All 6 SVGs generated and validated successfully!")

if __name__ == "__main__":
    main()
