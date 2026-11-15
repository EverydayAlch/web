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
        name='Aligned Action',
        image=DESERT,
        cover='THE ACTION GAP',
        one_line=True,
        subtitle='Stopping the Energy Leak of Overwhelm and Paralysis',
        quote='Choose your work… for all must labor.',
        credit='The Emerald Tablets',
        # sections layout (Tim, 2026-11-15), same as the other three
        sections=[
            ('Where You Are Right Now', [
                'You know what you want to build, but taking the physical steps to execute feels like pushing through wet cement. You find yourself trapped between a drive to move forward and a physical heaviness that stops you cold.',
                'It’s easy to call this laziness or a lack of discipline. It isn’t. You are simply running a high-frequency intention into an old, protective physical baseline, and the resulting static shuts down your momentum.',
            ]),
            '@image',
            '@pagebreak',
            ('The Reality', [
                '##The Identity Gap.',
                'When you set an intention for a new outcome, your mind instantly demands to see all ten steps before it allows your body to move.',
                'When you look across that gap without knowing the full blueprint, your brain perceives the unknown as a threat. It fires an electrical panic charge into your nervous system, which triggers a heavy magnetic response—fatigue, confusion, or sudden distraction.',
                'The leak happens when you sit in the overwhelm and believe you are stuck, rather than recognizing your system is simply running hot on outdated rules.',
            ]),
        ],
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
        cover='THE STATIC LOOP',
        one_line=True,
        subtitle='How to Stop the Electrical Noise and Reset Your Field',
        quote='As above, so below.',
        credit='The Emerald Tablets',
        # sections layout (Tim, 2026-11-14), same as Embodied Sovereignty
        sections=[
            ('Where You Are Right Now', [
                'Your mind is spinning, running scenarios, and trying to solve problems that aren’t happening right now. You find yourself trapped in overthinking, worrying that your fears will ruin your progress, or feeling completely exhausted by the noise in your head.',
                'You try to use your mind to fix your mind, which only makes the noise louder. Nothing is broken, but the fatigue is real.',
            ]),
            '@image',
            '@pagebreak',
            ('The Reality', [
                '##Conflating Electricity with Identity.',
                'Thoughts are purely electrical. Emotions are magnetic.',
                'When a stressful electrical thought fires, it instantly triggers a magnetic response in your body—tightness, anxiety, or a dip in your chest. Because magnetism pulls like-frequencies, that physical sensation immediately attracts three more electrical thoughts to justify why you feel that way.',
                'The leak happens when you sit in the middle of that loop and claim it as “yours.” Trying to think your way out of a thought loop just dumps more current into a short circuit. You aren’t failing; your electromagnetic system is simply running hot because you’re sitting in the driver’s seat of the noise instead of resting in the center of your head.',
            ]),
        ],
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
        cover='THE DOUBT LOOP',
        one_line=True,
        subtitle='Stopping the Energy Leak of Waiting for Proof',
        quote='Man is only what he believes.',
        credit='The Emerald Tablets',
        # sections layout (Tim, 2026-11-14), same as Internal Integrity
        sections=[
            ('Where You Are Right Now', [
                'You’ve done the work, cleared the past, and applied the tools, yet a quiet background voice keeps asking, “Is this actually working?” You catch yourself checking for physical proof before you fully commit your energy to the outcome.',
                'You hold a clear vision in meditation or quiet moments, but as soon as you step into daily demands, the certainty slips. It leaves you feeling like you’re constantly starting over, pulling up the seed to see if it’s growing, and exhausting yourself trying to fix a broken link that isn’t actually broken.',
            ]),
            '@image',
            '@pagebreak',
            ('The Reality', [
                '##Running Past Failure in Present Time.',
                'Doubt is not a personal weakness or a lack of faith; it is an electrical memory loop.',
                'When a past effort didn’t yield the physical result you wanted, the electrical charge of that disappointment was stored in your field. Today, when you launch a new intention, your electrical system automatically scans back to that old reference point.',
                'The moment you brace for potential disappointment, your body generates a magnetic response—tightness, hesitation, or subtle anxiety. That magnetic charge instantly clamps down on your field, pulling your focus out of present time and into a memory of failure. You end up trying to create a new future while running the energy of an old disappointment.',
            ]),
        ],
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
        cover='THE PERMISSION LOOP',
        one_line=True,
        subtitle='Stopping the Energy Leak of Hesitation and Second-Guessing:',
        quote='Master are ye of your destiny, free to take or reject at will.',
        credit='The Emerald Tablets',
        # sections layout (Tim, 2026-11-14): 'Where You Are Right Now' / 'The Reality' / 'The Truth of Your Worth'.
        # items: plain text = paragraph, '##' = sub-heading, '>>' = big line, '@image' / '@pagebreak' = layout markers
        sections=[
            ('Where You Are Right Now', [
                'You hesitate before making a choice, checking the room to see if it’s safe to simply be yourself. In your business, your relationships, and your daily life, you tone down your truth, edit your words, or wait for someone else to validate your position before you stand in it.',
                'You spend immense energy predicting how others will react to you. It leaves you feeling split—holding a massive, beautiful reality on the inside, while presenting a carefully filtered version on the outside.',
            ]),
            ('The Reality', [
                '##The Permission Loop.',
                'Every time you wait for external approval or alter your voice to prevent friction, your energy leaks out. You are attempting to run your life through other people’s considerations, past rules, and old survival stories, rather than resting in your own grounded center.',
                'The energy that is meant to build your life, your creative vision, and your joy gets burned up in hesitation, second-guessing, and holding yourself back.',
            ]),
            ('The Truth of Your Worth', [
                '##There is nothing wrong with you. There never was.',
                'Your worth isn’t something you have to prove, earn, or convince anyone of—including yourself. Worth isn’t given when a gate opens; worth is realizing the gate was never locked, and the only barrier was the habit of asking for permission to enter.',
                'You do not exist to be validated by the outside world. You are here, now, as a living, sovereign expression of creation.',
            ]),
            '@pagebreak',
            '@image',
        ],
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


def make_cover(out_path, headline, subtitle, photo, margin=62, one_line=False):
    """Same cover as the other PDFs (Aboreto title, Cantata One subtitle, photo with the offset gold frame, gold logo),
    but the title can run to several lines because these titles are longer."""
    from PIL import Image as PILImage
    W, H = letter
    width = W - 2 * margin
    c = rl_canvas.Canvas(out_path, pagesize=letter)
    c.setFillColor(OBSIDIAN)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    size = 44
    if one_line or '\n' in headline:               # one line, or explicit line breaks: use them as written, shrink to fit
        lines = [headline] if one_line else headline.split('\n')
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
    if d.get('sections'):
        first = True
        for sec in d['sections']:
            if sec == '@pagebreak':
                s += [PageBreak()]
                first = True
            elif sec == '@image':
                from PIL import Image as PILImage
                pw, ph = PILImage.open(d['image']).size
                s += [Spacer(1, 12), HeroImage(d['image'], CONTENT_W, CONTENT_W * ph / pw)]
            else:
                label, items = sec
                s += [Spaced(label, before=0 if first else 29, after=8)]
                first = False
                for it in items:
                    if it.startswith('##'):
                        s += [P(it[2:], qa)]
                    elif it.startswith('>>'):
                        s += [callout(it[2:])]
                    else:
                        s += [P(it)]
        s += [KeepTogether([Spaced('What to do', before=14)] + steps(d['todo']))]
        s += [KeepTogether([Spaced('If you’re ready, reach out to start the next level.', before=14, after=4),
                            Paragraph('<a href="%s?utm_source=%s-pdf&amp;utm_medium=pdf&amp;utm_campaign=quiz" color="#e2c98a">%s</a>' % (BOOK_URL, os.path.splitext(d['file'])[0], BOOK_LABEL), link)])]
        return finish_build(doc, s, out, d)
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
    return finish_build(doc, s, out, d)


def finish_build(doc, s, out, d):
    doc.build(s, canvasmaker=ClosingCanvas)

    cover = out + '.cover.pdf'
    make_cover(cover, d['cover'], d['subtitle'], COVER_PHOTO, one_line=d.get('one_line', False))
    prepend_cover(out, cover)
    os.remove(cover)
    print('wrote', out)


if __name__ == '__main__':
    for k in (sys.argv[1:] or list(PDFS)):
        build(k)
