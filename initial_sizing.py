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
AR = opti.variable() #Aspect ratio [-]
S = opti.variable() # Wing Area [-]



# Flow parameters

altitude = 0 # m ISA
