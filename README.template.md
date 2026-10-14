# README KIT — UNIVERSAL DESIGN SYSTEM FOR GITHUB REPOSITORIES & DEVELOPER PROFILES

<div id="top"></div>

<div align="center">

<!-- readme-kit:header style="pixel" theme="cyberpunk" primary="#00E5FF" accent="#FF0055" tertiary="#9D00FF" title="README KIT" subtitle="UNIVERSAL DESIGN SYSTEM FOR GITHUB REPOSITORIES & PROFILES" spec1="DUAL TARGET: REPOSITORIES // DEVELOPER PROFILES" spec2="MULTI-STYLE: RETRO-PIXEL // MODERN CLEAN // SKETCH" spec3="FULL SUITE: LIVE STUDIO // MARKDOWN COMPILER // AI MCP SERVER" tag="v5.1.0 STABLE" out="assets/generated/header-readme.svg" -->

<br/><br/>

<!-- readme-kit:chip style="pixel" theme="cyberpunk" type="pulse" text="🌐 ИНТЕРАКТИВНЫЙ САЙТ / ДЕМО" href="https://kazinagg.github.io/readme-kit/" out="assets/generated/chip-readme-demo.svg" -->
&nbsp;&nbsp;
<!-- readme-kit:chip style="pixel" theme="cyberpunk" type="closed" text="[DOCS] КАТАЛОГ СТИЛЕЙ И БЛОКОВ" href="CATALOG.md" out="assets/generated/chip-readme-catalog.svg" -->
&nbsp;&nbsp;
<!-- readme-kit:chip style="pixel" theme="cyberpunk" type="closed" text="[SPEC] СИСТЕМА КАСТОМИЗАЦИИ" href="EXAMPLES.md" out="assets/generated/chip-readme-examples.svg" -->
&nbsp;&nbsp;
<!-- readme-kit:chip style="pixel" theme="cyberpunk" type="pulse" text="● v5.1.0 STABLE" href="#top" out="assets/generated/chip-readme-version.svg" -->
&nbsp;&nbsp;
<!-- readme-kit:chip style="pixel" theme="cyberpunk" type="closed" github="stars" repo="Kazinagg/readme-kit" out="assets/generated/chip-readme-stars.svg" -->
&nbsp;&nbsp;
<!-- readme-kit:chip style="pixel" theme="cyberpunk" type="closed" github="forks" repo="Kazinagg/readme-kit" out="assets/generated/chip-readme-forks.svg" -->
&nbsp;&nbsp;
<!-- readme-kit:chip style="pixel" theme="cyberpunk" type="pulse" github="license" repo="Kazinagg/readme-kit" out="assets/generated/chip-readme-license.svg" -->

<br/><br/>

<!-- readme-kit:divider style="pixel" theme="cyberpunk" primary="#00E5FF" out="assets/generated/divider-readme.svg" -->

</div>

<br/>

## 01 // Телеметрия системы (System Telemetry)

<!-- readme-kit:metrics style="pixel" theme="cyberpunk" out="assets/generated/metrics-readme.svg" -->
- label="CUSTOMIZATION" value="3 STYLES" delta="Pixel, Modern, Sketch" trend="up"
- label="THEME PALETTES" value="13+ THEMES" delta="Adaptive Dark/Light" trend="up"
- label="TEST SUITE" value="176 PASS" status="100% GREEN"
- label="RUNTIME DEPS" value="0 EXT" status="STD-LIB ONLY"
<!-- /readme-kit:metrics -->

<br/>

<!-- readme-kit:progress style="pixel" theme="cyberpunk" value="100" label="UNIVERSAL CUSTOMIZATION SYSTEM & DESIGN ENGINE COMPLETE" sub="MULTI-STYLE ARCHITECTURE // STAR CHART // DOSSIER // STUDIO // MCP" out="assets/generated/progress-readme.svg" -->

<br/>

## 02 // Концепция проекта (Project Overview)

**ReadmeKit** — универсальная модульная **система кастомизации**, генератор динамических SVG-ассетов и интерактивная дизайн-студия для оформления **Репозиториев (Repositories Showcase)** и **Профилей разработчиков (Developer Profiles `username/username`)** на GitHub.

Проект вырос из моно-темы в **полноценный дизайн-движок кастомизации**:
- **Ортогональная архитектура**: визуальная форма (геометрия стиля) полностью отделена от цветовой палитры (темы и пресеты). Вы вольны комбинировать любой стиль с любой палитрой.
- **Zero-Flicker адаптивный SVG (`mode="auto"`)**: единый автономный SVG-файл использует нативные CSS-переменные и медиа-запрос `@media (prefers-color-scheme: dark)`. Переключается мгновенно вместе с системной темой браузера без дублирования файлов и мерцания.
- **Два ключевых сценария кастомизации**:
  1. **Оформление репозиториев (Repositories Showcase & Documentation)**:
     - Оформление библиотек, CLI-утилит, веб-сервисов, монорепозиториев и аналитических отчетов.
     - Модульные окна контента с копируемым Markdown внутри, сворачиваемые интерактивные терминалы, матрицы стека технологий, плашки алертов, KPI-метрики и футеры.
  2. **Оформление профилей разработчиков (Developer Profiles & Portfolios)**:
     - Флагманские досье-карточки профиля (`readme-kit:profile`) с аватаром, LED-индикатором статуса, специализацией, локацией и био.
     - График динамики звёзд и активности (`readme-kit:starchart`) с гладкими кривыми Безье, координатной сеткой и градиентной заливкой.
     - Витрины ключевых проектов, OpenGraph превью-карточки (1280x640) и социальные чипы.

<br/>

## 03 // Флагманские компоненты v5.1 (Showcase)

### 1. Modern Vector Style — Карточка профиля разработчика
> 🔵 **Стиль Modern (`style="modern" theme="slate-dark"`):** Четкие 1px векторные контуры, сглаженные скругления, бейджи специализации и кривые Безье.

<!-- readme-kit:profile style="modern" theme="slate-dark" name="ALEX DEVELOPER" role="FULLSTACK & SYSTEMS ARCHITECT" bio="Building high-performance runtimes and resilient developer tooling." status="AVAILABLE FOR HIRE" location="REMOTE // UTC+3" badge="LEVEL_99" out="assets/generated/profile-readme-demo.svg" -->

<br/>

### 2. Hand-Drawn Sketch Style — График динамики звёзд
> ✏️ **Стиль Sketch (`style="sketch" theme="excali-dark"`):** Живой рукописный штрих (Rough Jitter), двойные контуры, карандашная штриховка и шрифт заметок.

<!-- readme-kit:starchart style="sketch" theme="excali-dark" repo="Kazinagg/readme-kit" points="15,65,190,480,950,1650" current="1,650" delta="+78% past 6m" title="OPEN SOURCE STARS TRAJECTORY" out="assets/generated/starchart-readme-demo.svg" -->

<br/>

### 3. Retro-Tech Pixel Style — Архитектурный инлайн-алерт
> 👾 **Стиль Pixel (`style="pixel" theme="cyberpunk"`):** Фирменный неоновый HUD, пиксельные рамки, CRT-сканлайны и скобы 45°.

<!-- readme-kit:callout style="pixel" theme="cyberpunk" type="note" title="АРХИТЕКТУРНЫЙ ПРИНЦИП" subtitle="Ортогональное разделение формы (3 стиля) и цвета (13+ тем)" out="assets/generated/callout-readme-arch.svg" -->

---

## 04 // Мульти-стилевая архитектура (3 Дизайн-парадигмы)

Дизайн-система предлагает 3 глобальные визуальные парадигмы с ортогональным разделением **Геометрии (`style`)** и **Цветовых палитр (`theme`)**:

| Парадигма (Стиль `style`) | Канонические темы (`theme`) | Основная палитра | Особенности геометрии | Статус готовности |
| :--- | :--- | :--- | :--- | :--- |
| **Pixel / Retro-Tech** (`pixel`) | `cyberpunk`, `tactical`, `tokyo`, `matrix`, `amber` | Cyan / Magenta, Phosphor Amber, Tokyo Neon, Matrix Green | 3D пиксельный шрифт, радары 360°, CRT-сканлайн, скобы 45°, дизеринг | ● **READY (CORE)** |
| **Clean / Modern Vector** (`modern`) | `slate-dark`, `nordic-frost`, `linear-violet`, `emerald-clean` | Matte Graphite, Nordic Frost, Linear Violet, Emerald Clean | Четкие векторные контуры 1px, сглаженные скругления, pill-бейджи, кривые Безье | ● **READY (CORE)** |
| **Hand-Drawn / Sketch** (`sketch`) | `excali-dark`, `whiteboard`, `notebook-graph`, `blueprint-sketch` | Excali Dark, Clean Whiteboard, Graph Paper, Blueprint Blue | Живой штрих руки (Jitter), двойные контуры, карандашная штриховка, шрифт заметок | ● **READY (CORE)** |

> [!NOTE]
> **Канонические темы по стилям**:
> 1. **Pixel Style**: `cyberpunk` (неон), `tactical` (янтарь), `tokyo` (ночной Токио), `matrix` (зеленый монохром), `amber` (янтарь CRT).
> 2. **Modern Vector Style**: `slate-dark` (графит + циан), `nordic-frost` (арктический лед), `linear-violet` (Linear App космос), `emerald-clean` (Supabase/Vercel изумруд).
> 3. **Sketch Style**: `excali-dark` (тёмный Excalidraw), `whiteboard` (белая доска), `notebook-graph` (тетрадь в клетку), `blueprint-sketch` (чертёж).

<br/>

## 05 // Стек технологий и поддерживаемое окружение

<!-- readme-kit:techstack style="pixel" theme="cyberpunk" items="python,docker,git,linux,github" columns="5" out="assets/generated/techstack-readme.svg" -->

<br/>

## 06 // Дорожная карта развития (Roadmap)

<!-- readme-kit:timeline style="pixel" theme="cyberpunk" out="assets/generated/timeline-readme.svg" -->
- title="v1.0 - SVG HUD BANNER FOUNDATION" sub="Флагманские адаптивные шапки, 3D пиксельные шрифты, радары 360°" status="COMPLETED"
- title="v2.0 - MODULAR WINDOW CHASSIS" sub="Оконные рамки, чипы со статистикой GitHub, инлайн-алерты, разделители" status="COMPLETED"
- title="v3.0 - MULTI-THEMING & ANTI-COLLISION" sub="Автоматическая смена dark/light тем через CSS, безопасные зоны" status="COMPLETED"
- title="v4.0 - DATA VIZ, LIVE STUDIO & MCP" sub="Метрики, прогресс, стек, таймлайн, веб-студия, MCP сервер, кэш" status="COMPLETED"
- title="v5.0 - REPOSITORIES & DEVELOPER PROFILES" sub="Мульти-стили, график звезд, карточки профилей, шаблоны repo/ и profile/" status="COMPLETED"
- title="v6.5 - STUDIO OVERHAUL & MULTI-STYLE ARCH" sub="3 стиля (Pixel, Modern, Sketch), каталог компонентов, полная изоляция тем" status="COMPLETED"
<!-- /readme-kit:timeline -->

<br/>

## 07 // Руководство по началу работы (Quick Start Guide)

### 0. Онлайн-витрина и симулятор (GitHub Pages)
Опробуйте все стили, темы и генерацию SVG прямо в браузере: **[https://kazinagg.github.io/readme-kit/](https://kazinagg.github.io/readme-kit/)**

### 1. Мгновенный запуск Студии локально (Zero-Install)
```bash
# Запуск через pipx без предварительного клонирования (рекомендуется):
pipx run readme-kit studio --open

# Или классическая установка пакета через pip:
pip install readme-kit
readme-kit studio --open

# (Также сохранена обратная совместимость вызова через pixel-kit studio --open)
```

### 2. Инициализация шаблона с помощью Scaffolder
```bash
# Оформление репозитория (Modern Vector, Hand-Drawn Sketch или Retro-Pixel):
readme-kit init --category repo --type modern --title "MY-MODERN-LIB"
readme-kit init --category repo --type sketch --title "MY-SKETCH-PROJECT"
readme-kit init --category repo --type library --title "MY-AWESOME-LIB"

# Оформление профиля разработчика (Clean Vector, Dossier или Sketch):
readme-kit init --category profile --type modern --title "ALEX DEVELOPER"
readme-kit init --category profile --type sketch --title "ALEX DEVELOPER"
readme-kit init --category profile --type developer --title "ALEX DEVELOPER"
```

### 3. Компиляция и синхронизация (с автоподхватом данных GitHub)
```bash
# Полная сборка с актуализацией звезд, очисткой сирот и сбросом кэша Camo:
readme-kit sync

# Или ручная компиляция шаблона Markdown:
readme-kit compile --fetch-github --clean-assets --bust-cache
```

### 4. Автоматическое обновление по расписанию в GitHub Actions
Чтобы график звезд, бейджи и метрики всегда оставались актуальными, добавьте workflow `.github/workflows/update-readme.yml`:
```yaml
name: Sync Readme
on:
  schedule:
    - cron: '0 0 * * *' # Ежедневное обновление в полночь
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: Kazinagg/readme-kit@v5
        with:
          fetch-github: 'true'
          bust-cache: 'true'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: auto-update readme stats and starchart [skip ci]"
```

### 5. Подключение через MCP (Claude Desktop, Cursor, Antigravity)
Добавьте сервер в ваш `mcp_config.json`:
```json
{
  "mcpServers": {
    "readme-kit": {
      "command": "python",
      "args": ["-m", "generator.mcp_server"],
      "cwd": "/path/to/readme-kit"
    }
  }
}
```

---

## 08 // Интерактивный пример окна контента

<!-- readme-kit:window style="pixel" theme="cyberpunk" title="╔═ RUNTIME.SYS // MODULE_INTERFACE" tag="[ONLINE]" out_top="assets/generated/frame-readme-top.svg" out_bottom="assets/generated/frame-readme-bottom.svg" -->
### [SPEC] Спецификация подсистем ядра ReadmeKit

Контент внутри окон остаётся полноценным копируемым Markdown:

| Подсистема | Протокол | Статус | Задержка |
| :--- | :--- | :--- | :--- |
| **Multi-Style Engine** | `PIXEL + MODERN + SKETCH` | `● TRI-PARADIGM` | `0.00 ms` |
| **Theme Engine** | `CSS_VARS_MEDIA_QUERY` | `● AUTO_ADAPTIVE` | `0.00 ms` |
| **Incremental Cache** | `SHA-256 DIGEST` | `● 98% HIT_RATE` | `0.02 s` |
| **Live Studio v6.5** | `SSE REALTIME SYNC` | `● 300ms INTERVAL` | `< 50 ms` |

```bash
# Клонирование и запуск студии кастомизации
git clone https://github.com/Kazinagg/readme-kit.git
cd readme-kit
python -m generator.cli studio
```
<!-- /readme-kit:window -->

<br/>

<!-- readme-kit:quote style="pixel" theme="cyberpunk" title="РУКОВОДСТВО ПО СТИЛЮ" subtitle="Где найти полные справочники и примеры" badge="NOTE" out="assets/generated/callout-quote-readme.svg" -->
> **Навигация по документации**:
> - 🌐 **Интерактивный веб-сайт и симулятор**: [kazinagg.github.io/readme-kit](https://kazinagg.github.io/readme-kit/)
> - Полный каталог всех компонентов во всех стилях доступен в **[CATALOG.md](CATALOG.md)**.
> - Детальный разбор «сырой шаблон $\rightarrow$ скомпилированный результат» приведён в **[EXAMPLES.md](EXAMPLES.md)**.
> - Лицензия проекта: [LICENSE](LICENSE) (MIT).
<!-- /readme-kit:quote -->

<br/>

<!-- readme-kit:terminal style="pixel" theme="cyberpunk" title="CLI_COMMANDS.LIST" state="closed" out_top="assets/generated/term-top-readme.svg" out_bottom="assets/generated/term-bottom-readme.svg" -->
```bash
# Список всех доступных команд генератора:
python -m generator.cli studio --help    # Запуск HUD Studio с Live Reload
python -m generator.cli serve --help     # Запуск HTTP сервера предпросмотра
python -m generator.cli compile --help   # Компилятор шаблонов Markdown
python -m generator.cli init --help      # Скаффолдер шаблонов (repo/* и profile/*)
python -m generator.cli header --help    # Заглавные шапки (включая --compact)
python -m generator.cli starchart --help # График динамики звезд и роста
python -m generator.cli profile --help   # Карточка профиля разработчика
python -m generator.cli social --help    # OpenGraph социальные карточки 1280x640
python -m generator.cli metrics --help   # KPI метрики
python -m generator.cli progress --help  # Индикаторы прогресса
python -m generator.cli techstack --help # Матрицы технологий
python -m generator.cli timeline --help  # PCB таймлайны
python -m generator.cli footer --help    # Закрывающие пластины
python -m generator.cli callout --help   # Инлайн-алерты и плашки
python -m generator.cli frame --help     # Рамки окон (top/bottom)
python -m generator.cli chip --help      # Чипы и пилюли
python -m generator.cli divider --help   # Разделители глав
python -m generator.cli splitter --help  # Сплиттеры подмодулей
```
<!-- /readme-kit:terminal -->

<br/><br/>

<!-- readme-kit:footer style="pixel" theme="cyberpunk" status="SESSION_ONLINE // READY" nav="▲ НАВЕРХ" out="assets/generated/footer-readme.svg" -->
