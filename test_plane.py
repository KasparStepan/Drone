import Airplane_class
from PostPro import PostPro

chord = { #m
       'Main_root':0.15,
         'Main_mid_center': 0.15,
         'Main_end_center': 0.13,
         'Main_tip':0.05,
         'Tail_root':0.13,
         'Tail_tip':0.05 
         }



wingspan = { #m
       'Main_mid':0.2,
            'Main_center':0.3,
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
        'Big':0.05,
        'Small':0.02
}

airplane_length = 1.2





endurance_plane = Airplane_class.Airplane(name = "Endurance plane",airplane_type="Endurance",wingspan=wingspan,chord=chord,twist=twist,sweep_angle=sweep_angle,dihedral_angle=dihedral_angle,fuselage_radius=fuselage_radius,airplane_length=airplane_length)
speed_plane = Airplane_class.Airplane(name = "Speed plane",airplane_type="Speed",wingspan=wingspan,chord=chord,twist=twist,sweep_angle=sweep_angle,dihedral_angle=dihedral_angle,fuselage_radius=fuselage_radius,airplane_length=airplane_length)

endurance_plane.runVLM()
speed_plane.runVLM()

print(f"Parameters evaluated for: {endurance_plane.name}")
print(f'Maximum efficiency of airplane is at AoA: {endurance_plane.max_efficiency_AoA} deg')
print(f'AoA difference for maximum efficiency and zero pitch: {endurance_plane.pitch_criteria} [deg]')
print(f'Pitch moment slope is negative acros the whole range of AoA: {endurance_plane.pitch_slope_check}')
print(f'Zero pitch is at AoA: {endurance_plane.zero_aoa_pitch} [deg]')

print(f"Parameters evaluated for: {speed_plane.name}")
print(f'Maximum efficiency of airplane is at AoA: {speed_plane.max_efficiency_AoA} deg')
print(f'AoA difference for maximum efficiency and zero pitch: {speed_plane.pitch_criteria} [deg]')
print(f'Pitch moment slope is negative acros the whole range of AoA: {speed_plane.pitch_slope_check}')
print(f'Zero pitch is at AoA: {speed_plane.zero_aoa_pitch} [deg]')



post = PostPro()
post.add_plane(endurance_plane.aero_data,label=endurance_plane.name)
post.add_plane(plane_data=speed_plane.aero_data,label=speed_plane.name)

post.plot_results()

endurance_plane.draw_airplane()
