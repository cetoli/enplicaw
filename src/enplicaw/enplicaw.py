# -*- coding: UTF8 -*-
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

from random import shuffle, random
import operator
from constants import PRIMES, DATA

__author__ = 'carlo'
__version__ = "0.2.0"
RND = 3141
SBLEACH = 3
EBLEACH = 1
IBLEACH = 1
FATOR = 1
ZFATOR = 2  # 2 * FATOR
TOP = 50 // FATOR
ZO = 3


def tupler(x):
    return [(bit,) + tup for bit in (0, 1) for tup in tupler(x - 1)] if x else [(0,), (1,)]


class Wisard:
    """Rede neural sem peso. :ref:`wisard'
    """

    def __init__(self, retinasize=3 * 4, bleach=0, mapper={i: i for i in range(4)}, enf=1, sup=0):
        self.bleacher, self.enf, self.sup = mapper, enf, sup
        self.clazzes = list(mapper.keys())
        # self.cortex = [{t: 0 for t in tupler(ramorder-1)} for _ in range(retinasize//2)]
        self.cortex = {key: [{(a, b): 0 for a in [0, 1] for b in [0, 1]} for _ in range(retinasize // 2)]
                       for key in mapper.keys()}
        self.auto_bleach = {key: 1 for key in mapper.keys()}
        self.bleach = bleach

    def update_balance(self):
        for clazz in self.clazzes:
            auto = sum(next(ram.values() for ram in self.cortex[clazz]))
            print(clazz, auto)
            self.auto_bleach[clazz] = auto if auto else 1
        return None

    def learn_samples(self, samples):
        return len([self.learn(s[1], self.retinify(s[2:])) for s in samples if s[1]])

    def retinify_samples(self, samples):
        [self.retinify(sample[2:]) for sample in samples]

    @staticmethod
    def retinify(retina, threshold=32, band=8, zoom=4):
        def retinate(value, pix=0, bnd=0):
            return [pix] * int(float(bnd + (1 - pix) * value) * zoom // ZFATOR)

        def deretinate(value, pix=0):
            return [pix] * (TOP - (band + int(float(value) * zoom // ZFATOR)))

        # print(retina, [(int(float(ZO * v) // ZFATOR), (TOP - (2 * int(float(ZO * v) // ZFATOR)))) for v in retina])
        retina = [
            (retinate(value) + retinate(value, 1, band) + deretinate(value))[:threshold]
            for value in retina]
        return [pix for line in retina for pix in line]

    @staticmethod
    def sense_domain(data):
        def updater(lobe, index, off):
            return {index: lobe[index] + off}
        data = [[float(p) for p in line.split(",")[:-1]] for i, line in enumerate(data)]

        retina = Wisard.retinify(data[0])
        lobe = [{(a, b): 0 for a in [0, 1] for b in [0, 1]} for _ in range(len(retina) // 2)]
        master_retina = [0 for line in range(len(retina))]
        for sample in data:
            retina = Wisard.retinify(sample)
            [master_retina.__setitem__(pix, master_retina[pix]+retina[pix]) for pix in range(len(master_retina))]
            [neuron.update(
                updater(neuron, (retina.pop(RND % len(retina)), retina.pop(RND % len(retina))), 1))
             for neuron in lobe]
        domain = list(set(master_retina[:]))
        domain.sort()
        domain = [(tre, sum(1 for pix in master_retina if tre == pix)) for tre in domain]
        print(domain, len(master_retina), len(data), len(data[0]), sum(dm[1] for dm in domain[1:-1]))
        domain = list(set([val for neuron in lobe for val in neuron.values()]))
        domain.sort()
        domain = [(tre, sum(1 for neuron in lobe for val in neuron.values() if tre == val)) for tre in domain]
        print(domain, len(lobe), sum(dm[1] for dm in domain[1:-1])), sum(dm[0] for dm in domain[1:-1])
        cutter = sum(dm[0]*dm[1] for dm in domain[1:-1])//2
        lower_half = []
        higher_half = []
        wheighted_sum = 0
        for wheight, count in domain[1:-1]:
            if wheighted_sum > cutter:
                break
            wheighted_sum += wheight * count
            [lower_half.append(neuron) if wheighted_sum < cutter else higher_half.append(neuron) for neuron in lobe
             if any(neuron[(a, b)] == wheight for a in [0, 1] for b in [0, 1])]
        print(cutter, len(lower_half), len(higher_half), wheighted_sum)

        show([1 if pix == 3 else 0 for pix in master_retina])
        return {"l": lower_half, "h": higher_half}

    def unsupervised_learn(self, data):
        clazzes = self.sense_domain(data)
        self.cortex = clazzes
        self.bleacher = {key: 0 for key in clazzes.keys()}
        data = [[i, line.split(",")[-1]] + [float(p) for p in line.split(",")[:-1]] for i, line in enumerate(data)]
        result = self.classify_samples(data=data)
        for line in result:
            print(line)

    def learn(self, clazz, master_retina):
        def updater(lobe, index, off):
            return {index: lobe[index] + off}

        # if random() > 0.6:
        #     return
        clazzes = self.clazzes
        shuffle(clazzes)
        for cls in clazzes:
            retina = master_retina[:]
            [lobe.update(
                updater(lobe, (retina.pop(RND % len(retina)), retina.pop(RND % len(retina))),
                        self.enf if cls == clazz else self.sup if cls != "N" else 0))
             for lobe in self.cortex[cls] if len(retina)]

    def classify_samples(self, data):
        return [(s[0], s[1], self.classify(self.retinify(s[2:]))) for s in data]

    def classify(self, retina):
        def calculate_for_claz(lobe, clazz):
            uma_retina = retina[:]
            bleach = 0  # min(self.auto_bleach.values())
            auto = 0  # (self.auto_bleach[clazz]-bleach)/1.9
            return sum(
                neuron[(uma_retina.pop(RND % len(uma_retina)), uma_retina.pop(RND % len(uma_retina)))]
                - self.bleach - bleach - self.bleacher[clazz] - auto for neuron in lobe if len(uma_retina))

        return {clazz: calculate_for_claz(lobe, clazz) for clazz, lobe in self.cortex.items()}


def show(retina):
    for i in range(len(retina)//32):
        print("".join([str(retina[j + 32 * i]) for j in range(32)]))
    return


def _run(data):
    bleacher = dict(V=20, S=24, E=34, F=2)
    w = Wisard(32 * 32, bleach=28, mapper=bleacher, enf=22, sup=4)
    # bleacher = dict(V=60, S=0, E=8, F=15)
    # w = Wisard(32 * 32, bleach=62, mapper=bleacher, enf=11, sup=2)
    # bleacher = dict(V=29, S=-4, E=4, F=4)
    # bleacher = dict(V=0, S=0, E=0, F=0)
    # w = Wisard(32 * 64, bleach=0, mapper=bleacher, enf=11, sup=2)
    # show(w.retinify(data[0][2:]))
    # return
    w.learn_samples(data[:8])
    w.update_balance()
    res = w.classify_samples(data)
    return res


def run(data):
    cls = "Iris-setosa Iris-versicolor Iris-virginica".split()
    bleacher = {"Iris-setosa": 9, "Iris-versicolor": 3, "Iris-virginica": 4}
    w = Wisard(22 * 4, bleach=502, mapper=bleacher, enf=10, sup=1)
    # show(w.retinify(data[0][2:]))
    # return
    w.learn_samples(data)
    res = w.classify_samples(data)
    return res


def main(data):
    global RND
    cls = "U Iris-setosa Iris-versicolor Iris-virginica".split()
    data = [[i, line.split(",")[-1]] + [float(p) for p in line.split(",")[:-1]] for i, line in enumerate(data)]
    tot = {u[0]: {key: 0 if key != "U" else str(u[0]) + " " + str(u[1]) for _, key in enumerate(cls)} for u in data}
    primes = PRIMES[:]
    for _ in range(1):
        shuffle(data)
        RND = primes.pop()
        res = run(data)
        [tot[line[0]].update({cl: tot[line[0]][cl] + s for cl, s in line[2].items()}) for line in res]
    total = list(tot.keys())
    total.sort()
    total_conf = 0
    for line in total:
        val = dict(tot[line])
        user = val.pop("U").split()[-1]
        val = list(val.items())
        # print(val)
        val.sort(key=operator.itemgetter(1), reverse=True)
        first, sec = val[0][1], val[1][1]
        conf = min(100 * abs(first - sec) // abs(first), 100)
        conf = conf if (user == val[0][0]) or ("e" == user) else -conf
        # conf = 100 * abs(first-sec) // max(abs(first), abs(sec))
        # conf = 100 * (max(first, 0)-max(sec, 0)) // first
        total_conf += conf
        print(tot[line]["U"] + "  " + "".join(["%s:%8.0f " % (a[-3:], b) for a, b in val]), "conf: %d" % conf)
        # print("{U}: {tot}".format(result))
    print("total confidence %d" % (total_conf // len(total)))
    return


def _main(_):
    global RND
    data = Learn().build_with_User_table_for_prog()
    data = [line[:2] + [float(t) - float(t0) + 10 for t, t0 in zip(line[3:32], line[2:32])] for line in data]
    print("Tabela gerada por rede neural sem peso para derivada segunda do tempo com prognóstico da carla")
    tot = {u[0]: {key: 0 if key != "U" else str(u[0]) + " " + str(u[1]) for _, key in enumerate("VSEFU")} for u in data}
    primes = PRIMES[:]
    for _ in range(1):
        # shuffle(data)
        RND = primes.pop()
        res = run(data)
        [tot[line[0]].update({cl: tot[line[0]][cl] + s for cl, s in line[2].items()}) for line in res]
    total = list(tot.keys())
    total.sort()
    total_conf = 0
    total_sec = 0
    for line in total:
        val = dict(tot[line])
        user = val.pop("U")[-1:]
        val = list(val.items())
        # print(val)
        val.sort(key=operator.itemgetter(1), reverse=True)
        first, sec, third = val[0][1], val[1][1], val[2][1]
        conf = min(100 * abs(first - sec) // abs(first), 100) if (user == val[0][0]) or ("e" == user) else 0
        secd = min(abs(sec // first) * conf, 100)  # if (user == val[0][0]) or ("e" == user) else 0
        # conf = 100 * abs(first-sec) // max(abs(first), abs(sec))
        # conf = 100 * (max(first, 0)-max(sec, 0)) // first
        total_conf += conf
        total_sec += secd
        # print(tot[line]["U"] + "  " + "".join(["%s:%8.0f " % (a[-3:], b) for a, b in val]), "conf: %d" % conf)
        print("{name: >42} {val} conf: {conf}".format(name=tot[line]["U"],
                                                      val="".join(["%s:%8.0f " % (a[-3:], b) for a, b in val]),
                                                      conf=conf))
        out_form = "{name: >42} classe original: {era} pri: {prim}  1ªconf: {conf: >3}% sec: {sec} 2ªconf: {csec: >3}%"
        name = " ".join(tot[line]["U"].split()[:-1])
        era = tot[line]["U"].split()[-1][0]
        # print(out_form.format(name=name, era=era, prim=val[0][0], conf=conf, sec=val[1][0], csec=secd))
        # print("{U}: {tot}".format(result))
    print("total confidence %d" % (total_conf // len(total)))
    return


if __name__ == '__main__':
    # main(DATA)
    Wisard.sense_domain(DATA)
    Wisard().unsupervised_learn(DATA)
