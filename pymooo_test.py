
import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import ElementwiseProblem, Problem
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling

class MyProblem(ElementwiseProblem):
          def __init__(self):
                    super().__init__(n_var=2,
                         n_obj=2,
                         n_ieq_constr=2,
                         xl=np.array([-2,-2]),
                         xu=np.array([2,2]))

          def _evaluate(self, x, out, *args, **kwargs):
                              f1 = 100 * (x[0]**2 + x[1]**2)
                              f2 = (x[0]-1)**2 + x[1]**2

                              g1 = 2*(x[0]-0.1) * (x[0]-0.9) / 0.18
                              g2 = - 20*(x[0]-0.4) * (x[0]-0.6) / 4.8

                              out["F"] = [f1, f2]
                              out["G"] = [g1, g2]

problem = MyProblem()
termination = get_termination("n_gen", 150)
algorithm = NSGA2(
    pop_size=100,
    n_offsprings=10,
    sampling=FloatRandomSampling(),
    eliminate_duplicates=True
)

res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True)

X = res.X
F = res.F

ideal = F.min(axis=0)
nadir = F.max(axis=0)

nF = (F-ideal)/(nadir-ideal)

fl=nF.min(axis=0)
fu=nF.max(axis=0)
print(f"Scale f1: [{fl[0]}, {fu[0]}]")
print(f"Scale f2: [{fl[1]}, {fu[1]}]")

from pymoo.decomposition.asf import ASF
weights = np.array([0.2,0.8])
decomp = ASF()

i = decomp.do(nF, 1/weights).argmin()

import matplotlib.pyplot as plt
print("Best regarding ASF: Point \ni = %s\nF = %s" % (i, F[i]))

plt.figure(figsize=(7, 5))
plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
plt.scatter(F[i, 0], F[i, 1], marker="x", color="red", s=200)
plt.title("Objective Space")
plt.show()

