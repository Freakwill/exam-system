#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import numpy as np
import pandas as pd

# 原始评分文件
F = pathlib.Path('../Linux基础/xinji18/原始评分.xls')

data = pd.read_excel(F, sheet_name='xinji18')
data = data.fillna(0)


# 评分依据
import yaml
s = F.with_name('criteria.yaml').read_text()
C = yaml.full_load(s)


# 评分
exam = 0
for k, fw in C.items():
    f, w = fw['f'], fw['w']
    if isinstance(f, str):
        if f == '':
            exam += data[k] * w
            continue
        else:
            f = eval(f)
    if isinstance(f, tuple):
        exam0 = f[0] + f[1] * data[k]
    elif isinstance(f, (list, dict)):
        exam0 = np.array([f[i] for i in data[k]])
    else:
        exam0 = f * data[k]
    exam += exam0 * w


data['exam']=np.int16(np.round(exam))
data.to_excel(F.with_name('评分.xls'))
