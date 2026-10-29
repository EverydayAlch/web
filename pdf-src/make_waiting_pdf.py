"""Builds the "When It's Been Far Too Long" PDF (the guide for the Waiting result). FIRST DRAFT.

Run:  python make_waiting_pdf.py
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
OUT = os.path.join(OUT_DIR, 'its-been-far-too-long.pdf')
PHOTO = os.path.join(HERE, 'images', 'desert.jpg')  # this guide's own image (the clock belongs to the Doubt guide)

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
TITLE = 'It’s Been <font color="#e2c98a"><i>Far Too Long</i></font>'
SUBTITLE = '…and still nothing'
INNER = [
    '“I’m so tired and exhausted of all this.”',
    '“I just wanna get out of this cycle.”',
    '“How do I not be stuck anymore?”',
    '“So it’s like I either give up or don’t.”',
]
OPENING = 'That’s a lot, and nothing is wrong with you.'

MORE = [
    '“The weight of it all is too much.”',
    '“I’m stuck in this cycle and I don’t know what to do.”',
    '“My mind says give up but my heart says I can’t.”',
    '“I truly don’t want to give up.”',
    '“I’m just really torn.”',
]
ISNT = 'There’s more to it than you’ve been told.'
# held back (Tim's, not placed yet): 'The thing the gurus don’t tell you is that they talk about their successes, but they don’t talk about everything they do and everything they did that didn’t work. Not only is there more to the story, by the time they figure it out, they have forgotten how to talk to normal people.'
WHY = [
    '##Is it me?',
    'No, it’s not you. Every modern spiritual practice describes the mechanism in purely spiritualized terms — Raise your vibration, maintain the state, set your intention, allow, align. That spiritualized language makes it difficult to connect the dots between your inner world and the outer world. In other words, the spiritualized language makes it difficult to connect the consciousness work, the spiritual work, with watching things unfold in your physical reality.',
    '##Does this work work?',
    'Yes, it does work. It works when we do the consciousness work, the spiritual work, and we align our physical lives to reflect the being we define in that work, in physical reality. It works when we go and implement becoming that human in the real world.',
]
# quotes in italics are REAL short phrases from the two people who spiral most (Messenger export) plus Tim's own examples, no names; explanations are Tim's own email lines
BRIDGE = []
SOURCE = ''
TODO = [
    '<font name="Jost">Find a comfortable space to sit down.</font> Give yourself fifteen or thirty minutes.',
    '<font name="Jost">Get quiet.</font> Take a breath and bring yourself into the present moment.',
    '<font name="Jost">Ask yourself:</font> “What is it that hasn’t come yet?” Allow your mind to tune in to that.',
    '<font name="Jost">Then ask yourself one simple question:</font> “Why is this so important to me?” Just let the answer emerge. Whatever the answer is, it’s okay. Write it down on a piece of paper or in your notebook.',
    '<font name="Jost">If your body starts to tighten or tense,</font> take a breath and tell yourself that you’re just playing with an idea.',
    '<font name="Jost">Then ask yourself:</font> “What if I just don’t know what to do next?”',
]
NEXT = '[Your next step goes here]'
# cover (page 1) and the quote band at the top of the next page; the cover photo is the same stones image on all three guides
COVER_LINES = ('IT’S BEEN', 'FAR TOO LONG')
QUOTE = 'As above, so below.'
CREDIT = 'The Emerald Tablet'
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
    doc = BaseDocTemplate(OUT, pagesize=letter, title='It’s Been Far Too Long',
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
    s += [Spaced('The endless nothing', before=0, after=8)] + [Paragraph(t, mine, bulletText='\u2014') for t in MORE]

    s += [Spaced('Guess what?', before=16), P(ISNT)]

    why_text = [P(t[2:], qa) if t.startswith('##') else P(t) for t in WHY]
    s += [KeepTogether([Spaced('Why it makes sense', before=14)] + why_text)]

    # what they say, then what is behind it: plain pairs, no table, no labels
    pairs = [Spacer(1, 6)]
    for q, e in BRIDGE:
        pairs += [P(q, quote), P(e, body)]
    s += [KeepTogether(pairs + ([P(SOURCE, note)] if SOURCE else []))]

    s += [KeepTogether([Spaced('What to do', before=10)] + steps(TODO))]
    s += [KeepTogether([Spaced('Not sure where to go next? Check out the link below.', before=14, after=4), P(NEXT, link)])]
    doc.build(s, canvasmaker=ClosingCanvas)
    cover = OUT + '.cover.pdf'
    make_cover(cover, COVER_LINES[0], COVER_LINES[1], SUBTITLE, COVER_PHOTO)
    prepend_cover(OUT, cover)
    os.remove(cover)
    print('wrote', OUT)


if __name__ == '__main__':
    build()
