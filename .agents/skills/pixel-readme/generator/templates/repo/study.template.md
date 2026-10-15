# <div id="top"></div>

<!-- pixel-kit:header style="cyberpunk" title="{PROJECT_TITLE}" subtitle="ЛАБОРАТОРНАЯ РАБОТА // ОТЧЕТ ПО ПРАКТИКУМУ" spec1="ДИСЦИПЛИНА: {DISCIPLINE}" spec2="СТУДЕНТ: {AUTHOR} // ГРУППА: {GROUP}" spec3="СТАТУС: ЗАЩИТА // СИСТЕМА ВЫЧИСЛЕНИЙ" tag="GRADE: A+" out="assets/generated/header-study.svg" -->

<br/><br/>

<div align="center">

<!-- pixel-kit:chip style="cyberpunk" type="closed" text="👨‍🎓 СТУДЕНТ: {AUTHOR}" out="assets/generated/chip-student.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="tactical" type="decay" text="🏫 ГРУППА: {GROUP}" out="assets/generated/chip-group.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="minimal" type="pulse" text="● СДАНО НА ПРОВЕРКУ" out="assets/generated/chip-status.svg" -->

<br/><br/>

<!-- pixel-kit:divider style="cyberpunk" out="assets/generated/divider-study.svg" -->

</div>

<br/>

## 🎯 1. Цель работы и теоретическая справка

<!-- pixel-kit:callout style="cyberpunk" type="note" title="ЦЕЛЬ ИССЛЕДОВАНИЯ" subtitle="Освоение алгоритмов, профилирование и визуализация вычислений" out="assets/generated/callout-goal.svg" -->

<!-- pixel-kit:window style="cyberpunk" title="ТЕОРЕТИЧЕСКИЙ БАЗИС И ПОСТАНОВКА ЗАДАЧИ" out_top="assets/generated/frame-theory-top.svg" out_bottom="assets/generated/frame-theory-bot.svg" -->

### Формулировка задачи

В ходе лабораторной работы требуется разработать высокопроизводительный модуль и исследовать сходимость алгоритма.

Математическая модель:
$$f(x) = \sum_{i=1}^{n} \frac{\alpha_i \cdot x^i}{\sqrt{1 + \beta_i^2}}$$

- **Входные данные**: Матрица коэффициентов $A \in \mathbb{R}^{n \times m}$
- **Выходные данные**: Вектор экстремумов и оценка времени сходимости

<!-- /pixel-kit:window -->

<br/>

## 💻 2. Реализация и код программы

<!-- pixel-kit:terminal style="cyberpunk" title="ИНСТРУКЦИЯ ПО СБОРКЕ И ЗАПУСКУ" state="open" out_top="assets/generated/terminal-build-top.svg" out_bottom="assets/generated/terminal-build-bot.svg" -->

```bash
# Клонирование и переход в каталог:
git clone https://github.com/{REPO}.git
cd {PROJECT_SLUG}

# Сборка проекта через CMake / Makefile:
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .

# Запуск тестов:
./run_tests --verbose
```

<!-- /pixel-kit:terminal -->

<br/>

## 📊 3. Результаты экспериментов

<!-- pixel-kit:window style="cyberpunk" title="РЕЗУЛЬТАТЫ И ВЫВОДЫ" out_top="assets/generated/frame-results-top.svg" out_bottom="assets/generated/frame-results-bot.svg" -->

| Итерация | Метод A (мс) | Метод B (мс) | Ускорение | Погрешность $\epsilon$ |
| :---: | :---: | :---: | :---: | :---: |
| 10,000 | 142.4 | 18.2 | **7.8x** | $1.2 \times 10^{-6}$ |
| 50,000 | 780.1 | 89.6 | **8.7x** | $3.5 \times 10^{-6}$ |
| 100,000 | 1650.0 | 174.3 | **9.4x** | $7.1 \times 10^{-6}$ |

> **Вывод**: В ходе работы цель была полностью достигнута. Алгоритм B продемонстрировал многократное превосходство по времени вычислений при сохранении заданной точности.

<!-- /pixel-kit:window -->

<br/>

<!-- pixel-kit:footer style="cyberpunk" status="LAB_SESSION_COMPLETED // 0xDEADBEEF" nav="▲ НАВЕРХ К ДОСЬЕ" out="assets/generated/footer-study.svg" -->
