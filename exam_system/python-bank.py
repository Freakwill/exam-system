#!/usr/bin/env python3

from exam import *
from plugin import *


paper = ExamPaper()

paper.calculation = []
paper.fill = [p @ replace_backticks_with_verb for p in FillProblem.read_yaml(filename='python_fill')]
paper.choice = [p @ replace_backticks_with_verb for p in ChoiceProblem.read_yaml(filename='python_choice')]
paper.truefalse = [p @ replace_backticks_with_verb for p in TrueFalseProblem.read_yaml(filename='python_truefalse')]
paper.calculation = [p @ replace_backticks_with_listing for p in CalculationProblem.read_yaml(filename='python_calculation')]
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