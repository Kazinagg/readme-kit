---
name: pixel-readme
description: "Use this skill whenever the user asks to create, format, style, or upgrade a GitHub README, profile README, or repository documentation with ReadmeKit (formerly Pixel Readme Kit). Covers 4 Architectural Styles (Modern Clean Vector, Pixel Retro-Tech, Hand-Drawn Sketch, Corporate Minimalist), 13+ Themes, SVG generator CLI, markdown compiler with directives (<!-- readme-kit:... -->), multi-mode theming (auto, dark, light, transparent, gh, picture), 100% full-width table wrappers, quote headers, Camo-proxy compatibility, infographical components (metrics, progress, techstack, timeline, starchart, profile card, social cards), live preview studio, and native stdio MCP server. Canonical specification is in DESIGN_SYSTEM.md."
---

# ReadmeKit — Universal Multi-Style Design System, Customization Engine & MCP Server

Этот навык используется AI-агентом для проектирования, стилизации и автоматической сборки GitHub README и профилей в рамках универсальной системы кастомизации **ReadmeKit** (ранее Pixel Readme Kit).

> [!IMPORTANT]
> **Единый источник правды по геометрии и палитрам**: [DESIGN_SYSTEM.md](file:///d:/ForWorkStudy/Projects/Readmekit/DESIGN_SYSTEM.md). Всегда сверяйтесь со спецификацией стилей и тем при подборе компонентов.

---

## 🏛️ Фундаментальные принципы архитектуры

1. **Двухуровневая ортогональность Геометрии и Цвета**:
   - **Стиль (`style`)**: `pixel` (Retro-Tech / 8-Bit), `modern` (Clean Vector / SaaS), `sketch` (Hand-Drawn / Excalidraw).
   - **Цветовая палитра (`theme`)**: независима от формы и свободно комбинируется со стилями (`cyberpunk`, `tactical`, `tokyo`, `slate-dark`, `nordic-frost`, `linear-violet`, `emerald-clean`, `excali-dark`, `whiteboard` и др.).
2. **Адаптивная мульти-режимность (Multi-Mode Theming)**:
   - `mode="auto"` (**по умолчанию**): единый автономный SVG с нативными CSS-переменными и медиа-запросом `@media (prefers-color-scheme: dark)`. Переключается мгновенно вместе с системной темой ОС или браузера, без дублирования файлов.
   - `mode="dark"`: всегда тёмная контрастная тема.
   - `mode="light"`: всегда светлая высококонтрастная тема.
   - `mode="transparent"`: тёмные элементы на полностью прозрачном фоне (без подложки).
   - `mode="gh"`: официальный синтаксис GitHub с генерацией пары файлов (`-dark.svg` и `-light.svg`) и атрибутами `#gh-dark-mode-only` / `#gh-light-mode-only`.
   - `mode="picture"`: тег HTML5 `<picture>` с источниками `(prefers-color-scheme: dark)` и `(prefers-color-scheme: light)`.
3. **Anti-Collision Engine (Защита от наложения текста)**:
   - Интеллектуальный расчет раскладки шрифта: длинные заголовки плавно уменьшают размер пикселя (`px=6 ➔ 5 ➔ 4 ➔ 3`) или кегль Sans (`34px ➔ 26px ➔ 20px`) и аккуратно переносятся на 2 строки по границам слов.
   - Плашка подзаголовка рассчитывается динамически по ширине текста.
   - Тег статуса привязан к правому краю (`text-anchor="end"`), исключая столкновение с кнопками управления окна.
4. **Mobile Readability (Безопасные шрифты >= 11px)**:
   - Все текстовые элементы (включая бейджи, подзаголовки, спецификации и футеры) используют размер шрифта $\ge 11$px, предотвращая микроскопический нечитаемый текст на мобильных экранах смартфонов.
5. **100% Живой Markdown-текст**:
   - Текст внутри окон, цитат и терминалов остаётся копируемым Markdown, формулы — KaTeX/LaTeX, ссылки кликабельны.

---

## 📐 3 Глобальных стиля дизайн-системы

| Характеристика | 👾 Стиль 1: Pixel (`pixel`) | 💎 Стиль 2: Modern (`modern`) | ✏️ Стиль 3: Sketch (`sketch`) |
| :--- | :--- | :--- | :--- |
| **Геометрия формы** | Скосы 45° (`chamfer`), 90° ступени, зацепы `┌ ┐ └ ┘` | Мягкие скругления `rx="8..16"`, pill-бейджи `rx="999"` | Неровные живые штрихи (Jitter), двойные линии, овершуты |
| **Физика линий** | Контрастные рамки 1.5–2px, дизеринг-шины | Ультратонкие 1px границы с `top highlight` градиентом | Двойной карандашный штрих, легкое расхождение концов |
| **Заливка областей** | Дизеринг-сетки (Dither 4x4 / 2x2) | Мягкие градиенты (`rgba`, Area Fill) | Карандашная штриховка (`hatch /////` или `XXXX`) |
| **Типографика** | Псевдо-3D растровый (`render_3d_text`) + Mono | Пропорциональный Sans-Serif (`Inter`) + Mono | Рукописный архитектурный (`Virgil`, `Chalkboard`) |
| **Графика данных** | Полигональные ломаные + прицелы | Smooth Cubic Bezier Spline + Area Fill | Hand-Drawn Star-History + штриховка + дудл-звезды |
| **Спецэффекты** | Радар 360°, CRT-сканлайн, эквалайзер | macOS traffic lights, pulse live status | Хайлайтер, стикеры (Post-it), скотч (Washi tape) |
| **Канонические темы** | `cyberpunk`, `tactical`, `tokyo`, `amber`, `matrix` | `slate-dark`, `nordic-frost`, `linear-violet`, `emerald-clean` | `excali-dark`, `whiteboard`, `notebook-graph`, `blueprint-sketch` |

---

## 📏 Safe Text Budgets (Безопасные лимиты текста для AI-моделей)

Чтобы сгенерированные блоки выглядели идеально и не ломали композицию:

| Элемент | Рекомендуемый бюджет | Поведение Anti-Collision Engine |
| :--- | :--- | :--- |
| **Header Title** | **8–16 символов** (1 строка)<br/>**17–32 символов** (2 строки) | При длине до 14 симв. — `px_size=6`. При 15–20 симв. — даунскейлинг до `px=5/4`. При > 20 симв. — перенос на 2 строки по пробелам с автоматическим смещением подзаголовка вниз. При экстремальной длине (> 36 симв.) — обрезка с `...`. |
| **Header Subtitle** | **20–45 символов** | Ширина рамки подзаголовка рассчитывается строго по ширине текста (`sub_w`). |
| **Header Tag** | **6–16 символов** | Заякорен справа с отступом `x=755` (`text-anchor="end"`), защищен от наложения на кнопки окна `[ _ ] [ □ ] [ × ]`. |
| **Specs (L3)** | **до 3 строк по 20–35 симв.** | Формат: `spec1="LABEL: VALUE"`. Размещается строго под подзаголовком. |
| **Window Title** | **15–30 символов** | Префикс `╔═ ` добавляется автоматически. |
| **Callout Subtitle** | **25–60 символов** | Безопасно размещается правее бейджа типа (`NOTE`, `WARNING` и т.д.). При длине > 100 симв. переносится на 2 строки с ростом высоты. |
| **Chip Text** | **6–20 символов** | Ширина чипа рассчитывается автоматически с учётом пиксельных эмодзи и отступов. |
| **Metric Value / Label**| **Значение: 3–8 симв.**, **Лейбл: 6–18 симв.** | 2–4 карточки в ряду с автоматическим расчётом ширины `col_w`. |
| **Progress Label** | **15–35 символов** | Процент и статус размещаются по правому краю, сегменты адаптируются под значение 0–100%. |
| **Timeline Item** | **Заголовок: 8–20 симв.**, **Описание: 20–45 симв.** | 2–6 этапов, соединяемых горизонтальной PCB-шиной со статусами (`COMPLETED`, `ACTIVE`, `PLANNED`). |
| **Social Title / Sub** | **Заголовок: 10–24 симв.**, **Подзаголовок: 25–55 симв.** | Формат 1280x640 OpenGraph Preview для репозитория. |

---

## 🛠️ Способ 1: Компилятор Markdown (Рекомендуемый воркфлоу)

Агент создает шаблонный файл `README.template.md` с декларативными директивами `<!-- pixel-kit:... -->` и запускает компилятор:

```bash
python -m generator.cli compile --input README.template.md --output README.md --assets-dir assets/generated
```

### Дополнительные флаги компилятора v4.0:
- `--clean-assets`: автоматическое удаление неиспользуемых SVG-файлов (Garbage Collector).
- `--dry-run-clean`: просмотр файлов-сирот без удаления.
- `--no-cache`: отключение инкрементального SHA-256 кэша.
- `--bust-cache`: добавление `?v=<hash>` к путям изображений для пробития кэша GitHub Camo Proxy.

### Синтаксис директив в Markdown:

Все директивы поддерживают атрибут `mode="auto|dark|light|transparent|gh|picture"` (по умолчанию `auto`) и `preset="cyberpunk|amber|matrix|tokyo|..."`.

#### 1. Заглавная шапка (Header)
```markdown
<!-- Стандартная шапка -->
<!-- pixel-kit:header style="cyberpunk" title="PROJECT NAME" subtitle="SYSTEM SPECIFICATION" tag="RELEASE_v4.0" spec1="HUD ARCHITECTURE: TRANSLUCENT GLASS" spec2="THEMING: ADAPTIVE DUAL-THEME SVG" spec3="ANIMATION SUITE: RADAR // SCANLINE" mode="auto" out="assets/header.svg" -->

<!-- Компактная шапка (высота 84px вместо 180px) -->
<!-- pixel-kit:header style="tactical" title="SUBMODULE" subtitle="MICRO-SERVICE KERNEL" tag="v1.0" compact="true" mode="auto" out="assets/header-compact.svg" -->
```

#### 2. Карточки метрик и KPI (Metrics)
```markdown
<!-- pixel-kit:metrics style="cyberpunk" primary="#00C8D7" accent="#A855F7" out="assets/metrics.svg" -->
- label="THROUGHPUT" value="48.2 GB/s" delta="+18.4% PEAK" trend="up"
- label="LATENCY" value="0.14 ms" delta="p99 < 0.2ms" trend="up"
- label="CLUSTER NODES" value="1,024" delta="+64" trend="up"
- label="SYSTEM STATUS" value="99.98%" status="NOMINAL"
<!-- /pixel-kit:metrics -->
```

#### 3. Индикатор прогресса и статуса (Progress)
```markdown
<!-- pixel-kit:progress style="cyberpunk" value="85" label="SPRINT 04 COMPLETION" sub="4/5 MILESTONES VERIFIED" primary="#00C8D7" accent="#A855F7" out="assets/progress.svg" -->
```

#### 4. Матрица стека технологий (Tech Stack)
```markdown
<!-- pixel-kit:techstack style="tactical" items="python,rust,cpp,docker,git,linux,k8s,react" columns="4" out="assets/techstack.svg" -->
```

#### 5. Таймлайн / Дорожная карта (Timeline)
```markdown
<!-- pixel-kit:timeline style="cyberpunk" primary="#00C8D7" accent="#A855F7" out="assets/timeline.svg" -->
- stage="01" title="CORE ENGINE" date="2026-Q1" status="COMPLETED" desc="Vector pixel rendering pipeline"
- stage="02" title="METRICS WIDGETS" date="2026-Q2" status="COMPLETED" desc="Realtime HUD KPI & progress widgets"
- stage="03" title="STUDIO & MCP" date="2026-Q3" status="ACTIVE" desc="Zero-dep web studio & AI model protocol"
- stage="04" title="GLOBAL CDN" date="2026-Q4" status="PLANNED" desc="Dynamic edge badge synthesis"
<!-- /pixel-kit:timeline -->
```

#### 6. Социальная карточка (OpenGraph 1280x640)
```markdown
<!-- pixel-kit:social style="cyberpunk" title="PIXEL-KIT" subtitle="RETRO HUD READMES" repo="Kazinagg/pixel-readme-kit" tags="PYTHON,SVG,HUD,MARKDOWN" out="assets/social.svg" -->
```

#### 7. Окно с контентом (Window Container)
```markdown
<!-- pixel-kit:window style="tactical" title="TACTICAL CONSOLE" tag="HUD" mode="auto" out_top="assets/top.svg" out_bottom="assets/bottom.svg" -->
#### Живой Markdown контент внутри окна
- Окно накрывает таблицу на 100% ширины.
- Для Minimal Glass компилятор автоматически генерирует 3-строчную единую монолитную таблицу.
<!-- /pixel-kit:window -->
```

#### 8. Интерактивный терминал (Collapsible Details/Summary)
```markdown
<!-- pixel-kit:terminal style="cyberpunk" title="HUD.TERMINAL" state="open" mode="auto" -->
```bash
git clone https://github.com/Kazinagg/pixel-readme-kit.git
```
<!-- /pixel-kit:terminal -->
```

#### 9. Плашка для цитаты (Quote Header Container)
```markdown
<!-- pixel-kit:quote style="cyberpunk" badge="NOTE" title="SPECIFICATION NOTICE" subtitle="Flows into live text" mode="auto" -->
**Живой текст цитаты**: плашка бесшовно открыта слева к серой полосе цитаты `border-left`, а пунктирная нижняя линия направляет внимание в текст.
<!-- /pixel-kit:quote -->
```

#### 10. Закрывающая пластина (Footer)
```markdown
<!-- pixel-kit:footer style="cyberpunk" status="SYSTEM_ONLINE // STANDBY" nav="RETURN TO TOP" mode="auto" -->
```

#### 11. Автономная закрытая плашка (Callout)
```markdown
<!-- pixel-kit:callout style="tactical" type="warning" title="WARNING" subtitle="Important operational parameter" mode="auto" -->
```

#### 12. Разделители и сплиттеры
```markdown
<!-- pixel-kit:divider style="minimal" mode="auto" -->
<!-- pixel-kit:splitter style="tactical" label="[MODULE: AUTH]" mode="auto" -->
```

#### 13. Голографические чипы и живые счетчики GitHub
```markdown
<!-- pixel-kit:chip style="cyberpunk" type="closed" text="CORE_SYS" href="https://github.com" mode="auto" -->
<!-- pixel-kit:chip style="tactical" type="decay" text="DEF_ALERT" mode="auto" -->
<!-- pixel-kit:chip style="minimal" type="pulse" text="SYNC_IDLE" mode="auto" -->

<!-- Живые счетчики GitHub с авто-ссылками: -->
<!-- pixel-kit:chip github="stars" repo="Kazinagg/pixel-readme-kit" style="cyberpunk" -->
<!-- pixel-kit:chip github="forks" repo="Kazinagg/pixel-readme-kit" style="tactical" -->
<!-- pixel-kit:chip github="license" repo="Kazinagg/pixel-readme-kit" style="minimal" -->
```

---

## 🖥️ Способ 2: Интерактивный Live Preview и HUD Studio

Встроенный веб-сервер и графическая студия без единой сторонней зависимости:

```bash
# Запуск веб-студии с визуальным конструктором блоков:
python -m generator.cli studio --open --port 8080

# Запуск Live Preview сервера для отслеживания изменений в файле шаблона:
python -m generator.cli serve --template README.template.md --open
```

- **SSE Live-Reload**: автообновление страницы браузера за 300 мс при сохранении файла шаблона.
- **Realtime Render API**: генерация любого SVG прямо в браузере (< 50 мс) по адресу `/api/render`.
- **HUD Debug Mode**: оверлей сетки 20px и проверка бюджета символов прямо в интерфейсе.

---

## 🤖 Способ 3: Нативный stdio MCP Сервер для AI-агентов

Для интеграции с Claude Desktop, Antigravity, Roo-Code или Cursor:

```bash
python -m generator.mcp_server
```

### Доступные инструменты (Tools):
1. `pixel_compile_template`: компиляция файла шаблона с авто-сохранением SVG и кэшем.
2. `pixel_generate_header`: генерация заглавной или компактной шапки.
3. `pixel_generate_metrics`: карточки KPI/метрик.
4. `pixel_generate_progress`: индикаторы выполнения.
5. `pixel_generate_techstack`: сетка стека технологий с пиксельными иконками.
6. `pixel_generate_timeline`: дорожная карта / таймлайн.
7. `pixel_generate_social`: баннер 1280x640 OpenGraph Social Preview.
8. `pixel_generate_callout`: плашки алертов.
9. `pixel_generate_frame`: верхние и нижние рамки окон.
10. `pixel_generate_chip`: пиксельные чипы и GitHub-счётчики.
11. `pixel_generate_divider`: лазерные и спектральные разделители.
12. `pixel_generate_splitter`: тактические сплиттеры подмодулей.

---

## ⚡ Способ 4: Генерация одиночных SVG через CLI

```bash
# Флагманский адаптивный хедер (авто-тема):
python -m generator.cli header --style tactical --title "TACTICAL COMMAND" --subtitle "SECURITY LAYER" --mode auto -o assets/header.svg

# Компактный хедер:
python -m generator.cli header --style cyberpunk --title "COMPACT HUD" --compact -o assets/header-compact.svg

# Баннер для соцсетей (1280x640):
python -m generator.cli social --style cyberpunk --title "MY PROJECT" --subtitle "CORE FRAMEWORK" -o assets/social.svg

# Закрывающий футер:
python -m generator.cli footer --style minimal --status "SESSION_ACTIVE" -o assets/footer.svg

# Плашка алерта или цитаты (--quote):
python -m generator.cli callout --style cyberpunk --type note --title "SYS NOTICE" --quote -o assets/quote-note.svg

# Рамка окна (top или bottom):
python -m generator.cli frame --style minimal --type top --title "╔═ MINIMAL.SYS" -o assets/frame-top.svg

# Чип (closed, decay, pulse):
python -m generator.cli chip --style tactical --type decay --text "SECTOR_01" -o assets/chip-tactical.svg

# Разделитель глав:
python -m generator.cli divider --style minimal -o assets/divider-spectrum.svg

# Сплиттер подмодулей:
python -m generator.cli splitter --style cyberpunk --label "[MODULE: AUTH]" -o assets/splitter.svg
```

---

## 🏗️ Способ 5: Скаффолдер новых проектов (`init`)

Быстрое развертывание Pixel Readme в любом репозитории:

```bash
# Создать шаблон с профилем cyberpunk:
python -m generator.cli init ./my-project --profile cyberpunk

# Создать тактический профиль:
python -m generator.cli init . --profile tactical
```

---

## ⚠️ Критические правила вёрстки

1. **Запрет `<img>` внутри `<summary>`**:
   - На GitHub веб-клиент вешает обработчик Lightbox на все изображения `<img>`. Если в `<summary>` поместить картинку, клик по ней **открывает SVG в браузере, а не раскрывает блок**.
   - **Правило**: Внутри `<summary>` всегда использовать текстовые теги: `<summary><kbd>▶ TITLE</kbd> <b>[...]</b> <code>[...]</code></summary>`.
2. **Таблицы на 100% ширины**:
   - GitHub сжимает таблицы по содержимому текста (`width: max-content`).
   - **Правило**: Всегда указывать `<table width="100%"><tr><td width="2000">`. Значение `width="2000"` на ячейке `<td>` сообщает браузеру предпочтительную ширину, благодаря чему таблица гарантированно растягивается на все 100% доступной ширины контейнера (`max-width: 100%`), а зубцы крышек садятся ровно на серые рамки.
3. **XML-экранирование**:
   - Неэкранированные символы `&`, `<`, `>` внутри SVG ломают GitHub Camo Proxy.
   - Всегда валидировать SVG через `xml.etree.ElementTree.fromstring()`.
4. **Адаптивный вертикальный поток (DOM-like Flow Layout)**:
   - Высота шапок (`generate_header`) автоматически рассчитывается динамически: при 2-строчных заголовках или наличии спецификаций все нижние блоки плавно съезжают вниз (как `div` в браузере), а сам SVG динамически увеличивает высоту (`viewBox` и шасси), гарантируя запас отступа (clearance $\ge 18-26$px) до нижних линий и скосов.
5. **Адаптивные Callouts по высоте**:
   - При длине подзаголовка более 100 символов текст автоматически переносится на 2 строки, а высота SVG адаптируется с 48px до 62px (или с 42px до 56px для цитат), предотвращая наложение и выход текста за нижние границы шасси. Одиночный заголовок без подзаголовка автоматически центрируется по вертикали.
6. **Mobile Font Size $\ge 11$px**:
   - Никаких микрошрифтов 7-9px. Все бейджи, метки, даты и подзаголовки рендерятся шрифтом не менее 11px для читаемости на экранах мобильных телефонов.
