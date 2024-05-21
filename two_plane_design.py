import aerosandbox as asb
import matplotlib.pyplot as plt
import aerosandbox.numpy as np
import copy

def plot_results(endurance,speed):
    plt.subplot(3,3,1)
    plt.plot(endurance['CD'],endurance['CL'],label = 'Endurance airplane')
    plt.plot(speed['CD'],speed['CL'],label = 'Speed airplane')
    plt.legend()
    plt.grid()
    plt.title('Aerodynamic polar')
    plt.xlabel('CD [-]')
    plt.ylabel('CL [-]')


    plt.subplot(3,3,2)
    plt.plot(endurance['alpha'],endurance['Cm'],label = 'Endurance airplane')
    plt.plot(speed['alpha'],speed['Cm'],label = 'Speed airplane')
    plt.legend()
    plt.grid()
    plt.title('Moment polar')
    plt.xlabel('alpha [deg]')
    plt.ylabel('CM [-]')


    plt.subplot(3,3,3)
    plt.plot(endurance['alpha'],endurance['CL'],label = 'Endurance airplane')
    plt.plot(speed['alpha'],speed['CL'],label = 'Speed airplane')
    plt.legend()
    plt.grid()
    plt.title('Lift curve')
    plt.xlabel('alpha [deg]')
    plt.ylabel('CL [-]')

    plt.subplot(3,3,4)
    plt.plot(endurance['alpha'],endurance['CD'],label = 'Endurance airplane')   
    plt.plot(speed['alpha'],speed['CD'],label = 'Speed airplane')
    plt.legend()
    plt.grid()
    plt.title('Drag curve')
    plt.xlabel('alpha [deg]')
    plt.ylabel('CD [-]')


    plt.subplot(3,3,5)
    plt.plot(endurance['alpha'],endurance['total_pitch'],label = 'Endurance airplane')
    plt.plot(speed['alpha'],speed['total_pitch'],label= 'Speed airplane')
    plt.legend()
    plt.grid()
    plt.title('Airplane moment curve with CoG moment')
    plt.xlabel('alpha [deg]')
    plt.ylabel('Cm_airplane [-]')


    plt.subplot(3,3,6)
    plt.plot(endurance['alpha'],endurance['efficiency'],label = 'Endurance airplane')
    plt.plot(speed['alpha'],speed['efficiency'],label = 'Speed airplane')
    plt.legend()
    plt.grid()
    plt.title('Aerodynamic efficiency')
    plt.xlabel('alpha [deg]')
    plt.ylabel('CL/CD [-]')

    plt.subplot(3,3,7)
    plt.plot(endurance['alpha'],endurance['endurance'],label = 'Endurance airplane')
    plt.plot(speed['alpha'],speed['endurance'],label = 'Speed airplane')
    plt.legend()
    plt.grid()
    plt.title('Endurance')
    plt.xlabel('alpha [deg]')
    plt.ylabel('Time [h]')

    plt.show()


def find_zero(aoa,array):
      for i in range(len(array)-1):
            if (array[i]*array[i+1])<0:
                  print(i + array[i]/(array[i]-array[i+1]))
                  return (i + array[i]*(aoa[i+1]-aoa[i])/(array[i]-array[i+1]))
            

opti = asb.Opti()

battery_usable_capacity = 0.5 #-
material_type = 'LW-PLA'
voltage = 11.1 #V

cruise_speed={'Endurance':15,
              'Speed':25}

endurance = { #h
       'Endurance':1, 
       'Speed':0.5}

batteries = {#mAh
       'Base':2200} 

main_chord = 0.15#opti.variable(init_guess=0.15,upper_bound=0.25,lower_bound=0.075)

chord = { #m
       'Main_root':main_chord,
         'Main_mid_center': main_chord,
         'Main_end_center': 0.13,#opti.variable(init_guess=0.13,upper_bound=0.2,lower_bound=0.075),
         'Main_tip':0.05,#opti.variable(init_guess=0.05,upper_bound=0.15,lower_bound=0.025),
         'Tail_root':0.13,#opti.variable(init_guess=0.13,upper_bound=0.25,lower_bound=0.05),
         'Tail_tip':0.05 #opti.variable(init_guess=0.1,upper_bound=0.15,lower_bound=0.02)
         }



wingspan = { #m
       'Main_mid':0.2,
            'Main_center':0.3,
            'Main_tip':0.15,
            'Tail':0.1}

opti.subject_to([
       wingspan['Main_mid']+wingspan['Main_center']+wingspan['Main_tip']<0.75,
])

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
         'Tail_root':opti.variable(init_guess=-5,upper_bound=2,lower_bound=-5),
         'Tail_tip':opti.variable(init_guess=-5,upper_bound=2,lower_bound=-5),
}

fuselage_radius = { #m
        'Big':0.015,
        'Small':0.01
}

airplane_length = opti.variable(init_guess=0.7,upper_bound=0.3,lower_bound=1.1) #m



Endurance_wing = asb.Wing(
            name = "Endurance wing",
            xyz_le=[0,
                    0,
                    0],
            symmetric=True,
            xsecs=[# The wing's cross ("X") sections, or "XSecs"
                asb.WingXSec(#Root
                    xyz_le = [0,
                              0,
                              0],
                    chord = chord['Main_root'], 
                    twist = twist['Main_root'], 
                    airfoil=asb.Airfoil('rg15'), # Flap # Control surfaces are applied between a given XSec and the next one.
                    ),
                asb.WingXSec(#Center mid
                    xyz_le = [0,
                              wingspan['Main_mid'],
                              0],
                    chord = chord['Main_mid_center'],
                    twist = twist['Main_mid_center'],
                    airfoil=asb.Airfoil('rg15'),
                    ),
                asb.WingXSec(#Center tip
                    xyz_le=[wingspan['Main_center']*np.tan(np.deg2rad(sweep_angle['Main_center'])),
                            wingspan['Main_mid']+wingspan['Main_center'],
                            wingspan['Main_center']*np.tan(np.deg2rad(dihedral_angle['Main_center']))],
                    chord=chord['Main_end_center'],
                    twist=twist['Main_end_center'],
                    airfoil= asb.Airfoil('rg15')

                ),
                asb.WingXSec(#Tip
                    xyz_le=[wingspan['Main_center']*np.tan(np.deg2rad(sweep_angle['Main_center']))+wingspan['Main_tip']*np.tan(np.deg2rad(sweep_angle['Main_tip'])),
                            wingspan['Main_mid']+wingspan['Main_center']+wingspan['Main_tip'],
                            wingspan['Main_center']*np.tan(np.deg2rad(dihedral_angle['Main_center']))+wingspan['Main_tip']*np.tan(np.deg2rad(dihedral_angle['Main_tip']))],
                    chord=chord['Main_tip'],
                    twist=twist['Main_tip'],
                    airfoil= asb.Airfoil('rg15')
                )
                ]
            )

Speed_wing = asb.Wing(
            name = "Speed wing",
            xyz_le=[0,
                    0,
                    0],
            symmetric=True,
            xsecs=[# The wing's cross ("X") sections, or "XSecs"
                asb.WingXSec(#Center mid
                    xyz_le = [0,
                              0,
                              0],
                    chord = chord['Main_mid_center'],
                    twist = twist['Main_mid_center'],
                    airfoil=asb.Airfoil('rg15'),
                    ),
                asb.WingXSec(#Center tip
                    xyz_le=[wingspan['Main_center']*np.tan(np.deg2rad(sweep_angle['Main_center'])),
                            wingspan['Main_center'],
                            wingspan['Main_center']*np.tan(np.deg2rad(dihedral_angle['Main_center']))],
                    chord=chord['Main_end_center'],
                    twist=twist['Main_end_center'],
                    airfoil= asb.Airfoil('rg15')

                ),
                asb.WingXSec(#Tip
                    xyz_le=[wingspan['Main_center']*np.tan(np.deg2rad(sweep_angle['Main_center']))+wingspan['Main_tip']*np.tan(np.deg2rad(sweep_angle['Main_tip'])),
                            wingspan['Main_center']+wingspan['Main_tip'],
                            wingspan['Main_center']*np.tan(np.deg2rad(dihedral_angle['Main_center']))+wingspan['Main_tip']*np.tan(np.deg2rad(dihedral_angle['Main_tip']))],
                    chord=chord['Main_tip'],
                    twist=twist['Main_tip'],
                    airfoil= asb.Airfoil('rg15')
                )
                ]
            )

Tail_wing = asb.Wing(
    name = "Speed wing",
    xyz_le=[0,
            0,
            0],
    symmetric=True,
    xsecs=[asb.WingXSec(
        xyz_le=[airplane_length-chord['Tail_root'],
                0,
                0],
        chord=chord['Tail_root'],
        twist=twist['Tail_root'],
        airfoil=asb.Airfoil('naca0012')
        ),
        asb.WingXSec(
            xyz_le=[airplane_length+wingspan['Tail']*np.tan(np.deg2rad(sweep_angle['Tail']))-chord['Tail_tip'],
                wingspan['Tail']*np.tan(np.deg2rad(dihedral_angle['Tail'])),
                wingspan['Tail']],
        chord=chord['Tail_tip'],
        twist=twist['Tail_tip'],
        airfoil=asb.Airfoil('naca0012')
        )
    ]
    
)


fuselage_tip = asb.Fuselage(
        name="Fuselage tip",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [ xi*0.1*airplane_length-0.1*airplane_length,0,0],
                # radius = np.sin(xi/0.1*np.pi/2)*0.05
                radius = np.sqrt(1-(-1+xi)**2)*fuselage_radius['Big']
            )for xi in np.cosspace(0,1,30)            


        ]
        )
fuselage_body = asb.Fuselage(
        name="Fuselage body",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [0,0,0],
                radius = fuselage_radius['Big']               
            ),
            asb.FuselageXSec(
                xyz_c = [chord['Main_root']*1.2,0,0],
                radius = fuselage_radius['Big'] 
            )
        ]
    )
fuselage_transition = asb.Fuselage(
        name ="Fuselage transition",
        xsecs = [
            asb.FuselageXSec(
                xyz_c=[chord['Main_root']*1.2+xi/np.pi*airplane_length*0.1,0,0],
                radius = (np.cos(xi)+1)*(fuselage_radius['Big']-fuselage_radius['Small'])/2+fuselage_radius['Small']
            )for xi in np.cosspace(0,np.pi,30)
        ]
    )
fuselage_tail = asb.Fuselage(
        name = "Fuselage tail",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [chord['Main_root']*1.2+airplane_length*0.1,0,0],
                radius = fuselage_radius['Small']               
            ),
            asb.FuselageXSec(
                xyz_c = [airplane_length,0,0],
                radius = fuselage_radius['Small']  
            )
        ]
    )
fuselage_tail_tip = asb.Fuselage(
        name="Fuselage tail tip",
        xsecs=[
            asb.FuselageXSec(
                xyz_c = [ airplane_length+xi*0.05,0,0],
                radius = np.sqrt(1-(xi)**2)*fuselage_radius['Small']  
            )for xi in np.cosspace(0,1,30)
    ]
    )


Endurance_airplane = asb.Airplane(
    name = "Endurance Airplane",
    xyz_ref = [Endurance_wing.aerodynamic_center(chord_fraction=0.25)[0],0,0],
    s_ref = Endurance_wing.area(), #Reference area
    c_ref = Endurance_wing.mean_aerodynamic_chord(), #Reference chord
    b_ref = Endurance_wing.span(), #Reference span
    wings=[
        Endurance_wing,        
        Tail_wing    
    ],
    fuselages=[
        fuselage_tip,
        fuselage_body,
        fuselage_transition,
        fuselage_tail,
        fuselage_tail_tip
    ]
)

Speed_airplane = asb.Airplane(
    name = "Speed Airplane",
    xyz_ref = [Speed_wing.aerodynamic_center(chord_fraction=0.25)[0],0,0],
    s_ref = Speed_wing.area(), #Reference area
    c_ref = Speed_wing.mean_aerodynamic_chord(), #Reference chord
    b_ref = Speed_wing.span(), #Reference span
    wings=[
        Speed_wing,        
        Tail_wing    
    ],
    fuselages=[
        fuselage_tip,
        fuselage_body,
        fuselage_transition,
        fuselage_tail,
        fuselage_tail_tip
    ]
)

mass_props = {}

infill_default = 0.2
skin_thickness_default = 0.001

filament_density = {
          'PLA': 1250,
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
          "Fuselage tip" : 0,
          "Fuselage body": 0,
          "Fuselage transition": 0,
          "Fuselage tail": 0,
          "Fuselage tail tip": 0,
}


for i in Speed_airplane.fuselages:
          mass_props[i.name] = asb.mass_properties_from_radius_of_gyration(
                    (i.volume()*infill[i.name]+i.area_wetted()*skin_thickness[i.name])*filament_density[material_type],
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
    x_cg=0,
    y_cg = 0
)

mass_props['battery'] = asb.mass_properties_from_radius_of_gyration(
    mass=0.22, #To be determined
    x_cg=0,
    z_cg=0
)

mass_props["Payload"] = asb.mass_properties_from_radius_of_gyration(
    mass=1, #To be determined
    x_cg=0,
    z_cg=0
)

mass_props['Tail_wing'] = asb.mass_properties_from_radius_of_gyration(
          mass = (Tail_wing.volume()*infill["Tail wing"]+Tail_wing.area("wetted")*skin_thickness["Tail wing"])*filament_density[material_type],
          x_cg = Tail_wing.aerodynamic_center(chord_fraction=0.25)[0],
          y_cg = Tail_wing.aerodynamic_center(chord_fraction=0.25)[1],
          z_cg = Tail_wing.aerodynamic_center(chord_fraction=0.25)[2]

)


speed_airplane_mass_props = mass_props.copy()
endurance_airplane_mass_props = mass_props.copy()

speed_airplane_mass_props['Speed_wing'] = asb.mass_properties_from_radius_of_gyration(
          mass = (Speed_wing.volume()*infill["Tip wing"]+Speed_wing.area("wetted")*skin_thickness["Tip wing"])*filament_density[material_type],
          x_cg = Speed_wing.aerodynamic_center(chord_fraction=0.25)[0],
          y_cg = Speed_wing.aerodynamic_center(chord_fraction=0.25)[1],
          z_cg = Speed_wing.aerodynamic_center(chord_fraction=0.25)[2]
)

endurance_airplane_mass_props['Endurance_wing'] = asb.mass_properties_from_radius_of_gyration(
          mass = (Endurance_wing.volume()*infill["Tip wing"]+Endurance_wing.area("wetted")*skin_thickness["Tip wing"])*filament_density[material_type],
          x_cg = Endurance_wing.aerodynamic_center(chord_fraction=0.25)[0],
          y_cg = Endurance_wing.aerodynamic_center(chord_fraction=0.25)[1],
          z_cg = Endurance_wing.aerodynamic_center(chord_fraction=0.25)[2]
)




endurance_total_mass = asb.MassProperties(mass=0)
for k,v in endurance_airplane_mass_props.items():
        endurance_total_mass = endurance_total_mass+v

speed_total_mass = asb.MassProperties(mass=0)
for k,v in speed_airplane_mass_props.items():
        speed_total_mass = speed_total_mass+v

### Letove podminky pro let

alpha = np.linspace(0,10,10)
range_aoa = len(alpha)
#alpha = np.array([0,1])
speed_airplane_operating_point = asb.OperatingPoint(
        atmosphere=asb.Atmosphere(altitude=0),
        velocity= cruise_speed['Speed'],
        alpha=alpha
)

endurance_airplane_operating_point = asb.OperatingPoint(
        atmosphere=asb.Atmosphere(altitude=0),
        velocity= cruise_speed['Endurance'],
        alpha=alpha
)

speed_aero_data_run = [
    asb.LiftingLine(
        airplane=Speed_airplane,
        op_point=op,
    ).run()
    for op in speed_airplane_operating_point
]

speed_aero_data = {'alpha':alpha}

for k in speed_aero_data_run[0].keys():
    speed_aero_data[k] = np.array([
        aero[k]
        for aero in speed_aero_data_run
    ])


endurance_aero_data_run = [
    asb.LiftingLine(
        airplane=Endurance_airplane,
        op_point=op,
    ).run() for op in endurance_airplane_operating_point
]

endurance_aero_data = {'alpha':alpha}

for k in endurance_aero_data_run[0].keys():
    endurance_aero_data[k] = np.array([
        aero[k]
        for aero in endurance_aero_data_run
    ])

# Calculation of airplane efficiency
endurance_aero_data['efficiency'] = endurance_aero_data['CL']/endurance_aero_data['CD']
speed_aero_data['efficiency'] = speed_aero_data['CL']/speed_aero_data['CD']

endurance_max_efficiency= np.max(endurance_aero_data['efficiency'])

endurance_max_efficiency_AoA = 0

speed_max_efficiency = np.max(speed_aero_data['efficiency'])
speed_max_efficiency_AoA = 0


endurance_zero_pitch_AoA = find_zero(endurance_aero_data['alpha'],endurance_aero_data['Cm'])
speed_zero_pitch_AoA = find_zero(speed_aero_data['alpha'],speed_aero_data['Cm'])

endurance_pitch_error = endurance_max_efficiency_AoA-endurance_zero_pitch_AoA
speed_pitch_error = speed_max_efficiency_AoA-speed_zero_pitch_AoA


endurance_aero_data['total_pitch'] = endurance_aero_data['Cm'] - (endurance_total_mass.x_cg-Endurance_wing.aerodynamic_center(chord_fraction=0.25)[0])*endurance_aero_data['CL']
speed_aero_data['total_pitch'] = speed_aero_data['Cm'] - (speed_total_mass.x_cg-Speed_wing.aerodynamic_center(chord_fraction=0.25)[0])*speed_aero_data['CL']

endurance_aero_data['endurance'] = battery_usable_capacity*batteries['Base']*voltage/(endurance_aero_data['D']*cruise_speed['Endurance']*1000)
max_endurance_endurance = np.max(endurance_aero_data['endurance'])


speed_aero_data['endurance'] = battery_usable_capacity*batteries['Base']*voltage/(speed_aero_data['D']*cruise_speed['Speed']*1000)
max_speed_endurance = np.max(speed_aero_data['endurance'])

opti.minimize(endurance_pitch_error+speed_pitch_error)

sol = opti.solve(max_iter=100)



print(f"Endurance airplane")
print(f"Total mass = {endurance_total_mass.mass:3} kg")
print(f"Maximal aerodynamic effciency AoA = {endurance_max_efficiency_AoA:2}")
print(f"Zero pitch AoA = {endurance_zero_pitch_AoA:2} deg")
print(f"Pitch AoA diference = {endurance_pitch_error} deg")
print(f"Maximal endurance = {np.max(endurance_aero_data['endurance']):0} h")

print(f"Speed airplane")
print(f"Total mass = {speed_total_mass.mass:3} kg")
print(f"Maximal aerodynamic effciency AoA = {speed_max_efficiency_AoA:2}")
print(f"Zero pitch AoA = {speed_zero_pitch_AoA:2} deg")
print(f"Pitch AoA diference = {speed_pitch_error} deg")
print(f"Maximal endurance = {np.max(speed_aero_data['endurance']):0} h")

plot_results(sol(eval(endurance_aero_data)),sol(eval(speed_aero_data)))


