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

"""Weightless neural network based on WISARD.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
from random import shuffle

__author__ = 'carlo'
RND = 3141
SBLEACH = 3
EBLEACH = 1
IBLEACH = 1


def tupler(x):
    return [(bit,) + tup for bit in (0, 1) for tup in tupler(x - 1)] if x else [(0,), (1,)]


class Cortex:
    """Neuron cortex with a collection of RAM nodes. :ref:`enplicaw`

    :param retinasize: dimension in pixels of the retina.
    :param bleach: bleaching factor at classify stage.
    :param ramorder: number of bits of the RAM address.
    """

    def __init__(self, retinasize=3 * 4, bleach=0, ramorder=2):
        self.cortex = [{(a, b): 0 for a in [0, 1] for b in [0, 1]} for _ in range(retinasize // 2)]
        self.bleach = bleach

    def learn(self, retina, offset=1):
        """Learn new patterns. :class:`lib.enplicaw.core.Cortex`

        :param retina: retina pixel vector to be learned.
        :param offset: ammount of offset to be added to RAM node at learning.
        """
        def updater(ram, index):
            return {index: self.cortex[ram][index] + offset}
        fixedretinasize = len(retina)
        [self.cortex[ram].update(updater(ram, (retina.pop(RND % len(retina)), retina.pop(RND % len(retina)))))
         for ram in range(fixedretinasize // 2)]
        # print(self.cortex)

    def classify(self, retina):
        """Classify a given pattern. :class:`lib.enplicaw.core.Cortex`

        :param retina: retina pixel vector to be classified.
        :return: vector of responding RAM node values.
        """
        retinasize = (len(retina) // 2)
        return ([self.cortex[ram][(retina.pop(RND % len(retina)), retina.pop(RND % len(retina)))] - self.bleach
                 for ram in range(retinasize)])


class Lobe:
    """Rede neural sem peso. :ref:`enplicaw`

    :param data: input data stream.
    :param topvalue: the largest value of any data.
    :param factor: retina reduction factor to speed up processing.
    :param ramorder: number obits adressing the RAM.
    :param enforce_supress: tuple with one value to offset leraning and a negative to suppress.
    :param bleach: dictionary of bleaches {classkey: bleach_value}
    """

    def __init__(self, data, topvalue, factor=1, ramorder=2, enforce_supress=(1, 0), bleach={k: 0 for k in range(6)}):
        self.retinasize, self.data = self.retinify(data, topvalue, factor)
        self.l, self.m, self.n = range(len(self.data))[::-1], range(len(self.data[0][0])), range(len(self.data[0]))
        l, m, n = self.l, self.m, self.n
        self.cortex = {key: Cortex(self.retinasize, bleacher) for key, bleacher in bleach.items()}
        self.enforce, self.supress = enforce_supress
        self.bleach = bleach
        self.cortex_keys = sorted(class_key for class_key in bleach.keys())
        self.sample_entries = [[[self.data[i][j][k] for k in m] for i in l] for j in n]

    @classmethod
    def retinify(cls, histogram_data, topvalue, factor=1):
        """ Formats a histogram into a histogram_data format. :class:`lib.enplicaw.core.Lobe`

        :param histogram_data: input data stream.
        :param topvalue: the largest value of any data.
        :param factor: retina reduction factor to speed up processing.
        :return: the size of the final histogram data and the histogram_data itself.
        """
        zfactor = 2 * factor
        TOP = topvalue // factor
        retinadata = {i: [[([0] * (1 * (j // zfactor))) + ([1] * (j // zfactor)) + ([0] * (TOP - (2 * (j // zfactor))))
                      for j in k] for k in d] for i, d in sorted(histogram_data.items())}
        retinasize = (sum(1 for j in retinadata[0][0] for i in j))
        return retinasize, retinadata

    def samplelearn(self, samplesize):
        """ Extract a sample of retina data for learning. :class:`lib.enplicaw.core.Lobe`

        :param samplesize: The amount of retinas to sample.
        :return:
        """
        data = self.sample_entries[:samplesize]
        self.learn(data)

    def learn(self, retinadata):
        """Learn patterns from a collection of retinas. :class:`lib.enplicaw.core.Lobe`

        :param retinadata: collection of retinas.
        """
        enf, sup, keys = self.enforce, self.supress, self.cortex_keys
        [self.cortex[2 - key].learn([i for j in retina for i in j],
                                    offset=enf if key == learnkey else sup) for retini in retinadata
         for key in keys for learnkey, retina in enumerate(retini)]

    def classifynlearn(self):
        """Classifies a batch of retina data, and attempt to online leanr from the best. :class:`lib.enplicaw.core.Lobe`

        :return: a colection of tuples of votes given from each discriminator.
        """
        def discriminate(retina, key):
            votes = sorted([(sum(self.cortex[2 - key].classify([i for j in retina for i in j])), key) for key in keys])
            confidence = (votes[-1][0] - max(0, votes[-2][0])) / (abs(votes[-1][0]) + 0.001)
            if max(votes)[1] != key:
                print(votes, confidence, 'become', max(votes)[1], 'but was', key)
            else:
                print(votes, confidence)

            if confidence > CONFIDENCE:
                self.cortex[votes[-1][1]].learn([i for j in retina for i in j], offset=self.enforce)
            return votes

        keys = self.cortex_keys
        return [[discriminate(retina, key) for key, retina in enumerate(retini)] for retini in self.sample_entries]

    def classify(self):
        """ A simple classification routine. :class:`lib.enplicaw.core.Lobe`

        :return: a colection of tuples of votes given from each discriminator.
        """
        keys = self.cortex_keys
        return [[
                sorted([(sum(self.cortex[2 - key].classify([i for j in retina for i in j])), key)
                        for key in keys]) for retina in retini
                ] for retini in self.sample_entries]

    def results(self):
        """ Compile confidences, hitsample lists. :class:`lib.enplicaw.core.Lobe`

        :return: accuracy performance in hits/total.
        """
        self.samplelearn(SAMPLESIZE)
        classifications = self.classifynlearn()
        confidences = [[(tup[-1][1], 100 * (tup[-1][0] - tup[-2][0]) // (abs(tup[-1][0]) + 0.01))
                        for tup in triade] for triade in classifications]
        hitsamples = [[1 if clsd[0] == real else 0 for clsd, real in zip(cl, (0, 1, 2))] for cl in confidences]
        total_hits = sum(1 for cl in confidences for clsd, real in zip(cl, (0, 1, 2)) if clsd[0] == real)
        print([sum(c[k][1] for c in confidences) / len(confidences) for k in range(3)],
              [100 * sum(tr) // (len(hitsamples)) for tr in zip(*hitsamples)])
        return 100 * total_hits // (len(hitsamples) * 3)


def main(data, sample=1):
    """ Main task, runs, leaning, classification, and report results. :class:`lib.enplicaw.core.Lobe`

    :param data: input data stream with all samples formatted as values tuples.
    :param sample: ammount of times that whole cicly will run.
    :return:
    """
    from time import time
    lobe = Lobe(data, 100, factor=4, enforce_supress=ENFSUP, bleach=BLEACH)
    timer = time()
    acc = [lobe.results() for _ in range(sample)]
    print("min: %d, max: %d, average; %d, elapset time %f" % (min(acc), max(acc), sum(acc) // sample, time() - timer))


CONFIDENCE = 2
SAMPLESIZE = 3
ENFSUP = (20, 0)
BLEACH = {0: 150, 1: 150, 2: 150}
DATA = '''
5.1,3.5,1.4,0.2,Iris-setosa
4.9,3.0,1.4,0.2,Iris-setosa
4.7,3.2,1.3,0.2,Iris-setosa
4.6,3.1,1.5,0.2,Iris-setosa
5.0,3.6,1.4,0.2,Iris-setosa
5.4,3.9,1.7,0.4,Iris-setosa
4.6,3.4,1.4,0.3,Iris-setosa
5.0,3.4,1.5,0.2,Iris-setosa
4.4,2.9,1.4,0.2,Iris-setosa
4.9,3.1,1.5,0.1,Iris-setosa
5.4,3.7,1.5,0.2,Iris-setosa
4.8,3.4,1.6,0.2,Iris-setosa
4.8,3.0,1.4,0.1,Iris-setosa
4.3,3.0,1.1,0.1,Iris-setosa
5.8,4.0,1.2,0.2,Iris-setosa
5.7,4.4,1.5,0.4,Iris-setosa
5.4,3.9,1.3,0.4,Iris-setosa
5.1,3.5,1.4,0.3,Iris-setosa
5.7,3.8,1.7,0.3,Iris-setosa
5.1,3.8,1.5,0.3,Iris-setosa
5.4,3.4,1.7,0.2,Iris-setosa
5.1,3.7,1.5,0.4,Iris-setosa
4.6,3.6,1.0,0.2,Iris-setosa
5.1,3.3,1.7,0.5,Iris-setosa
4.8,3.4,1.9,0.2,Iris-setosa
5.0,3.0,1.6,0.2,Iris-setosa
5.0,3.4,1.6,0.4,Iris-setosa
5.2,3.5,1.5,0.2,Iris-setosa
5.2,3.4,1.4,0.2,Iris-setosa
4.7,3.2,1.6,0.2,Iris-setosa
4.8,3.1,1.6,0.2,Iris-setosa
5.4,3.4,1.5,0.4,Iris-setosa
5.2,4.1,1.5,0.1,Iris-setosa
5.5,4.2,1.4,0.2,Iris-setosa
4.9,3.1,1.5,0.1,Iris-setosa
5.0,3.2,1.2,0.2,Iris-setosa
5.5,3.5,1.3,0.2,Iris-setosa
4.9,3.1,1.5,0.1,Iris-setosa
4.4,3.0,1.3,0.2,Iris-setosa
5.1,3.4,1.5,0.2,Iris-setosa
5.0,3.5,1.3,0.3,Iris-setosa
4.5,2.3,1.3,0.3,Iris-setosa
4.4,3.2,1.3,0.2,Iris-setosa
5.0,3.5,1.6,0.6,Iris-setosa
5.1,3.8,1.9,0.4,Iris-setosa
4.8,3.0,1.4,0.3,Iris-setosa
5.1,3.8,1.6,0.2,Iris-setosa
4.6,3.2,1.4,0.2,Iris-setosa
5.3,3.7,1.5,0.2,Iris-setosa
5.0,3.3,1.4,0.2,Iris-setosa
7.0,3.2,4.7,1.4,Iris-versicolor
6.4,3.2,4.5,1.5,Iris-versicolor
6.9,3.1,4.9,1.5,Iris-versicolor
5.5,2.3,4.0,1.3,Iris-versicolor
6.5,2.8,4.6,1.5,Iris-versicolor
5.7,2.8,4.5,1.3,Iris-versicolor
6.3,3.3,4.7,1.6,Iris-versicolor
4.9,2.4,3.3,1.0,Iris-versicolor
6.6,2.9,4.6,1.3,Iris-versicolor
5.2,2.7,3.9,1.4,Iris-versicolor
5.0,2.0,3.5,1.0,Iris-versicolor
5.9,3.0,4.2,1.5,Iris-versicolor
6.0,2.2,4.0,1.0,Iris-versicolor
6.1,2.9,4.7,1.4,Iris-versicolor
5.6,2.9,3.6,1.3,Iris-versicolor
6.7,3.1,4.4,1.4,Iris-versicolor
5.6,3.0,4.5,1.5,Iris-versicolor
5.8,2.7,4.1,1.0,Iris-versicolor
6.2,2.2,4.5,1.5,Iris-versicolor
5.6,2.5,3.9,1.1,Iris-versicolor
5.9,3.2,4.8,1.8,Iris-versicolor
6.1,2.8,4.0,1.3,Iris-versicolor
6.3,2.5,4.9,1.5,Iris-versicolor
6.1,2.8,4.7,1.2,Iris-versicolor
6.4,2.9,4.3,1.3,Iris-versicolor
6.6,3.0,4.4,1.4,Iris-versicolor
6.8,2.8,4.8,1.4,Iris-versicolor
6.7,3.0,5.0,1.7,Iris-versicolor
6.0,2.9,4.5,1.5,Iris-versicolor
5.7,2.6,3.5,1.0,Iris-versicolor
5.5,2.4,3.8,1.1,Iris-versicolor
5.5,2.4,3.7,1.0,Iris-versicolor
5.8,2.7,3.9,1.2,Iris-versicolor
6.0,2.7,5.1,1.6,Iris-versicolor
5.4,3.0,4.5,1.5,Iris-versicolor
6.0,3.4,4.5,1.6,Iris-versicolor
6.7,3.1,4.7,1.5,Iris-versicolor
6.3,2.3,4.4,1.3,Iris-versicolor
5.6,3.0,4.1,1.3,Iris-versicolor
5.5,2.5,4.0,1.3,Iris-versicolor
5.5,2.6,4.4,1.2,Iris-versicolor
6.1,3.0,4.6,1.4,Iris-versicolor
5.8,2.6,4.0,1.2,Iris-versicolor
5.0,2.3,3.3,1.0,Iris-versicolor
5.6,2.7,4.2,1.3,Iris-versicolor
5.7,3.0,4.2,1.2,Iris-versicolor
5.7,2.9,4.2,1.3,Iris-versicolor
6.2,2.9,4.3,1.3,Iris-versicolor
5.1,2.5,3.0,1.1,Iris-versicolor
5.7,2.8,4.1,1.3,Iris-versicolor
6.3,3.3,6.0,2.5,Iris-virginica
5.8,2.7,5.1,1.9,Iris-virginica
7.1,3.0,5.9,2.1,Iris-virginica
6.3,2.9,5.6,1.8,Iris-virginica
6.5,3.0,5.8,2.2,Iris-virginica
7.6,3.0,6.6,2.1,Iris-virginica
4.9,2.5,4.5,1.7,Iris-virginica
7.3,2.9,6.3,1.8,Iris-virginica
6.7,2.5,5.8,1.8,Iris-virginica
7.2,3.6,6.1,2.5,Iris-virginica
6.5,3.2,5.1,2.0,Iris-virginica
6.4,2.7,5.3,1.9,Iris-virginica
6.8,3.0,5.5,2.1,Iris-virginica
5.7,2.5,5.0,2.0,Iris-virginica
5.8,2.8,5.1,2.4,Iris-virginica
6.4,3.2,5.3,2.3,Iris-virginica
6.5,3.0,5.5,1.8,Iris-virginica
7.7,3.8,6.7,2.2,Iris-virginica
7.7,2.6,6.9,2.3,Iris-virginica
6.0,2.2,5.0,1.5,Iris-virginica
6.9,3.2,5.7,2.3,Iris-virginica
5.6,2.8,4.9,2.0,Iris-virginica
7.7,2.8,6.7,2.0,Iris-virginica
6.3,2.7,4.9,1.8,Iris-virginica
6.7,3.3,5.7,2.1,Iris-virginica
7.2,3.2,6.0,1.8,Iris-virginica
6.2,2.8,4.8,1.8,Iris-virginica
6.1,3.0,4.9,1.8,Iris-virginica
6.4,2.8,5.6,2.1,Iris-virginica
7.2,3.0,5.8,1.6,Iris-virginica
7.4,2.8,6.1,1.9,Iris-virginica
7.9,3.8,6.4,2.0,Iris-virginica
6.4,2.8,5.6,2.2,Iris-virginica
6.3,2.8,5.1,1.5,Iris-virginica
6.1,2.6,5.6,1.4,Iris-virginica
7.7,3.0,6.1,2.3,Iris-virginica
6.3,3.4,5.6,2.4,Iris-virginica
6.4,3.1,5.5,1.8,Iris-virginica
6.0,3.0,4.8,1.8,Iris-virginica
6.9,3.1,5.4,2.1,Iris-virginica
6.7,3.1,5.6,2.4,Iris-virginica
6.9,3.1,5.1,2.3,Iris-virginica
5.8,2.7,5.1,1.9,Iris-virginica
6.8,3.2,5.9,2.3,Iris-virginica
6.7,3.3,5.7,2.5,Iris-virginica
6.7,3.0,5.2,2.3,Iris-virginica
6.3,2.5,5.0,1.9,Iris-virginica
6.5,3.0,5.2,2.0,Iris-virginica
6.2,3.4,5.4,2.3,Iris-virginica
5.9,3.0,5.1,1.8,Iris-virginica
'''.split()
MAP = {"Iris-virginica": 0, "Iris-versicolor": 1, "Iris-setosa": 2}
SDATA = {0: [], 1: [], 2: []}
[SDATA[MAP[r.split(",")[-1]]].append([int(float(d) * 10)
                                      for d in r.split(",")[:-1]]) for r in DATA]

if __name__ == '__main__':
    main(SDATA)
