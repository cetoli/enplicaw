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
Enplicaw - Teste
############################################################

Verifica a funcionalidade do cliente web.

"""
import unittest
from client.enplicaw.core import Enplicaw
from client.enplicaw import main


class EnplicawTest(unittest.TestCase):

    def setUp(self):

        class Gui(object):
            def __init__(self, x=0):
                self.svg = None
                self.html = None
                self.ajax = None


            def __getitem__(self, x):
                return self

            def __le__(self, *x):
                pass

            def setAttribute(self, *x):
                self.opacity = 0.5

            def image(self, *x, **kw):
                return self

            def svg(self, *x, **kw):
                return self
       
        self.gui = Gui()
        self.app = Enplicaw(self.gui)

    def test_main(self):
        """garante que intância de Enplicaw é criada."""
        sp = main(self.gui)
        assert sp is not None


if __name__ == '__main__':
    unittest.main()