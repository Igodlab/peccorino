# Main private repo for [Peccorino](https://www.youtube.com/@peccorino) YouTube

![peccorino logo](assets/logos/pecorino-logo.png)

## Channel Information

This is a repo dump for every video produced for peccorino's YouTube channel.

## Manim custom configuration

Peccorino uses [Manim](https://docs.manim.community/en/stable/index.html) (the best open source scientific animation software). The channel aesthetics require some different custom configurations. Add the folowing lines starting with `X***` referring to custom **Excalidraw font colors** to the `manim_colors.py` file which shoul be in `.venv/lib/python3.12/site-packages/manim/utils/color/manim_colors.py` (assuming we created the project with super fast [uv](https://docs.astral.sh/uv/pip/environments/#using-arbitrary-python-environments) project manager, otherwise simply edit the `site-packages` wherever it was installed either w/ pip or conda)

```python
# .venv/lib/python3.12/site-packages/manim/utils/color/manim_colors.py
GREY_BROWN = ManimColor("#736357")

# Custom Excalidraw
XBCK = ManimColor("#303446")
XTXT = ManimColor("#c6d0f5")

XALICE   = ManimColor("#1971c2")
XBOB     = ManimColor("#ff0000")
XCHARLIE = ManimColor("#6741d9")
XEVE     = ManimColor("#ffd43b")
XMALLORY = ManimColor("#e8590c")
XTRENT   = ManimColor("#12b886")
XPEGGY   = ManimColor("#846358")
XVICTOR  = ManimColor("#1e1e1e")
XGRACE   = ManimColor("#c4037e")
XSYBIL   = ManimColor("#f783ac")

# Colors used for Manim Community's logo and banner

LOGO_WHITE = ManimColor("#ECE7E2")

