import aerosandbox as asb
import aerosandbox.numpy as np
from aerosandbox.library import airfoils



#Fluid properties
density = 1.225
viscosity = 1.81e-5
xyz_ref = [0,0,0]

    
    
op_point = asb.OperatingPoint(
    atmosphere=asb.Atmosphere(altitude=0),
    velocity=91.3,  # m/s
    )


airplane = asb.Airplane(
    name = "SKD",
    xyz_ref = [0,0,0],
    s_ref = 9, #Reference area
    c_ref = 0.9, #Reference chord
    b_ref = 10, #Reference span
    


    wings=[
        asb.Wing(
            name = "Main wing",
            xyz_le=[0, 0, 0],
            symmetric=True,
            xsecs=[# The wing's cross ("X") sections, or "XSecs"
                asb.WingXSec(#Root
                    xyz_le = [0.1,0,0],
                    chord = 0.15, #meters
                    twist = 0, #degrees
                    airfoil=asb.Airfoil("s1223"), # Flap # Control surfaces are applied between a given XSec and the next one.
                    
                    ),
                asb.WingXSec(#Mid
                    xyz_le = [0.1,0.5,0],
                    chord = 0.13,
                    twist = -2,
                    airfoil=asb.Airfoil("s1223"),
                    
                    
                    
                ),
                asb.WingXSec(#Tip
                    xyz_le = [0.1,0.8,0.12],
                    chord = 0.05,
                    twist = -10,
                    airfoil=asb.Airfoil("s1223"),
                    ),
                ]
        ),
        asb.Wing(
            name="Vertical Stabilizer",
            symmetric=True,
            xsecs=[
                asb.WingXSec(
                    xyz_le=[0, 0, 0],
                    chord=0.1,
                    twist=0,
                    airfoil=asb.Airfoil("naca0012"),
                    
                ),
                asb.WingXSec(
                    xyz_le=[0, 0.2, 0.15],
                    chord=0.06,
                    twist=0,
                    airfoil=asb.Airfoil("naca0012")
                )
            ]
        ).translate([0.6, 0, 0])    
    ],

    fuselages = [asb.Fuselage(
        name="Fuselage tip",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [ xi*0.1,0,0],
                # radius = np.sin(xi/0.1*np.pi/2)*0.05
                radius = np.sqrt(1-(-1+xi)**2)*0.025
            )for xi in np.cosspace(0,1,30)            


        ]
    ),
    asb.Fuselage(
        name="Fuselage body",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [0.1,0,0],
                radius = 0.025               
            ),
            asb.FuselageXSec(
                xyz_c = [0.25,0,0],
                radius = 0.025
            )
        ]
    ),
    asb.Fuselage(
        name ="Fuselage trannsition",
        xsecs = [
            asb.FuselageXSec(
                xyz_c=[0.25+xi/np.pi*0.1,0,0],
                radius = (np.cos(xi)+1)*0.0125/2+0.0125
            )for xi in np.cosspace(0,np.pi,30)
        ]
    ),
    asb.Fuselage(
        name = "Fuselage Tail",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [0.35,0,0],
                radius = 0.0125               
            ),
            asb.FuselageXSec(
                xyz_c = [0.7,0,0],
                radius = 0.0125
            )
        ]
    ),
    asb.Fuselage(
        name="Fuselage Tail tip ",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [ 0.7+xi*0.05,0,0],
                radius = np.sqrt(1-(xi)**2)*0.0125
            )for xi in np.cosspace(0,1,30)
    ]
    )
    ]
)

## Aero builduup

# ab_op_point = op_point.copy()
# ab_op_point.alpha = np.linspace(-12, 12, 50)

# aerobuildup_aero = asb.AeroBuildup(
#     airplane=airplane,
#     op_point=ab_op_point,
#     xyz_ref=xyz_ref
# ).run()
# aerobuildup_aero["alpha"] = ab_op_point.alpha

# print(aerobuildup_aero)

## Nonlinear lifting Line 

nlll_op_point = op_point.copy()
nlll_op_point.alpha = np.linspace(-10, 10, 5)

nlll_aeros = [
    asb.NonlinearLiftingLine(
        airplane=airplane,
        op_point=op,
        xyz_ref=xyz_ref,
    ).run()
    for op in nlll_op_point
]

nlll_aero = {}
for k in nlll_aeros[0].keys():
    nlll_aero[k] = np.array([
        aero[k]
        for aero in nlll_aeros
    ])
nlll_aero["alpha"] = nlll_op_point.alpha

print(nlll_aero)

## Quasi Lifting line
ll_op_point = op_point.copy()
ll_op_point.alpha = np.linspace(0, 14, 4)

ll_aeros = [
    asb.LiftingLine(
        airplane=airplane,
        op_point=op,
        xyz_ref=xyz_ref,
    ).run()
    for op in ll_op_point
]

ll_aero = {}
for k in ll_aeros[0].keys():
    ll_aero[k] = np.array([
        aero[k]
        for aero in ll_aeros
    ])
ll_aero["alpha"] = ll_op_point.alpha

print(ll_aero)



### VLM

# vlm.draw(show_kwargs=dict(jupyter_backend="static"))

# if __name__ == '__main__':
#     airplane.draw_three_view()