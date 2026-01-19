#!/usr/bin/env python3

from exam import *
from plugin import *


n_fill = 16
n_choice = 10
n_truefalse = 10

class PythonExamPaper(ExamPaper):

    def make_head(self):
        self.append(Center(data=pylatex_ext.large(bold(NoEscape(self.title)))))
        clopen = NoEscape(r"($\square$闭卷/$\square$开卷)")
        line = Command('autolenunderline', '')
        table = Tabular('cccccc')
        table.escape = False
        table.add_row((bold('考试形式：'), MultiColumn(2, data=clopen), MultiColumn(3)))
        table.add_row(('姓名', line, '学号', line, '教师姓名', line))

        # mark_table = Tabular('|c|c|c|c|c|c|')
        # mark_table.escape = False
        # mark_table.add_hline()
        # mark_table.add_row(r'\sws{题号} \sws{一} \sws{二} \sws{三} \sws{四} \sws{总评}'.split())
        # mark_table.add_hline()
        # mark_table.add_row((MultiRow(2, data='计分'), '', '', '', '', ''))
        # mark_table.add_empty_row()
        # mark_table.add_hline()
        self.append(Center(data=table))
        # self.append(Center(data=mark_table))
        self.append(Command('vspace', '10pt'))
        self.append(Command('thispagestyle', 'plain'))

    def make_fill(self):
        # make filling problems
        self.append('\\noindent')
        self.append(bold("一、填空题 (本题满分40分，每空 2 分, 共 20 空):"))
        with self.create(Enumerate(options='1)')) as enum:
            enum.escape = False
            for p in self.fill:
                enum.add_item(NoEscape(p.totex()))

    def make_truefalse(self):
        # make true-false problem
        self.append('\\noindent')
        self.append(bold('二、判断题 (本题满分20分，每题 2 分, 共 10 题):'))
        with self.create(Enumerate(options='1)')) as enum:
            enum.escape = False
            for p in self.truefalse:
                enum.add_item(NoEscape(p.totex()))

    def make_choice(self):
        # make choice problems
        self.append('\\noindent')
        self.append(bold('三、选择题 (本题满分40分，每题 4 分, 共 10 题):'))
        with self.create(Enumerate(options='1)')) as enum:
            enum.escape = False
            for p in self.choice:
                enum.add_item(NoEscape(p.totex()))

paper = PythonExamPaper(title="北京雁栖湖数学与人工智能学院2025-2026学年第一学期《Python程序设计》课程期末考试试卷（A卷）")

# paper.calculation = []
paper.fill = (FillProblem@ code).random(filename='python_fill', n=n_fill)
paper.truefalse = (TrueFalseProblem @ replace_backticks_with_verb).random(filename='python_truefalse', n=n_truefalse)
paper.choice = (ChoiceProblem@ code).random(filename='python_choice', n=n_choice) 
paper.build()
paper.write(filename='exam/python_ans')

paper.mask_answer()

paper.data = []
paper.build()
paper.write('exam/python_exam')
