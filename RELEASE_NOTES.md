# ReadmeKit v5.1.0 — Release Notes & Marketplace Package

> **Инструкция для публикации релиза**:
> 1. Ссылка: [https://github.com/Kazinagg/readme-kit/releases/new?marketplace=true](https://github.com/Kazinagg/readme-kit/releases/new?marketplace=true)
> 2. Примите соглашение: кликните по синей ссылке `accept the GitHub Marketplace Developer Agreement`.
> 3. Поставьте галочку в чекбоксе `Publish this release to the GitHub Marketplace`.
> 4. Скопируйте текст из блока ниже в поле описания.

---

## 📌 Параметры формы

- **Tag**: `v5.1.0` *(Target: `main`)*
- **Title**: `ReadmeKit v5.1.0 — Multi-Style Design System & Live Studio`
- **Pre-release**: **НЕ СТАВИТЬ** *(иначе GitHub заблокирует публикацию в Marketplace)*
- **Set as the latest release**: **ДА** (отмечено)
- **Primary Category**: `Utilities`
- **Additional Category**: `Continuous integration`

---

## 📝 Текст описания для вставки в Release Notes:

```markdown
# ReadmeKit v5.1.0

Deterministic SVG instrumentation engine and automated sync action for GitHub repositories and developer profiles.

## Architecture & Subsystems

- Multi-Style Geometry:
  - Pixel (Retro-Tech): 3D pixel typography, 360-degree radar sweeps, CRT scanlines, 45-degree chamfers, dither patterns.
  - Modern (Clean Vector): 1px borders, smooth pill badges, cubic Bezier curves.
  - Sketch (Hand-Drawn): rough jitter strokes, double contours, graph paper background.
- Zero-Flicker Theming: native `@media (prefers-color-scheme: dark)` adapts SVG assets directly in browser without duplicate files or proxy flicker.
- HUD Studio v6.5: component catalog with live SVG cards, block inspector, and independent GitHub background preview mode.
- Runtime Engine: pure Python standard library (`xml.etree`, `urllib`). Zero external dependencies. 176 unit tests passing.

## GitHub Action Usage

Automated cron sync for repository stars, metrics, and profile dossiers:

```yaml
name: Update Readme
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - name: Compile ReadmeKit
        uses: Kazinagg/readme-kit@v5
        with:
          fetch-github: 'true'
          bust-cache: 'true'

      - name: Push Updated Assets
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: auto-update readme stats and starchart [skip ci]"
```

## CLI

```bash
# Live Studio
pipx run readme-kit studio --open

# Compile template
readme-kit compile --input README.template.md --output README.md --fetch-github --bust-cache
```

## Links

- Web Simulator: https://kazinagg.github.io/readme-kit/
- Repository: https://github.com/Kazinagg/readme-kit
```
