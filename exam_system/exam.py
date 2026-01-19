#!/usr/bin/env python3

"""myfile.exam

To edit examination paper

-------------------------------
Path: examsystem/exam.py
Author: William/2016-01-02
"""

import collections
import pathlib
import datetime
import copy
import yaml

import numpy as np

from pylatex import *
from pylatex.base_classes import *
from pylatex.utils import *

import pylatex_ext

from base import *
import problem_selection

from config import *

 
class Solve(Environment):
    """solve environment
    Solve(data='the solution')
    """
    escape = False
    content_separator = "\\\\\n"


class ExamPaper(pylatex_ext.XeDocument):
    """ExamPaper < Document
    """

    def __init__(self, subject='', title=None, *args, **kwargs):
        """
        Argument:
            subject: str, the name of the subject of the examination;
            title: str, will be given automaticly
        """
        super().__init__(documentclass='ctexart', document_options='12pt,a4paper', *args, **kwargs)
        self.latex_name = 'document'
        self.escape = False
        self.subject = subject
        if title is None:
            import semester
            s = semester.Semester()
            title = f'{COLLEGE}{s.totex()}试卷'
        self.title = title

        self.usepackage(('mathrsfs, amsfonts, amsmath, amssymb', 'enumerate', 'exampaper',
            'fancyhdr', 'geometry', 'listings'))

        self.preamble.append(Command('geometry', 'left=3.3cm,right=3.3cm,top=2.3cm,foot=1.5cm'))
        self.preamble.append(Command('pagestyle', 'fancy'))
        self.preamble.append(Command('chead', NoEscape(Command('footnotesize', bold(f'{COLLEGE}考试命题纸')).dumps())))
        self.preamble.append(Command('cfoot', NoEscape(Command('footnotesize', NoEscape(r'第~\thepage~页~(共~\pageref{LastPage}~页)')).dumps())))
        self.preamble.append(Command('renewcommand', arguments=Arguments(NoEscape(r'\headrulewidth'), '0pt')))



        # header = PageStyle("header")      
        # with header.create(Foot("C")):
        #     ft = Command('footnotesize', arguments=NoEscape('第~\\thepage~页~(共~\pageref{LastPage}~页)'))
        #     header.append(ft)
        # self.preamble.append(header)

    def build(self):
        
        # the head of the paper
        self.make_head()
        
        # make problems
        if self.check('fill'):
            self.make_fill()
        self.append('\n\n')
        if self.check('truefalse'):
            self.make_truefalse()
        self.append('\n\n')
        if self.check('choice'):
            self.make_choice()
        self.append('\n\n')
        if self.check('calculation'):
            self.make_calculation()

    def make_head(self):
        self.append(Center(data=pylatex_ext.large(bold(NoEscape(self.title)))))
        line2 = Command('autolenunderline', '______________')
        line = Command('autolenunderline', '')
        table = Tabular('lclclc')
        table.escape = False
        table.add_row(('课程', MultiColumn(2, data=line2), '班级', MultiColumn(2, data=line2)))
        table.add_row(('姓名', line, '学号', line, '教师姓名', line))

        mark_table = Tabular('|c|c|c|c|c|c|')
        mark_table.escape = False
        mark_table.add_hline()
        mark_table.add_row(r'\sws{题号} \sws{一} \sws{二} \sws{三} \sws{四} \sws{总评}'.split())
        mark_table.add_hline()
        mark_table.add_row((MultiRow(2, data='计分'), '', '', '', '', ''))
        mark_table.add_empty_row()
        mark_table.add_hline()
        self.append(Center(data=table))
        self.append(Center(data=mark_table))
        self.append(Command('thispagestyle', 'plain'))

    def check(self, a):
        return hasattr(self, a)

    def make_fill(self):
        # make filling problems
        self.append('\\noindent 一、填空题 (每空 2 分, 共 20 空):')
        with self.create(Enumerate(options='1)')) as enum:
            enum.escape = False
            for p in self.fill:
                enum.add_item(NoEscape(p.totex()))

    def make_truefalse(self):
        # make true-false problem
        self.append('\\noindent 二、判断题 (每空 2 分, 共 10 空):')
        with self.create(Enumerate(options='1)')) as enum:
            enum.escape = False
            for p in self.truefalse:
                enum.add_item(NoEscape(p.totex()))

    def make_choice(self):
        # make choice problems
        self.append('\\noindent 三、选择题 (每空 4 分, 共 10 空):')
        with self.create(Enumerate(options='1)')) as enum:
            enum.escape = False
            for p in self.choice:
                enum.add_item(NoEscape(p.totex()))

    def make_calculation(self):
        # make calculation problems
        self.append('\\noindent 四、计算题 (每题 10 分, 共 2 题):')
        with self.create(Enumerate(options='1)')) as enum:
            enum.escape = False
            for p in self.calculation:
                if p.solution is None:
                    enum.add_item(NoEscape(p.totex() + '\n\n' + Command('vspace', '10cm').dumps()))
                else:
                    enum.add_item(NoEscape(p.totex()))

    def write(self, filename=None):
        if filename is None:
            filename = self.subject + '.exam'
        super().write(filename)

    def topdf(self, filename=None):
        if filename is None:
            filename = self.subject + '.exam'
        super().topdf(filename)

    def print(self, filename=None):
        self.topdf(filename=filename)
        import sh
        sh.lpr('temp.pdf')
        sh.rm('temp.pdf')

    def mask_answer(self):
        if hasattr(self, 'choice'):
            for p in self.choice:
                p.mask_flag = True
        if hasattr(self, 'truefalse'):
            for p in self.truefalse:
                p.mask_flag = True
        if hasattr(self, 'fill'):
            for p in self.fill:
                p.mask_flag = True
        if hasattr(self, 'calculation'):
            for p in self.calculation:
                p.solution = None


class Problem(BaseTemplate):
    # Problem class

    def __init__(self, template='', parameter={}, answer={}, realm=None, solution=None):
        """Initialize a problem
        
        Keyword Arguments:
            answer {dict} -- the answer for masked parameters (default: {{}})
            template {str} -- the template of the problem (default: {''})
            parameter {dict} -- dict of parameters for the problem (default: {{}})
            realm {str} -- the realm of the problem (default: {None})
            solution {Solution} -- the procedure to solving the problem (default: {None})
        """

        super().__init__(template, parameter)
        self.answer = answer
        self.realm = realm
        self.point = 10
        self.solution = solution

    @classmethod
    def random(cls, filename, n=1, strategy='rand', *args, **kwargs):
        # read n problems from yaml files (randomly)
        problems = cls.read_yaml(filename, *args, **kwargs)
        return getattr(problem_selection, strategy)(problems, n)

    @classmethod
    def read_yaml(cls, filename, *args, **kwargs):
        filename = (BANK_FOLDER / filename).with_suffix('.yaml')
        yaml_text = filename.read_text(*args, **kwargs)
        return yaml.unsafe_load(yaml_text)

    def __setstate__(self, state):
        super().__setstate__(state)
        self.realm = state.get('realm', '')


class Solution(BaseTemplate):
    """Solution class
    
    solution of a problem
    
    Extends:
        BaseTemplate
    """

    def __init__(self, template='', parameter={}, solver=None):
        super().__init__(template, parameter)
        self.solver = solver
        if solver:
            self.parameter.update({'process': solver.process(), 'answer':'?'})

    @classmethod
    def fromProblem(cls, problem):
        obj = cls(parameter=problem.parameter)
        obj.genTemplate(problem)
        return obj

    def genTemplate(self, problem=None):
        # self.template = ''
        pass


class CalculationProblem(Problem):
    # should show the solution for calculation problems

    def __setstate__(self, state):
        super().__setstate__(state)
        self.point = state.get('point', 10)
        self.solution = state.get('solution', None)

    def totex(self):
        solution = self.solution
        if solution is not None:   # with solution
            if isinstance(solution, type) and issubclass(solution, Solution):
                # get solution automatically
                solution = solution.fromProblem(self)
            else:
                solution.update(self.parameter)
            return super().totex() + '\n\n' + Solve(data=solution.totex()).dumps()
        else:  # without solution
            return super().totex()


class OtherSolution(Solution):

    def genTemplate(self, problem):
        self.template = problem.template


class OtherProblem(Problem):

    solution = OtherSolution
    mask = Command('mypar', '')
    mask_flag = False
    masked = {'answer'}

    def totex(self):
        if self.mask_flag:
            self.mask_answer()
        return super().totex()

    def mask_answer(self):
        if self.mask_flag:
            for k in self.masked:
                self[k] = self.mask

    def __setstate__(self, state):
        super().__setstate__(state)
        self.answer = state['answer']
        self.solution = None


class TrueFalseProblem(OtherProblem):

    def __setstate__(self, state):
        super().__setstate__(state)
        self.template += r'\hfill~~{{answer}}'
        if 'answer' in state:
            if isinstance(state['answer'], bool):
                self.answer = 'true' if state['answer'] else 'false'
            else:
                self.answer = state['answer']
        else:
            self.answer = 'true'
        self.parameter.update({'answer': Command(self.answer)})


class ChoiceProblem(OtherProblem):

    def __setstate__(self, state):
        super().__setstate__(state)
        self.template += r'\hfill~~{{answer}}'
        option_len = sum(map(len, state['options'].values()))
        options = ['(%s) %s'%(k, v) for k, v in state['options'].items()]
        if option_len > 40:
            choices = f"{options[0]}~~{options[1]}\\\\\n{options[2]}~~{options[3]}"
        else:
            choices = '~~'.join(options)
        self.template += '\\\\\n' + choices
        self.solution = None
        self.parameter.update({'answer': Command('mypar', self.answer)})
        self.realm = state.get('realm', '')


class FillProblem(OtherProblem):

    mask = Command('autolenunderline', '')

    def __setstate__(self, state):
        super().__setstate__(state)
        self.masked = set(self.answer.keys())
        self.parameter.update({k: Command('autolenunderline', NoEscape(v)) for k, v in self.answer.items()})

    def mask_answer(self):
        if self.mask_flag:
            for k in self.masked:
                self[k] = Command('autolenunderline', NoEscape(self.answer[k]), options='mask')

    @property
    def n_fills(self):
        return len(self.answer)

    # @classmethod
    # def random(cls, n=1, *args, **kwargs):
    #     # read n problems from yaml files (randomly)
    #     problems = super().random(n=n, *args, **kwargs)
    #     n_ = 0
    #     for k, p in enumerate(problems):
    #         if n_ >= n:
    #             return problems[:k]
    #         n_ += p.n_fills
    #     return problems

    @classmethod
    def random(cls, filename, n=1, strategy='deap', *args, **kwargs):
        # read n problems from yaml files (randomly)
        problems = cls.read_yaml(filename, *args, **kwargs)
        return getattr(problem_selection, strategy)(problems, n)

