#!/usr/bin/env python3

from exam import *
from plugin import *


paper = ExamPaper()

paper.calculation = []
paper.fill = FillProblem.random(filename='python_fill', n=8) @ replace_backticks_with_verb
paper.choice = ChoiceProblem.random(filename='python_choice', n=5) @ replace_backticks_with_verb
paper.truefalse = TrueFalseProblem.random(filename='python_truefalse', n=5) @ replace_backticks_with_verb
paper.build()
paper.write(filename='exam/python_ans')


for p in paper.choice:
    p.mask_flag = True
for p in paper.truefalse:
    p.mask_flag = True
for p in paper.fill:
    p.mask_flag = True

for p in paper.calculation:
    p.solution = None

paper.data = []
paper.build()
paper.write('exam/python_exam')