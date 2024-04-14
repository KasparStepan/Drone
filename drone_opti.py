import aerosandbox as asb
import aerosandbox.numpy as np
from aerosandbox.library import airfoils



#Fluid properties
density = 1.225
viscosity = 1.81e-5

af = asb.Airfoil(name="naca0012").add_control_surface(
    deflection=30.0,
    hinge_point_x=0.7
)


Aileron = asb.geometry.wing.ControlSurface(
    name="Aileron",
    symmetric = False,
    deflection = 30,
    hinge_point = 0.7,
    
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
                    control_surface=[Aileron],
                    
                    
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

vlm = asb.VortexLatticeMethod(
    airplane=airplane,
    op_point=asb.OperatingPoint(
        velocity=25,  # m/s
        alpha=0,  # degree
    )
)

aero = vlm.run()  # Returns a dictionary
for k, v in aero.items():
    print(f"{k.rjust(4)} : {v}")

    # NBVAL_SKIP

vlm.draw(show_kwargs=dict(jupyter_backend="static"))

if __name__ == '__main__':
    airplane.draw_three_view()