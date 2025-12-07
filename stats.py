#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def CalcLinesPy(line, isBlockComment):
    """Calculate the lines in python codes
    
    Arguments:
        line {[str]} -- lines of codes
        isBlockComment {bool} -- [single quotes, double quotes]
    
    Returns:
        [type] -- [description]
    """

    lineType, lineLen = 0, len(line)
    if not lineLen:
        return lineType

    line = line + '\n\n' #添加两个字符防止iChar+2时越界
    iChar, isLineComment = 0, False
    while iChar < lineLen:
        if line[iChar] == ' ' or line[iChar] == '\t':   #空白字符
            iChar += 1; continue
        elif line[iChar] == '#':            #行注释
            isLineComment = True
            lineType |= 2
        elif line[iChar:iChar+3] == "'''":  #单引号块注释
            if isBlockComment[0] or isBlockComment[1]:
                isBlockComment[0] = False
            else:
                isBlockComment[0] = True
            lineType |= 2; iChar += 2
        elif line[iChar:iChar+3] == '"""':  #双引号块注释
            if isBlockComment[0] or isBlockComment[1]:
                isBlockComment[1] = False
            else:
                isBlockComment[1] = True
            lineType |= 2; iChar += 2
        else:
            if isLineComment or isBlockComment[0] or isBlockComment[1]:
                lineType |= 2
            else:
                lineType |= 1
        iChar += 1

    return lineType   #Bitmap：0空行，1代码，2注释，3代码和注释