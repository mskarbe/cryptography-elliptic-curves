import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List

from types import EllipticCurve, Point
from elapse_time import elapseTimeWithResult
from ec_multiplication import toBinary, doubleAndAddBase, pointMultiplication
from curves import getCurve, ELLIPTIC_CURVES

# class for calculating common statistics results from any list
@dataclass
class MeasurementsProps:
    data: list
    name: str = "undefined"
    standardDeviation: float = field(init=False)
    mean: float = field(init=False)
    variance: float = field(init=False)
    median: float = field(init=False)
    max: float = field(init=False)
    min: float = field(init=False)

    def __post_init__(self):
        self.standardDeviation = np.std(self.data)
        self.mean = np.mean(self.data)
        self.variance = np.var(self.data)
        self.median = np.median(self.data)
        self.max = np.amax(self.data)
        self.min = np.amin(self.data)

    def __str__(self):
        return f'- {self.name} {("".join(["-" for _ in range(80-len(self.name))]))} \n\tstandard deviation: {self.standardDeviation} \n\tvariance: {self.variance} \n\tarithmetic mean: {self.mean} \n\tmedian: {self.median} \n\tmaximum: {self.max} \n\tminimum: {self.min} \n'


def measureDoubleAndAdd(ec: EllipticCurve, scalars: List):
    dataTitleMult = "Multiplicant"
    dataTitleMultBin = "Multiplicant (bin)"
    dataTitleMlTime = "Montgomery Ladder time"
    dataTitleDaaTime = "Standard DAA time"
    dataTitleResultEq = "Results equal"
    # array for data collection
    data = {
        dataTitleMult: [],
        dataTitleMultBin: [],
        dataTitleMlTime: [],
        dataTitleDaaTime: [],
        dataTitleResultEq: [],
    }

    for r in scalars:
        rBin = toBinary(r)
        daa = elapseTimeWithResult(doubleAndAddBase, ec, rBin)
        ml = elapseTimeWithResult(pointMultiplication, ec, rBin)
        # save data
        data[dataTitleMult].append(r)
        data[dataTitleMultBin].append(rBin)
        data[dataTitleMlTime].append(ml[1])
        data[dataTitleDaaTime].append(daa[1])
        data[dataTitleResultEq].append(daa[0] == ml[0])

    # pandas data frame for pretty print table
    pd.set_option("display.width", 140)
    df = pd.DataFrame(data)
    # results computation
    mlMeasurementsResults = MeasurementsProps(
        name="Montgomery Ladder Timing", data=data[dataTitleMlTime]
    )
    daaMeasurementsResults = MeasurementsProps(
        name="Standard Double-and-add Timing", data=data[dataTitleDaaTime]
    )

    dashes = "".join(["=" for _ in range(40 - len(ec.name) // 2)])
    print(
        dashes,
        "Curve: ",
        ec.name,
        ", samples bit size: ",
        len(toBinary(scalars[0])),
        dashes,
    )
    print(mlMeasurementsResults)
    print(daaMeasurementsResults)
    print(df)
    print()


# data samples: 30 primes from different bit-length ranges
primes1 = [
    11731,
    11743,
    11777,
    11779,
    11783,
    11789,
    11801,
    11807,
    11813,
    11821,
    11827,
    11831,
    11833,
    11839,
    11863,
    11867,
    11887,
    11897,
    11903,
    11909,
    11923,
    11927,
    11933,
    11939,
    11941,
    11953,
    11959,
    11969,
    11971,
    11981,
]

primes2 = [
    284059,
    284083,
    284093,
    284111,
    284117,
    284129,
    284131,
    284149,
    284153,
    284159,
    284161,
    284173,
    284191,
    284201,
    284227,
    284231,
    284233,
    284237,
    284243,
    284261,
    284267,
    284269,
    284293,
    284311,
    284341,
    284357,
    284369,
    284377,
    284387,
    284407,
]

primes3 = [
    14837491,
    14837503,
    14837513,
    14837519,
    14837527,
    14837533,
    14837539,
    14837551,
    14837587,
    14837591,
    14837593,
    14837609,
    14837653,
    14837657,
    14837663,
    14837677,
    14837681,
    14837687,
    14837707,
    14837723,
    14837743,
    14837789,
    14837807,
    14837839,
    14837857,
    14837861,
    14837873,
    14837891,
    14837897,
    14837899,
]


ecBp256 = getCurve(ELLIPTIC_CURVES.bp256.value)
ecBp512 = getCurve(ELLIPTIC_CURVES.bp512.value)

measureDoubleAndAdd(ecBp256, primes1)
measureDoubleAndAdd(ecBp512, primes1)
measureDoubleAndAdd(ecBp256, primes2)
measureDoubleAndAdd(ecBp512, primes2)
measureDoubleAndAdd(ecBp256, primes3)
measureDoubleAndAdd(ecBp512, primes3)
