import numpy as np

def interference(Ng, Np, phi, k=1):
  '''
  Outputs True if there is no interference between gears

  Ng: number of teeth of the gear
  Np: number of teeth of the pinion
  phi: pressure angle
  k = 1: full depth teeth (stub teeth = 0.8)
  '''
  phi_rad = phi * np.pi/180
  m = Ng/Np
  Npmin = (2 * k)/((1 + 2 * m)*np.sin(phi_rad)**2)*(m + np.sqrt(m**2+(1+2*m)*np.sin(phi_rad)**2))

  if (Npmin > Np):
    # print("There is interference between the gears")
    return False
  else:
    # print("No interference")
    return True
