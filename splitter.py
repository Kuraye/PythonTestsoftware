"""
Author: T. van Es
Date: 07-11-2022

Description:
This file controls every aspect of splitting the SVG-files and editing them.
"""

import re
import ast

def getOrdered(file):
    f = open(file, 'r')
    combis = []
    indexPlaced = []
    for i, line in enumerate(f):
        if re.search('(.*)\<g(.|\n)*?>', line):
            combis.append([i+1])
            indexPlaced.append(len(combis))
        if re.search('(.*)\</g(.|\n)*?>', line):
            combis[indexPlaced[-1]-1].append(i+1)
            indexPlaced = indexPlaced[:-1]
    inOrder = {}
    unPlaced = list(reversed(combis))
    for i, line in enumerate(unPlaced):
        j = i+1
        while j < len(unPlaced):
            if unPlaced[i][0] > unPlaced[j][0] and unPlaced[i][1] < unPlaced[j][1]:
                if str(line) not in inOrder:
                    inOrder[str(line)] = []
                inOrder.setdefault(str(unPlaced[j]), []).append(line)
                j += 1
                break
            else:
                if str(line) not in inOrder:
                    inOrder[str(line)] = []
                j += 1
    return inOrder

def getHighestGroup(design, orderedList):
    lo, hi = None, None
    for i in orderedList:
        start = int(i.strip('][').split(', ')[0])
        end = int(i.strip('][').split(', ')[1])
        if lo is None or start < lo:
            lo = start
        if hi is None or hi < end:
            hi = end
    highestGroup = {}
    highestGroup['name'] = str([lo, hi])
    highestGroup['parents'] = None
    highestGroup['children'] = orderedList[str([lo, hi])]
    with open(design, 'r') as file:
        lines = file.readlines()[lo-1:hi]
        f = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="200px" viewBox="0 0 1920 1080">"""
        for line in lines:
            f += '\n' + line
        f += '\n' + '</svg>'
        highestGroup['svg'] = f
    return highestGroup

def getChildren(design, parent, orderedList):
    children = []
    for child in ast.literal_eval(parent):
        lo, hi = child[0], child[1]
        highestGroup = {}
        highestGroup['name'] = str([lo, hi])
        highestGroup['parents'] = None
        highestGroup['children'] = orderedList[str([lo, hi])]
        highestGroup['additionalDescription'] = ""
        highestGroup['description'] = ""
        with open(design, 'r') as file:
            lines = file.readlines()[lo-1:hi]
            f = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="200px" viewBox="0 0 1920 1080">"""
            for line in lines:
                f += '\n' + line
            f += '\n' + '</svg>'
            highestGroup['svg'] = f
        children.append(highestGroup)
    return children

def updateExtraInfo(list, itemID, extraInfo):
    for item in list:
        if item['name'] == itemID:
            index = list.index(item)
            list[index]['additionalDescription'] = extraInfo
    return(list)

def updateDescription(list, itemID, description):
    for item in list:
        if item['name'] == itemID:
            index = list.index(item)
            list[index]['description'] = description
    return(list)
