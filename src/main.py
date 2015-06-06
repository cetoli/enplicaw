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

"""Main.py is the top level script.

Loads the Bottle framework and mounts controllers.  Also adds a custom error
handler.
"""
from lib import bottle
from lib.bottle import Bottle, view, request, response
# name and list your controllers here so their routes become accessible.
from server.controllers import main_controller
import collections
LIKERT = "nunca pouquíssimo pouco mediano, muito, muitíssimo sempre".split()
Item = collections.namedtuple('Item', 'label value')
Likert = collections.namedtuple('Item', 'label name value')
TITLE = "Enquete de Habilidades de Alunos - %s"
PICTURE = "https://dl.dropboxusercontent.com/u/1751704/igames/img/superp%C3%BDthon.jpg"
PROJECTS = "jardim spy super geo".split()
# Enable debugging, which gives us tracebacks
bottle.DEBUG = True

# Run the Bottle wsgi application. We don't need to call run() since our
# application is embedded within an App Engine WSGI application server.
bottle = Bottle()

# Mount a new instance of bottle for each controller and URL prefix.
bottle.mount("/pontos", main_controller.bottle)
# bottle.mount("/projeto", project_controller.bottle)
# bottle.mount("/pontos", pontos_controller.bottle)



@bottle.get('/')
@view('index')
def home():
    """ Return Hello World at application root URL"""
    ident = [dict(label="Nome", name="name"), dict(label="Escola", name="school")]
    project = request.urlparts.geturl().split('/')[2].split('.')[0]
    if project in PROJECTS:
            response.set_cookie('_enplicaw_project_', project)
    else:
        project = "SuperPython"
        response.set_cookie('_enplicaw_project_', project)

    #  items = [[Item(name='projeto %d' % (a*4+b), picture=PICTURE) for a in range(4)] for b in range(4)]
    # items = [Item(name='projeto %d' % (a*4+b), picture=PICTURE) for a in range(4) for b in range(4)]
    return dict(title=TITLE % project, image=PICTURE, identification=ident, submit="Enviar")


@bottle.post('/identify')
@view('survey')
def survey():
    """ Return Hello World at application root URL"""
    project = "SuperPython"
    username = request.forms.get('name')
    password = request.forms.get('school')

    survey = [Likert(label=question, name=qname, value=LIKERT) for qname, question in QUESTION]
    return dict(title=TITLE % project, columns=len(LIKERT), survey=survey, submit="Enviar")


@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'

QUESTION = """O aluno demonstra prazer em realizar ou planejar quebra-cabeças e problemas em forma de jogos.
O aluno tem coordenação, agilidade para participar de exercícios e jogos.
O aluno põe em prática os conhecimentos adquiridos.
Demonstra realizar com acerto e aperfeiçoar cada vez mais tudo que faz.
Sente prazer em superar obstáculos ou tarefas difíceis.
O aluno dirige sua atenção para fazer coisas novas do que para o que já conhece.
Mantém e defende suas próprias ideias.
Demonstra não precisar de ajuda para se desincumbir das atividades.
O aluno faz atividades a mais do que foram pedidos.
O aluno não precisa de muito tempo para produzir ideias novas.
Faz contatos sociais e inicia conversas com facilidade; faz amigos facilmente.
Perceber o que seus colegas são capazes de fazer e orientá-los para que utilizem esta capacidade nos trabalhos do próprio grupo.
Demonstra saber chegar ao término do pensamento, problema etc.
Ideias novas e diferentes com facilidade (FLEXIVEL).
Usa métodos novos, combina ideias, cria produtos diferentes.
Produz, inventa suas próprias respostas, encontrando soluções originais.
Analisa e julga trabalhos artísticos.
Produz ideias e faz associações.
Emite opinião pensada e refletida.
Não precisa de muito tempo para produzir o novo.
Usa objetos com função definida de diferentes maneiras.
Concatena, relaciona, deduz e demonstra.
Pergunta assuntos corriqueiros e diferentes ligados à física, astronomia, filosofia e outros.
Demonstra verbalmente ideias novas e diferentes através de histórias, solução de problemas, elaboração de textos e objetos.""".split("\n")
QUESTION = [("q%d" % item, question) for item, question in enumerate(QUESTION)]
