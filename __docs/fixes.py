#  -*- coding: utf-8 -*-
"""

Author: Rafael R. L. Benevides
Date: 15/11/2021

"""

import os

from io import StringIO


# ======================================================================== TITLE
index_html = os.path.join("./_build/html/index.html")

new_html = StringIO()

with open(index_html, 'r') as html:

    for line in html:

        if all(piece in line for piece in ["<title>", "</title>"]):

            junk = line[line.find("<title>")+7:line.find(';')+2]

            line = line.replace(junk, '')

        new_html.write(line)

new_html.seek(0)

with open(index_html, 'w') as html:
    for line in new_html:
        html.write(line)

new_html.close()


# ======================================================================== THEME
theme_css = os.path.join("./_build/html/_static/css/theme.css")

with open(theme_css, 'a') as css:
    css.write("div.section {text-align: justify; text-justify: inter-word;}")