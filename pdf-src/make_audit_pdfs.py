"""Builds the audit result PDFs (one per area; a person gets the PDF for their lowest-scoring area).

Same look as the three quiz PDFs: it reuses their styles, fonts, cover photo and quote band.
Only the words are new, and they live in the PDFS dict below, exactly as Tim gave them.

Run:  python make_audit_pdfs.py            (builds every PDF in PDFS)
      python make_audit_pdfs.py action     (builds just one)
"""
import os
import sys
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Spacer, KeepTogether, Paragraph, PageBreak, Flowable

# the shared look: styles, fonts, helpers and the page background come from the first guide's script
from make_waiting_pdf import (HERE, OUT_DIR, MARGIN_X, CONTENT_W, PAGE_W, PAGE_H, OBSIDIAN, GOLD, GOLD_DIM,
                              CREAM, LOGO, title, inner, mine, body, link, qa, quote, note, Spaced, P, callout, steps, page_bg)
from pdf_extras import GoldBand, ClosingCanvas, HeroImage, prepend_cover

BOOK_URL = 'https://api.leadconnectorhq.com/widget/booking/BdQTYPdQvcf1Z43zc0pg'   # Tim's calendar, same link as the results page button
BOOK_LABEL = 'Get in touch'
THUNDERHEAD = os.path.join(HERE, 'images', 'thunderhead.jpg')       # the Embodied Sovereignty image (Unsplash storm photo, trimmed)
CLOCK = os.path.join(HERE, 'images', 'clock.png')                  # the Doubt image
WHIRLPOOL = os.path.join(HERE, 'images', 'whirlpool-wide.jpg')   # the Spiralling image
DESERT = os.path.join(HERE, 'images', 'desert.jpg')         # the cracked desert, as on the old Waiting PDF
COVER_PHOTO = os.path.join(HERE, 'images', 'stones.jpg')   # the same cover photo on every PDF (Tim, 2026-11-04)

# ------------------------------------------------------------------ TEXT
PDFS = {
    'action': dict(
        file='aligned-action.pdf',
        image=DESERT,
        inner_label='The inner monologue',
        loops_label='The friction loops',
        name='Aligned Action',
        cover='IT’S BEEN\nFAR TOO LONG',
        subtitle='…and still nothing',
        quote='Choose your work… for all must labor.',
        credit='The Emerald Tablets',
        monologue=[
            '“I’m so tired and exhausted of all this.”',
            '“I just wanna get out of this cycle.”',
            '“How do I not be stuck anymore?”',
            '“So it’s like I either give up or don’t.”',
        ],
        callout='That’s exhausting and you’re not broken.',
        loops=[
            '“The weight of it all is too much.”',
            '“I’m stuck in this cycle and I don’t know what to do.”',
            '“My mind says give up but my heart says I can’t.”',
            '“I truly don’t want to give up.”',
            '“I’m just really torn.”',
        ],
        guess='You don’t have a motivation problem. You have an identity gap.',
        why=[
            'When you set a clear vision, your physical reality doesn’t shift instantly. There is a gap between who you are today and the version of you who comfortably owns that reality.',
            'When you look across that gap without knowing the exact steps, your brain sees an invisible threat. It floods your system with overwhelm to keep you safe from making a mistake. You aren’t lazy, and you aren’t self-sabotaging. Your system just shut down because it hit a wall of static.',
        ],
        shift='Aligned action isn’t about figuring out the whole 10-step plan. It’s about letting the version of you who already has the outcome tell you the very next micro-step. You don’t need the whole map; you just need the immediate move.',
        todo=[
            'Write down the one physical action you keep avoiding or overthinking.',
            'Don’t force yourself to do it, and don’t analyze why you haven’t.',
            'Look at it on the page from the center of your head.',
            'Ask yourself: “What is the smallest, single step I can take on this without needing to see the whole staircase?”',
        ],
    ),
    'core': dict(
        file='internal-integrity.pdf',
        name='Internal Integrity',
        image=WHIRLPOOL,
        cover='WHY YOUR MIND\nWON’T SLOW DOWN',
        subtitle='…your thoughts won’t stop spinning',
        quote='As above, so below.',
        credit='The Emerald Tablets',
        inner_label=None,
        monologue=[
            '“If I’m doing all the work, why is this still happening?”',
            '“It’s never gonna happen.”',
            '“Why? Why me?”',
            '“I cannot get out of my head today.”',
            '“I’m scared my fears and thoughts are going to ruin it.”',
        ],
        callout='That’s exhausting, and nothing is wrong with you.',
        loops_label='The swirling thoughts',
        loops=[
            '“I overthink everything.”',
            '“I’m spiraling again.”',
            '“I spend hours spiraling.”',
            '“I’m just too much in my head.”',
            '“My brain doesn’t stop.”',
            '“I go straight to panic.”',
            '“I’m driving myself crazy.”',
        ],
        guess='There’s more to this than just wanting it.',
        why=[
            'When thoughts loop, nothing is broken. You are simply experiencing how an electromagnetic system operates when it runs hot.',
            '##Is it me?',
            'No. A single thought is electric and triggers a physical, magnetic reaction in the body—tightness, panic, or adrenaline. Because that physical feeling is magnetic, it naturally pulls in more thoughts that match its exact frequency. You aren’t failing; your system is simply reacting to its own feedback loop.',
            '##Does this work work?',
            'Yes, but not by using the mind to fix the mind. Trying to think your way out of a thought loop only adds more electricity to the circuit. This work changes the dynamic entirely: instead of trying to control or stop the thoughts, you shift your attention to the neutral observer. The moment you step back and observe the loop without engaging it, the electrical charge drops, and the loop naturally dissolves.',
        ],
        shift=None,
        tight=True,                      # page 3 is full: trim the spacing a little so the two links can sit apart
        todo=[
            '<font name="Jost">Tonight, write down the thought that loops the most.</font>',
            '<font name="Jost">Don’t fix it or argue with it.</font>',
            '<font name="Jost">Step back and look at it on the page.</font>',
            '<font name="Jost">Ask yourself:</font> “What if I don’t have to solve this right now?”',
        ],
    ),
    'belief': dict(
        file='belief-alignment.pdf',
        name='Belief Alignment',
        image=CLOCK,
        cover='IT’S NOT THAT\nNOTHING WORKS',
        subtitle='…not sure it’s going to work',
        quote='Man is only what he believes.',
        credit='The Emerald Tablets',
        inner_label=None,
        monologue=[
            '“I’ve tried everything, so why hasn’t it happened yet?”',
            '“What if it all just isn’t true?”',
            '“Am I missing some secret everyone else knows?”',
            '“I don’t love it. It could be a little bit better.”',
        ],
        callout='That makes sense, and nothing is wrong with you.',
        loops_label='The uncertainty',
        loops=[
            '“Is it my blocks? My trauma? My resistance?”',
            '“The more I understand, the more I question.”',
            '“I’ll try one more technique, one more teacher, one more course.”',
            '“I already know this. What the hell.”',
            '“It works sometimes, then it stops working and I don’t know why.”',
            '“I find the feeling in meditation and lose it before lunch.”',
            '“I’m tired of trying the same things over and over again… And nothing seems to work.”',
        ],
        guess='There’s more to this than just wanting it.',
        why=[
            'Wondering whether it will work is a kind of fear. You’re not sure it will, so part of you braces for it to fail.',
            'And that comes from somewhere real. At some point in your past, something you tried didn’t work. Now you’re doing something today that’s meant to bring a result later, and that old moment speaks up about the future. Of course it does. Part of you is remembering.',
        ],
        bridge=[
            ('“What if it all just isn’t true?”',
             'That’s a fear that it won’t work. You’re not sure it will, so part of you expects it to fail.'),
            ('“I always plant a seed and after a few days I dig it up.”',
             'That’s the past speaking about the future. An old moment where something didn’t work is shaping what you expect from today.'),
            ('“Something’s not right. I just need to fix it.”',
             'That’s feedback from Source. When something doesn’t feel right yet, it lets you tune what you’re doing to get better results.'),
        ],
        source='Source is the larger field of intelligence that everything comes from, and that you’re part of.',
        shift=None,
        tight=True,
        todo=[
            '<font name="Jost">Notice the thought</font> when it comes up. Don’t argue with it.',
            '<font name="Jost">Breathe into right now.</font> The past is over and the future hasn’t happened. This moment is where you work from.',
            '<font name="Jost">Remember that what didn’t work before helped you become successful.</font> It’s part of how you got here.',
            '<font name="Jost">Treat what happens as feedback.</font> If today doesn’t go the way you hoped, it brings you feedback from Source, and you tune from there.',
            '<font name="Jost">Ask yourself:</font> “What if I’m not doing this wrong at all?”',
        ],
    ),
    'sovereignty': dict(
        file='embodied-sovereignty.pdf',
        name='Embodied Sovereignty',
        image=THUNDERHEAD,
        cover='STILL ASKING\nIF I SHOULD',
        subtitle='…will it work?',
        quote='Master are ye of your destiny, free to take or reject at will.',
        credit='The Emerald Tablets',
        inner_label=None,
        monologue=[
            '“Is it okay? What if I say no?”',
            '“Is that ok to think?”',
            '“I’m scared to say.”',
            '“Should I start being more real and genuine?”',
        ],
        callout='There is nothing wrong with you. There never was.',     # Tim's Sanctum "Deserving" page
        loops_label='The hesitation',
        loops=[
            '“I don’t want to say too much.”',
            '“I just felt I need to speak up about it.”',
            '“I get told I’m too much.”',
            '“I don’t know who I am anymore, I think.”',
            '“I don’t know who I’m being because what I’m saying I am doesn’t match who I am.”',
        ],
        guess='Worth is not confirmed by others.',                         # Tim's Sanctum "Worthy" page, as are the rest below
        why=[
            'Worthy isn’t something you say to convince yourself. It’s where you are. It’s home.',
            'You are not worthy because of what you’ve done or do. You are worthy because you are here now.',
            'Worthy is not proven. Worthy is not earned. Worthy is chosen. Choosing… not being shown.',
            'Worthy is not when the gate opens to you. Worthy is when you realize it always was. And the only gate was the one you placed there.',
        ],
        shift='The moment the self says: “I will no longer change to be allowed.” “I already match. I already belong.”',
        todo=[
            'Write down one thing you aren’t sure if you should do.',
            'Take three slow connected breaths.',
            'Ask yourself, “Is this what I want to do?”',
            'Allow your deepest, most inner knowing to answer.',
            'Ask yourself: “What if I just do it and see what happens?”',
        ],
    ),
}
# ------------------------------------------------------------------ /TEXT


def wrap_words(text, font, size, width):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def make_cover(out_path, headline, subtitle, photo, margin=62):
    """Same cover as the other PDFs (Aboreto title, Cantata One subtitle, photo with the offset gold frame, gold logo),
    but the title can run to several lines because these titles are longer."""
    from PIL import Image as PILImage
    W, H = letter
    width = W - 2 * margin
    c = rl_canvas.Canvas(out_path, pagesize=letter)
    c.setFillColor(OBSIDIAN)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    size = 44
    if '\n' in headline:                           # explicit line breaks: use them as written, shrink to fit
        lines = headline.split('\n')
        while max(pdfmetrics.stringWidth(ln, 'Aboreto', size) for ln in lines) > width and size > 24:
            size -= 1
    else:
        while len(wrap_words(headline, 'Aboreto', size, width)) > 4 and size > 24:
            size -= 1
        lines = wrap_words(headline, 'Aboreto', size, width)
    c.setFillColor(HexColor('#f0e8d8'))
    c.setFont('Aboreto', size)
    y = H - 100
    for i, ln in enumerate(lines):
        c.drawString(margin, y - i * size * 1.14, ln)
    sub_y = y - (len(lines) - 1) * size * 1.14 - 30
    c.setFillColor(HexColor('#a8a193'))
    ssize = 12
    while pdfmetrics.stringWidth(subtitle, 'CantataOne', ssize) > width and ssize > 8:
        ssize -= 0.5
    c.setFont('CantataOne', ssize)
    c.drawString(margin + 2, sub_y, subtitle)
    iw, ih = PILImage.open(photo).size
    pw = 420
    ph = pw * ih / iw
    x, y2, off = margin, sub_y - 30 - ph, 16
    if y2 < 95:                                   # keep clear of the logo: shrink the photo to fit
        ph = sub_y - 30 - 95
        pw = ph * iw / ih
        y2 = 95
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setStrokeAlpha(0.55)
    c.setLineWidth(0.8)
    c.rect(x + off, y2 - off, pw, ph, stroke=1, fill=0)
    c.restoreState()
    c.drawImage(photo, x, y2, pw, ph)
    lw = 230
    c.drawImage(LOGO, (W - lw) / 2, 40, lw, lw * 350 / 2440, mask='auto')
    c.save()


def build(key):
    d = PDFS[key]
    out = os.path.join(OUT_DIR, d['file'])
    os.makedirs(OUT_DIR, exist_ok=True)
    doc = BaseDocTemplate(out, pagesize=letter, title=d['name'], author='Everyday Alchemy', subject='Everyday Alchemy',
                          leftMargin=MARGIN_X, rightMargin=MARGIN_X, topMargin=70, bottomMargin=62)
    frame = Frame(MARGIN_X, 62, CONTENT_W, PAGE_H - 70 - 62, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='p', frames=[frame], onPage=page_bg)])

    s = [Spacer(1, 18), GoldBand(d['quote'], d['credit']), Spacer(1, 26)]
    if d.get('inner_label'):
        s += [Spaced(d['inner_label'], before=0, after=8)]
    s += [P(t, inner) for t in d['monologue']]
    s += [callout(d['callout'])]
    if d.get('image'):
        from PIL import Image as PILImage
        pw, ph = PILImage.open(d['image']).size         # page 2 closes with the photo, full content width, uncropped
        s += [Spacer(1, 10), HeroImage(d['image'], CONTENT_W, CONTENT_W * ph / pw), PageBreak()]
    s += [Spaced(d['loops_label'], before=0 if d.get('image') else 10, after=8)] + [Paragraph(t, mine, bulletText='\u2014') for t in d['loops']]
    tg = 6 if d.get('tight') else 0
    s += [Spaced('Guess what?', before=16 - tg), P(d['guess'])]
    why = [P(t[2:], qa) if t.startswith('##') else P(t) for t in d['why']]
    s += [KeepTogether([Spaced('Why it makes sense', before=14 - tg * 2 // 3)] + why)]
    if d.get('bridge'):                              # what they say, then what is behind it: plain pairs
        pairs = [Spacer(1, 6)]
        for q, e in d['bridge']:
            pairs += [P(q, quote), P(e, body)]
        s += [KeepTogether(pairs + ([P(d['source'], note)] if d.get('source') else []))]
    if d.get('shift'):
        s += [KeepTogether([Spaced('The shift', before=14), P(d['shift'])])]
    s += [KeepTogether([Spaced('What to do', before=10 - tg // 3)] + steps(d['todo']))]
    s += [KeepTogether([Spaced('If you’re ready, reach out to start the next level.', before=14 - tg * 2 // 3, after=4),
                        Paragraph('<a href="%s?utm_source=%s-pdf&amp;utm_medium=pdf&amp;utm_campaign=quiz" color="#e2c98a">%s</a>' % (BOOK_URL, os.path.splitext(d['file'])[0], BOOK_LABEL), link)])]
    doc.build(s, canvasmaker=ClosingCanvas)

    cover = out + '.cover.pdf'
    make_cover(cover, d['cover'], d['subtitle'], COVER_PHOTO)
    prepend_cover(out, cover)
    os.remove(cover)
    print('wrote', out)


if __name__ == '__main__':
    for k in (sys.argv[1:] or list(PDFS)):
        build(k)
