#!/usr/bin/env python
# CPIP is a C/C++ Preprocessor implemented in Python.
# Copyright (C) 2008-2014 Paul Ross
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Paul Ross: cpipdev@googlemail.com

"""CSS Support for ITU+TU files in HTML."""

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

