import aerosandbox.numpy as np
import aerosandbox as asb




class Airplane():
        def __init__(self,wingspan,chord,twist,sweep_angle,dihedral_angle,fuselage_radius,airplane_length,airplane_type,
                       name = "deafult name",
                       infill_default = 0.2,
                       skin_thickness_default = 0.002,
                       material_type = "PLA",
                       ):
                    

                self.wingspan = wingspan
                self.chord = chord
                self.twist = twist
                self.sweep_angle = sweep_angle
                self.dihedral_angle = dihedral_angle
                self.airplane_length = airplane_length
                self.fuselage_radius = fuselage_radius
                self.cruise_speed = 10
                self.minAoA = 0
                self.maxAoA = 15
                self.stepAoA = 1
                self.name = name
                self.alpha = np.linspace(self.minAoA,self.maxAoA,int((self.maxAoA-self.minAoA)/self.stepAoA))


                self.mass_props = {}
                self.object_props = []

                self.infill_default = infill_default
                self.skin_thickness_default = skin_thickness_default

                self.filament_density = {
                'PLA': 1250,
                "LW-PLA": 800
                }
                
                self.material_type = material_type
                
                self.skin_thickness = {
                "Wing": self.skin_thickness_default,
                "Fuselage tip" : self.skin_thickness_default,
                "Fuselage body": self.skin_thickness_default,
                "Fuselage transition": self.skin_thickness_default,
                "Fuselage tail": self.skin_thickness_default,
                "Fuselage tail tip": self.skin_thickness_default,
                }
                
                self.infill = {
                "Wing": self.infill_default,
                "Fuselage tip" : 0,
                "Fuselage body": 0,
                "Fuselage transition": 0,
                "Fuselage tail": 0,
                "Fuselage tail tip": 0,
                }
                
                self.airplane_type = airplane_type


                self.generate_airplane()

                
        def generate_wings(self):
                self.speed_wing = asb.Wing(
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
                                                chord = self.chord['Main_mid_center'],
                                                twist = self.twist['Main_mid_center'],
                                                airfoil=asb.Airfoil('rg15'),
                                                ),
                                asb.WingXSec(#Center tip
                                        xyz_le=[self.wingspan['Main_center']*np.tan(np.deg2rad(self.sweep_angle['Main_center'])),
                                                self.wingspan['Main_center'],
                                                self.wingspan['Main_center']*np.tan(np.deg2rad(self.dihedral_angle['Main_center']))],
                                                chord=self.chord['Main_end_center'],
                                                twist=self.twist['Main_end_center'],
                                                airfoil= asb.Airfoil('rg15')
                                                ),
                                asb.WingXSec(#Tip
                                        xyz_le=[self.wingspan['Main_center']*np.tan(np.deg2rad(self.sweep_angle['Main_center']))+self.wingspan['Main_tip']*np.tan(np.deg2rad(self.sweep_angle['Main_tip'])),
                                                self.wingspan['Main_center']+self.wingspan['Main_tip'],
                                                self.wingspan['Main_center']*np.tan(np.deg2rad(self.dihedral_angle['Main_center']))+self.wingspan['Main_tip']*np.tan(np.deg2rad(self.dihedral_angle['Main_tip']))],
                                                chord=self.chord['Main_tip'],
                                                twist=self.twist['Main_tip'],
                                                airfoil= asb.Airfoil('rg15')
                                                )
                        ]
                        )
                self.endurance_wing = asb.Wing(
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
                                                chord = self.chord['Main_root'],
                                                twist = self.twist['Main_root'],
                                                airfoil=asb.Airfoil('rg15'), # Flap # Control surfaces are applied between a given XSec and the next one.
                                                ),
                                asb.WingXSec(#Center mid
                                        xyz_le = [0,
                                                self.wingspan['Main_mid'],
                                                0],
                                                chord = self.chord['Main_mid_center'],
                                                twist = self.twist['Main_mid_center'],
                                                airfoil=asb.Airfoil('rg15'),
                                                ),
                                asb.WingXSec(#Center tip
                                        xyz_le=[self.wingspan['Main_center']*np.tan(np.deg2rad(self.sweep_angle['Main_center'])),
                                                self.wingspan['Main_mid']+self.wingspan['Main_center'],
                                                self.wingspan['Main_center']*np.tan(np.deg2rad(self.dihedral_angle['Main_center']))],
                                                chord=self.chord['Main_end_center'],
                                                twist=self.twist['Main_end_center'],
                                                airfoil= asb.Airfoil('rg15')
                                                ),
                                asb.WingXSec(#Tip
                                        xyz_le=[self.wingspan['Main_center']*np.tan(np.deg2rad(self.sweep_angle['Main_center']))+self.wingspan['Main_tip']*np.tan(np.deg2rad(self.sweep_angle['Main_tip'])),
                                                self.wingspan['Main_mid']+self.wingspan['Main_center']+self.wingspan['Main_tip'],
                                                self.wingspan['Main_center']*np.tan(np.deg2rad(self.dihedral_angle['Main_center']))+self.wingspan['Main_tip']*np.tan(np.deg2rad(self.dihedral_angle['Main_tip']))],
                                                chord=self.chord['Main_tip'],
                                                twist=self.twist['Main_tip'],
                                                airfoil= asb.Airfoil('rg15')
                                                )
                        ]
                        )

                self.fuselage_translation = -1*(0.2237-(self.speed_wing.aerodynamic_center(chord_fraction=0.25)[0]+self.endurance_wing.aerodynamic_center(chord_fraction=0.25)[0])/2)     
                
                        



        def generate_airplane(self):

                self.generate_wings()
                self.generate_tail_wing()
                self.generate_fuselage()

                if self.airplane_type == "Endurance":
                        self.Wing = self.endurance_wing
                        
                elif self.airplane_type == "Speed":
                        self.Wing = self.speed_wing

                self.airplane = asb.Airplane(
                        name = self.name,
                        xyz_ref = [self.Wing.aerodynamic_center(chord_fraction=0.25)[0],0,0],
                        s_ref = self.Wing.area(), #Reference area
                        c_ref = self.Wing.mean_aerodynamic_chord(), #Reference chord
                        b_ref = self.Wing.span(), #Reference span
                        wings=[
                                self.Wing,
                                self.Tail_wing
                                ],
                        fuselages=self.fuselage

                        )
                self.mass_plane()

        
        def generate_tail_wing(self):
                self.Tail_wing = asb.Wing(
                        name = "Tail wing",
                        xyz_le=[0,
                                0,
                                0],
                                symmetric=True,
                                xsecs=[
                                        asb.WingXSec(
                                                xyz_le=[self.airplane_length-self.chord['Tail_root'],
                                                        0,
                                                        0],
                                                chord=self.chord['Tail_root'],
                                                twist=self.twist['Tail_root'],
                                                airfoil=asb.Airfoil('naca0012')
                                                ),
                                        asb.WingXSec(
                                                xyz_le=[self.airplane_length+self.wingspan['Tail']*np.tan(np.deg2rad(self.sweep_angle['Tail']))-self.chord['Tail_tip'],
                                                        self.wingspan['Tail']*np.tan(np.deg2rad(self.dihedral_angle['Tail'])),
                                                        self.wingspan['Tail']],
                                                chord=self.chord['Tail_tip'],
                                                twist=self.twist['Tail_tip'],
                                                airfoil=asb.Airfoil('naca0012')
                                                )
                                ]
                        ).translate([self.fuselage_translation,0,0])
                
        def generate_fuselage(self):
                self.fuselage_tip = asb.Fuselage(
                        name="Fuselage tip",
                        xsecs=[
                                asb.FuselageXSec(
                                        xyz_c = [ xi*0.1*self.airplane_length-0.1*self.airplane_length,0,0],
                                        radius = np.sqrt(1-(-1+xi)**2)*self.fuselage_radius['Big']
                                        )for xi in np.cosspace(0,1,30)
                        ]
                ).translate([self.fuselage_translation,0,0])
                self.fuselage_body = asb.Fuselage(
                        name="Fuselage body",
                        xsecs=[
                                asb.FuselageXSec(
                                        xyz_c = [0,0,0],
                                        radius = self.fuselage_radius['Big']
                                        ),
                                asb.FuselageXSec(
                                        xyz_c = [0.45,0,0],
                                        radius = self.fuselage_radius['Big']
                                        )
                                        ]
                                        ).translate([self.fuselage_translation,0,0])
                self.fuselage_transition = asb.Fuselage(
                        name ="Fuselage transition",
                        xsecs = [
                                asb.FuselageXSec(
                                        xyz_c=[0.45+xi/np.pi*self.airplane_length*0.2,0,(np.cos(xi+np.pi)+1)/2*(self.fuselage_radius['Small'])/2],
                                        radius = (np.cos(xi)+1)*(self.fuselage_radius['Big']-self.fuselage_radius['Small'])/2+self.fuselage_radius['Small']
                                        )for xi in np.cosspace(0,np.pi,30)
                                        ]
                                        ).translate([self.fuselage_translation,0,0])
                
                self.fuselage_tail = asb.Fuselage(
                        name = "Fuselage tail",
                        xsecs=[
                                asb.FuselageXSec(
                                        xyz_c = [0.45+self.airplane_length*0.2,0,self.fuselage_radius['Small']/2],
                                        radius = self.fuselage_radius['Small']
                                        ),
                                asb.FuselageXSec(
                                        xyz_c = [self.airplane_length,0,self.fuselage_radius['Small']/2],
                                        radius = self.fuselage_radius['Small']
                                        )
                        ]
                ).translate([self.fuselage_translation,0,0])
                
                self.fuselage_tail_tip = asb.Fuselage(
                        name="Fuselage tail tip",
                        xsecs=[
                                asb.FuselageXSec(
                                        xyz_c = [self.airplane_length+xi*0.05,0,self.fuselage_radius['Small']/2],
                                        radius = np.sqrt(1-(xi)**2)*self.fuselage_radius['Small']
                                        )for xi in np.cosspace(0,1,30)
                        ]
                        ).translate([self.fuselage_translation,0,0])
                
                self.fuselage = [self.fuselage_tip,
                                self.fuselage_body,
                                self.fuselage_transition,
                                self.fuselage_tail,
                                self.fuselage_tail_tip]
                
        def draw_airplane(self):
                self.airplane.draw()
        
        def set_speed(self,speed):
                self.cruise_speed = speed
                self.create_operating_point()
        
        def set_AoA_range(self,min=0,max=15,step=1):
                self.alpha = np.linspace(min,max,int((max-min)/step))
                self.create_operating_point()
        
        def create_operating_point(self):
                self.airplane_operating_point = asb.OperatingPoint(
                        atmosphere=asb.Atmosphere(altitude=0),
                        velocity= self.cruise_speed,
                        alpha=self.alpha
                )
        def runVLM(self):
                self.create_operating_point()
                self.aero_data_run = [
                        asb.VortexLatticeMethod(
                                airplane=self.airplane,
                                op_point=op,
                                ).run() for op in self.airplane_operating_point
                                ]
                self.aero_data = {'alpha':self.alpha}
                
                for k in self.aero_data_run[0].keys():
                        self.aero_data[k] = np.array([
                                aero[k]
                                for aero in self.aero_data_run
                                ])
                      
                self.evaluation()

        def runLL(self):
                self.create_operating_point()
                self.aero_data_run = [
                        asb.LiftingLine(
                                airplane=self.airplane,
                                op_point=op,
                                ).run() for op in self.airplane_operating_point
                                ]
                self.aero_data = {'alpha':self.alpha}
                
                for k in self.aero_data_run[0].keys():
                        self.aero_data[k] = np.array([
                                aero[k]
                                for aero in self.aero_data_run
                                ])
                        
                self.evaluation()
                
                        
                
        def evaluation(self):
                self.eval_efficiency()
                self.eval_pitch_criteria()
                self.eval_negative_slope_pitch()
                self.eval_total_pitch()

        def eval_efficiency(self):
                # Calculation of airplane efficiency
                self.aero_data['efficiency'] = self.aero_data['CL']/self.aero_data['CD']
                self.aero_data['total_pitch'] = self.aero_data['Cm'] - (self.total_mass.x_cg-self.Wing.aerodynamic_center(chord_fraction=0.25)[0])*self.aero_data['CL']
                
                self.max_efficiency_AoA = self.aero_data['alpha'][np.argmax(self.aero_data['efficiency'])]
                
                return self.max_efficiency_AoA


        def eval_pitch_criteria(self):
                ## Evaluation of difference of angle of attack of zero pitch and maximum efficiency

                for i in range(len(self.aero_data['Cm'])-1):
                        if (self.aero_data['Cm'][i]*self.aero_data['Cm'][i+1]) < 0:
                                self.zero_pitch_aoa = self.aero_data['Cm'][i]*(self.aero_data['alpha'][i]-self.aero_data['alpha'][i+1])/(self.aero_data['Cm'][i+1]-self.aero_data['Cm'][i])+self.aero_data['alpha'][i]
                                

                self.pitch_criteria = np.abs(self.max_efficiency_AoA-self.zero_pitch_aoa)
                return self.pitch_criteria               

                 
        def eval_total_pitch(self):
                for i in range(len(self.aero_data['alpha'])):
                        if self.aero_data['alpha'][i] == 0:
                                self.zero_aoa_pitch = self.aero_data['Cm'][i]
                return self.zero_aoa_pitch

        def eval_negative_slope_pitch(self):
                for i in range(len(self.aero_data['Cm'])-1):
                        if (self.aero_data['Cm'][i+1]-self.aero_data['Cm'][i]) > 0:
                                self.pitch_slope_check = False
                        else:
                                self.pitch_slope_check = True
                return self.pitch_slope_check
        
        def set_name(self,name):
                self.name = name 

        def mass_plane(self):
                for i in self.fuselage:
                        self.mass_props[i.name] = asb.mass_properties_from_radius_of_gyration(
                                (i.volume()*self.infill[i.name]+i.area_wetted()*self.skin_thickness[i.name])*self.filament_density[self.material_type],
                                x_cg = i.x_centroid_projected('XY')
                        )

                self.mass_props["Electric motor"] = asb.mass_properties_from_radius_of_gyration(
                        mass = 0.05, # Needs to be researched
                        x_cg = 0,
                        y_cg = 0,
                        z_cg = 0,
                        radius_of_gyration_x = 0,
                        radius_of_gyration_y = 0,
                        radius_of_gyration_z = 0,
                )

                self.mass_props["Propeller"] = asb.mass_properties_from_radius_of_gyration(
                        mass = 0.04, # Needs to be researched
                        x_cg = 0,
                        y_cg = 0,
                        z_cg = 0,
                        radius_of_gyration_x = 0,
                        radius_of_gyration_y = 0,
                        radius_of_gyration_z = 0,
                )


                self.mass_props['Avionics'] = asb.mass_properties_from_radius_of_gyration(
                mass=0.060,  # RX, pixhawk mini
                x_cg=0.3425,
                y_cg=0,
                z_cg=-0.00625
                )

                

                self.mass_props['servos'] = asb.mass_properties_from_radius_of_gyration(
                mass=0.050, #find the number and the weight
                x_cg=0,
                y_cg = 0
                )

                self.mass_props['battery'] = asb.mass_properties_from_radius_of_gyration(
                mass=0.22, #To be determined
                x_cg=0.352,
                y_cg=0,
                z_cg=0.025
                )


                self.mass_props["Payload"] = asb.mass_properties_from_radius_of_gyration(
                mass=0.73, #To be determined
                x_cg=0.15,
                y_cg=0,
                z_cg=0
                )


                self.mass_props['Tail_wing'] = asb.mass_properties_from_radius_of_gyration(
                        mass = (self.Tail_wing.volume()*self.infill["Wing"]+self.Tail_wing.area("wetted")*self.skin_thickness["Wing"])*self.filament_density[self.material_type],
                        x_cg = self.Tail_wing.aerodynamic_center(chord_fraction=0.25)[0],
                        y_cg = self.Tail_wing.aerodynamic_center(chord_fraction=0.25)[1],
                        z_cg = self.Tail_wing.aerodynamic_center(chord_fraction=0.25)[2]

                )

                self.mass_props['Wing'] = asb.mass_properties_from_radius_of_gyration(
                        mass = (self.Wing.volume()*self.infill["Wing"]+self.Wing.area("wetted")*self.skin_thickness["Wing"])*self.filament_density[self.material_type],
                        x_cg = self.Wing.aerodynamic_center(chord_fraction=0.25)[0],
                        y_cg = self.Wing.aerodynamic_center(chord_fraction=0.25)[1],
                        z_cg = self.Wing.aerodynamic_center(chord_fraction=0.25)[2]
                        )       
                
                self.total_mass = asb.MassProperties(mass=0)
                for k,v in self.mass_props.items():
                        self.total_mass = self.total_mass+v
                       
