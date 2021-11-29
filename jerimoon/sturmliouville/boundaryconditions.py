#  -*- coding: utf-8 -*-
"""

Author: Rafael R. L. Benevides
Date: 22/11/2021

"""


import numpy

from jerimoon.utils import parse_float


class BoundaryCondition:
    """
    Abstraction for conditions of the form

    a*y(x) + b*y'(x) = c

    where a, b and c are real numbers

    """

    # ========== ========== ========== ========== ========== class attributes
    ...

    # ========== ========== ========== ========== ========== special methods
    def __init__(self, x, a=1, b=0, c=0, theta=None):

        self.__x = parse_float(x)
        self._parse_theta_and_c(a, b, c, theta)

    def __copy__(self):
        return type(self)(self.x, theta=self.theta, c=self.c)

    def __repr__(self):

        if self.sin_theta == 0:
            return f"Boundary Condition: y({self.x:.4g}) = {self.c:.4g}"

        if self.sin_theta == 1:
            return f"Boundary Condition: y'({self.x:.4g}) = {self.c:.4g}"

        if self.sin_theta > 0:
            return f"Boundary Condition: {self.cos_theta:.4g}*y({self.x:.4g}) + {self.sin_theta:.4g}*y'({self.x:.4g}) = {self.c:.4g}"

        return f"Boundary Condition: {self.cos_theta:.4g}*y({self.x:.4g}) - {-self.sin_theta:.4g}*y'({self.x:.4g}) = {self.c:.4g}"

    # ========== ========== ========== ========== ========== private methods
    ...

    # ========== ========== ========== ========== ========== protected methods
    def _parse_theta_and_c(self, a, b, c, theta):

        if theta is not None:
            self.__theta = parse_float(theta)
            assert -numpy.pi/2 < self.__theta <= numpy.pi/2, f"Expected -pi/2 < theta <= pi/2. Given {theta}"
            self.__c = parse_float(c)

        else:
            a, b, c = parse_float(a), parse_float(b), parse_float(c)

            if a == 0:
                if b == 0:
                    error = "'a' and 'b' can not be both zero"
                    raise ValueError(error)

                self.__theta = numpy.pi / 2
                self.__c = c / b

            else:
                self.__theta = numpy.arctan(b / a)
                self.__c = (numpy.cos(self.__theta) / a) * c

    @classmethod
    def _equals_zero(cls, value):
        return numpy.abs(value) < 1e-14

    # ========== ========== ========== ========== ========== public methods
    def is_homogeneous(self):
        return self.c == 0

    def is_dirichlet(self):
        return self.theta == 0

    def is_neumann(self):
        return self.theta == numpy.pi/2

    def is_mixed(self):
        return not self.is_dirichlet() and not self.is_neumann()

    def get_homogenous_copy(self):
        return type(self)(self.x, theta=self.theta, c=0)

    def get_nonhomogeneous_copy(self, c):
        return type(self)(self.x, theta=self.theta, c=parse_float(c))

    # ---------- ---------- ---------- ---------- ---------- properties
    @property
    def x(self):
        return self.__x

    @property
    def theta(self):
        return self.__theta

    @property
    def c(self):
        return self.__c

    @property
    def cos_theta(self):

        try:
            return self.__cos_theta

        except AttributeError:
            self.__cos_theta = 0.0 if self.theta == numpy.pi/2 else numpy.cos(self.theta)

            return self.__cos_theta

    @property
    def sin_theta(self):

        try:
            return self.__sin_theta

        except AttributeError:
            self.__sin_theta = numpy.sin(self.theta)

            return self.__sin_theta

    @property
    def tan_theta(self):

        try:
            return self.__tan_theta

        except AttributeError:
            self.__tan_theta = numpy.inf if self.theta == numpy.pi/2 else numpy.tan(self.theta)

            return self.__tan_theta


class RegularSLProblem:

    def __init__(self, domain):
        pass


