#  -*- coding: utf-8 -*-
"""

Author: Rafael R. L. Benevides
Date: 16/11/2021

"""


import numpy

from abc import ABCMeta, abstractmethod

from matplotlib import pyplot


class SignalInterpolation(metaclass=ABCMeta):

    # ========== ========== ========== ========== ========== class attributes
    ...

    # ========== ========== ========== ========== ========== special methods
    def __init__(self, x_samples, y_samples):
        self.__x_samples = numpy.array(x_samples).reshape(-1, )
        self.__y_samples = numpy.array(y_samples).reshape(-1, )

        assert len(self.x_samples) == len(self.y_samples)

    def __call__(self, x):
        return (self.y_samples @ self.pulses(x)).reshape(-1,)

    # ========== ========== ========== ========== ========== private methods
    ...

    # ========== ========== ========== ========== ========== protected methods
    ...

    # ========== ========== ========== ========== ========== public methods
    @abstractmethod
    def pulses(self, x):
        raise NotImplementedError()

    def plot_signal(self, x):
        figure, axes = pyplot.subplots()
        axes.plot(x, self(x), label='Interpolation')
        axes.plot(self.x_samples, self.y_samples, marker='o', linestyle='', label='Samples')
        axes.grid()
        axes.legend()

        return figure, axes

    def plot_pulses(self, x, *args, **kwargs):
        figure, axes = pyplot.subplots()

        for pulse in self.pulses(x):
            axes.plot(x, pulse, *args, **kwargs)

        axes.grid()

    # ---------- ---------- ---------- ---------- ---------- properties
    @property
    def x_samples(self):
        return self.__x_samples

    @property
    def y_samples(self):
        return self.__y_samples

    @property
    def n_samples(self):
        try:
            return self.__n_samples
        except AttributeError:
            self.__n_samples = len(self.x_samples)
            return self.__n_samples


class NyquistInterpolation(SignalInterpolation):

    # ========== ========== ========== ========== ========== class attributes
    ...

    # ========== ========== ========== ========== ========== special methods
    def __init__(self, y_samples, x_samples=None, period=None, rate=None, bandwidth=None):

        # ---------- ---------- ---------- ---------- ---------- parsing

        if x_samples is not None:
            super().__init__(x_samples, y_samples)

            period = self.x_samples[1:] - self.x_samples[:-1]

            std = period.std(ddof=0)
            if std != 0 and std/period.mean() > 1e-5:
                print(std/std.max())
                raise ValueError()

            self.__period = period.mean()

        else:

            if period:
                assert float(period) > 0, "sampling period must be a positive number"
                self.__period = float(period)

            elif rate:
                assert float(rate) > 0, "sampling rate must be a positive number"
                self.__period = 1 / float(rate)

            elif bandwidth:
                assert float(bandwidth) > 0, "bandwidth must be a positive number"
                self.__period = 1/2/float(bandwidth)

            else:
                error = "At least one option among 'ts', 'fs' and 'bandwidth' must be provided"
                raise ValueError(error)

            x_samples = numpy.arange(len(y_samples)) * self.period
            super(NyquistInterpolation, self).__init__(x_samples, y_samples)

    # ========== ========== ========== ========== ========== private methods
    ...

    # ========== ========== ========== ========== ========== protected methods
    ...

    # ========== ========== ========== ========== ========== public methods
    def pulses(self, x):

        x = numpy.array(x).reshape(1, -1)

        return numpy.sinc((x - self.x_samples.reshape(-1, 1))/self.period)

    # ---------- ---------- ---------- ---------- ---------- properties
    @property
    def period(self):
        return self.__period

    @property
    def rate(self):
        return 1 / self.period

    @property
    def bandwidth(self):
        return self.rate / 2


class SLInterpolation(SignalInterpolation):

    # ========== ========== ========== ========== ========== class attributes
    ...

    # ========== ========== ========== ========== ========== special methods
    def __init__(self, func, Cq=0, Cw=1, Wt=1, n_samples=10):

        n = 1 + numpy.arange(n_samples)

        x_samples = Cq/Cw + Cw*(numpy.pi / Wt)**2 * n**2
        y_samples = func(x_samples)

        super(SLInterpolation, self).__init__(x_samples, y_samples)

        self.Cq = Cq
        self.Cw = Cw
        self.Wt = Wt

    # ========== ========== ========== ========== ========== private methods
    ...

    # ========== ========== ========== ========== ========== protected methods
    ...

    # ========== ========== ========== ========== ========== public methods
    def pulses(self, x):

        lamb = numpy.array(x).reshape(1, -1)

        lamb_n = self.x_samples.reshape(-1, 1)

        def f(_lamb):
            return numpy.sqrt(_lamb * self.Cw - self.Cq) / self.Cw

        a = f(lamb) * self.Wt / numpy.pi
        b = f(lamb_n) * self.Wt / numpy.pi

        num = numpy.sinc(a - b) - numpy.sinc(a + b)
        den = numpy.sqrt((1 - numpy.sinc(2*a)) * (1 - numpy.sinc(2*b)))

        return num / den

    # ---------- ---------- ---------- ---------- ---------- properties
    ...