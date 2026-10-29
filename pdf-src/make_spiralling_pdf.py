"""Builds the "Why Your Mind Won't Slow Down" PDF (the guide for the Spiralling result).

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
OUT = os.path.join(OUT_DIR, 'why-your-mind-wont-slow-down.pdf')
PHOTO = os.path.join(HERE, 'images', 'whirlpool-wide.jpg')  # this guide's own image (the clock belongs to the Doubt guide)

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
title = ParagraphStyle('title', fontName='Corm-Light', fontSize=33, leading=38, textColor=CREAM, spaceAfter=8)
subtitle = ParagraphStyle('subtitle', fontName='Jost-Light', fontSize=12.5, leading=18, textColor=HexColor('#a8a193'), spaceAfter=26)
inner = ParagraphStyle('inner', fontName='Jost', fontSize=14.5, leading=22, textColor=CREAM, spaceAfter=4)
lede = ParagraphStyle('lede', fontName='Jost', fontSize=12.5, leading=19, textColor=CREAM, spaceAfter=10)
body = ParagraphStyle('body', fontName='Jost-Light', fontSize=10.5, leading=17, textColor=BODY, spaceAfter=9)
bullet = ParagraphStyle('bullet', parent=body, leftIndent=16, bulletIndent=0, spaceAfter=5, bulletFontName='Jost-Light',
                        bulletFontSize=10.5, bulletColor=GOLD_DIM)
step = ParagraphStyle('step', parent=body, leftIndent=20, bulletIndent=0, spaceAfter=5, bulletFontName='Cinzel',
                      bulletFontSize=9.5, bulletColor=GOLD)
quote = ParagraphStyle('quote', fontName='Jost', fontSize=11.5, leading=17, textColor=TEAL_SOFT, spaceBefore=10, spaceAfter=3)
mine = ParagraphStyle('mine', fontName='Jost', fontSize=11, leading=17, textColor=HexColor('#d9d2c3'), leftIndent=18, bulletIndent=0, spaceAfter=4, bulletFontName='Jost-Light', bulletFontSize=10, bulletColor=GOLD_DIM)
msg = ParagraphStyle('msg', fontName='Corm-Italic', fontSize=24, leading=30, textColor=TEAL)
sig = ParagraphStyle('sig', fontName='Cinzel', fontSize=9, leading=12, textColor=GOLD, spaceBefore=8)
qa = ParagraphStyle('qa', fontName='Jost', fontSize=12, leading=17, textColor=CREAM, spaceBefore=8, spaceAfter=2)
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
TITLE = 'Why Your Mind Won’t <font color="#e2c98a"><i>Slow Down</i></font>'
SUBTITLE = 'For when your thoughts won’t stop spinning'
INNER = [
    '“If I’m doing all the work, why is this still happening?”',
    '“It’s never gonna happen.”',
    '“Why? Why me?”',
    '“I cannot get out of my head today.”',
    '“I’m scared my fears and thoughts are going to ruin it.”',
]
OPENING = 'That’s exhausting, and nothing is wrong with you.'

MORE = [
    '“I overthink everything.”',
    '“I’m spiraling again.”',
    '“I spend hours spiraling.”',
    '“I’m just too much in my head.”',
    '“My brain doesn’t stop.”',
    '“I go straight to panic.”',
    '“I’m driving myself crazy.”',
]
ISNT = 'There’s more to this than just wanting it.'
WHY = [
    'When thoughts loop, nothing is broken. You are simply experiencing how an electromagnetic system operates when it runs hot.',
    '##Is it me?',
    'No. A single thought is electric and triggers a physical, magnetic reaction in the body—tightness, panic, or adrenaline. Because that physical feeling is magnetic, it naturally pulls in more thoughts that match its exact frequency. You aren’t failing; your system is simply reacting to its own feedback loop.',
    '##Does this work work?',
    'Yes, but not by using the mind to fix the mind. Trying to think your way out of a thought loop only adds more electricity to the circuit. This work changes the dynamic entirely: instead of trying to control or stop the thoughts, you shift your attention to the neutral observer. The moment you step back and observe the loop without engaging it, the electrical charge drops, and the loop naturally dissolves.',
]
# quotes in italics are REAL short phrases from the two people who spiral most (Messenger export) plus Tim's own examples, no names; explanations are Tim's own email lines
BRIDGE = []
SOURCE = ''
TODO = [
    '<font name="Jost">Tonight, write down the thought that loops the most.</font>',
    '<font name="Jost">Don’t fix it or argue with it.</font>',
    '<font name="Jost">Step back and look at it on the page.</font>',
    '<font name="Jost">Ask yourself:</font> “What if I don’t have to solve this right now?”',
]
NEXT = '[Your next step goes here]'
# cover (page 1) and the quote band at the top of the next page; the cover photo is the same stones image on all three guides
COVER_LINES = ('WHY YOUR MIND', 'WON’T SLOW DOWN')
QUOTE = 'Nothing rests; everything moves; everything vibrates.'
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
    doc = BaseDocTemplate(OUT, pagesize=letter, title='Why Your Mind Won’t Slow Down',
                          author='Everyday Alchemy', subject='Everyday Alchemy',
                          leftMargin=MARGIN_X, rightMargin=MARGIN_X, topMargin=70, bottomMargin=62)
    frame = Frame(MARGIN_X, 62, CONTENT_W, PAGE_H - 70 - 62, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='p', frames=[frame], onPage=page_bg)])

    s = []
    s += [Spacer(1, 18), GoldBand(QUOTE, CREDIT), Spacer(1, 26)] + [P(t, inner) for t in INNER] + [callout(OPENING)]

    # page 1 closes with the whirlpool: the full width of the page, uncropped
    from PIL import Image as PILImage
    pw, ph = PILImage.open(PHOTO).size
    s += [Spacer(1, 10), HeroImage(PHOTO, CONTENT_W, CONTENT_W * ph / pw), PageBreak()]

    # page 2: their thoughts, then the rest
    s += [Spaced('The swirling thoughts', before=0, after=8)] + [Paragraph(t, mine, bulletText='\u2014') for t in MORE]

    s += [Spaced('Guess what?', before=16), P(ISNT)]

    why_text = [P(t[2:], qa) if t.startswith('##') else P(t) for t in WHY]
    s += [KeepTogether([Spaced('Why it makes sense', before=14)] + why_text)]

    # what they say, then what is behind it: plain pairs, no table, no labels
    pairs = [Spacer(1, 6)]
    for q, e in BRIDGE:
        pairs += [P(q, quote), P(e, body)]
    s += [KeepTogether(pairs + ([P(SOURCE, note)] if SOURCE else []))]

    s += [KeepTogether([Spaced('What to do', before=10)] + steps(TODO))]
    s += [KeepTogether([Spaced('Where to go next', before=14, after=4), P(NEXT, link)])]
    doc.build(s, canvasmaker=ClosingCanvas)
    cover = OUT + '.cover.pdf'
    make_cover(cover, COVER_LINES[0], COVER_LINES[1], SUBTITLE, COVER_PHOTO)
    prepend_cover(OUT, cover)
    os.remove(cover)
    print('wrote', OUT)


if __name__ == '__main__':
    build()
