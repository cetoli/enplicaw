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

"""
############################################################
Enplicaw - Pacote Cliente
############################################################

Define a função main do módulo superpython, criando uma instância de Enplicaw.

"""
__version__ = "0.1.0"
from .core import Enplicaw
import os
#  IS_GAE = os.environ['SERVER_SOFTWARE'].startswith('Development')
IS_GAE = os.environ.get('SERVER_SOFTWARE') and os.environ['SERVER_SOFTWARE'].startswith('Development')


def main(doc, svg=None):
    print('Enplicaw '+__version__)
    enplicaw = Enplicaw(doc)
    return enplicaw
