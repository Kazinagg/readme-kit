"""
3D Chunky Pixel Font Engine for Pixel Readme Kit
Supports Cyrillic, Latin, Digits and Symbols.
Renders razor-sharp pixel typography with 3D drop-shadows.
"""

GLYPHS = {
    # Latin
    'A': [".XXXX.", "XX..XX", "XX..XX", "XXXXXX", "XXXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'B': ["XXXXX.", "XX..XX", "XX..XX", "XXXXX.", "XXXXX.", "XX..XX", "XX..XX", "XX..XX", "XXXXX."],
    'C': [".XXXXX", "XX...X", "XX....", "XX....", "XX....", "XX....", "XX....", "XX...X", ".XXXXX"],
    'D': ["XXXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XXXXX."],
    'E': ["XXXXXX", "XX....", "XX....", "XXXXX.", "XXXXX.", "XX....", "XX....", "XX....", "XXXXXX"],
    'F': ["XXXXXX", "XX....", "XX....", "XXXXX.", "XXXXX.", "XX....", "XX....", "XX....", "XX...."],
    'G': [".XXXXX", "XX...X", "XX....", "XX.XXX", "XX.XXX", "XX..XX", "XX..XX", "XXXXXX", ".XXXX."],
    'H': ["XX..XX", "XX..XX", "XX..XX", "XXXXXX", "XXXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'I': ["XXXXXX", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "XXXXXX"],
    'J': ["...XXX", "....XX", "....XX", "....XX", "....XX", "....XX", "XX..XX", "XX..XX", ".XXXX."],
    'K': ["XX...X", "XX..XX", "XX.XX.", "XXXX..", "XXXX..", "XX.XX.", "XX..XX", "XX...X", "XX...X"],
    'L': ["XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XXXXXX"],
    'M': ["XX...XX", "XXX.XXX", "XXXXXXX", "XX.X.XX", "XX...XX", "XX...XX", "XX...XX", "XX...XX", "XX...XX"],
    'N': ["XX..XX", "XXX.XX", "XXXXXX", "XX.XXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'O': [".XXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", ".XXXX."],
    'P': ["XXXXX.", "XX..XX", "XX..XX", "XXXXX.", "XXXXX.", "XX....", "XX....", "XX....", "XX...."],
    'Q': [".XXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX.XXX", ".XXXX.", "....XX"],
    'R': ["XXXXX.", "XX..XX", "XX..XX", "XXXXX.", "XXXXX.", "XX.XX.", "XX..XX", "XX..XX", "XX...X"],
    'S': [".XXXXX", "XX...X", "XX....", ".XXXX.", ".XXXX.", "....XX", "X...XX", "XX..XX", ".XXXX."],
    'T': ["XXXXXXX", "XXXXXXX", "...XX..", "...XX..", "...XX..", "...XX..", "...XX..", "...XX..", "...XX.."],
    'U': ["XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", ".XXXX."],
    'V': ["XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", ".XXXX.", ".XXXX.", "..XX..", "..XX.."],
    'W': ["XX...XX", "XX...XX", "XX...XX", "XX...XX", "XX.X.XX", "XXXXXXX", "XXX.XXX", "XX...XX", "XX...XX"],
    'X': ["XX..XX", "XX..XX", ".XXXX.", "..XX..", "..XX..", ".XXXX.", "XX..XX", "XX..XX", "XX..XX"],
    'Y': ["XX..XX", "XX..XX", ".XXXX.", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX.."],
    'Z': ["XXXXXX", "XXXXXX", "....XX", "...XX.", "..XX..", ".XX...", "XX....", "XXXXXX", "XXXXXX"],

    # Cyrillic
    'А': [".XXXX.", "XX..XX", "XX..XX", "XXXXXX", "XXXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'Б': ["XXXXXX", "XX....", "XX....", "XXXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XXXXX."],
    'В': ["XXXXX.", "XX..XX", "XX..XX", "XXXXX.", "XXXXX.", "XX..XX", "XX..XX", "XX..XX", "XXXXX."],
    'Г': ["XXXXXX", "XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XX...."],
    'Д': ["..XXXX.", "..XX.XX", "..XX.XX", "..XX.XX", "..XX.XX", "..XX.XX", "XXXXXXXX", "XX....XX", "XX....XX"],
    'Е': ["XXXXXX", "XX....", "XX....", "XXXXX.", "XXXXX.", "XX....", "XX....", "XX....", "XXXXXX"],
    'Ё': ["..XX..", "XXXXXX", "XX....", "XXXXX.", "XXXXX.", "XX....", "XX....", "XX....", "XXXXXX"],
    'Ж': ["XX.X.XX", "XX.X.XX", ".XXXXX.", "..XXX..", "..XXX..", ".XXXXX.", "XX.X.XX", "XX.X.XX", "XX.X.XX"],
    'З': ["XXXXXX", "....XX", "....XX", "..XXXX", "....XX", "....XX", "....XX", "X...XX", ".XXXX."],
    'И': ["XX..XX", "XX..XX", "XX..XX", "XX.XXX", "XXXXXX", "XXX.XX", "XX..XX", "XX..XX", "XX..XX"],
    'Й': [".XXXX.", "XX..XX", "XX..XX", "XX.XXX", "XXXXXX", "XXX.XX", "XX..XX", "XX..XX", "XX..XX"],
    'К': ["XX...X", "XX..XX", "XX.XX.", "XXXX..", "XXXX..", "XX.XX.", "XX..XX", "XX...X", "XX...X"],
    'Л': ["..XXXX", ".XX.XX", ".XX.XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'М': ["XX...XX", "XXX.XXX", "XXXXXXX", "XX.X.XX", "XX...XX", "XX...XX", "XX...XX", "XX...XX", "XX...XX"],
    'Н': ["XX..XX", "XX..XX", "XX..XX", "XXXXXX", "XXXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'О': [".XXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", ".XXXX."],
    'П': ["XXXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    'Р': ["XXXXX.", "XX..XX", "XX..XX", "XXXXX.", "XXXXX.", "XX....", "XX....", "XX....", "XX...."],
    'С': [".XXXXX", "XX...X", "XX....", "XX....", "XX....", "XX....", "XX....", "XX...X", ".XXXXX"],
    'Т': ["XXXXXXX", "XXXXXXX", "...XX..", "...XX..", "...XX..", "...XX..", "...XX..", "...XX..", "...XX.."],
    'У': ["XX..XX", "XX..XX", "XX..XX", ".XXXXX", "....XX", "....XX", "...XX.", "..XX..", ".XX..."],
    'Ф': ["..XXX..", ".XX.XX.", "XXXXXXX", "XX.X.XX", "XXXXXXX", ".XX.XX.", "..XXX..", "..XXX..", "..XXX.."],
    'Х': ["XX..XX", "XX..XX", ".XXXX.", "..XX..", "..XX..", ".XXXX.", "XX..XX", "XX..XX", "XX..XX"],
    'Ц': ["XX..XX.", "XX..XX.", "XX..XX.", "XX..XX.", "XX..XX.", "XX..XX.", "XXXXXXX", "....XXX", ".....XX"],
    'Ч': ["XX..XX", "XX..XX", "XX..XX", ".XXXXX", "....XX", "....XX", "....XX", "....XX", "....XX"],
    'Ш': ["XX.X.XX", "XX.X.XX", "XX.X.XX", "XX.X.XX", "XX.X.XX", "XX.X.XX", "XX.X.XX", "XXXXXXX", "XXXXXXX"],
    'Щ': ["XX.X.XX.", "XX.X.XX.", "XX.X.XX.", "XX.X.XX.", "XX.X.XX.", "XX.X.XX.", "XXXXXXXX", "....XXXX", "......XX"],
    'Ъ': ["XXXX...", "..XX...", "..XX...", "..XXXX.", "..XX.XX", "..XX.XX", "..XX.XX", "..XX.XX", "..XXXX."],
    'Ы': ["XX...XX", "XX...XX", "XX...XX", "XXXX.XX", "XX.X.XX", "XX.X.XX", "XX.X.XX", "XX.X.XX", "XXXX.XX"],
    'Ь': ["XX....", "XX....", "XX....", "XXXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", "XXXXX."],
    'Э': [".XXXX.", "XX...X", "....XX", "....XX", "..XXXX", "....XX", "....XX", "XX...X", ".XXXX."],
    'Ю': ["XX.XXXX", "XX.X..X", "XX.X..X", "XXXX..X", "XXXX..X", "XX.X..X", "XX.X..X", "XX.X..X", "XX.XXXX"],
    'Я': [".XXXXX", "XX..XX", "XX..XX", ".XXXXX", ".XXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],

    # Digits
    '0': [".XXXX.", "XX..XX", "XX.XXX", "XX.XXX", "XX..XX", "XXX.XX", "XXX.XX", "XX..XX", ".XXXX."],
    '1': ["..XX..", ".XXX..", "XXXX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "XXXXXX"],
    '2': [".XXXX.", "XX..XX", "....XX", "...XX.", "..XX..", ".XX...", "XX....", "XXXXXX", "XXXXXX"],
    '3': ["XXXXXX", "....XX", "...XX.", "..XXX.", "...XX.", "....XX", "....XX", "XX..XX", ".XXXX."],
    '4': ["XX..XX", "XX..XX", "XX..XX", "XXXXXX", "XXXXXX", "....XX", "....XX", "....XX", "....XX"],
    '5': ["XXXXXX", "XX....", "XX....", "XXXXX.", "....XX", "....XX", "....XX", "XX..XX", ".XXXX."],
    '6': [".XXXX.", "XX..XX", "XX....", "XXXXX.", "XX..XX", "XX..XX", "XX..XX", "XX..XX", ".XXXX."],
    '7': ["XXXXXX", "XXXXXX", "....XX", "...XX.", "..XX..", ".XX...", "XX....", "XX....", "XX...."],
    '8': [".XXXX.", "XX..XX", "XX..XX", ".XXXX.", ".XXXX.", "XX..XX", "XX..XX", "XX..XX", ".XXXX."],
    '9': [".XXXX.", "XX..XX", "XX..XX", "XX..XX", ".XXXXX", "....XX", "....XX", "XX..XX", ".XXXX."],

    # Symbols
    ' ': ["......", "......", "......", "......", "......", "......", "......", "......", "......"],
    '-': ["......", "......", "......", "XXXXXX", "XXXXXX", "......", "......", "......", "......"],
    '_': ["......", "......", "......", "......", "......", "......", "......", "XXXXXX", "XXXXXX"],
    '/': ["....XX", "...XX.", "...XX.", "..XX..", "..XX..", ".XX...", ".XX...", "XX....", "XX...."],
    '\\': ["XX....", "XX....", ".XX...", ".XX...", "..XX..", "..XX..", "...XX.", "...XX.", "....XX"],
    ':': ["......", "..XX..", "..XX..", "......", "......", "..XX..", "..XX..", "......", "......"],
    '.': ["......", "......", "......", "......", "......", "......", "..XX..", "..XX..", "......"],
    ',': ["......", "......", "......", "......", "......", "......", "..XX..", "..XX..", ".XX..."],
    '!': ["..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "......", "..XX..", "..XX..", "......"],
    '?': [".XXXX.", "XX..XX", "....XX", "...XX.", "..XX..", "......", "..XX..", "..XX..", "......"],
    '+': ["......", "..XX..", "..XX..", "XXXXXX", "XXXXXX", "..XX..", "..XX..", "......", "......"],
    '=': ["......", "......", "XXXXXX", "XXXXXX", "......", "XXXXXX", "XXXXXX", "......", "......"],
    '&': [".XX...", "XX.XX.", "XX.XX.", ".XXXX.", "XX..XX", "XX.XXX", "XX..XX", ".XXXX.", "....XX"],
    '[': ["XXXX..", "XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XXXX.."],
    ']': ["..XXXX", "....XX", "....XX", "....XX", "....XX", "....XX", "....XX", "....XX", "..XXXX"],
    '(': ["...XX.", "..XX..", ".XX...", ".XX...", ".XX...", ".XX...", ".XX...", "..XX..", "...XX."],
    ')': [".XX...", "..XX..", "...XX.", "...XX.", "...XX.", "...XX.", "...XX.", "..XX..", ".XX..."],
    '|': ["..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX.."],
    '#': [".X..X.", "XXXXXX", ".X..X.", ".X..X.", "XXXXXX", ".X..X.", ".X..X.", "......", "......"],
    '*': ["......", ".X..X.", "..XX..", "XXXXXX", "..XX..", ".X..X.", "......", "......", "......"],
    '>': ["XX....", ".XX...", "..XX..", "...XX.", "....XX", "...XX.", "..XX..", ".XX...", "XX...."],
    '<': ["....XX", "...XX.", "..XX..", ".XX...", "XX....", ".XX...", "..XX..", "...XX.", "....XX"],
    '\'': ["..XX..", "..XX..", ".XX...", "......", "......", "......", "......", "......", "......"],
    '"': [".XX.XX", ".XX.XX", ".XX.XX", "......", "......", "......", "......", "......", "......"],
}

def matrix_to_rects(matrix, char_symbol, color, px_size, offset_x, offset_y):
    rects = []
    for row_idx, row in enumerate(matrix):
        col_idx = 0
        while col_idx < len(row):
            if row[col_idx] == char_symbol:
                start_col = col_idx
                while col_idx < len(row) and row[col_idx] == char_symbol:
                    col_idx += 1
                run = col_idx - start_col
                x = offset_x + start_col * px_size
                y = offset_y + row_idx * px_size
                w = run * px_size
                h = px_size
                rects.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>')
            else:
                col_idx += 1
    return "".join(rects)

def measure_text_cols(text, spacing=2):
    """Calculates total columns for a string of pixel characters."""
    total = 0
    for char in text.upper():
        glyph = GLYPHS.get(char, GLYPHS[' '])
        w = len(glyph[0])
        total += (w + spacing)
    if total > 0:
        total -= spacing
    return max(0, total)

def measure_text_width(text, px_size, spacing=2):
    """Calculates pixel width of a string at given px_size."""
    return measure_text_cols(text, spacing=spacing) * px_size

def split_text_into_lines(text, max_width, px_size, spacing=2, max_lines=2):
    """
    Splits text into up to max_lines lines respecting word boundaries,
    ensuring each line fits within max_width.
    """
    words = text.strip().split()
    if not words:
        return [""]

    if max_lines <= 1 or len(words) == 1:
        # Check if single word fits or needs truncation
        line = words[0]
        while len(line) > 3 and measure_text_width(line, px_size, spacing) > max_width:
            line = line[:-1]
        return [line]

    # Attempt to divide words into balanced lines
    best_lines = None
    min_imbalance = float('inf')

    # Try all valid split points for 2 lines
    for i in range(1, len(words)):
        l1 = " ".join(words[:i])
        l2 = " ".join(words[i:])
        w1 = measure_text_width(l1, px_size, spacing)
        w2 = measure_text_width(l2, px_size, spacing)

        if w1 <= max_width and w2 <= max_width:
            imbalance = abs(w1 - w2)
            if imbalance < min_imbalance:
                min_imbalance = imbalance
                best_lines = [l1, l2]

    if best_lines:
        return best_lines

    # Greedy fallback: fit as much into line 1, then line 2
    l1_words = []
    l2_words = []
    for word in words:
        test_l1 = " ".join(l1_words + [word])
        if measure_text_width(test_l1, px_size, spacing) <= max_width and not l2_words:
            l1_words.append(word)
        else:
            l2_words.append(word)

    if not l1_words and words:
        l1_words = [words[0]]
        l2_words = words[1:]

    l1 = " ".join(l1_words)
    l2 = " ".join(l2_words)

    # Clamping/truncating l2 if it still overflows
    while len(l2) > 3 and measure_text_width(l2 + "...", px_size, spacing) > max_width:
        l2 = l2[:-1]
    if len(l2_words) > 0 and len(l2) < len(" ".join(l2_words)):
        l2 = l2.rstrip() + "..."

    lines = [l1]
    if l2:
        lines.append(l2)
    return lines[:max_lines]

def calculate_smart_layout(text, max_width=480, default_px_size=6, min_px_size=3, spacing=2, allow_wrap=True):
    """
    Determines optimal px_size and line splits (1 or 2 lines)
    to keep typography within max_width without colliding with HUD elements.
    """
    clean_text = text.strip()
    if not clean_text:
        return [""], default_px_size

    # Step 1: Try single line at px_size in [6, 5, 4]
    for px in range(default_px_size, 3, -1):
        if measure_text_width(clean_text, px, spacing) <= max_width:
            return [clean_text], px

    # Step 2: If single line at px=4 overflows, try 2 lines at px=4, then px=5, then px=3 (without truncation)
    if allow_wrap and " " in clean_text:
        for px in [4, 5, 3]:
            lines = split_text_into_lines(clean_text, max_width, px, spacing=spacing, max_lines=2)
            if len(lines) == 2 and not any(l.endswith("...") for l in lines) and all(measure_text_width(l, px, spacing) <= max_width for l in lines):
                return lines, px

    # Step 3: Single line fallback at min_px_size
    px = min_px_size
    if measure_text_width(clean_text, px, spacing) <= max_width:
        return [clean_text], px

    # Step 4: Final 2-line fallback at min_px_size with truncation if needed
    if allow_wrap:
        lines = split_text_into_lines(clean_text, max_width, px, spacing=spacing, max_lines=2)
        return lines, px

    # Hard clamp single line
    clamped = clean_text
    while len(clamped) > 3 and measure_text_width(clamped + "...", px, spacing) > max_width:
        clamped = clamped[:-1]
    return [clamped + "..."], px

def calculate_px_size(text, max_width=520, spacing=2, default_px_size=6, min_px_size=3):
    """Legacy helper for backward compatibility."""
    lines, px = calculate_smart_layout(text, max_width=max_width, default_px_size=default_px_size,
                                       min_px_size=min_px_size, spacing=spacing, allow_wrap=False)
    return px

def render_3d_text(text, x, y, px_size=None, front_color="#00C8D7", mid_shadow="#005577", dark_shadow="#050B14",
                   spacing=2, max_width=480, allow_wrap=True):
    """
    Renders razor-sharp 3D pixel typography.
    Automatically handles smart downscaling and 2-line word wrapping
    to prevent collision with right-side HUD widgets.
    """
    if px_size is None or px_size == "auto":
        lines, px_size = calculate_smart_layout(text, max_width=max_width, default_px_size=6,
                                                min_px_size=3, spacing=spacing, allow_wrap=allow_wrap)
    else:
        # User specified explicit px_size
        if allow_wrap and measure_text_width(text, px_size, spacing) > max_width and " " in text:
            lines = split_text_into_lines(text, max_width, px_size, spacing=spacing, max_lines=2)
        else:
            lines = [text]

    glyph_h = 9
    single_line_h = glyph_h * px_size + int(px_size * 1.2)
    line_gap = max(4, int(px_size * 1.4))

    all_shadow_dark = []
    all_shadow_mid = []
    all_front = []
    max_line_width = 0

    curr_y = y
    for line_idx, line in enumerate(lines):
        curr_x = x
        for char in line.upper():
            glyph = GLYPHS.get(char, GLYPHS[' '])
            w = len(glyph[0])
            all_shadow_dark.append(matrix_to_rects(glyph, 'X', dark_shadow, px_size, curr_x + int(px_size * 1.2), curr_y + int(px_size * 1.2)))
            all_shadow_mid.append(matrix_to_rects(glyph, 'X', mid_shadow, px_size, curr_x + int(px_size * 0.6), curr_y + int(px_size * 0.6)))
            all_front.append(matrix_to_rects(glyph, 'X', front_color, px_size, curr_x, curr_y))
            curr_x += (w + spacing) * px_size

        line_w = curr_x - x
        if line_w > max_line_width:
            max_line_width = line_w
        curr_y += single_line_h + line_gap

    total_width = max_line_width
    total_height = len(lines) * single_line_h + (len(lines) - 1) * line_gap

    svg_markup = f"""<g class="pixel-text-3d">
  <!-- Shadow Dark -->
  {''.join(all_shadow_dark)}
  <!-- Shadow Mid -->
  {''.join(all_shadow_mid)}
  <!-- Front Face -->
  {''.join(all_front)}
</g>"""
    return svg_markup, total_width, total_height

