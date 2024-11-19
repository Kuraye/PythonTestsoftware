"""
Author: T. van Es
Date: 10-10-2022

Description:
This file creates the required documents from (splitted)SVG-file inputs.
"""

import os
import re
import string

"""
createComponent opens an template of the component file and reads through all lines.
Where needed, it replaces the placeholder with the component information.
createStory does the same thing, but for the stories template.
"""

def createComponent(item):
    component = """"""
    nameComponent = string.capwords(item['description']).replace(" ", "")
    loc = os.path.join(os.path.dirname(__file__), 'static/template/component.jsx')
    f = open(loc, "r")
    for x in f:
        if re.search('%%NAAM%%', x):
            component += re.sub(r'%%NAAM%%', nameComponent, x)
        else:
            component += x
    f.close()

    newFile = open(os.path.join(os.path.dirname(__file__), 'static/template/exports/'+nameComponent+'.jsx'), "wt")
    newFile.write(component)
    newFile.close()
    return

def createStory(item):
    component = """"""
    nameComponent = string.capwords(item['description']).replace(" ", "")
    loc = os.path.join(os.path.dirname(__file__), 'static/template/stories.jsx')
    f = open(loc, "r")
    for x in f:
        if re.search('%%NAAM%%', x):
            component += re.sub(r'%%NAAM%%', nameComponent, x)
        elif re.search('%%IMAGE%%', x):
            component += re.sub(r'%%IMAGE%%', item['svg'].replace("\n", ""), x)
        elif re.search('%%INFO%%', x):
            component += re.sub(r'%%INFO%%', item['additionalDescription'], x)
        else:
            component += x
        
    f.close()

    newFile = open(os.path.join(os.path.dirname(__file__), 'static/template/exports/'+nameComponent+'.stories.jsx'), "wt")
    newFile.write(component)
    newFile.close()
    return
