#!/usr/bin/env python3

from exam import *
from plugin import *


paper = ExamPaper()

paper.calculation = []
paper.fill = (FillProblem @ (replace_backticks_with_listing+replace_backticks_with_verb)).read_yaml(filename='python_fill')
paper.choice = (ChoiceProblem @ replace_backticks_with_verb).read_yaml(filename='python_choice')
paper.truefalse = (TrueFalseProblem @ replace_backticks_with_verb).read_yaml(filename='python_truefalse')
paper.calculation = (CalculationProblem @ (replace_backticks_with_listing+replace_backticks_with_verb)).read_yaml(filename='python_calculation')
paper.build()
paper.write(filename='exam/python-bank')


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