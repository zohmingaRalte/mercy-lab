"""
Mercy Hospital Lab Report — clean Apple-inspired design
"""

from fpdf import FPDF
import os
from datetime import date

# Works both in development and inside a PyInstaller exe
def _base_dir():
    import sys
    if getattr(sys, "frozen", False):
        # Running as PyInstaller bundle — assets extracted to sys._MEIPASS
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = _base_dir()
LOGO_PATH        = os.path.join(BASE_DIR, "assets_logo.jpg")
FONT_REGULAR     = os.path.join(BASE_DIR, "DejaVuSans.ttf")
FONT_BOLD        = os.path.join(BASE_DIR, "DejaVuSans-Bold.ttf")
FONT_ITALIC      = os.path.join(BASE_DIR, "DejaVuSans-Oblique.ttf")
FONT_BOLD_ITALIC = os.path.join(BASE_DIR, "DejaVuSans-BoldOblique.ttf")
FONT_AWESOME     = os.path.join(BASE_DIR, "fontawesome.ttf")

# Palette
BLUE      = (25, 105, 210)
BLUE_DARK = (15,  65, 130)
WHITE     = (255, 255, 255)
GR6       = (240, 242, 248)   # systemGray6
GR5       = (210, 215, 228)   # separator
GR3       = (185, 192, 210)
GR        = (120, 128, 150)   # secondary label
T1        = (0,    0,   0)    # primary
T2        = (50,  58,  80)
T3        = (130, 138, 160)   # ref range

# Layout
PW, PH  = 210, 297
HDR_H      = 30          # header height — branding only
INFO_BAR_H = 9           # grey contact bar height
LS_W    = 30          # left strip width — slim
RC_X    = LS_W + 5
RC_W    = PW - RC_X - 6
RC_P    = 4
CL      = 64          # col label
CV      = 34          # col value
CR      = RC_W - RC_P - CL - CV

# Two-column layout for dense sections
TC_GAP  = 4                        # gap between the two content cols
TC_W    = (RC_W - TC_GAP) / 2     # each col width
TC_X_L  = RC_X                    # left col start x
TC_X_R  = RC_X + TC_W + TC_GAP   # right col start x
TC_P    = 3                        # padding inside each col
TC_CL   = 44                       # label col in two-col mode
TC_CV   = 22                       # value col
TC_CR   = TC_W - TC_P - TC_CL - TC_CV  # ref col

MIZO = [
    "Mercy Hospital Laboratory ah I thisen test tura I lo kal theilo anih pawhin kan rawn pan chilh the che.",
    "Mercy Hospital ah 24x7 in damdawi leitheihin a awm e.",
    "Mercy Hospital ah doctor rawn tur zing 10:00am atangin a awm reng e.",
    "Mercy Hospital ah emergency casualty 24x7 a pan theih tur a awm e.",
    "Mercy Hospital ahOxygen cylinder hawh tur kan nei e.",
    "Mercy Hospital ah MUHCS a hman theih e.",
    "Mercy Hospitalah Mit en tir a theih e.",
]


class LabReport(FPDF):
    def __init__(self, patient, technician):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(0, 0, 0)
        self.set_auto_page_break(True, margin=20)  # auto new page, 20mm bottom margin
        self.patient    = patient
        self.technician = technician
        self.add_font("DJ", "",   fname=FONT_REGULAR)
        self.add_font("DJ", "B",  fname=FONT_BOLD)
        self.add_font("DJ", "I",  fname=FONT_ITALIC)
        self.add_font("DJ", "BI", fname=FONT_BOLD_ITALIC)
        if os.path.exists(FONT_AWESOME):
            self.add_font("FA", "", fname=FONT_AWESOME)

    def c(self, rgb): self.set_text_color(*rgb)
    def f(self, rgb): self.set_fill_color(*rgb)
    def d(self, rgb): self.set_draw_color(*rgb)

    # ── HEADER ────────────────────────────────────────────────────────────────
    def _header(self):
        # ── Pure white branding area ──
        self.f(WHITE); self.rect(0, 0, PW, HDR_H, "F")

        # Logo — vertically centred
        logo_h = 22
        logo_x = 5
        logo_y = (HDR_H - logo_h) / 2
        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, x=logo_x, y=logo_y, h=logo_h)
            tx = logo_x + logo_h + 6
        else:
            tx = 8

        # Text block centred against logo
        block_h = 15
        name_y  = logo_y + (logo_h - block_h) / 2
        self.set_font("DJ", "B", 18); self.c(T1)
        self.set_xy(tx, name_y)
        self.cell(PW - tx - 10, 8, "MERCY HOSPITAL")

        self.set_font("DJ", "", 12); self.c(T2)
        self.set_xy(tx, name_y + 9)
        self.cell(PW - tx - 10, 6, "Rural Diagnostic & Research Centre")



    def _info_bar(self):
        y  = HDR_H
        h  = INFO_BAR_H
        dt = self.patient.get("date", date.today().strftime("%d-%m-%Y"))

        # Thinner black lines — full page width, drawn last so strip cant overlap
        self.d(T1); self.set_line_width(0.4)
        self.line(0, y,     210, y)
        self.line(0, y + h, 210, y + h)

        # FontAwesome 4 codepoints
        FA_PHONE    = chr(0xf095)   # fa-phone
        FA_LOCATION = chr(0xf041)   # fa-map-marker
        FA_CALENDAR = chr(0xf073)   # fa-calendar

        items = [
            (FA_PHONE,    "7630974750"),
            (FA_LOCATION, "Bazar Veng, New Serchhip"),
            (FA_CALENDAR, dt),
        ]

        item_w  = PW / len(items)
        ty      = y + (h - 4.5) / 2
        use_fa  = os.path.exists(FONT_AWESOME)

        for i, (icon, value) in enumerate(items):
            icon_w = 4.5 if use_fa else 0
            gap    = 1.5 if use_fa else 0
            txt_w  = len(value) * 1.62
            unit_w = icon_w + gap + txt_w
            sx     = i * item_w + (item_w - unit_w) / 2

            if use_fa:
                self.set_font("FA", "", 9); self.c(T2)
                self.set_xy(sx, ty)
                self.cell(icon_w, 4.5, icon)

            self.set_font("DJ", "", 8.5); self.c(T2)
            self.set_xy(sx + icon_w + gap, ty + 0.2)
            self.cell(txt_w + 2, 4, value)

            if i < len(items) - 1:
                self.d((180,180,180)); self.set_line_width(0.3)
                self.line((i+1)*item_w, y+2, (i+1)*item_w, y+h-2)

    def _patient(self):
        y    = HDR_H + INFO_BAR_H + 5
        rx   = RC_X
        ptype = self.patient.get("type", "IPD").upper()
        is_ipd = (ptype == "IPD")

        # Sentence-case helper for patient text fields
        def sc(val): return val.strip().title() if val and val.strip() else ""

        if is_ipd:
            # ── IPD: 2 rows ───────────────────────────────────────────────────
            # Row 1: Name | Age | Sex | Type
            # Row 2: Address | Ward | Bed No.
            col_x = [rx, rx + RC_W * 0.46, rx + RC_W * 0.64, rx + RC_W * 0.82]
            col_w = [RC_W * 0.46, RC_W * 0.18, RC_W * 0.18, RC_W * 0.18]

            rows = [
                [("Name",    sc(self.patient.get("name",""))),
                 ("Age",     self.patient.get("age","")),
                 ("Sex",     self.patient.get("sex","")),
                 ("Patient Type", ptype)],
                [("Address", sc(self.patient.get("address",""))),
                 ("Ward",    sc(self.patient.get("ward",""))),
                 ("Bed No.", self.patient.get("bed_no","")),
                 None],
            ]

            for ri, row in enumerate(rows):
                row_y = y + ri * 14
                for ci, item in enumerate(row):
                    if item is None:
                        continue
                    label, value = item
                    x = col_x[ci]
                    w = col_w[ci]
                    self.set_xy(x, row_y)
                    self.set_font("DJ", "B", 9.5); self.c(T1)
                    self.cell(w, 4, label.upper())
                    self.set_xy(x, row_y + 5)
                    self.set_font("DJ", "", 9.5); self.c(T1)
                    self.cell(w - 2, 4.5, value if value else "—")

            bot_y = y + 28

        else:
            # ── OPD: 2 rows ───────────────────────────────────────────────────
            # Row 1: Name | Age | Sex
            # Row 2: Patient Type | Address
            rows = [
                [
                    (rx,               RC_W * 0.52, "Name",         sc(self.patient.get("name",""))),
                    (rx + RC_W * 0.52, RC_W * 0.24, "Age",          self.patient.get("age","")),
                    (rx + RC_W * 0.76, RC_W * 0.24, "Sex",          self.patient.get("sex","")),
                ],
                [
                    (rx,               RC_W * 0.52, "Patient Type", ptype),
                    (rx + RC_W * 0.52, RC_W * 0.48, "Address",      sc(self.patient.get("address",""))),
                ],
            ]

            for ri, row in enumerate(rows):
                row_y = y + ri * 14
                for cx, cw, label, value in row:
                    self.set_xy(cx, row_y)
                    self.set_font("DJ", "B", 9.5); self.c(T1)
                    self.cell(cw, 4, label.upper())
                    self.set_xy(cx, row_y + 5)
                    self.set_font("DJ", "", 9.5); self.c(T1)
                    self.cell(cw - 2, 4.5, value if value else "—")

            bot_y = y + 28

        return bot_y + 2

    # ── LEFT STRIP ────────────────────────────────────────────────────────────
    def _left_strip(self):
        strip_y = HDR_H + INFO_BAR_H
        # Warm gold/amber background
        self.f((252, 246, 220)); self.rect(0, strip_y, LS_W, PH - strip_y, "F")

        # Subtle right border — toned down
        self.d((200, 185, 140)); self.set_line_width(0.25)
        self.line(LS_W, strip_y, LS_W, PH)

        # Distribute messages evenly — measure real heights then spread gaps
        line_h   = 4.0
        font_sz  = 8.5
        col_w_mm = LS_W - 6
        pad_top  = strip_y + 6
        pad_bot  = PH - 6
        avail    = pad_bot - pad_top

        # Measure each message by rendering off-screen
        self.set_font("DJ", "", font_sz)
        msg_heights = []
        for msg in MIZO:
            self.set_xy(0, 1000)
            self.multi_cell(col_w_mm, line_h, msg, align="L")
            msg_heights.append(self.get_y() - 1000)

        # Distribute remaining space evenly as gaps between messages
        total_text_h = sum(msg_heights)
        gap = (avail - total_text_h) / (len(MIZO) - 1)
        gap = max(4.0, min(gap, 12.0))  # clamp: generous breathing room

        # Recalc start_y to truly centre the block
        total_h = total_text_h + gap * (len(MIZO) - 1)
        start_y = pad_top + max(0, (avail - total_h) / 2)

        y = start_y
        for i, msg in enumerate(MIZO):
            self.set_xy(3, y)
            self.set_font("DJ", "", font_sz); self.c(GR)
            self.multi_cell(col_w_mm, line_h, msg, align="L")
            y += msg_heights[i] + (gap if i < len(MIZO) - 1 else 0)

    # ── SECTION / SUB ────────────────────────────────────────────────────────
    def section_title(self, title, x=None, w=None):
        if x is None: x = RC_X
        if w is None: w = RC_W
        self.ln(5)
        y = self.get_y()
        self.f((215, 225, 245)); self.rect(x, y, w, 9, "F")
        self.set_xy(x + RC_P, y + 1.5)
        self.set_font("DJ", "B", 12); self.c(T1)
        self.cell(w - RC_P, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub_section(self, title, x=None, w=None):
        if x is None: x = RC_X
        if w is None: w = RC_W
        self.ln(1)
        y = self.get_y()
        self.set_xy(x + RC_P, y)
        self.set_font("DJ", "B", 9.5); self.c(T1)
        self.cell(w - RC_P, 5.5, title, new_x="LMARGIN", new_y="NEXT")
        uy = self.get_y()
        self.d((215, 225, 245)); self.set_line_width(0.6)
        self.line(x, uy, x + w, uy)
        self.ln(1.5)

    # ── TEST ROW ─────────────────────────────────────────────────────────────
    def dash_col(self, labels, indent=0, font_sz=9.5):
        """Calculate the X position for em dash alignment based on longest label."""
        self.set_font("DJ", "", font_sz)
        max_w = max(self.get_string_width(l) for l in labels)
        return RC_X + RC_P + indent + max_w + 4

    def test_row(self, label, value, ref="", indent=0, dash_x=None, x=None, col_w=None):
        if value is None:   # test not selected — skip entirely
            return
        if x is None: x = RC_X
        if col_w is None: col_w = RC_W
        rh = 8
        y  = self.get_y()

        # Label
        lx = x + RC_P + indent
        self.set_xy(lx, y + 0.5)
        self.set_font("DJ", "", 9.5); self.c(T1)
        if dash_x is None:
            dash_x = lx + self.get_string_width(label) + 3
        # Clamp label cell to available space before dash — prevents overflow
        label_cell_w = min(self.get_string_width(label) + 1, dash_x - lx - 1)
        self.cell(label_cell_w, rh - 1, label)

        # Em dash
        self.set_xy(dash_x, y + 0.5)
        self.set_font("DJ", "", 9.5); self.c(T1)
        self.cell(6, rh - 1, "—")

        # Measure actual widths to avoid overlap
        val_x   = dash_x + 7
        val_str = str(value) if value else ""
        self.set_font("DJ", "", 9.5)
        val_w_actual = self.get_string_width(val_str)
        self.set_font("DJ", "", 8.5)
        ref_w_actual = self.get_string_width(ref) if ref else 0

        # Total available space from val_x to end of col
        avail = x + col_w - val_x - 2
        # Give ref what it needs (+ 2mm padding), value gets the rest
        ref_w  = min(ref_w_actual + 2, avail * 0.55) if ref else 0
        val_w  = max(avail - ref_w, val_w_actual)

        # Value
        self.set_xy(val_x, y + 0.5)
        self.set_font("DJ", "", 9.5); self.c(T1)
        self.cell(val_w, rh - 1, val_str)

        # Ref — right aligned
        if ref:
            self.set_font("DJ", "", 8.5); self.c((90, 100, 130))
            self.set_xy(x + col_w - ref_w, y + 0.5)
            self.cell(ref_w, rh - 1, ref, align="R")
        self.ln(rh)

    def test_row_multiref(self, label, value, refs, indent=0, dash_x=None, x=None, col_w=None):
        """Like test_row but refs is a list of strings printed on separate lines."""
        if value is None:
            return
        if x is None: x = RC_X
        if col_w is None: col_w = RC_W
        line_h = 5.5
        rh = max(7, line_h * len(refs))
        y  = self.get_y()

        # Label
        lx = x + RC_P + indent
        self.set_xy(lx, y + 0.5)
        self.set_font("DJ", "", 9.5); self.c(T1)
        self.cell(self.get_string_width(label), line_h, label)

        # Em dash
        if dash_x is None:
            dash_x = lx + self.get_string_width(label) + 3
        self.set_xy(dash_x, y + 0.5)
        self.set_font("DJ", "", 9.5); self.c(T1)
        self.cell(6, line_h, "—")

        # Value
        val_x = dash_x + 7
        ref_w = min(62, col_w * 0.42)
        val_end = x + col_w - ref_w
        self.set_xy(val_x, y + 0.5)
        self.set_font("DJ", "", 9.5); self.c(T1)
        self.cell(max(val_end - val_x, 1), line_h, str(value) if value else "")

        # Multi-line refs — each on its own line, right-aligned
        self.set_font("DJ", "", 8); self.c((90, 100, 130))
        for i, ref_line in enumerate(refs):
            self.set_xy(x + col_w - ref_w, y + 0.5 + i * line_h)
            self.cell(ref_w, line_h, ref_line, align="R")

        self.set_y(y + rh)

    def test_row_pair(self, l1, v1, l2, v2, indent=0, dash_x=None):
        if v1 is None and v2 is None:
            return
        v1 = "" if v1 is None else v1
        v2 = "" if v2 is None else v2
        rh   = 7
        half = RC_W / 2
        y    = self.get_y()
        self.set_font("DJ", "", 8.5)
        if dash_x is not None:
            dx_offset = dash_x - RC_X - RC_P
        else:
            dx_offset = max(self.get_string_width(l1), self.get_string_width(l2)) + indent + 3
        for lbl, val, cx in [(l1, v1, RC_X), (l2, v2, RC_X + half)]:
            lx = cx + RC_P + indent
            self.set_xy(lx, y + 0.5)
            self.set_font("DJ", "", 9.5); self.c(T1)
            self.cell(self.get_string_width(lbl), rh - 1, lbl)
            self.set_xy(cx + RC_P + dx_offset, y + 0.5)
            self.cell(6, rh - 1, "—")
            self.set_xy(cx + RC_P + dx_offset + 7, y + 0.5)
            self.set_font("DJ", "", 9.5); self.c(T1)
            self.cell(half - RC_P - dx_offset - 7, rh - 1, str(val) if val else "")
        self.ln(rh)

    # ── TWO-COLUMN HELPERS ───────────────────────────────────────────────────
    def tc_section(self, title, col=0):
        """Section header spanning full RC_W regardless of column."""
        self.ln(5)
        self.set_x(RC_X + RC_P)
        self.set_font("DJ", "B", 8.5); self.c(GR)
        self.cell(RC_W, 5, title.upper(), new_x="LMARGIN", new_y="NEXT")
        self.d(GR5); self.set_line_width(0.3)
        self.line(RC_X, self.get_y(), RC_X + RC_W, self.get_y())
        self.ln(0.5)

    def tc_sub(self, title, x, w):
        """Sub-section header for a specific column."""
        y = self.get_y()
        self.set_xy(x + TC_P, y)
        self.set_font("DJ", "B", 8); self.c(GR)
        self.cell(w - TC_P, 4.5, title.upper(), new_x="LMARGIN", new_y="NEXT")
        self.d(GR5); self.set_line_width(0.2)
        self.line(x, self.get_y(), x + w, self.get_y())
        self.ln(0.5)

    def tc_row(self, label, value, ref="", x=None, w=None, indent=0):
        """Single test row inside a two-col layout."""
        if x is None: x = RC_X
        if w is None: w = TC_W
        rh = 6.5
        y  = self.get_y()

        self.set_xy(x + TC_P + indent, y + 0.3)
        self.set_font("DJ", "", 9.5); self.c(T1)
        lw = TC_CL - indent
        self.cell(lw, rh - 0.5, label)

        self.set_font("DJ", "B", 10); self.c(BLUE if value else GR3)
        self.cell(TC_CV, rh - 0.5, str(value) if value else "—", align="C")

        self.set_font("DJ", "", 8.5); self.c(T3)
        self.cell(w - TC_P - lw - TC_CV - indent, rh - 0.5, ref, align="R")
        self.ln(rh)

    def paint_two_col(self, left_rows, right_rows, start_y):
        """
        Paint two independent columns. Each col tracks its own Y.
        Fonts/sizes match patient info section for consistency.
        """
        x_left   = RC_X + RC_P          # align with patient NAME label
        x_right  = RC_X + RC_P + (RC_W - RC_P) / 2 + 2
        col_w    = (RC_W - RC_P) / 2 - 4
        rh       = 7.5                  # roomier rows
        sub_h    = 9                    # sub-section with breathing space above
        page_bot = PH - 18

        # Calculate content height of each col to set divider end
        def _col_h(rows):
            h = 0
            for r in rows:
                if r['type'] == 'sub':
                    h += 4 + 9    # gap + sub_h
                else:
                    h += 7.5      # rh
            return h
        div_end = start_y + max(_col_h(left_rows), _col_h(right_rows)) + 2

        # Subtle vertical divider — ends at last row, not page bottom
        div_x = x_left + col_w + (x_right - x_left - col_w) / 2
        self.d(GR5); self.set_line_width(0.25)
        self.line(div_x, start_y, div_x, div_end)

        # Pre-compute dash_x per column — longest label + gap, capped at 45% col width
        self.set_font("DJ", "", 9.5)
        def _col_dash_x(rows, cx):
            row_labels = [r['label'] for r in rows if r['type'] == 'row']
            if not row_labels:
                return cx + 30
            max_w = max(self.get_string_width(r['label']) + r.get('indent', 0)
                        for r in rows if r['type'] == 'row')
            max_allowed = col_w * 0.45
            return cx + min(max_w, max_allowed) + 4

        dash_x_left  = _col_dash_x(left_rows,  x_left)
        dash_x_right = _col_dash_x(right_rows, x_right)

        for col_rows, cx, col_dash_x in [
            (left_rows,  x_left,  dash_x_left),
            (right_rows, x_right, dash_x_right)
        ]:
            y = start_y
            for row in col_rows:
                if row['type'] == 'sub':
                    y += 1
                    self.set_xy(cx + RC_P, y)
                    self.set_font("DJ", "B", 9.5); self.c(T1)
                    self.cell(col_w - RC_P, 5.5, row['label'])
                    y += 5.5
                    self.d((215, 225, 245)); self.set_line_width(0.6)
                    self.line(cx, y, cx + col_w, y)
                    y += 2
                else:
                    indent = row.get('indent', 0)
                    value  = row.get('value', '')
                    ref    = row.get('ref', '')

                    if value is None:   # not selected — skip
                        continue

                    # Hairline

                    # Label — clamped to available space before dash
                    self.set_xy(cx + indent, y + 1)
                    self.set_font("DJ", "", 9.5); self.c(T1)
                    lbl_w = min(self.get_string_width(row['label']) + 1,
                                col_dash_x - cx - indent - 1)
                    self.cell(lbl_w, rh - 1.5, row['label'])

                    # Em dash — aligned to col_dash_x
                    self.set_xy(col_dash_x, y + 1)
                    self.cell(6, rh - 1.5, "—")

                    # Value & ref — dynamic widths
                    val_x2  = col_dash_x + 7
                    val_str = str(value) if value else ""
                    self.set_font("DJ", "", 9.5)
                    val_w_actual = self.get_string_width(val_str)
                    self.set_font("DJ", "", 8.5)
                    ref_w_actual = self.get_string_width(ref) if ref else 0
                    avail   = cx + col_w - val_x2 - 2
                    ref_w   = min(ref_w_actual + 2, avail * 0.5) if ref else 0
                    val_w   = max(avail - ref_w, val_w_actual)

                    self.set_xy(val_x2, y + 1)
                    self.set_font("DJ", "", 9.5); self.c(T1)
                    self.cell(val_w, rh - 1.5, val_str)

                    if ref:
                        self.set_font("DJ", "", 8.5); self.c((90, 100, 130))
                        self.set_xy(cx + col_w - ref_w, y + 1)
                        self.cell(ref_w, rh - 1.5, ref, align="R")
                    y += rh

    # ── SIGNATURE ────────────────────────────────────────────────────────────
    def signature_line(self):
        sy = PH - 15
        x1 = RC_X + RC_W - 74
        self.d(GR5); self.set_line_width(0.35)
        self.line(x1, sy, RC_X + RC_W, sy)
        self.set_xy(x1, sy + 2.5)
        self.set_font("DJ", "B", 8.5); self.c(T1)
        self.cell(74, 5, "SIGNATURE OF LAB. TECHNICIAN", align="C",
                  new_x="LMARGIN", new_y="NEXT")
        if self.technician:
            self.set_x(x1)
            self.set_font("DJ", "B", 10); self.c(T1)
            self.cell(74, 5, self.technician, align="C")

    # ── RENDER ───────────────────────────────────────────────────────────────
    def render_page(self, fn, data):
        self.add_page()
        self.f(WHITE); self.rect(0, 0, PW, PH, "F")
        self._header()
        self._left_strip()
        self._info_bar()   # drawn after strip so lines are never covered
        cy = self._patient()
        self.set_xy(RC_X, cy)
        fn(self, data)
        self.signature_line()


# ── Renderers ─────────────────────────────────────────────────────────────────

def _haematology(pdf, d):
    pdf.section_title("Haematology")
    top_labels = ["Hb", "TLC", "ESR"]
    dx_top = pdf.dash_col(top_labels)
    pdf.test_row("Hb",  d.get("Hb",""),  "gm/dl (12–18)",       dash_x=dx_top)
    pdf.test_row("TLC", d.get("TLC",""), "(4000–11000) /cumm",   dash_x=dx_top)
    pdf.test_row("ESR", d.get("ESR",""), "<20 mm / 1st hour",    dash_x=dx_top)
    pdf.sub_section("DLC")
    dlc_labels = ["Neutrophils","Lymphocyte","Eosinophils","Monocytes","Basophils",
                  "Platelets","ANC","AEC","TRBC","PCV","Bleeding Time","Clotting Time"]
    dx_dlc = pdf.dash_col(dlc_labels, indent=5)
    for lbl, key, ref in [
        ("Neutrophils",   "Neutrophils",   "%(40–70)",                "Haematology"),
        ("Lymphocyte",    "Lymphocyte",    "%(20–40)",                "Haematology"),
        ("Eosinophils",   "Eosinophils",   "%(01–06)",                "Haematology"),
        ("Monocytes",     "Monocytes",     "%(02–10)",                "Haematology"),
        ("Basophils",     "Basophils",     "%(0–1)",                  "Haematology"),
        ("Platelets",     "Platelets",     "(1.5–04) lakh",           "Haematology"),
        ("ANC",           "ANC",           "(1800–7000) /cumm",       "Haematology"),
        ("AEC",           "AEC",           "(40–450) /cumm",          "Haematology"),
        ("TRBC",          "TRBC",          "(4.2–6.1 millions/McL)",  "Haematology"),
        ("PCV",           "PCV",           "%(40–55)",                "Haematology"),
        ("Bleeding Time", "Bleeding Time", "(1–5 mins)",              "Haematology"),
        ("Clotting Time", "Clotting Time", "(4–9 mins)",              "Haematology"),
        ("PT",            "PT",             "(11–16 seconds)",         "Haematology"),
        ("INR",           "INR",            "(0.64–1.17)",             "Haematology"),
    ]:
        pdf.test_row(lbl, d.get(key,""), ref, indent=5, dash_x=dx_dlc)
    bg_raw = d.get("Blood Group", "")
    try:
        import json as _json
        bg_data = _json.loads(bg_raw) if bg_raw else {}
        bg_val = bg_data.get("bg", "") or ""
        rh_val = bg_data.get("rh", "") or ""
    except Exception:
        # Fallback: old format "O +" split by space
        parts = bg_raw.split() if bg_raw else []
        bg_val = parts[0] if parts else ""
        rh_val = parts[1] if len(parts) > 1 else ""
    pdf.test_row_pair(
        "Blood Group", bg_val if bg_val else None,
        "RH",          rh_val if rh_val else None,
        indent=5, dash_x=dx_dlc
    )


def _urine_stool(pdf, d):
    pdf.section_title("Urine")
    pdf.test_row_pair("Pro/Alb", d.get("Pro/Alb",""), "Sugar", d.get("Sugar",""))
    pdf.sub_section("Microscopic Examination")
    mic_labels = ["Pus","Epi","RBC","Crystal","Cast","Others"]
    dx_mic = pdf.dash_col(mic_labels, indent=5)
    for lbl, key in [("Pus","Pus"),("Epi","Epi"),("RBC","RBC (Urine)"),
                     ("Crystal","Crystal"),("Cast","Cast"),("Others","Others (Urine)")]:
        pdf.test_row(lbl, d.get(key,""), "/hpf", indent=5, dash_x=dx_mic)
    pdf.sub_section("Special Tests")
    sp_labels = ["Pregnancy Test","24hrs Urine Protein","24hrs Urine Output",
                 "HEV-IgM","HBeAg","HAV-IgM","Urine AFB","Sputum AFB"]
    dx_sp = pdf.dash_col(sp_labels)
    for lbl, key, ref in [
        ("Pregnancy Test","Pregnancy Test","+ve / -ve"),
        ("24hrs Urine Protein","24hrs Urine Protein",""),
        ("24hrs Urine Output","24hrs Urine Output",""),
        ("HEV-IgM","HEV-IgM",""),("HBeAg","HBeAg",""),("HAV-IgM","HAV-IgM",""),
        ("Urine AFB","Urine AFB",""),("Sputum AFB","Sputum AFB",""),
    ]:
        pdf.test_row(lbl, d.get(key,""), ref, dash_x=dx_sp)
    pdf.section_title("Stool")
    st_labels = ["Stool Occult Blood","Stool RE","Gross"]
    dx_st = pdf.dash_col(st_labels)
    pdf.test_row("Stool Occult Blood", d.get("Stool Occult Blood",""), "", dash_x=dx_st)
    pdf.test_row("Stool RE",           d.get("Stool RE",""),           "", dash_x=dx_st)
    pdf.test_row("Gross",              d.get("Gross",""),              "", dash_x=dx_st)


def _serology(pdf, d):
    pdf.section_title("Serology & Parasitology")
    cy = pdf.get_y()

    def R(key): return d.get(key, "")

    left = [
        {'type':'sub',  'label':'General'},
        {'type':'row',  'label':'H. Pylori',      'value':R("H. Pylori"),      'ref':''},
        {'type':'row',  'label':'HBsAg',           'value':R("HBsAg"),          'ref':''},
        {'type':'row',  'label':'ANTI HCV',        'value':R("ANTI HCV"),       'ref':''},
        {'type':'row',  'label':'Retro',           'value':R("Retro"),          'ref':''},
        {'type':'row',  'label':'Syphilis',        'value':R("Syphilis"),       'ref':''},
        {'type':'row',  'label':'BI.MP (Slide)',   'value':R("BI.MP (Slide)"),  'ref':''},
        {'type':'row',  'label':'BI.MP (ICT)',     'value':R("BI.MP (ICT)"),    'ref':''},
        {'type':'row',  'label':'Scrub Typhus',    'value':R("Scrub Typhus"),   'ref':''},
        {'type':'row',  'label':'Influenza',        'value':R("Influenza"),      'ref':''},
        {'type':'row',  'label':'Typhi IgG IgM',  'value':R("Typhi IgG IgM"), 'ref':''},
        {'type':'sub',  'label':'Dengue'},
        {'type':'row',  'label':'NslAg',           'value':R("Dengue NslAg"),   'ref':'', 'indent':4},
        {'type':'row',  'label':'IgM / IgG',       'value':R("Dengue IgM/IgG"),'ref':'', 'indent':4},
        {'type':'sub',  'label':'Widal'},
        {'type':'row',  'label':"S. Typhi 'O'",   'value':R("S. Typhi O"),     'ref':'', 'indent':4},
        {'type':'row',  'label':"S. Typhi 'H'",   'value':R("S. Typhi H"),     'ref':'', 'indent':4},
        {'type':'row',  'label':'S. Paratyphi AH','value':R("S. Paratyphi AH"),'ref':'', 'indent':4},
        {'type':'row',  'label':'S. Paratyphi BH','value':R("S. Paratyphi BH"),'ref':'', 'indent':4},
    ]
    right = [
        {'type':'sub',  'label':'Well Felix'},
        {'type':'row',  'label':'OXK',  'value':R("OXK"),  'ref':'', 'indent':4},
        {'type':'row',  'label':'OX2',  'value':R("OX2"),  'ref':'', 'indent':4},
        {'type':'row',  'label':'OX19', 'value':R("OX19"), 'ref':'', 'indent':4},
        {'type':'sub',  'label':'Quantitative Tests'},
        {'type':'row',  'label':'RA / RF',          'value':R("RA/RF"),                  'ref':'<20 IU/ml'},
        {'type':'row',  'label':'ASO Adult',        'value':R("ASO Adult"),              'ref':'<200 IU/ml'},
        {'type':'row',  'label':'ASO Child <5yr',   'value':R("ASO Children <5yrs"),     'ref':'100 IU/ml'},
        {'type':'row',  'label':'CRP Adult',        'value':R("CRP Adult"),              'ref':'<6 mg/L'},
        {'type':'row',  'label':'CRP Infant',       'value':R("CRP Infants & Children"), 'ref':'<2.8 mg/L'},
        {'type':'row',  'label':'CRP Newborn',      'value':R("CRP Newborn <3 weeks"),   'ref':'<4.1 mg/L'},
    ]
    pdf.paint_two_col(left, right, cy)


def _biochemistry(pdf, d):
    pdf.section_title("Biochemistry")
    cy = pdf.get_y()

    def R(key): return d.get(key, "")

    left = [
        {'type':'sub',  'label':'Blood Sugar'},
        {'type':'row',  'label':'Fasting',     'value':R("Fasting"),     'ref':'70–110 mg/dl',   'indent':4},
        {'type':'row',  'label':'PP',          'value':R("PP"),          'ref':'<150 mg/dl',      'indent':4},
        {'type':'row',  'label':'RBS',         'value':R("RBS"),         'ref':'70–150 mg/dl',    'indent':4},
        {'type':'sub',  'label':'RFT / KFT'},
        {'type':'row',  'label':'Urea',        'value':R("Urea"),        'ref':'14–40 mg/dl',     'indent':4},
        {'type':'row',  'label':'Creatinine',  'value':R("Creatinine"),  'ref':'0.2–1.4 mg/dl',   'indent':4},
        {'type':'sub',  'label':'LFT'},
        {'type':'row',  'label':'T. Bilirubin','value':R("T. Bilirubin"),'ref':'0.1–1.0 mg/dl',   'indent':4},
        {'type':'row',  'label':'D. Bilirubin','value':R("D. Bilirubin"),'ref':'0–0.5 mg/dl',     'indent':4},
        {'type':'row',  'label':'ID. Bilirubin','value':R("ID. Bilirubin"),'ref':'0.1–0.7 mg/dl', 'indent':4},
        {'type':'row',  'label':'SGOT (AST)',  'value':R("SGOT (AST)"),  'ref':'5–40 U/L',        'indent':4},
        {'type':'row',  'label':'SGPT (ALT)',  'value':R("SGPT (ALT)"),  'ref':'5–45 U/L',        'indent':4},
        {'type':'row',  'label':'T. Protein',  'value':R("T. Protein"),  'ref':'6–8 gm/dl',       'indent':4},
        {'type':'row',  'label':'Albumin',     'value':R("Albumin"),     'ref':'3.2–5.5 gm/dl',   'indent':4},
        {'type':'row',  'label':'Globulin',    'value':R("Globulin"),    'ref':'2.3–3.5 gm/dl',   'indent':4},
        {'type':'sub',  'label':'Alka. Phos'},
        {'type':'row',  'label':'M',                  'value':R("Alka. Phos M"),        'ref':'53–128 U/L',  'indent':4},
        {'type':'row',  'label':'F',                  'value':R("Alka. Phos F"),        'ref':'42–141 U/L',  'indent':4},
        {'type':'row',  'label':'Children (1–14 yrs)','value':R("Alka. Phos Children"), 'ref':'54–369 U/L',  'indent':4},
    ]
    right = [
        {'type':'sub',  'label':'Lipid Profile'},
        {'type':'row',  'label':'T. Cholesterol','value':R("T. Cholesterol"),'ref':'<200 mg/dl',  'indent':4},
        {'type':'row',  'label':'Triglyceride',  'value':R("Triglyceride"),  'ref':'<160 mg/dl',  'indent':4},
        {'type':'row',  'label':'HDL',           'value':R("HDL"),           'ref':'30–80 mg/dl', 'indent':4},
        {'type':'row',  'label':'LDL',           'value':R("LDL"),           'ref':'<130 mg/dl',  'indent':4},
        {'type':'row',  'label':'VLDL',          'value':R("VLDL"),          'ref':'7–30 mg/dl',  'indent':4},
    ]
    pdf.paint_two_col(left, right, cy)



def _electrolytes(pdf, d):
    pdf.section_title("Electrolytes & Cardiac")
    pdf.sub_section("Serum Electrolyte")
    el_labels = ["Sodium (NA)","Potassium (K)","Chloride","S. Calcium",
                 "S. Uric Acid","S. Amylase","S. Lipase"]
    dx_el = pdf.dash_col(el_labels, indent=5)
    for lbl, key, ref in [
        ("Sodium (NA)",   "Sodium (NA)",   "135–155 mmol/L"),
        ("Potassium (K)", "Potassium (K)", "3.5–5.5 mmol/L"),
        ("Chloride",      "Chloride",      "97–107 mg/dl"),
        ("S. Calcium",    "S. Calcium",    "8.7–11.0 mg/L"),
        ("S. Uric Acid",  "S. Uric Acid",  "M:3.5–7.2 / F:2.6–6.0"),
        ("S. Amylase",    "S. Amylase",    "<90 IU/L"),
        ("S. Lipase",     "S. Lipase",     "<30 IU/L"),
    ]:
        pdf.test_row(lbl, d.get(key,""), ref, indent=5, dash_x=dx_el)
    pdf.sub_section("Cardiac Profile")
    ca_labels = ["CK — MB","Troponin 'I'"]
    dx_ca = pdf.dash_col(ca_labels, indent=5)
    pdf.test_row("CK — MB",      d.get("CK-MB",""),      "0–24 U/L", indent=5, dash_x=dx_ca)
    pdf.test_row("Troponin 'I'", d.get("Troponin I",""), "",         indent=5, dash_x=dx_ca)


# ── Master test registry — (key, label, ref, sub_section) ───────────────────
# sub_section is what prints as the header above each group of tests
TEST_REGISTRY = [
    # key                   label                  ref                        sub_section
    ("Hb",            "Hb",            "gm/dl (12–18)",          "Haematology"),
    ("TLC",           "TLC",           "(4000–11000) /cumm",     "Haematology"),
    ("ESR",           "ESR",           "<20 mm / 1st hour",      "Haematology"),
    ("Neutrophils",   "Neutrophils",   "%(40–70)",               "Haematology|DLC"),
    ("Lymphocyte",    "Lymphocyte",    "%(20–40)",               "Haematology|DLC"),
    ("Eosinophils",   "Eosinophils",   "%(01–06)",               "Haematology|DLC"),
    ("Monocytes",     "Monocytes",     "%(02–10)",               "Haematology|DLC"),
    ("Basophils",     "Basophils",     "%(0–1)",                 "Haematology|DLC"),
    ("Platelets",     "Platelets",     "(1.5–04) lakh",          "Haematology|DLC"),
    ("ANC",           "ANC",           "(1800–7000) /cumm",      "Haematology|DLC"),
    ("AEC",           "AEC",           "(40–450) /cumm",         "Haematology|DLC"),
    ("TRBC",          "TRBC",          "(4.2–6.1 millions/McL)", "Haematology|DLC"),
    ("PCV",           "PCV",           "%(40–55)",               "Haematology|DLC"),
    ("Bleeding Time", "Bleeding Time", "(1–5 mins)",             "Haematology|DLC"),
    ("Clotting Time", "Clotting Time", "(4–9 mins)",             "Haematology|DLC"),
    ("PT",            "PT",            "(11–16 seconds)",        "Haematology|DLC"),
    ("INR",           "INR",           "(0.64–1.17)",            "Haematology|DLC"),
    ("Blood Group",   "Blood Group",   "",                       "Haematology|DLC"),
    ("Pro/Alb",            "Pro / Alb",          "",            "Urine"),
    ("Sugar",              "Sugar",               "",            "Urine"),
    ("Pus",                "Pus",                 "/hpf",        "Urine|Microscopic Examination"),
    ("Epi",                "Epi",                 "/hpf",        "Urine|Microscopic Examination"),
    ("RBC (Urine)",        "RBC",                 "/hpf",        "Urine|Microscopic Examination"),
    ("Crystal",            "Crystal",             "/hpf",        "Urine|Microscopic Examination"),
    ("Cast",               "Cast",                "/hpf",        "Urine|Microscopic Examination"),
    ("Others (Urine)",     "Others",              "/hpf",        "Urine|Microscopic Examination"),
    ("Pregnancy Test",     "Pregnancy Test",      "+ve / -ve",   "Special Urine Tests"),
    ("24hrs Urine Protein","24hrs Urine Protein", "",            "Special Urine Tests"),
    ("24hrs Urine Output", "24hrs Urine Output",  "",            "Special Urine Tests"),
    ("HEV-IgM",            "HEV-IgM",             "",            "Special Urine Tests"),
    ("HBeAg",              "HBeAg",               "",            "Special Urine Tests"),
    ("HAV-IgM",            "HAV-IgM",             "",            "Special Urine Tests"),
    ("Urine AFB",          "Urine AFB",           "",            "Special Urine Tests"),
    ("Sputum AFB",         "Sputum AFB",          "",            "Special Urine Tests"),
    ("Stool Occult Blood", "Stool Occult Blood",  "",            "Stool"),
    ("Stool RE",           "Stool RE",            "",            "Stool"),
    ("Gross",              "Gross",               "",            "Stool"),
    ("H. Pylori",          "H. Pylori",           "",            "Serology & Parasitology"),
    ("HBsAg",              "HBsAg",               "",            "Serology & Parasitology"),
    ("ANTI HCV",           "ANTI HCV",            "",            "Serology & Parasitology"),
    ("Retro",              "Retro",               "",            "Serology & Parasitology"),
    ("Syphilis",           "Syphilis",            "",            "Serology & Parasitology"),
    ("BI.MP (Slide)",      "BI.MP (Slide)",       "",            "Serology & Parasitology"),
    ("BI.MP (ICT)",        "BI.MP (ICT)",         "",            "Serology & Parasitology"),
    ("Scrub Typhus",       "Scrub Typhus",        "",            "Serology & Parasitology"),
    ("Influenza",          "Influenza",           "",            "Serology & Parasitology"),
    ("Typhi IgG IgM",      "Typhi IgG IgM",      "",            "Serology & Parasitology"),
    ("Dengue NslAg",       "NslAg",               "",            "Serology & Parasitology|Dengue"),
    ("Dengue IgM/IgG",     "IgM / IgG",           "",            "Serology & Parasitology|Dengue"),
    ("S. Typhi O",         "S. Typhi 'O'",        "",            "Widal"),
    ("S. Typhi H",         "S. Typhi 'H'",        "",            "Widal"),
    ("S. Paratyphi AH",    "S. Paratyphi AH",     "",            "Widal"),
    ("S. Paratyphi BH",    "S. Paratyphi BH",     "",            "Widal"),
    ("OXK",                "OXK",                 "",            "Well Felix"),
    ("OX2",                "OX2",                 "",            "Well Felix"),
    ("OX19",               "OX19",                "",            "Well Felix"),
    ("RA/RF",              "RA / RF",             "<20 IU/ml",   "Quantitative Tests"),
    ("ASO Adult",          "ASO Adult",           "<200 IU/ml",  "Quantitative Tests"),
    ("ASO Children <5yrs", "ASO Child <5yr",      "100 IU/ml",   "Quantitative Tests"),
    ("CRP Adult",          "CRP Adult",           "<6 mg/L",     "Quantitative Tests"),
    ("CRP Infants & Children","CRP Infant",       "<2.8 mg/L",   "Quantitative Tests"),
    ("CRP Newborn <3 weeks","CRP Newborn",        "<4.1 mg/L",   "Quantitative Tests"),
    ("Fasting",       "Fasting",        "70–110 mg/dl",          "Blood Sugar"),
    ("PP",            "PP",             "<150 mg/dl",            "Blood Sugar"),
    ("RBS",           "RBS",            "70–150 mg/dl",          "Blood Sugar"),
    ("Urea",          "Urea",           "14–40 mg/dl",           "RFT / KFT"),
    ("Creatinine",    "Creatinine",     "0.2–1.4 mg/dl",         "RFT / KFT"),
    ("T. Bilirubin",  "T. Bilirubin",   "0.1–1.0 mg/dl",         "LFT"),
    ("D. Bilirubin",  "D. Bilirubin",   "0–0.5 mg/dl",           "LFT"),
    ("ID. Bilirubin", "ID. Bilirubin",  "0.1–0.7 mg/dl",         "LFT"),
    ("SGOT (AST)",    "SGOT (AST)",     "5–40 U/L",              "LFT"),
    ("SGPT (ALT)",    "SGPT (ALT)",     "5–45 U/L",              "LFT"),
    ("T. Protein",    "T. Protein",     "6–8 gm/dl",             "LFT"),
    ("Albumin",       "Albumin",        "3.2–5.5 gm/dl",         "LFT"),
    ("Globulin",      "Globulin",       "2.3–3.5 gm/dl",         "LFT"),
    ("Alka. Phos M",          "M",                   "53–128 U/L",  "LFT|Alka. Phos"),
    ("Alka. Phos F",          "F",                   "42–141 U/L",  "LFT|Alka. Phos"),
    ("Alka. Phos Children",   "Children (1–14 yrs)", "54–369 U/L",  "LFT|Alka. Phos"),
    ("T. Cholesterol","T. Cholesterol", "<200 mg/dl",            "Lipid Profile"),
    ("Triglyceride",  "Triglyceride",   "<160 mg/dl",            "Lipid Profile"),
    ("HDL",           "HDL",            "30–80 mg/dl",           "Lipid Profile"),
    ("LDL",           "LDL",            "<130 mg/dl",            "Lipid Profile"),
    ("VLDL",          "VLDL",           "7–30 mg/dl",            "Lipid Profile"),
    ("Sodium (NA)",   "Sodium (NA)",    "135–155 mmol/L",        "Serum Electrolytes"),
    ("Potassium (K)", "Potassium (K)",  "3.5–5.5 mmol/L",        "Serum Electrolytes"),
    ("Chloride",      "Chloride",       "97–107 mg/dl",          "Serum Electrolytes"),
    ("Ionized Calcium","Ionized Calcium", "1.15–1.33 mmol/L",      "Serum Electrolytes"),
    ("S. Calcium",    "S. Calcium",     "8.7–11.0 mg/L",         "Biochemistry"),
    ("S. Uric Acid",  "S. Uric Acid",   "M:3.5–7.2 / F:2.6–6.0","Biochemistry"),
    ("S. Amylase",    "S. Amylase",     "<90 IU/L",              "Biochemistry"),
    ("S. Lipase",     "S. Lipase",      "<30 IU/L",              "Biochemistry"),
    ("CK-MB",         "CK — MB",        "0–24 U/L",              "Cardiac Profile"),
    ("Troponin I",    "Troponin 'I'",   "",                      "Cardiac Profile"),
    # Thyroid
    ("TSH",    "Thyroid Stimulating Hormone",  ["New Born: 0.70–15.2", "6d–3mths: 0.72–11.0", "4–12mths: 0.73–8.35", "1–6yrs: 0.70–5.97", "7–11yrs: 0.60–4.84", "12–20yrs: 0.51–4.30", "Adult: 0.35–4.2", "(Unit: uIU/mL)"], "Thyroid Stimulating Hormone", "uIU/mL"),
    ("T3",     "T3",                           ["1.23–3.07 (nmol/l)"],                                                                                                                                                                "Thyroid Stimulating Hormone|T3 & T4", "nmol/l"),
    ("T4",     "T4",                           ["66–181 nmol/L", "(5.1–14.1 Ug/dL)"],                                                                                                                                                 "Thyroid Stimulating Hormone|T3 & T4", "nmol/L"),
    ("Free T3","Free T3",                      ["3.1–6.8 pmol/L"],                                                                                                                                                                    "Thyroid Stimulating Hormone|Free T3 & Free T4", "pmol/L"),
    ("Free T4","Free T4",                      ["12–22 pmol/L"],                                                                                                                                                                       "Thyroid Stimulating Hormone|Free T3 & Free T4", "pmol/L"),
    # Vit D
    ("Vit D",  "Vit D",                        ["Deficient: <20 ng/mL", "Insufficient: 20–30 ng/mL", "Sufficient: >30 ng/mL"],                                                                                                        "Vit D", "ng/mL"),
    # HBA1C
    ("HBA1C",  "HBA1C",                        ["Normal: <5.7%", "Prediabetes: 5.7–6.4%", "Diabetes: >6.5%"],                                                                                                                         "HBA1C", "%"),
]


def _start_page(pdf, all_labels, col_x=None):
    """Draw a fresh page. Returns (content_start_y, dx) for given col_x."""
    pdf.f(WHITE); pdf.rect(0, 0, PW, PH, "F")
    pdf._header()
    pdf._left_strip()
    pdf._info_bar()
    cy = pdf._patient()
    pdf.set_font("DJ", "", 8.5)
    x = col_x if col_x is not None else RC_X
    dx = x + RC_P + max(pdf.get_string_width(l) for l in all_labels) + 3
    return cy, dx

def generate_pdf(patient, sections, technician, output_path, section_key=None):
    all_data = {}
    for sec_data in sections.values():
        if sec_data:
            all_data.update(sec_data)

    # Parse Blood Group JSON into a display string with RH label
    import json as _json
    bg_raw = all_data.get("Blood Group", "")
    if bg_raw and bg_raw.startswith("{"):
        try:
            bg_data = _json.loads(bg_raw)
            bg_val = bg_data.get("bg", "") or ""
            rh_val = bg_data.get("rh", "") or ""
            if bg_val and rh_val:
                all_data["Blood Group"] = f"{bg_val}    RH: {rh_val}"
            elif bg_val:
                all_data["Blood Group"] = bg_val
            elif rh_val:
                all_data["Blood Group"] = f"RH: {rh_val}"
            else:
                all_data["Blood Group"] = ""
        except Exception:
            pass

    from collections import OrderedDict
    groups = OrderedDict()
    for entry in TEST_REGISTRY:
        key, label, ref, tag = entry[0], entry[1], entry[2], entry[3]
        val = all_data.get(key)
        if val is not None:
            if "|" in tag:
                section, sub = tag.split("|", 1)
            else:
                section, sub = tag, None
            group_key = (section, sub)
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append((label, val, ref))

    all_labels = [lbl for rows in groups.values() for lbl, _, _ in rows]
    if not all_labels:
        return output_path

    row_count   = sum(len(r) for r in groups.values())
    TWO_COL     = row_count > 12
    PAGE_BOTTOM = PH - 22

    pdf = LabReport(patient, technician)
    pdf.set_auto_page_break(False)
    pdf.add_page()

    if not TWO_COL:
        # ── Single column ──────────────────────────────────────────────────
        start_y, dx = _start_page(pdf, all_labels)
        pdf.set_xy(RC_X, start_y)

        last_section = None
        for (section, sub), rows in groups.items():
            if not rows:
                continue
            if section != last_section:
                if pdf.get_y() + 16 > PAGE_BOTTOM:
                    pdf.signature_line()
                    pdf.add_page()
                    start_y, dx = _start_page(pdf, all_labels)
                    pdf.set_xy(RC_X, start_y)
                pdf.section_title(section)
                last_section = section
            if sub:
                if pdf.get_y() + 12 > PAGE_BOTTOM:
                    pdf.signature_line()
                    pdf.add_page()
                    start_y, dx = _start_page(pdf, all_labels)
                    pdf.set_xy(RC_X, start_y)
                pdf.sub_section(sub)
            for label, value, ref in rows:
                row_h = len(ref) * 5.5 if isinstance(ref, list) else 7
                if pdf.get_y() + row_h > PAGE_BOTTOM:
                    pdf.signature_line()
                    pdf.add_page()
                    start_y, dx = _start_page(pdf, all_labels)
                    pdf.set_xy(RC_X, start_y)
                if isinstance(ref, list):
                    pdf.test_row_multiref(label, value, ref, dash_x=dx)
                else:
                    pdf.test_row(label, value, ref, dash_x=dx)

    else:
        # ── Two columns ────────────────────────────────────────────────────
        # Split groups at section boundary nearest the halfway point
        group_items = list(groups.items())
        half = row_count // 2
        counted, split_idx = 0, len(group_items)
        for i, (_, rows) in enumerate(group_items):
            counted += len(rows)
            if counted >= half:
                split_idx = i + 1
                break

        left_groups  = group_items[:split_idx]
        right_groups = group_items[split_idx:]

        left_labels  = [lbl for (_, _), rows in left_groups  for lbl, _, _ in rows]
        right_labels = [lbl for (_, _), rows in right_groups for lbl, _, _ in rows]

        def col_dx(labels, x_off):
            if not labels: return x_off + RC_P + 20
            pdf.set_font("DJ", "", 9.5)
            max_lbl_w = max(pdf.get_string_width(l) for l in labels)
            # Cap dash_x so it never exceeds 45% of col width from col start
            max_allowed = TC_W * 0.45
            return x_off + RC_P + min(max_lbl_w, max_allowed) + 4

        # ── Two-col page-aware renderer ───────────────────────────────────────
        # Strategy: render both cols in passes per page.
        # Each pass fills both cols on the same page, then a new page is added.

        def measure_group(grp_list):
            """Return list of (section, sub, rows) with row heights pre-computed."""
            out = []
            for (section, sub), rows in grp_list:
                if rows:
                    out.append((section, sub, rows))
            return out

        def render_pass(groups_queue, x_off, col_w, dx, y, page_bottom):
            """
            Render as many groups as fit from groups_queue into one column
            starting at y. Mutates groups_queue (pops completed groups).
            Returns final y. If a group is partially rendered, the remainder
            stays at the front of groups_queue.
            """
            last_sec = None
            while groups_queue:
                section, sub, rows = groups_queue[0]
                # Section title
                if section != last_sec:
                    if y + 16 > page_bottom:
                        return y   # no room — stop this pass
                    pdf.set_xy(x_off, y)
                    pdf.section_title(section, x=x_off, w=col_w)
                    y = pdf.get_y()
                    last_sec = section
                # Sub-section
                if sub:
                    if y + 10 > page_bottom:
                        return y
                    pdf.set_xy(x_off, y)
                    pdf.sub_section(sub, x=x_off, w=col_w)
                    y = pdf.get_y()
                # Rows — render one at a time, leave remainder if overflow
                remaining = []
                for ri, (label, value, ref) in enumerate(rows):
                    row_h = len(ref) * 5.5 if isinstance(ref, list) else 7
                    if y + row_h > page_bottom:
                        remaining = rows[ri:]
                        break
                    pdf.set_xy(x_off, y)
                    if isinstance(ref, list):
                        pdf.test_row_multiref(label, value, ref, dash_x=dx, x=x_off, col_w=col_w)
                    else:
                        pdf.test_row(label, value, ref, dash_x=dx, x=x_off, col_w=col_w)
                    y = pdf.get_y()

                if remaining:
                    # Replace front of queue with remainder (same section/sub)
                    groups_queue[0] = (section, sub, remaining)
                    return y   # column full
                else:
                    groups_queue.pop(0)   # group done
            return y

        # Build mutable queues
        left_q  = [(s, b, list(r)) for s, b, r in measure_group(left_groups)]
        right_q = [(s, b, list(r)) for s, b, r in measure_group(right_groups)]

        # First page
        start_y, _ = _start_page(pdf, all_labels)
        dx_l = col_dx(left_labels,  TC_X_L)
        dx_r = col_dx(right_labels, TC_X_R)

        # Page 1 — two columns
        render_pass(left_q,  TC_X_L, TC_W, dx_l, start_y, PAGE_BOTTOM)
        render_pass(right_q, TC_X_R, TC_W, dx_r, start_y, PAGE_BOTTOM)

        # Overflow pages — single column (cleaner, no cramping)
        if left_q or right_q:
            # Merge remaining left + right back into ordered single queue
            overflow_q = left_q + right_q
            while overflow_q:
                pdf.signature_line()
                pdf.add_page()
                start_y, dx_single = _start_page(pdf, all_labels)
                pdf.set_xy(RC_X, start_y)
                while overflow_q:
                    section, sub, rows = overflow_q[0]
                    if pdf.get_y() + 16 > PAGE_BOTTOM:
                        break
                    pdf.section_title(section)
                    if sub:
                        if pdf.get_y() + 10 > PAGE_BOTTOM:
                            break
                        pdf.sub_section(sub)
                    remaining = []
                    for ri, (label, value, ref) in enumerate(rows):
                        row_h = len(ref) * 5.5 if isinstance(ref, list) else 7
                        if pdf.get_y() + row_h > PAGE_BOTTOM:
                            remaining = rows[ri:]
                            break
                        pdf.set_xy(RC_X, pdf.get_y())
                        if isinstance(ref, list):
                            pdf.test_row_multiref(label, value, ref, dash_x=dx_single)
                        else:
                            pdf.test_row(label, value, ref, dash_x=dx_single)
                    if remaining:
                        overflow_q[0] = (section, sub, remaining)
                        break
                    else:
                        overflow_q.pop(0)

    pdf.signature_line()
    pdf.output(output_path)
    return output_path