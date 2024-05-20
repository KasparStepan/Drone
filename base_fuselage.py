import numpy as np
import aerosandbox as asb

class Base_fuselage():
    def __init__(self,fuselage_length):
        self.fuselage_length = fuselage_length

        self.fuselage_tip = asb.Fuselage(
            name="Fuselage tip",
            xsecs=[
                asb.FuselageXSec(
                    xyz_c = [ xi*0.1-0.1,0,0],
                    # radius = np.sin(xi/0.1*np.pi/2)*0.05
                    radius = np.sqrt(1-(-1+xi)**2)*0.015
                )for xi in np.cosspace(0,1,30)            
            ]
        )

        self.fuselage_body = asb.Fuselage(
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
        self.fuselage_transition = asb.Fuselage(
            name ="Fuselage transition",
            xsecs = [
                asb.FuselageXSec(
                    xyz_c=[0.25+xi/np.pi*0.1,0,0],
                    radius = (np.cos(xi)+1)*0.0075/2+0.0075
                )for xi in np.cosspace(0,np.pi,30)
            ]
        )
        self.fuselage_tail = asb.Fuselage(
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
        self.fuselage_tail_tip = asb.Fuselage(
            name="Fuselage tail tip",
            xsecs=[
                asb.FuselageXSec(
                    xyz_c = [ 0.7+xi*0.05,0,0],
                    radius = np.sqrt(1-(xi)**2)*0.0075
                )for xi in np.cosspace(0,1,30)
            ]
        )
