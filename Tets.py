import aerosandbox as asb
import aerosandbox.numpy as np
from aerosandbox.library import airfoils
import copy

### Enviroment Constants
g = 9.80665

### Flight conditions
altitude_flight = 0
atmosphere = asb.Atmosphere(altitude=altitude_flight)
freestream_velocity = 25
# alpha = 4
density  = atmosphere.density()
viscosity = atmosphere.dynamic_viscosity()
pressure = atmosphere.pressure()

### Optimization variables

# opti = asb.Opti()

method_type = {
       "VLM": False,
       "Lifting line": True,
       "AeroBuildup": False,
       "AVL": False,
}

# alpha = opti.variable(init_guess=4,lower_bound = 0, upper_bound = 6)




## Wing parameters

max_taper = 0.7

chord = { #m
      "Wing root":0.15,
      "Wing mid": 0.13,
      "Wing tip" : 0.05,
      "Wing tail root": 0.1,
      "Wing tail tip":0.06,
}

# opti.subject_to([
#        chord["Wing root"]>chord["Wing mid"],
#        chord["Wing mid"]>chord["Wing tip"],
#        chord["Wing tail root"]>chord["Wing tail tip"],
#        (chord["Wing mid"]/chord["Wing root"])>max_taper,
#        (chord["Wing tip"]/chord["Wing mid"])>max_taper
# ])

wing_span = { #m
      "Wing center": 0.4,
      "Wing tip" : 0.2,
      "Wing tail": 0.15,
}

# opti.subject_to([
#       wing_span["Wing center"]+wing_span["Wing tip"]<=0.75,
#       wing_span["Wing center"]+wing_span["Wing tip"]>=0.3
# ])

sweep_angle = { #deg
      "Wing center": 0,
      "Wing tip" : 0,
      "Wing tail": 10,    
}

dihedral_angle = { #deg
      "Wing center": 0,
      "Wing tip": 10,
      "Wing tail": 45
}

twist = { #deg
      "Wing root": 0,
      "Wing mid": 0,
      "Wing tip" : 0,
      "Wing tail root": 0,
      "Wing tail tip":0,
}

tail_length = 6
body_length = 2



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


airfoil_main_wing = asb.Airfoil("rg15")

## Definition of Main wing
Center_wing = asb.Wing(
            name = "Center wing",
            xyz_le=[0, 0, 0],
            symmetric=True,
            xsecs=[# The wing's cross ("X") sections, or "XSecs"
                asb.WingXSec(#Root
                    xyz_le = [0,0,0],
                    chord = chord["Wing root"], #meters
                    twist = twist["Wing root"], #degrees
                    airfoil=airfoil_main_wing, # Flap # Control surfaces are applied between a given XSec and the next one.
                    ),
                asb.WingXSec(#Mid
                    xyz_le = [wing_span["Wing center"]*np.sin(np.deg2rad(sweep_angle["Wing center"])),wing_span["Wing center"],wing_span["Wing center"]*np.sin(np.deg2rad(dihedral_angle["Wing center"]))],
                    chord = chord["Wing mid"],
                    twist = twist["Wing mid"],
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
                    xyz_le = [wing_span["Wing center"]*np.sin(np.deg2rad(sweep_angle["Wing center"])),wing_span["Wing center"],wing_span["Wing center"]*np.sin(np.deg2rad(dihedral_angle["Wing center"]))],
                    chord = chord["Wing mid"],
                    twist = twist["Wing mid"],
                    airfoil=airfoil_main_wing,
                ),
                asb.WingXSec(#Tip
                    xyz_le = [wing_span["Wing center"]*np.sin(np.deg2rad(sweep_angle["Wing center"]))+wing_span["Wing tip"]*np.sin(np.deg2rad(sweep_angle["Wing tip"])),wing_span["Wing center"]+wing_span["Wing tip"],wing_span["Wing center"]*np.sin(np.deg2rad(dihedral_angle["Wing center"]))+wing_span["Wing tip"]*np.sin(np.deg2rad(dihedral_angle["Wing tip"]))],
                    chord = chord["Wing tip"],
                    twist = twist["Wing tip"],
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
                    chord=chord["Wing tail root"],
                    twist=0,
                    airfoil=asb.Airfoil("naca0012"),
                    
                ),
                asb.WingXSec(
                    xyz_le=[0, 0.2, 0.15],
                    chord=chord["Wing tail tip"],
                    twist=0,
                    airfoil=asb.Airfoil("naca0012")
                )
            ]
            ).translate([0.6, 0, 0])

fuselage_tip = asb.Fuselage(
        name="Fuselage tip",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [ xi*0.1-0.1,0,0],
                # radius = np.sin(xi/0.1*np.pi/2)*0.05
                radius = np.sqrt(1-(-1+xi)**2)*0.015
            )for xi in np.cosspace(0,1,30)            


        ]
        )
fuselage_body = asb.Fuselage(
        name="Fuselage body",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [0,0,0],
                radius = 0.015               
            ),
            asb.FuselageXSec(
                xyz_c = [0.25,0,0],
                radius = 0.015
            )
        ]
    )
fuselage_transition = asb.Fuselage(
        name ="Fuselage transition",
        xsecs = [
            asb.FuselageXSec(
                xyz_c=[0.25+xi/np.pi*0.1,0,0],
                radius = (np.cos(xi)+1)*0.0075/2+0.0075
            )for xi in np.cosspace(0,np.pi,30)
        ]
    )
fuselage_tail = asb.Fuselage(
        name = "Fuselage tail",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [0.35,0,0],
                radius = 0.0075               
            ),
            asb.FuselageXSec(
                xyz_c = [0.7,0,0],
                radius = 0.0075
            )
        ]
    )
fuselage_tail_tip = asb.Fuselage(
        name="Fuselage tail tip",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [ 0.7+xi*0.05,0,0],
                radius = np.sqrt(1-(xi)**2)*0.0075
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
    mass=1, #To be determined
    x_cg=0,
    z_cg=0
)

print(sum(mass_props.values()))


total_mass = asb.MassProperties(mass=0)
for k,v in mass_props.items():
        total_mass = total_mass+v


Lift_required = sum(mass_props.values())*g*1.2

vlm_op_point = asb.OperatingPoint(
        velocity=25,
)
vlm_op_point.alpha = 0

vlm_aeros = [
    asb.VortexLatticeMethod(
        airplane=airplane,
        op_point=vlm_op_point,
        spanwise_resolution=5
    ).run()

]

print(vlm_aeros)






        