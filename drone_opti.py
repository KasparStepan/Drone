import aerosandbox as asb
import aerosandbox.numpy as np
from aerosandbox.library import airfoils
import copy

# Enviroment Values
g = 9.80665



opti = asb.Opti(
    freeze_style = 'float'
)

infill_default = 0.2
skin_thickness_default = 0.0015

filament_density = {
          "PLA": 1250,
          "LW-PLA": 800
}


skin_thickness = {
          "Center wing": skin_thickness_default,
          "Tip wing": skin_thickness_default,
          "Tail wing": skin_thickness_default,
          "Fuselage tip" : skin_thickness_default,
          "Fuselage body": skin_thickness_default,
          "Fuselage transition": skin_thickness_default,
          "Fuselage tail": skin_thickness_default,
          "Fuselage tail tip": skin_thickness_default,
}

infill = {
          "Center wing": infill_default,
          "Tip wing": infill_default,
          "Tail wing": infill_default,
          "Fuselage tip" : infill_default,
          "Fuselage body": infill_default,
          "Fuselage transition": infill_default,
          "Fuselage tail": infill_default,
          "Fuselage tail tip": infill_default,
}


    
    
op_point = asb.OperatingPoint(
    atmosphere=asb.Atmosphere(altitude=0),
    velocity=25,  # m/s
    )


airfoil_main_wing = asb.Airfoil("rg15")


## Definition of Main wing
Center_wing = asb.Wing(
            name = "Center wing",
            xyz_le=[0, 0, 0],
            symmetric=True,
            xsecs=[# The wing's cross ("X") sections, or "XSecs"
                asb.WingXSec(#Root
                    xyz_le = [0.1,0,0],
                    chord = 0.15, #meters
                    twist = 0, #degrees
                    airfoil=airfoil_main_wing, # Flap # Control surfaces are applied between a given XSec and the next one.
                    ),
                asb.WingXSec(#Mid
                    xyz_le = [0.1,0.5,0],
                    chord = 0.13,
                    twist = -2,
                    airfoil=airfoil_main_wing,
                )
                ]
            )

Tip_wing = asb.Wing(
            name = "Tip wing",
            xyz_le=[0, 0, 0],
            symmetric=True,
            xsecs=[# The wing's cross ("X") sections, or "XSecs"
                    asb.WingXSec(#Mid
                    xyz_le = [0.1,0.5,0],
                    chord = 0.13,
                    twist = -2,
                    airfoil=airfoil_main_wing,
                ),
                asb.WingXSec(#Tip
                    xyz_le = [0.1,0.8,0.12],
                    chord = 0.05,
                    twist = -10,
                    airfoil=airfoil_main_wing,
                    ),
                ]
            )

Tail_wing = asb.Wing(
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

fuselage_tip = asb.Fuselage(
        name="Fuselage tip",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [ xi*0.1,0,0],
                # radius = np.sin(xi/0.1*np.pi/2)*0.05
                radius = np.sqrt(1-(-1+xi)**2)*0.025
            )for xi in np.cosspace(0,1,30)            


        ]
        )

fuselage_body = asb.Fuselage(
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
    )
fuselage_transition = asb.Fuselage(
        name ="Fuselage transition",
        xsecs = [
            asb.FuselageXSec(
                xyz_c=[0.25+xi/np.pi*0.1,0,0],
                radius = (np.cos(xi)+1)*0.0125/2+0.0125
            )for xi in np.cosspace(0,np.pi,30)
        ]
    )

fuselage_tail = asb.Fuselage(
        name = "Fuselage tail",
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
    )

fuselage_tail_tip = asb.Fuselage(
        name="Fuselage tail tip",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [ 0.7+xi*0.05,0,0],
                radius = np.sqrt(1-(xi)**2)*0.0125
            )for xi in np.cosspace(0,1,30)
    ]
    )

airplane = asb.Airplane(
    name = "SKD",
    xyz_ref = [0,0,0],
    s_ref = 9, #Reference area
    c_ref = 0.9, #Reference chord
    b_ref = 10, #Reference span
    wings=[
        Center_wing,
        Tip_wing,        
        Tail_wing    
    ],

    fuselages = [
        fuselage_tip,
        fuselage_body,
        fuselage_transition,
        fuselage_tail,
        fuselage_tail_tip
    ]
)



mass_props = {}

## Lifting bodies

mass_props['Center_wing'] = asb.mass_properties_from_radius_of_gyration(
          mass = (Center_wing.volume()*infill["Center wing"]+Center_wing.area("wetted")*skin_thickness["Center wing"])*filament_density["PLA"],
          x_cg = 0,
          y_cg = 0,
          z_cg = 0,
          radius_of_gyration_x = 0,
          radius_of_gyration_y = 0,
          radius_of_gyration_z = 0,

)

mass_props['Tip_wing'] = asb.mass_properties_from_radius_of_gyration(
          mass = (Tip_wing.volume()*infill["Tip wing"]+Tip_wing.area("wetted")*skin_thickness["Tip wing"])*filament_density["PLA"],
          x_cg = 0,
          y_cg = 0,
          z_cg = 0,
          radius_of_gyration_x = 0,
          radius_of_gyration_y = 0,
          radius_of_gyration_z = 0,

)

mass_props['Tail_wing'] = asb.mass_properties_from_radius_of_gyration(
          mass = (Tail_wing.volume()*infill["Tail wing"]+Tail_wing.area("wetted")*skin_thickness["Tail wing"])*filament_density["PLA"],
          x_cg = 0,
          y_cg = 0,
          z_cg = 0,
          radius_of_gyration_x = 0,
          radius_of_gyration_y = 0,
          radius_of_gyration_z = 0,

)

for i in airplane.fuselages:
          mass_props[i.name] = asb.mass_properties_from_radius_of_gyration(
                    (i.volume()*infill[i.name]+i.area_wetted()*skin_thickness[i.name])*filament_density["PLA"],
                    x_cg = i.x_centroid_projected('XY')
          )

mass_props["Electric motor"] = asb.mass_properties_from_radius_of_gyration(
          mass = 0.05, # Needs to be researched
          x_cg = 0,
          y_cg = 0,
          z_cg = 0,
          radius_of_gyration_x = 0,
          radius_of_gyration_y = 0,
          radius_of_gyration_z = 0,
)

mass_props["Propeller"] = asb.mass_properties_from_radius_of_gyration(
          mass = 0.04, # Needs to be researched
          x_cg = 0,
          y_cg = 0,
          z_cg = 0,
          radius_of_gyration_x = 0,
          radius_of_gyration_y = 0,
          radius_of_gyration_z = 0,
)

mass_props['Motor mount'] = copy.copy(
    mass_props['Electric motor']
) * 1

mass_props['Avionics'] = asb.mass_properties_from_radius_of_gyration(
    mass=0.060,  # RX, pixhawk mini
    x_cg=0,
    z_cg=0
)

mass_props['servos'] = asb.mass_properties_from_radius_of_gyration(
    mass=0.050, #find the number and the weight
    x_cg=0
)

mass_props['battery'] = asb.mass_properties_from_radius_of_gyration(
    mass=0, #To be determined
    x_cg=0,
    z_cg=0
)

mass_props["Payload"] = asb.mass_properties_from_radius_of_gyration(
    mass=0.25, #To be determined
    x_cg=0,
    z_cg=0
)

print(sum(mass_props.values()))


Lift_required = sum(mass_props.values())*g

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

# nlll_op_point = op_point.copy()
# nlll_op_point.alpha = np.linspace(-10, 10, 5)

# nlll_aeros = [
#     asb.NonlinearLiftingLine(
#         airplane=airplane,
#         op_point=op,
#         xyz_ref=xyz_ref,
#     ).run()
#     for op in nlll_op_point
# ]

# nlll_aero = {}
# for k in nlll_aeros[0].keys():
#     nlll_aero[k] = np.array([
#         aero[k]
#         for aero in nlll_aeros
#     ])
# nlll_aero["alpha"] = nlll_op_point.alpha

# print(nlll_aero)

# ## Quasi Lifting line
# ll_op_point = op_point.copy()
# ll_op_point.alpha = np.linspace(0, 14, 4)

# ll_aeros = [
#     asb.LiftingLine(
#         airplane=airplane,
#         op_point=op,
#         xyz_ref=xyz_ref,
#     ).run()
#     for op in ll_op_point
# ]

# ll_aero = {}
# for k in ll_aeros[0].keys():
#     ll_aero[k] = np.array([
#         aero[k]
#         for aero in ll_aeros
#     ])
# ll_aero["alpha"] = ll_op_point.alpha

# print(ll_aero)



### VLM

# vlm.draw(show_kwargs=dict(jupyter_backend="static"))

# if __name__ == '__main__':
#     airplane.draw_three_view()