"""MIT License

Copyright (c) 2017 Paul Ross https://github.com/paulross

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__author__  = 'Paul Ross'
__date__    = '2017-01-01'
__version__ = '0.0.1'
__rights__  = 'Copyright (c) 2017 Paul Ross'

import os
import string

CSS_LIST = [
    # HTML styling
    """body {
font-size:      12px;
font-family:    arial,helvetica,sans-serif;
margin:         6px;
padding:        6px;
}""",

#===============================================================================
#    """h1 {
# font-family:     Sans-serif;
# font-size:       1.5em;
# color:           silver;
# font-style:    italic;
# }""",
#===============================================================================
    """h1 {
color:            darkgoldenrod;
font-family:      sans-serif;
font-size:        14pt;
font-weight:      bold;
}""",
    """h2 {
color:          IndianRed;
font-family:    sans-serif;
font-size:      14pt;
font-weight:    normal;
}""",
    """h3 {
color:          Black;
font-family:    sans-serif;
font-size:      12pt;
font-weight:    bold;
}""",
    """h4 {
color:          FireBrick;
font-family:    sans-serif;
font-size:      10pt;
font-weight:    bold;
}""",
    # Specialised classes
    # Line numbers
    """span.line {
color:           slategrey;
/*font-style:    italic; */
}""",
    # File names
    """span.file {
 color:         black;
 font-style:    italic;
}""",
    # index.html table
    """table.indextable {
    border:         2px solid black;
    font-family:    sans-serif;
    color:          black;
    width:          96%;
    bgcolor:        #FFFFFF;
    align:          center;
}""",
    """th.indextable, td.indextable {
    /* border: 1px solid black; */
    border: 1px;
    border-top-style:solid;
    border-right-style:dotted;
    border-bottom-style:none;
    border-left-style:none;
    vertical-align:top;
    padding: 2px 6px 2px 6px;
}""",
    # Table of posts
    """table.posts {
border:            2px solid black;
border-collapse:   collapse;
font-family:       sans-serif;
color:             black;
}""",
"""th.post, td.post, td.alt1 {
border:            1px solid black;
vertical-align:    top;
padding:           2px 6px 2px 6px;
}""",

"""p.page_links {
    horizontal-align:          center;
    font-family:      sans-serif;
    font-size:        10pt;
    font-style:     italic;
}"""



    # Macro presentation
    """span.macro_s_f_r_f_name{
    color:          DarkSlateGray;
    font-family:    monospace;
    font-weight:    normal;
    font-style:     italic;
}""",
    """span.macro_s_t_r_f_name {
    color:          DarkSlateGray;
    font-family:    monospace;
    font-weight:    normal;
    font-style:     normal;
}""",
    """span.macro_s_f_r_t_name {
    color:          Red; /* OrangeRed; */
    font-family:    monospace;
    font-weight:    bold;
    font-style:     italic;
}""",
    """span.macro_s_t_r_t_name{
    color:          Red; /* OrangeRed; */
    font-family:    monospace;
    font-weight:    bold;
    font-style:     normal;
}""",
    """span.macro_s_f_r_f_repl{
    color:          SlateGray;
    font-family:    monospace;
    font-weight:    normal;
    font-style:     italic;
}""",
    """span.macro_s_t_r_f_repl {
    color:          SlateGray;
    font-family:    monospace;
    font-weight:    normal;
    font-style:     normal;
}""",
    """span.macro_s_f_r_t_repl {
    color:          RosyBrown; /* Orange; */
    font-family:    monospace;
    font-weight:    bold;
    font-style:     italic;
}""",
    """span.macro_s_t_r_t_repl{
    color:          RosyBrown; /* Orange; */
    font-family:    monospace;
    font-weight:    bold;
    font-style:     normal;
}""",
    # File declarations in the macro pages
    """span.file_decl {
    color:          black;
    font-family:    monospace;
    /* font-weight:    bold;
    font-style:     italic; */
}""",
    # Conditional preprocessing directives - True
    """span.CcgNodeTrue {
    color:          LimeGreen;
    font-family:    monospace;
    /* font-weight:    bold; */
    /* font-style:     italic; */
}""",
    # Conditional preprocessing directives - False
    """span.CcgNodeFalse {
    color:          red;
    font-family:    monospace;
    /* font-weight:    bold; */
    /* font-style:     italic; */
}""",
    ]

CSS_FILE = 'styles.css'
CSS_STRING = '\n'.join(CSS_LIST)

def writeCssToDir(theDir):
    """Writes the CSS file into to the directory."""
    if not os.path.exists(theDir):
        os.makedirs(theDir)
    with open(os.path.join(theDir, CSS_FILE), 'w') as f:
        f.write(CSS_STRING)

