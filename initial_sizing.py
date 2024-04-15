import aerosandbox as asb
import aerosandbox.numpy as np

opti = abs.Opti(
    freeze_style = 'float'
)

cruise_op_point = asb.OperatingPoint(
    velocity = opti.variable(
        init = 25, # m/s
        lower_bound = 15,
        upper_bound = 35,
        log_transform = True
    ),
    alpha=opti.variable(
        init_guess = 0, #deg
        lower_bound = -10,
        upper_bound = 10,
    )
)

### Definition of parameters to optimize
Aspect_ratio = opti.variable() #Aspect ratio [-]
wing_area = opti.variable() # Wing Area [-]
taper_ratio = opti.variable() #Taper ratio [-]
V_ht = opti.variable() # Doplnit
V_vt = opti.variable() # Doplnit
Aspect_ratio_ht = opti.variable() 
Aspect_ratio_vt = opti.variable()




# Enviroment parameters
g = 9.81
viscosity = 1.775e-5
density = 1.225
altitude = 0 # m ISA

# Base airplane parameters

weight_payload = 3
endurance = 1
fuselage_radius = 0.025 # poloměr draku [m]
design_weight = 2 # Očekávaná hmotnost


## Aerodynamics design 
chord_ref = wing_area
b_ref = Aspect_ratio/chord_ref


#Návrh ocasních plochy

chord_root = 2*chord_ref/(1+taper_ratio)
chord_tip = chord_root*taper_ratio

chord_mgc = 2/3*chord_root*(1+taper_ratio*taper_ratio**2)/(1+taper_ratio)

l_t = np.sqrt((2*V_ht*wing_area*chord_mgc)/np.pi*(2*fuselage_radius))

S_ht = V_ht*wing_area*chord_ref/l_t
b_ht = np.sqrt(Aspect_ratio_ht*S_ht)
chord_ht_ref = b_ht/Aspect_ratio_ht

S_vt = V_vt*wing_area*b_ref/l_t
b_vt = np.sqrt(Aspect_ratio_vt*S_vt)
chord_ht_ref = b_vt/Aspect_ratio_vt



### Weight estimation
##### Section: Internal Geometry and Weights

structural_mass_markup = 1.2  # over Enigma F5J

mass_props = {}

### Lifting bodies
mass_wing = (  # Engima F5J
                    (0.440 + 0.460) *
                    (wing_area() / (0.264 * 3.624 * np.pi / 4)) ** 0.758 *
                    (design_weight / 1.475) ** 0.49 *
                    (Aspect_ratio() / 18) ** 0.6
            ) * structural_mass_markup

mass_props['wing_center'] = asb.mass_properties_from_radius_of_gyration(
    mass=mass_wing * wing_y_break_fraction,
    x_cg=0,  # quarter-chord,
    radius_of_gyration_x=(wing_y_break_fraction * wing_span) / 12,
    radius_of_gyration_z=(wing_y_break_fraction * wing_span) / 12
)
mass_props['wing_tips'] = asb.mass_properties_from_radius_of_gyration(
    mass=mass_wing * (1 - wing_y_break_fraction),
    x_cg=0,  # quarter-chord,
    radius_of_gyration_x=(1 + wing_y_break_fraction) / 2 * (wing_span / 2),
    radius_of_gyration_z=(1 + wing_y_break_fraction) / 2 * (wing_span / 2),
)
mass_props['h_stab'] = asb.mass_properties_from_radius_of_gyration(
    mass=(
                 0.055 *
                 (
                         0.4 * (design_mass_TOGW / 1.475) ** 0.40 * (hstab_span / (0.670 / np.cosd(40))) ** 1.58 +
                         0.6 * (wing_root_chord / 0.264) * (hstab_span / (0.670 / np.cosd(40)))
                 )
         ) * structural_mass_markup,
    x_cg=hstab.xsecs[0].xyz_le[0] + hstab_chord / 2,
    z_cg=vstab.aerodynamic_center()[2],
    radius_of_gyration_x=hstab_span / 12,
    radius_of_gyration_y=hstab.xsecs[0].xyz_le[0] + hstab_chord / 2,
    radius_of_gyration_z=hstab.xsecs[0].xyz_le[0] + hstab_chord / 2
)
mass_props['v_stab'] = asb.mass_properties_from_radius_of_gyration(
    mass=(
                 0.055 *
                 (
                         0.3 * (design_mass_TOGW / 1.475) ** 0.40 * (vstab_span / (0.670 / np.cosd(40))) ** 1.58 +
                         0.7 * (wing_root_chord / 0.264) * (vstab_span / (0.670 / np.cosd(40)))
                 )
         ) * structural_mass_markup,
    x_cg=vstab.xsecs[0].xyz_le[0] + vstab_chord / 2,
    z_cg=vstab.aerodynamic_center()[2],
    radius_of_gyration_x=vstab_span / 12,
    radius_of_gyration_y=vstab.xsecs[0].xyz_le[0] + vstab_chord / 2,
    radius_of_gyration_z=vstab.xsecs[0].xyz_le[0] + vstab_chord / 2
)

### Other Structure
mass_props['boom'] = asb.mass_properties_from_radius_of_gyration(
    mass=(
                 0.235 *
                 (x_tail / 1.675) *
                 (design_mass_TOGW / 1.475) ** 0.49
         ) * structural_mass_markup,
    x_cg=x_tail / 2,
    radius_of_gyration_y=x_tail / 3,
    radius_of_gyration_z=x_tail / 3,
)

### Propulsion
mass_props['motors'] = asb.mass_properties_from_radius_of_gyration(
    mass=lib_prop_elec.mass_motor_electric(
        max_power=climb_power_propulsion / n_propellers,
        kv_rpm_volt=motor_kv,
        voltage=battery_voltage,
    ) * n_propellers,
    x_cg=-0.25 * wing_root_chord - 2 * u.inch,
    radius_of_gyration_x=motor_y_placement,
    radius_of_gyration_y=0.25 * wing_root_chord + 2 * u.inch,
    radius_of_gyration_z=motor_y_placement,
)

mass_props['motor_mounts'] = copy.copy(
    mass_props['motors']
) * 1  # similar to a quote from Raymer, modified to make sensible units, prop weight roughly subtracted

mass_props['propellers'] = asb.mass_properties_from_radius_of_gyration(
    mass=n_propellers * lib_prop_prop.mass_hpa_propeller(
        diameter=propeller_diameter,
        max_power=climb_power_propulsion / n_propellers,
        include_variable_pitch_mechanism=False
    ),
    x_cg=mass_props['motors'].x_cg - 1 * u.inch,
    radius_of_gyration_x=motor_y_placement,
    radius_of_gyration_z=motor_y_placement,
)

mass_props['ESCs'] = asb.mass_properties_from_radius_of_gyration(
    mass=lib_prop_elec.mass_ESC(max_power=climb_power_propulsion / n_propellers) * n_propellers,
    x_cg=0,
)

### Fuselage internals
mass_props['fuselage_skin'] = asb.mass_properties_from_radius_of_gyration(
    mass=(
                 fuse_wetted_area * (
                 np.minimum(2, 2 * fuselage_length) *  # plies
                 (4 * u.oz / u.yard ** 2)
         )
         ) * 1.5  # waterproofing markup
    ,
    x_cg=0.4 + x_fuse_nose,  # 0.4 to weight more towards thicker nose
    z_cg=-0.15 * fuselage_length
)
mass_props['fuselage_bulkheads'] = asb.mass_properties_from_radius_of_gyration(
    mass=(
            fuse_xsec_area * (  # These won't be anywhere near solid, but this is a rough estimate of material needed
            4 *  # n_bulkheads
            (1 / 8 * u.inch) * fuselage_length * (400)  # basswood
    )
    ),
    x_cg=(0.35 + x_fuse_nose) / 2,  # halfway between mid-fuse location and wing quarter-chord.
    z_cg=-0.15 * fuselage_length
)

mass_props['avionics'] = asb.mass_properties_from_radius_of_gyration(
    mass=0.060,  # RX, pixhawk mini
    x_cg=5 * u.inch + x_fuse_nose,
    z_cg=-0.15 * fuselage_length
)

mass_props['servos'] = asb.mass_properties_from_radius_of_gyration(
    mass=0.050,
    x_cg=x_tail * 0.5  # 2x tail, 2x wing
)

battery_capacity = (
        battery_reserve_time * (3 / 4) * cruise_power_propulsion +
        battery_reserve_time * (1 / 4) * climb_power_propulsion
)

battery_ampacity_amp_hours = battery_capacity / u.hour / battery_voltage

mass_props['battery'] = asb.mass_properties_from_radius_of_gyration(
    mass=battery_capacity / u.hour / battery_specific_energy_Wh_kg,
    x_cg=x_fuse_nose + 3 * u.inch,
    z_cg=-0.15 * fuselage_length
)

mass_props['MPPTs'] = asb.mass_properties_from_radius_of_gyration(
    mass=(n_panels / 36) * 0.080,  # Genasun GV-5
    x_cg=x_fuse_nose + 5 * u.inch,
    z_cg=-0.15 * fuselage_length
)

mass_props['solar_cells'] = asb.mass_properties_from_radius_of_gyration(
    mass=solar_area * rho_solar_cells,
    x_cg=0.25 * wing_root_chord,  # at the half-chord (remembering that datum is at quarter-chord)
)

mass_props['wiring'] = asb.mass_properties_from_radius_of_gyration(
    mass=(n_panels / 72) * 0.100,
    x_cg=-wing_root_chord / 4,  # at the leading edge
    z_cg=-0.05 * fuselage_length
)

### Other
mass_props['wing_sponsons'] = asb.mass_properties_from_radius_of_gyration(
    mass=2 * (  # 2 sponsons
            wing_sponson_wetted_area * (
            2 *  # plies
            (4 * u.oz / u.yard ** 2)
    )
    ) * 1.5  # waterproofing markup
    ,
    x_cg=0  # quarter-chord
)
mass_props['wing_sponson_mounts'] = copy.copy(
    mass_props['wing_sponsons']
) * 2  # a total guess

### Summation
mass_props_TOGW = sum(mass_props.values())

### Add glue weight
mass_props['glue_weight'] = mass_props_TOGW * 0.08
mass_props_TOGW += mass_props['glue_weight']









