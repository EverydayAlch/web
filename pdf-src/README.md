# Quiz result guides (PDF source)

Builds the three guide PDFs in `../downloads/`. Python 3 with `reportlab`, `pillow` and `pypdfium2`:

```
python3 -m venv .venv && .venv/bin/pip install reportlab pillow pypdfium2
.venv/bin/python make_waiting_pdf.py
.venv/bin/python make_spiralling_pdf.py
.venv/bin/python make_doubt_pdf.py
```

Text for each guide is in the `TEXT` block at the top of its script. Shared pieces (merkaba, cover, gold quote band) are in `pdf_extras.py`.
