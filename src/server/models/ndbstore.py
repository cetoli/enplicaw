#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Enplicaw
# Copyright 2013-2015 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
#
# Enplicaw é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>

"""Google HDB storage.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
__author__ = 'carlo'
# Imports the NDB data modeling API
import os
import sys

if "AUTH_DOMAIN" in os.environ.keys():
    from google.appengine.ext import ndb
else:
    from lib.minimock import Mock
    sys.modules['google.appengine.ext'] = Mock('google.appengine.ext')
    ndb = Mock('google.appengine.ext')

# import googledatastore as ndb

DEFAULT_PROJECTS = "DEFAULT_PROJECTS"
DEFAULT_PROJECT_NAMES = "JardimBotanico SuperPlataforma SuperPython MuseuGeo"


class Projects(ndb.Expando):
    """A main model for representing all projects."""
    name = ndb.StringProperty(indexed=True)
    names = ndb.StringProperty(indexed=False)
    contents = ndb.TextProperty(indexed=False)
    value = ndb.IntegerProperty(indexed=False)
    _projects = None

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def nget(cls, query):
        return query.fetch()[0] if query.fetch() else None

    @classmethod
    def instance(cls, name=DEFAULT_PROJECTS, names=DEFAULT_PROJECT_NAMES):
        def get_project():
            prj = cls.query(cls.name == name).fetch()
            print("prj", prj)
            cls._projects = prj[0] if prj else cls._start(name=name, names=names)

        return cls._projects or get_project()

    @classmethod
    def _start(cls, name=DEFAULT_PROJECTS, names=DEFAULT_PROJECT_NAMES):
        _prj = Projects.create(name=name, names=names)
        [Project.create(project=_prj.key, name=aname, kind=DEFAULT_PROJECTS) for aname in names.split()]
        return _prj


class Question(ndb.Model):
    """A sub model for representing an individual Question entry."""
    name = ndb.StringProperty(indexed=True)
    text = ndb.StringProperty(indexed=False)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def nget(cls, name):
        query = cls.query(cls.name == name).fetch()
        return query and query[0]

    @classmethod
    def obtain(cls, name):
        return Question.nget(name=name)


class Project(ndb.Expando):
    """Sub model for representing an project."""
    project = ndb.KeyProperty(kind=Projects)
    questions = ndb.StructuredProperty(Question, repeated=True)
    name = ndb.StringProperty(indexed=True)
    kind = ndb.StringProperty(indexed=False)
    populated = ndb.BooleanProperty(default=False)
    contents = ndb.TextProperty(indexed=False)
    modified_date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def nget(cls, name):
        query = cls.query(cls.name == name).fetch()
        return query and query[0]


class Learning(ndb.Expando):
    """A main model for representing an individual Question entry."""
    project = ndb.KeyProperty(kind=Project)


class Classifier(ndb.Expando):
    """Sub model for representing a student entry."""
    project = ndb.KeyProperty(kind=Project)
    name = ndb.StringProperty(indexed=True)
    value = ndb.IntegerProperty(indexed=False)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def obtain(cls, name, project):
        return cls.nget(name=name) or cls.create(project=project, name=name)

    @classmethod
    def nget(cls, name):
        query = cls.query(cls.name == name).fetch()
        return query and query[0]


class Person(ndb.Expando):
    """Sub model for representing an author."""
    name = ndb.StringProperty(indexed=True)
    identity = ndb.StringProperty(indexed=False)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def nget(cls, name):
        query = cls.query(cls.name == name).fetch()
        return query and query[0]

    @classmethod
    def obtain(cls, name):
        return Person.nget(name=name) or Person.create(name=name)


class Author(ndb.Model):
    """Sub model for representing an author."""
    project = ndb.KeyProperty(kind=Project)
    person = ndb.KeyProperty(kind=Person)
    school = ndb.StringProperty(indexed=False)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def nget(cls, project, person):
        query = cls.query(ndb.AND(cls.project == project, cls.person == person)).fetch()
        return query and query[0]

    @classmethod
    def obtain(cls, project, name, school=None):
        project_obj = Project.nget(name=project)
        person_obj = Person.obtain(name=name)
        # print(project_obj, person_obj, project, name, Project.query().fetch(), Projects.query().fetch())
        author_obj = project_obj and person_obj and Author.nget(
            project=project_obj.key, person=person_obj.key)
        return author_obj or Author.create(
            project=project_obj.key,
            person=person_obj.key,
            school=school
        )

    @classmethod
    def check(cls, project, name):
        project_obj = Project.nget(name=project)
        person_obj = Person.nget(name=name)
        return project_obj and project_obj or Author.nget(project=project_obj.key, person=person_obj.key)


class Session(ndb.Expando):
    """A main model for representing an individual Question entry."""
    _session = None
    project = ndb.KeyProperty(kind=Project)
    author = ndb.KeyProperty(kind=Author)
    name = ndb.StringProperty(indexed=True)
    updated = ndb.IntegerProperty(default=1, indexed=False)
    modified_date = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def check(cls, project, name):
        project_obj = Project.nget(name=project)
        person_obj = Person.nget(name=name)
        # author_obj = Author.nget(person=person_obj, project=project_obj)
        return project_obj and project_obj and Author.nget(project=project_obj.key, person=person_obj.key)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def post(cls, name, classifier, data, session):
        student = Student.obtain(name=name, classifier=classifier, authorkey=session.author)
        Entry.post(studentkey=student.key, data=data, session=session)

    @classmethod
    def instance(cls, project, author, school=None, questions=None):
        if cls._session and cls._session.check(project=project, name=author):
            print(cls._session, cls._session.updated)
            cls._session.updated += 1
            cls._session.put()
            return cls._session
        else:
            projectobj = Project.nget(name=project)
            author = Author.obtain(project=project, name=author)
            cls._session = Session.create(project=projectobj.key, author=author.key)
            if questions:
                cls._populate_questions(session=cls._session, questions=questions)

            return cls._session

    @classmethod
    def _populate_questions(cls, session, questions):
        prj = session.project.get()  # Project.kget(key=session.project)
        if prj.populated:
            return prj.questions
        oquestions = [
            Question.create(name=key, text=value) for key, value in questions
            ]
        print(oquestions)
        prj.populated = True
        prj.questions = oquestions
        prj.put()
        return oquestions


class Student(ndb.Model):
    """Sub model for representing a student entry."""
    author = ndb.KeyProperty(kind=Author)
    classifier = ndb.KeyProperty(kind=Classifier)
    person = ndb.KeyProperty(kind=Person)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def nget(cls, person, author):
        query = cls.query(ndb.AND(cls.person == person, cls.author == author)).fetch()
        return query and query[0]

    @classmethod
    def obtain(cls, name, classifier, authorkey):
        person_obj = Person.nget(name=name)
        return person_obj and Student.nget(person=Person.nget(name=name).key, author=authorkey) or Student.create(
            person=Person.obtain(name).key,
            classifier=Classifier.obtain(project=authorkey.get().project, name=name).key,
            author=authorkey
        )


class Sample(ndb.Model):
    """A main model for representing an individual Question entry."""
    project = ndb.KeyProperty(kind=Project)
    question = ndb.KeyProperty(kind=Question)
    value = ndb.IntegerProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class Entry(ndb.Model):
    """A main model for representing an individual Question entry."""
    student = ndb.KeyProperty(kind=Student)
    question = ndb.KeyProperty(kind=Question)
    value = ndb.IntegerProperty(indexed=False)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def post(cls, studentkey, data, session):
        for question, value in data.items():
            entry = Entry(
                student=studentkey, question=Question.nget(name=question).key, value=value)
            entry.put()


DB = Projects.instance()
