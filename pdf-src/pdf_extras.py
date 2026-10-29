"""Shared bits for the guide PDFs: the merkaba sigil, the cover photo with the sigil
cut into its corner, and a canvas that adds the closing sigil on the last page.

The sigil geometry is the same as the hero sigil on the home page (index.html),
redrawn as vector lines in gold. Nothing in web/ is read or changed by this file.
"""
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import Flowable

GOLD = HexColor('#c9a96e')
OBSIDIAN = HexColor('#0a0908')
PAGE_W, PAGE_H = letter

# the sigil's own coordinate system (from the SVG): centre and outer radius
CX, CY, R = 901.9, 584.0, 349.0

# (alpha, [points...]) drawn as open polylines; a closed polygon repeats its first point
SHAPES = [
    (0.9, [(1003.5, 412), (901.9, 235.9), (601.6, 756.2), (1202.3, 756.2), (1102.9, 584.1)]),
    (0.9, [(1102.9, 584.1), (1003.5, 412)]),
    (0.9, [(800.3, 756.1), (901.1, 930.8), (901.9, 932.2), (1003.5, 756.1)]),
    (0.9, [(800.3, 412), (601.6, 412), (700.9, 584.1)]),
    (0.9, [(1102.9, 584.1), (1202.3, 412), (1003.5, 412)]),
    (0.75, [(901.5, 756.2), (1051.3, 494.1), (751.7, 494.1), (901.5, 756.2)]),
    (0.75, [(601.6, 412), (901.5, 575.4)]),
    (0.75, [(901.9, 575.4), (1202.3, 412)]),
    (0.75, [(901.9, 575.4), (901.1, 932.2)]),
]


def draw_sigil(c, cx, cy, r, filled_bg=False, ring=0.7, circles=True):
    """Draw the merkaba sigil centred at (cx, cy) with outer radius r (points)."""
    s = r / R
    lw = max(0.45, 3 * s * 1.5)

    def P(x, y):
        return cx + (x - CX) * s, cy - (y - CY) * s

    c.saveState()
    if filled_bg:
        c.setFillColor(OBSIDIAN)
        c.circle(cx, cy, r, stroke=0, fill=1)
    clip = c.beginPath()
    clip.circle(cx, cy, r)
    c.clipPath(clip, stroke=0, fill=0)
    c.setStrokeColor(GOLD)
    c.setLineJoin(1)
    c.setLineCap(1)
    c.setLineWidth(lw)
    for rad, a in ((270, 0.4), (150, 0.3)):                      # the two inner rings
        if not circles:
            break
        c.setStrokeAlpha(a)
        c.circle(cx, cy, rad * s, stroke=1, fill=0)
    for a, pts in SHAPES:
        c.setStrokeAlpha(a)
        p = c.beginPath()
        x0, y0 = P(*pts[0])
        p.moveTo(x0, y0)
        for x, y in pts[1:]:
            p.lineTo(*P(x, y))
        c.drawPath(p, stroke=1, fill=0)
    c.setFillColor(GOLD)                                         # the centre dot
    c.setFillAlpha(0.9)
    dx, dy = P(901.9, 575.4)
    c.circle(dx, dy, max(0.9, 10 * s), stroke=0, fill=1)
    c.restoreState()
    if not circles:
        return
    c.saveState()                                                # the outer ring, drawn last and clean
    c.setStrokeColor(GOLD)
    c.setStrokeAlpha(ring)
    c.setLineWidth(max(0.6, 4 * s * 1.5))
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.restoreState()


class HeroImage(Flowable):
    """The cover photo, with the sigil on a black disc cut into its bottom-right corner (like the home page)."""

    def __init__(self, path, width, height, sigil_r=31, inset=30, pad=10):
        super().__init__()
        self.path, self.width, self.height = path, width, height
        self.sigil_r, self.inset, self.pad = sigil_r, inset, pad

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.drawImage(self.path, 0, 0, self.width, self.height)
        # centred exactly on the photo's bottom-right corner: the photo's right edge runs down the sigil's
        # vertical axis (through its top point) and the bottom edge runs across its middle
        cx, cy = self.width, 0
        # a solid black disc, larger than the sigil, so it reads as cut out of the photo with space around it
        c.saveState()
        c.setFillColor(OBSIDIAN)
        c.circle(cx, cy, self.sigil_r + self.pad, stroke=0, fill=1)
        c.restoreState()
        draw_sigil(c, cx, cy, self.sigil_r, filled_bg=False, ring=0.85, circles=False)


class ClosingCanvas(rl_canvas.Canvas):
    """Adds the merkaba, centred in the footer, on the LAST page only: the closer."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        n = len(self._saved)
        for i, state in enumerate(self._saved):
            self.__dict__.update(state)
            if i == n - 1:
                draw_sigil(self, PAGE_W / 2, 44, 14, ring=0.6, circles=False)
            super().showPage()
        super().save()


# ---------------------------------------------------------------- cover + quote band (all three guides)
import os
import tempfile
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

_HERE = os.path.dirname(os.path.abspath(__file__))
for _n, _f in [('Aboreto', 'Aboreto-Regular.ttf'), ('CantataOne', 'CantataOne-Regular.ttf')]:
    pdfmetrics.registerFont(TTFont(_n, os.path.join(_HERE, 'fonts', _f)))


class GoldBand(Flowable):
    """The quote band: full content width, fades from black (top) to gold (solid by 66% of the way down), black lettering."""

    def __init__(self, text, credit, height=84, stop=0.66):
        super().__init__()
        self.text, self.credit, self.h, self.stop = text, credit, height, stop

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        p = c.beginPath()
        p.rect(0, 0, self.aw, self.h)
        c.clipPath(p, stroke=0, fill=0)
        c.linearGradient(0, self.h, 0, 0, (OBSIDIAN, GOLD), (0, self.stop))
        c.restoreState()
        size = 26
        while pdfmetrics.stringWidth(self.text, 'Corm-Italic', size) > self.aw - 40 and size > 14:
            size -= 1
        c.setFillColor(OBSIDIAN)
        c.setFont('Corm-Italic', size)
        c.drawCentredString(self.aw / 2, 27, self.text)
        t = c.beginText()
        t.setFont('Cinzel', 7.5)
        t.setCharSpace(2.2)
        w = c.stringWidth(self.credit.upper(), 'Cinzel', 7.5) + 2.2 * len(self.credit)
        t.setTextOrigin((self.aw - w) / 2, 11)
        t.textOut(self.credit.upper())
        c.drawText(t)


def make_cover(out_path, line1, line2, subtitle, photo, margin=62):
    """The dark cover: Aboreto title, Cantata One subtitle, the photo with the website's offset gold frame, gold logo."""
    from PIL import Image as PILImage
    W, H = letter
    c = rl_canvas.Canvas(out_path, pagesize=letter)
    c.setFillColor(OBSIDIAN)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    size = 44
    while max(pdfmetrics.stringWidth(line1, 'Aboreto', size), pdfmetrics.stringWidth(line2, 'Aboreto', size)) > W - 2 * margin and size > 24:
        size -= 1
    c.setFillColor(HexColor('#f0e8d8'))
    c.setFont('Aboreto', size)
    c.drawString(margin, H - 110, line1)
    c.drawString(margin, H - 110 - size * 1.14, line2)
    sub_y = H - 110 - size * 1.14 - 30
    c.setFillColor(HexColor('#a8a193'))
    c.setFont('CantataOne', 12)
    c.drawString(margin + 2, sub_y, subtitle)
    iw, ih = PILImage.open(photo).size
    pw = 420
    ph = pw * ih / iw
    x, y, off = margin, sub_y - 30 - ph, 16
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setStrokeAlpha(0.55)
    c.setLineWidth(0.8)
    c.rect(x + off, y - off, pw, ph, stroke=1, fill=0)           # the website's offset gold frame, behind the photo
    c.restoreState()
    c.drawImage(photo, x, y, pw, ph)
    lw = 230
    c.drawImage(os.path.join(_HERE, 'images', 'logo-gold.png'), (W - lw) / 2, 40, lw, lw * 350 / 2440, mask='auto')
    c.save()


def prepend_cover(pdf_path, cover_path):
    """Put the cover in front of the finished guide (needs pypdfium2)."""
    import pypdfium2 as pdfium
    cover = pdfium.PdfDocument(cover_path)
    with open(pdf_path, 'rb') as fh:
        body = pdfium.PdfDocument(fh.read())
    cover.import_pages(body)
    tmp = pdf_path + '.tmp'
    cover.save(tmp)
    cover.close()
    body.close()
    os.replace(tmp, pdf_path)
