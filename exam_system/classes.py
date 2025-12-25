# -*- coding: utf-8 -*-

import copy
import collections
import pathlib

import pandas as pd
import numpy as np


class Orgonisation:
    '''Orgonisation has 1 (principal) proptery
    name: name'''
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def __str__(self):
        return self.name

    def __getitem__(self, key):
        return self.members[key]

    @property
    def size(self):
        return len(self.members)

    @classmethod
    def fromData(cls, df, mthd, name=''):
        return cls(name, members=[mthd(df.columns, row) for k, row in df.iterrows()])


class Class(Orgonisation):
    '''Class has 3 (principal) propteries
    name: name
    members: members'''
    def __init__(self, name, members):
        super().__init__(name, members)
        self.name = name
        self.members = members
        self.basic_keys = ['name', 'gender']

    def copy(self):
        cpy = Class(self.name, [member.copy() for member in self.members])
        return cpy

    def __add__(self, other):
        return BigClass(self.name + '&' + other.name, [], [self, other])

    @staticmethod
    def read_excel(filename, sheetname, name=None, *args, **kwargs):
        if isinstance(filename, str):
            filename = pathlib.Path(filename)
        if filename.suffix:
            df = pd.read_excel(filename, sheetname, *args, **kwargs)
        else:
            df = pd.read_excel(filename.with_suffix('.xls'), sheetname, *args, **kwargs)
        if name is None:
            name = sheetname
        return Class.fromData(df, Student.fromItem, name=name)

    def to_excel(self, filename, sheetname=None):
        if sheetname is None:
            sheetname = self.name
        values = []
        index = []
        for s in self.members:
            values.append([s.name, s.gender] + list(s.score.values()))
            index.append(s.no)
        columns = self.basic_keys + list(s.score.keys())
        if isinstance(filename, str):
            filename = pathlib.Path(filename)
        pd.DataFrame(values, columns=columns, index=index).to_excel(filename.with_suffix('.xls'), sheetname)

    @property
    def examSize(self):
        return len([s for s in self.members if s['exam']>0])

    def filter(self):
        self.members = [s for s in self.members if s['exam']>0]


class BigClass(Orgonisation):
    '''Class has 3 (principal) propteries
    name: name
    members: members
    subOrgonisation: subOrgonisation []'''
    def __init__(self, name, members=None, subClasses=[]):
        super(Class, self).__init__()
        self.name = name
        self.subClasses = subClasses

    def copy(self):
        cpy = Class(self.name, [c.copy() for c in self.subClasses])
        return cpy

    def __add__(self, other):
        if isinstance(other, Class):
            return BigClass(self.name + '&' + other.name, [], self.subClasses + [other])
        else:
            return BigClass(self.name + '&' + other.name, [], self.subClasses + other.subClasses)

    def walk(self):
        for c in self.subClasses:
            for s in c.members:
                yield c, s



class Student:
    '''Student has 5 (principal) propteries
    name: name
    no: no
    gender: gender
    score: score
    remark: remark'''
    def __init__(self, name='', no=0, gender='m', score={}, remark=''):
        self.name = name
        self.no = no
        self.gender = gender
        self.score = score
        self.remark = remark

    def copy(self):
        return Student(self.name, self.no, self.gender, self.score.copy(), self.remark)

    @staticmethod
    def fromItem(keys, values):
        """
        Create a Student object from keys and cooresponding values.
        
        Arguments:
            keys {list[str]} -- list of keys
            values {list} -- list of values
        
        Returns:
            Student
        """

        s = Student(score=collections.OrderedDict())
        for key, val in zip(keys, values):
            if key in {'name', 'Name', '姓名'}:
                s.name = val
            elif key in {'No', 'no', '学号'}:
                s.no = val
            elif key in {'gender', 'Gender', '性别'}:
                s.gender = val
            else:
                if str(val) == 'nan':
                    s.score.update({key:0})
                else:
                    s.score.update({key:val})
        return s


    def __getitem__(self, key):
        return self.score[key]

    def __setitem__(self, key, val):
        self.score[key] = val

    def __str__(self):
        return '%s(%d)'%(self.name, self.no)
