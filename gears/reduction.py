# imports
import numpy as np

def valid_reduction(N1, N2):
  '''
  determines whether 2 gear gears achieve the desired reduction

  N1: 1st and 3rd gear (driving) number of teeth
  N2: 2nd and 4th gear (driven) number of teeth
  '''
  
  # Design Inputs

  vmax = 180 # car max speed, km/hr
  tdia = 0.499 # tire diameter, m
  nmax = 10000 # motor max rotation speed

  # Rotation speed of geartrain output

  nl = vmax * 1000 / 3600 / (tdia/2) * 1 / (2*np.pi) * 60
  # print("Max Geartrain Output speed: ", nl, "rpm")

  # Rotation speed of geartrain 1st gear
  nf = nmax
  # print("First gear rotation speed: ", nf, "rpm")

  # Max Geartrain Value
  emax = nl/nf
  # print('Max geartrain value', emax)

  # Actual Geartrain value
  e = (N1/N2)**2
  # print("Actual geartrain value", e)

  if (e > emax):
    return False
    # raise ValueError("The geartrain value should not exceed the max value")
  
  else:
    return True

