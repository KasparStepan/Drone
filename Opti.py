import Airplane_class
from PostPro import PostPro
import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import FloatRandomSampling


class PlaneOpti(ElementwiseProblem):
          def __init__(self):
                  super().__init__(n_var=2,
                         n_obj=2,
                         n_ieq_constr=1,
                         xl=np.array([0.1,0.1,0.075,0.05,0.01]),
                         xu=np.array([0.4,0.4,0.25,0.175,0.075]))
                  
          def _evaluate(self, x, out):
                              chord = { #m
                                    'Main_root':x[2],#0.15,
                                    'Main_mid_center': x[2],#0.15,
                                    'Main_end_center': x[3],#0.13,
                                    'Main_tip':x[4],
                                    'Tail_root':0.13,
                                    'Tail_tip':0.05 
                                    }

                              wingspan = { #m
                                    'Main_mid':x[0],
                                    'Main_center':x[1],
                                    'Main_tip':0.15,
                                    'Tail':0.1}



                              sweep_angle = { #deg
                                    "Main_root": 0,
                                    "Main_center" : 0,
                                    'Main_tip':10,
                                    "Tail": 0,    
                              }

                              dihedral_angle = { #deg
                                    "Main_root": 0,
                                    "Main_center" : 0,
                                    'Main_tip':10,
                                    "Tail": 60,
                              }

                              twist = { #deg
                                    'Main_root':0,
                                    'Main_mid_center': 0,
                                    'Main_end_center': 0,
                                    'Main_tip':0,
                                    'Tail_root':-5,
                                    'Tail_tip':-5,
                              }

                              fuselage_radius = { #m
                                    'Big':0.015,
                                    'Small':0.01
                              }

                              airplane_length = 0.7 #m


                              endurance_plane = Airplane_class.Airplane(name = "Endurance plane",airplane_type="Endurance",wingspan=wingspan,chord=chord,twist=twist,sweep_angle=sweep_angle,dihedral_angle=dihedral_angle,fuselage_radius=fuselage_radius,airplane_length=airplane_length)
                              speed_plane = Airplane_class.Airplane(name = "Speed plane",airplane_type="Speed",wingspan=wingspan,chord=chord,twist=twist,sweep_angle=sweep_angle,dihedral_angle=dihedral_angle,fuselage_radius=fuselage_radius,airplane_length=airplane_length)

                              

                              endurance_plane.runVLM()
                              speed_plane.runVLM()

                              f1 = 1/np.max(endurance_plane.aero_data['efficiency'])
                              f2 = 1/np.max(speed_plane.aero_data['efficiency'])

                              g1 = (x[0]+x[1]+wingspan['Main_tip'])-0.75
                              

                              out["F"] = [f1, f2]
                              out["G"] = [g1]


problem = PlaneOpti()
termination = get_termination("n_gen",40)
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
'''
post = PostPro()
post.add_plane(endurance_plane.aero_data,label=endurance_plane.name)
post.add_plane(plane_data=speed_plane.aero_data,label=speed_plane.name)

post.plot_results()
'''