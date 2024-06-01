import numpy as np
import matplotlib.pyplot as plt

class PostPro():

          def __init__(self,plane_list=[],label_list=[]):
                  self.plane_list = plane_list
                  self.label_list = label_list
                                    
          def add_plane(self,plane_data,label):
                  self.plane_list.append(plane_data)
                  self.label_list.append(label)        

          def plot_results(self):
                    plt.subplot(3,3,1)
                    for i in range(len(self.plane_list)):
                              plt.plot(self.plane_list[i]['CD'],self.plane_list[i]['CL'],label = self.label_list[i])
                    plt.legend()
                    plt.grid()
                    plt.title('Aerodynamic polar')
                    plt.xlabel('CD [-]')
                    plt.ylabel('CL [-]')


                    plt.subplot(3,3,2)
                    for i in range(len(self.plane_list)):
                              plt.plot(self.plane_list[i]['alpha'],self.plane_list[i]['Cm'],label = self.label_list[i])
                    plt.legend()
                    plt.grid()
                    plt.title('Moment polar')
                    plt.xlabel('alpha [deg]')
                    plt.ylabel('CM [-]')


                    plt.subplot(3,3,3)
                    for i in range(len(self.plane_list)):
                              plt.plot(self.plane_list[i]['alpha'],self.plane_list[i]['CL'],label = self.label_list[i])
                    plt.legend()
                    plt.grid()
                    plt.title('Lift curve')
                    plt.xlabel('alpha [deg]')
                    plt.ylabel('CL [-]')

                    plt.subplot(3,3,4)
                    for i in range(len(self.plane_list)):
                              plt.plot(self.plane_list[i]['alpha'],self.plane_list[i]['CD'],label = self.label_list[i])
                    plt.legend()
                    plt.grid()
                    plt.title('Drag curve')
                    plt.xlabel('alpha [deg]')
                    plt.ylabel('CD [-]')

                    
                    plt.subplot(3,3,5)
                    for i in range(len(self.plane_list)):
                              plt.plot(self.plane_list[i]['alpha'],self.plane_list[i]['total_pitch'],label = self.label_list[i])
                    plt.legend()
                    plt.grid()
                    plt.title('Airplane moment curve with CoG moment')
                    plt.xlabel('alpha [deg]')
                    plt.ylabel('Cm_airplane [-]')
                    


                    plt.subplot(3,3,6)
                    for i in range(len(self.plane_list)):
                              plt.plot(self.plane_list[i]['alpha'],self.plane_list[i]['efficiency'],label = self.label_list[i])
                    plt.legend()
                    plt.grid()
                    plt.title('Aerodynamic efficiency')
                    plt.xlabel('alpha [deg]')
                    plt.ylabel('CL/CD [-]')

                    """

                    plt.subplot(3,3,7)
                    for i in range(len(self.plane_list)):
                              plt.plot(self.plane_list[i]['alpha'],self.plane_list[i]['endurance'],label = self.label_list[i])
                    plt.legend()
                    plt.grid()
                    plt.title('Endurance')
                    plt.xlabel('alpha [deg]')
                    plt.ylabel('Time [h]')
                    """

                    plt.show()