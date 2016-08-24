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

Verifica a funcionalidade do engenho neural.

"""
import unittest
from enplicaw.enplicaw import Wisard


class EnplicawTest(unittest.TestCase):

    def test_main(self):
        """garante que intância de Enplicaw é criada."""
        cls = "Iris-setosa Iris-versicolor Iris-virginica".split()
        bleacher = {"Iris-setosa": 9, "Iris-versicolor": 0, "Iris-virginica": 0}
        w = Wisard(22 * 4, bleach=579, mapper=bleacher, enf=10, sup=1)
        assert w is not None


if __name__ == '__main__':
    unittest.main()