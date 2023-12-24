from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import cumulative_trapezoid as ct

def input_diagrams(dele, w_gear, w_bear, w_motor, dg1, Wtg1, Wrg1, h=0.0005):
  '''
  Generate the Torque, shear and moment diagrams for an input shaft
  Input shaft must be configured in the following way:
    Spline -- Bearing -- Gear -- Bearing

  dele: distance between the elements , m
  w_gear: face width of the gear
  w_bear: width of the bearing
  w_motor: face width of the motor coupling
  dg1: diameter of 2nd gear in the train, m
  Wtg1: Tangential Force on G2, N
  Wrg1: Radial Force on G2, N
  h: step size
  '''

  # Torque
  Tg1 = Wtg1*dg1/2

  # Locate Elements
  L = w_bear + dele + w_gear + dele + w_bear + 2*dele + w_motor
  length = np.arange(0, L+h, h)

  print("Input Shaft Length: ", L*1000, "mm")

  i_motor = w_motor/2
  i_bear1 = w_motor + 2*dele + w_bear/2  
  i_gear1 = w_motor + 2*dele + w_bear + dele + w_gear/2
  i_bear2 = w_motor + 2*dele + w_bear + dele + w_gear + dele + w_bear/2

  print("Motor Coupling Location: ", i_motor*1000, "mm")
  print("Bearing 1 Location: ", i_bear1*1000, "mm")
  print("Gear 1 Location: ", i_gear1*1000, "mm")
  print("Bearing 2 Location: ", i_bear2*1000, "mm \n")

  # Reaction Forces
  Fr2_x = (Wrg1*(i_gear1 - i_bear1))/(i_bear2 - i_bear1)
  Fr2_y = (Wtg1*(i_gear1 - i_bear1))/(i_bear2 - i_bear1)
  Fr1_x = Wrg1 - Fr2_x
  Fr1_y = Wtg1 - Fr2_y

  print("Fx on Bearing 1: ", Fr1_x, "N")
  print("Fy on Bearing 1: ", Fr1_y, "N")
  print("Fx on Bearing 2: ", Fr2_x, "N")
  print("Fy on Bearing 2: ", Fr2_y, "N")

  i = np.where(np.isclose(length, i_motor))[0][0]
  j = np.where(np.isclose(length, i_gear1))[0][0]
  k = np.where(np.isclose(length, i_bear1))[0][0]
  l = np.where(np.isclose(length, i_bear2))[0][0]
  x = np.array(length)

  # Torque Diagram
  y = np.zeros((length.shape[0]))
  y[i:j] = Tg1

  # plot
  Tdiag, ax_t = plt.subplots()
  ax_t.set_xlabel(r'$x$ (position along the shaft, m)')
  ax_t.set_ylabel(r'$y$ (Torque N*m)')
  ax_t.set_title(r'Input Shaft Torque Diagram')
  ax_t.plot(x, y, label='Torque')
  ax_t.legend(loc='upper left')
  Tdiag.tight_layout()
  plt.show()

  Tmax = np.abs(y).max()

  # Shear & Moment Diagrams
  # x-z plane
  y = np.zeros((length.shape[0]))
  y[k:j] = Fr1_x
  y[j:l] = Fr1_x - Wrg1
  y[l:] = Fr1_x - Wrg1 + Fr2_x

  # plot
  Vdiag1, ax_Vx = plt.subplots()
  ax_Vx.set_xlabel(r'$x$ (position along the shaft, m)')
  ax_Vx.set_ylabel(r'$y$ (Shear in x-z plane N)')
  ax_Vx.set_title(r'Input Shaft x-z Plane Shear Diagram')
  ax_Vx.plot(x, y, label='Shear')
  ax_Vx.legend(loc='upper right')
  Vdiag1.tight_layout()
  plt.show()

  y = ct(y, x, initial=0)

  # plot
  Mdiag1, ax_Mx = plt.subplots()
  ax_Mx.set_xlabel(r'$x$ (position along the shaft, m)')
  ax_Mx.set_ylabel(r'$y$ (Moment in x-z plane N*m)')
  ax_Mx.set_title(r'Input Shaft x-z Plane Moment Diagram')
  ax_Mx.plot(x, y, label='Bending Moment')
  ax_Mx.legend(loc='upper left')
  Mdiag1.tight_layout()
  plt.show()

  Mxmax = np.abs(y).max()

  # x-y plane
  y = np.zeros((length.shape[0]))
  y[k:j] = Fr1_y
  y[j:l] = Fr1_y - Wtg1
  y[l:] = Fr1_y - Wtg1 + Fr2_y

  # plot
  Vdiag2, ax_Vy = plt.subplots()
  ax_Vy.set_xlabel(r'$x$ (position along the shaft, m)')
  ax_Vy.set_ylabel(r'$y$ (x-y Plane Shear N)')
  ax_Vy.set_title(r'Input Shaft x-y Plane Shear Diagram')
  ax_Vy.plot(x, y, label='Shear Force')
  ax_Vy.legend(loc='upper right')
  Vdiag2.tight_layout()
  plt.show()

  y = ct(y, x, initial=0)

  # plot
  Mdiag2, ax_My = plt.subplots()
  ax_My.set_xlabel(r'$x$ (position along the shaft, m)')
  ax_My.set_ylabel(r'$y$ (y-z plane Moment N*m)')
  ax_My.set_title(r'Input Shaft y-z Plane Moment Diagram')
  ax_My.plot(x, y, label='Bending Moment')
  ax_My.legend(loc='upper left')
  Mdiag2.tight_layout()
  plt.show()

  Mymax = np.abs(y).max()

  Fr1_combined = np.sqrt(Fr1_x**2 + Fr1_y**2)
  Fr2_combined = np.sqrt(Fr2_x**2 + Fr2_y**2)
  Mmax_combined = np.sqrt(Mxmax**2 + Mymax**2)
  return Fr1_combined, Fr2_combined, Mmax_combined, Tmax

def idler_diagrams(dele, w_gear, w_bear, dg2, Wtg2, Wrg2, dg3, Wtg3, Wrg3, h=0.0005):
  '''
  Generate the Torque, shear and moment diagrams for a idler shaft
  Shaft must be configured as follows: 
    Bearing -- Gear -- Gear -- Bearing
    
  dele: distance between the elements , m
  w_gear: face width of the gear
  w_bear: width of the bearing
  dg2: diameter of 2nd gear in the train, m
  Wtg2: Tangential Force on G2, N
  Wrg2: Radial Force on G2, N
  dg3: diameter of 3rd gear in the train, pinion for output, m
  Wtg3: Tangential Force on G3, N
  Wrg3: Radial Force on G3, N
  h: step size
  '''
  # Torque
  Tg2 = Wtg2*dg2/2
  Tg3 = Wtg3*dg3/2
  
  # Locate Elements
  L = w_bear + dele + w_gear + dele + w_gear + dele + w_bear
  print("Idler Shaft Length: ", L*1000, "mm" )
  length = np.arange(0, L+h, h)
  
  # bearings
  i_bear1 = w_bear/2
  i_bear2 = L - w_bear/2
  

  # gears 
  i_gear2 = w_bear + dele + w_gear/2 
  i_gear3 = L - w_bear - dele - w_gear/2

  print("Bearing 1 Location: ", i_bear1*1000, "mm")
  print("Gear 2 Location: ", i_gear2*1000, "mm")
  print("Gear 3 Location: ", i_gear3*1000, "mm")
  print("Gear 4 Location: ", i_bear2*1000, "mm \n")

  # Reaction Forces
  Fr2_x = (Wrg2*(i_gear2-i_bear1) + Wrg3*(i_gear3-i_bear1))/(i_bear2-i_bear1)
  Fr2_y = (Wtg2*(i_gear2 - i_bear1) + Wtg3*(i_gear3 - i_bear1))/(i_bear2 - i_bear1)
  Fr1_x = Wrg2 + Wrg3 - Fr2_x
  Fr1_y = Wtg2 + Wtg3 - Fr2_y

  print("Fx on Bearing 1: ", Fr1_x, "N")
  print("Fy on Bearing 1: ", Fr1_y, "N")
  print("Fx on Bearing 2: ", Fr2_x, "N")
  print("Fy on Bearing 2: ", Fr2_y, "N")

  # Indices
  i = np.where(np.isclose(length, i_gear2))[0][0]
  j = np.where(np.isclose(length, i_gear3))[0][0]
  k = np.where(np.isclose(length, i_bear1))[0][0]
  l = np.where(np.isclose(length, i_bear2))[0][0]
  x = np.array(length)

  # Torque Diagram 
  y = np.zeros((length.shape[0]))
  y[i:j] = Tg2
  y[j:] =  Tg2-Tg3

  # plot
  Tdiag, ax_t = plt.subplots()
  ax_t.set_xlabel(r'$x$ (position along the shaft, m)')
  ax_t.set_ylabel(r'$y$ (Torque N*m)')
  ax_t.set_title(r'Idler Shaft Torque Diagram')
  ax_t.plot(x, y, label='Torque')
  ax_t.legend(loc='upper left')
  Tdiag.tight_layout()
  plt.show()

  Tmax = np.abs(y).max()


  # Shear & Moment Diagrams
  # x-z plane
  y = np.zeros((length.shape[0]))
  y[k:i] = Fr1_x
  y[i:j] = Fr1_x - Wrg2
  y[j:l] = Fr1_x - Wrg2 - Wrg3
  y[l:] =  Fr1_x - Wrg2 - Wrg3 + Fr2_x

  # plot
  Vdiag1, ax_Vx = plt.subplots()
  ax_Vx.set_xlabel(r'$x$ (position along the shaft, m)')
  ax_Vx.set_ylabel(r'$y$ (Shear in x-z plane N)')
  ax_Vx.set_title(r'Idler Shaft x-z Plane Shear Diagram')
  ax_Vx.plot(x, y, label='Shear')
  ax_Vx.legend(loc='upper right')
  Vdiag1.tight_layout()
  plt.show()

  y = ct(y, x, initial=0)

  # plot
  Mdiag1, ax_Mx = plt.subplots()
  ax_Mx.set_xlabel(r'$x$ (position along the shaft, m)')
  ax_Mx.set_ylabel(r'$y$ (Moment in x-z plane N*m)')
  ax_Mx.set_title(r'Idler Shaft x-z Plane Moment Diagram')
  ax_Mx.plot(x, y, label='Bending Moment')
  ax_Mx.legend(loc='upper left')
  Mdiag1.tight_layout()
  plt.show()

  Mxmax = np.abs(y).max()


  # y-z plane
  y = np.zeros((length.shape[0]))
  y[k:i] = Fr1_y
  y[i:j] = Fr1_y - Wtg2
  y[j:l] = Fr1_y - Wtg2 - Wtg3
  y[l:] =  Fr1_y - Wtg2 - Wtg3 + Fr2_y

  # plot
  Vdiag2, ax_Vy = plt.subplots()
  ax_Vy.set_xlabel(r'$x$ (position along the shaft, m')
  ax_Vy.set_ylabel(r'$y$ (x-y Plane Shear N)')
  ax_Vy.set_title(r'Idler Shaft x-y Plane Shear Diagram')
  ax_Vy.plot(x, y, label='Shear Force')
  ax_Vy.legend(loc='upper right')
  Vdiag2.tight_layout()
  plt.show()

  y = ct(y, x, initial=0)

  # plot
  Mdiag2, ax_My = plt.subplots()
  ax_My.set_xlabel(r'$x$ (position along the shaft, m)')
  ax_My.set_ylabel(r'$y$ (y-z plane Moment N*m)')
  ax_My.set_title(r'Idler Shaft y-z Plane Moment Diagram')
  ax_My.plot(x, y, label='Bending Moment')
  ax_My.legend(loc='upper left')
  Mdiag2.tight_layout()
  plt.show()

  Mymax = np.abs(y).max()

  Fr1_combined = np.sqrt(Fr1_x**2 + Fr1_y**2)
  Fr2_combined = np.sqrt(Fr2_x**2 + Fr2_y**2)
  Mmax_combined = np.sqrt(Mxmax**2 + Mymax**2)

  return Fr1_combined, Fr2_combined, Mmax_combined, Tmax
