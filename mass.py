
mass = [0.182*2,0.06,0.73]
x = [0.352,0.342,0.15]

x_cg = 0
mass_cg=0

for i in range(len(mass)):
    x_cg = x_cg+x[i]*mass[i]
    mass_cg = mass_cg + mass[i]

x_cog = x_cg/mass_cg
print(x_cog)