"""Builds the "It's Not That Nothing Works" PDF (the guide for the Doubt result).

Run:  python make_doubt_pdf.py
Needs: reportlab, pillow. Fonts and the clock photo live next to this file.
Output goes to ../web/downloads/. Edit the TEXT section to change the words.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Flowable, Image, KeepTogether, PageBreak)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, '..', 'downloads'))
OUT = os.path.join(OUT_DIR, 'its-not-that-nothing-works.pdf')
PHOTO = os.path.join(HERE, 'images', 'clock.png')

# ---- brand (same values as the site) ----
OBSIDIAN = HexColor('#0a0908')
GOLD = HexColor('#c9a96e')
GOLD_LIGHT = HexColor('#e2c98a')
GOLD_DIM = HexColor('#8a6e3e')
CREAM = HexColor('#f0e8d8')
BODY = HexColor('#c7c0b3')
HAIR = HexColor('#3a3224')
TEAL = HexColor('#5aa9a3')       # verdigris: the colour that offsets the gold
TEAL_DIM = HexColor('#2a5a5c')
TEAL_DEEP = HexColor('#0c2325')
TEAL_SOFT = HexColor('#cfe8e5')

F = os.path.join(HERE, 'fonts')
for name, f in [('Corm-Light', 'CormorantGaramond-Light.ttf'), ('Corm', 'CormorantGaramond-Regular.ttf'),
                ('Corm-LightItalic', 'CormorantGaramond-LightItalic.ttf'), ('Corm-Italic', 'CormorantGaramond-Italic.ttf'),
                ('Cinzel', 'Cinzel-Regular.ttf'), ('Cinzel-Bold', 'Cinzel-SemiBold.ttf'),
                ('Jost-Light', 'Jost-Light.ttf'), ('Jost', 'Jost-Regular.ttf')]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(F, f)))
pdfmetrics.registerFontFamily('Corm-Light', normal='Corm-Light', italic='Corm-LightItalic', bold='Corm', boldItalic='Corm-Italic')
pdfmetrics.registerFontFamily('Jost-Light', normal='Jost-Light', bold='Jost', italic='Jost-Light', boldItalic='Jost')

from pdf_extras import HeroImage, ClosingCanvas, GoldBand, make_cover, prepend_cover
LOGO = os.path.join(HERE, 'images', 'logo-gold.png')

PAGE_W, PAGE_H = letter
MARGIN_X = 62
CONTENT_W = PAGE_W - 2 * MARGIN_X

# ---- styles ----
title = ParagraphStyle('title', fontName='Corm-Light', fontSize=38, leading=42, textColor=CREAM, spaceAfter=8)
subtitle = ParagraphStyle('subtitle', fontName='Jost-Light', fontSize=12.5, leading=18, textColor=HexColor('#a8a193'), spaceAfter=26)
inner = ParagraphStyle('inner', fontName='Jost', fontSize=14.5, leading=22, textColor=CREAM, spaceAfter=4)
mine = ParagraphStyle('mine', fontName='Jost', fontSize=11, leading=17, textColor=HexColor('#d9d2c3'), leftIndent=18, bulletIndent=0, spaceAfter=4, bulletFontName='Jost-Light', bulletFontSize=10, bulletColor=GOLD_DIM)
lede = ParagraphStyle('lede', fontName='Jost', fontSize=12.5, leading=19, textColor=CREAM, spaceAfter=10)
body = ParagraphStyle('body', fontName='Jost-Light', fontSize=10.5, leading=17, textColor=BODY, spaceAfter=9)
bullet = ParagraphStyle('bullet', parent=body, leftIndent=16, bulletIndent=0, spaceAfter=5, bulletFontName='Jost-Light',
                        bulletFontSize=10.5, bulletColor=GOLD_DIM)
step = ParagraphStyle('step', parent=body, leftIndent=20, bulletIndent=0, spaceAfter=5, bulletFontName='Cinzel',
                      bulletFontSize=9.5, bulletColor=GOLD)
quote = ParagraphStyle('quote', fontName='Jost', fontSize=11.5, leading=17, textColor=TEAL_SOFT, spaceBefore=10, spaceAfter=3)
msg = ParagraphStyle('msg', fontName='Corm-Italic', fontSize=24, leading=30, textColor=TEAL)
sig = ParagraphStyle('sig', fontName='Cinzel', fontSize=9, leading=12, textColor=GOLD, spaceBefore=8)
cell = ParagraphStyle('cell', fontName='Jost-Light', fontSize=9.5, leading=14, textColor=BODY)
cellq = ParagraphStyle('cellq', fontName='Corm-LightItalic', fontSize=13, leading=16, textColor=CREAM)
note = ParagraphStyle('note', fontName='Jost-Light', fontSize=10.5, leading=16, textColor=HexColor('#a8a193'), spaceBefore=5, spaceAfter=4)
link = ParagraphStyle('link', fontName='Jost', fontSize=13, leading=19, textColor=GOLD_LIGHT)


class Spaced(Flowable):
    """Small caps style label with letter spacing (Paragraph can't do this)."""
    def __init__(self, text, font='Cinzel', size=9, color=TEAL, space=2.2, before=18, after=8, rule=False):
        super().__init__()
        self.text, self.font, self.size, self.color, self.space = text.upper(), font, size, color, space
        self.before, self.after, self.rule = before, after, rule

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, self.size + self.before + self.after + (6 if self.rule else 0)

    def draw(self):
        c = self.canv
        t = c.beginText()
        t.setFont(self.font, self.size)
        t.setFillColor(self.color)
        t.setCharSpace(self.space)
        t.setTextOrigin(0, self.after + (6 if self.rule else 0))
        t.textOut(self.text)
        c.drawText(t)
        if self.rule:
            c.setStrokeColor(TEAL_DIM)
            c.setLineWidth(0.6)
            c.line(0, self.after - 2, self.aw, self.after - 2)


def P(text, style=body):
    return Paragraph(text, style)


def callout(text):
    """The one message that is from Tim: set apart by size, script and teal colour alone. No dash, panel, bar or attribution."""
    return KeepTogether([Spacer(1, 18), Paragraph(text, msg), Spacer(1, 14)])


def bullets(items):
    return [Paragraph(t, bullet, bulletText='—') for t in items]


def steps(items):
    return [Paragraph(t, step, bulletText=str(i + 1)) for i, t in enumerate(items)]


# ------------------------------------------------------------------ TEXT
TITLE = 'It’s Not That <font color="#e2c98a"><i>Nothing Works</i></font>'
SUBTITLE = 'For when you’re not sure it’s going to work'
INNER = [
    '“I’ve tried everything, so why hasn’t it happened yet?”',
    '“What if it all just isn’t true?”',
    '“Am I missing some secret everyone else knows?”',
    '“I don’t love it. It could be a little bit better.”',
]
OPENING = 'That makes sense, and nothing is wrong with you.'

MORE = [
    '“Is it my blocks? My trauma? My resistance?”',
    '“The more I understand, the more I question.”',
    '“I’ll try one more technique, one more teacher, one more course.”',
    '“I already know this. What the hell.”',
    '“It works sometimes, then it stops working and I don’t know why.”',
    '“I find the feeling in meditation and lose it before lunch.”',
    '“I’m tired of trying the same things over and over again… And nothing seems to work.”',
]
ISNT = 'There’s more to this than just wanting it.'
WHY = [
    'Wondering whether it will work is a kind of fear. You’re not sure it will, so part of you braces for it to fail.',
    'And that comes from somewhere real. At some point in your past, something you tried didn’t work. Now you’re doing '
    'something today that’s meant to bring a result later, and that old moment speaks up about the future. Of course it does. '
    'Part of you is remembering.',
]
BRIDGE = [
    ('“What if it all just isn’t true?”',
     'That’s a fear that it won’t work. You’re not sure it will, so part of you expects it to fail.'),
    ('“I always plant a seed and after a few days I dig it up.”',
     'That’s the past speaking about the future. An old moment where something didn’t work is shaping what you expect from today.'),
    ('“Something’s not right. I just need to fix it.”',
     'That’s feedback from Source. When something doesn’t feel right yet, it lets you tune what you’re doing to get better results.'),
]
SOURCE = 'Source is the larger field of intelligence that everything comes from, and that you’re part of.'
TODO = [
    '<font name="Jost">Notice the thought</font> when it comes up. Don’t argue with it.',
    '<font name="Jost">Breathe into right now.</font> The past is over and the future hasn’t happened. This moment is where you work from.',
    '<font name="Jost">Remember that what didn’t work before helped you become successful.</font> It’s part of how you got here.',
    '<font name="Jost">Treat what happens as feedback.</font> If today doesn’t go the way you hoped, it brings you feedback from Source, and you tune from there.',
    '<font name="Jost">Ask yourself:</font> “What if I’m not doing this wrong at all?”',
]
NEXT = '[Your next step goes here]'
# cover (page 1) and the quote band at the top of the next page; the cover photo is the same stones image on all three guides
COVER_LINES = ('IT’S NOT THAT', 'NOTHING WORKS')
QUOTE = 'Every Cause has its Effect; every Effect has its Cause.'
CREDIT = 'The Kybalion'
COVER_PHOTO = os.path.join(HERE, 'images', 'stones.jpg')
# ------------------------------------------------------------------ /TEXT


def page_bg(canv, doc):
    canv.saveState()
    canv.setFillColor(OBSIDIAN)
    canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # header: the logo, centred, in gold for the dark page
    lw = 176
    canv.drawImage(LOGO, (PAGE_W - lw) / 2, PAGE_H - 54, width=lw, height=lw * 350 / 2440, mask='auto')
    # footer
    canv.setFont('Jost-Light', 8)
    canv.setFillColor(HexColor('#6f695d'))
    canv.drawString(MARGIN_X, 30, 'Everyday Alchemy · Resonance Architecture™')
    if doc.page > 1:                      # the cover carries the sigil in that corner, so no number there
        canv.drawRightString(PAGE_W - MARGIN_X, 30, str(doc.page + 1))
    canv.restoreState()


def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    doc = BaseDocTemplate(OUT, pagesize=letter, title='It’s Not That Nothing Works',
                          author='Everyday Alchemy', subject='Everyday Alchemy',
                          leftMargin=MARGIN_X, rightMargin=MARGIN_X, topMargin=70, bottomMargin=62)
    frame = Frame(MARGIN_X, 62, CONTENT_W, PAGE_H - 70 - 62, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='p', frames=[frame], onPage=page_bg)])

    s = []
    s += [Spacer(1, 18), GoldBand(QUOTE, CREDIT), Spacer(1, 26)] + [P(t, inner) for t in INNER] + [callout(OPENING)]

    # page 1 closes with the clock: the full width of the page, uncropped
    from PIL import Image as PILImage
    pw, ph = PILImage.open(PHOTO).size
    s += [Spacer(1, 10), HeroImage(PHOTO, CONTENT_W, CONTENT_W * ph / pw), PageBreak()]

    # page 2: their thoughts, then the rest
    s += [Spaced('The uncertainty', before=0, after=8)] + [Paragraph(t, mine, bulletText='\u2014') for t in MORE]

    s += [Spaced('Guess what?', before=26), P(ISNT)]

    why_text = [P(t) for t in WHY]
    s += [KeepTogether([Spaced('Why it makes sense', before=22)] + why_text)]

    # what they say, then what is behind it: plain pairs, no table, no labels
    pairs = [Spacer(1, 6)]
    for q, e in BRIDGE:
        pairs += [P(q, quote), P(e, body)]
    s += [KeepTogether(pairs + [P(SOURCE, note)])]

    s += [KeepTogether([Spaced('What to do', before=16)] + steps(TODO))]
    s += [KeepTogether([Spaced('Where to go next', before=14, after=4), P(NEXT, link)])]
    doc.build(s, canvasmaker=ClosingCanvas)
    cover = OUT + '.cover.pdf'
    make_cover(cover, COVER_LINES[0], COVER_LINES[1], SUBTITLE, COVER_PHOTO)
    prepend_cover(OUT, cover)
    os.remove(cover)
    print('wrote', OUT)


if __name__ == '__main__':
    build()
