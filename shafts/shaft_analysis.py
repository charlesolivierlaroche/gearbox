import numpy as np
from matplotlib import pyplot as plt

def shaft_analysis_metric(d, Sy, Sut, q, qs, Kt, Kts, sf, Fa, Fm, Ma, Mm, Ta, Tm):
  '''
  d: shaft diameter
  Sy: material yield strength
  Sut: material ultimate strength
  q: notch sensitivity factor
  qs: notch shear sensitivity factor
  sf: safety factor
  Fa: alternating axial force (N)
  Fm: mean axial force (N)
  Ma: alternating moment (N*m)
  Mm: mean moment (N*m)
  Ta: alternating torque (N*m)
  Tm: mean torque (N*m)
  '''

  # Fatigue Analysis:
  
  # Endurance Limit
  if (Sut <= 1400):
    Se_prime = 0.5*Sut
  else:
    Se_prime = 700 # MPa


  # Surface Factor
  match sf:
    case "ground":
      a = 1.58
      b = -0.085
    case "machined":
      a = 4.51
      b = -0.265
    case "cold-drawn":
      a = 4.51
      b = -0.265
    case "hot-rolled":
      a = 57.7
      b = -0.718
    case "as-forged":
      a = 272
      b= -0.995
  Ka = a*(Sut)**b

  # Size Factor

  if (d >= 2.79 and d <= 51):
    Kb = 1.24*d**(-0.107)
  elif (d > 51 and d <= 254):
    Kb = 1.51*d**(-0.157)
  else:
    print("diameter out of range")
    return
  
  # Loading Factor
  Kc = 1

  # Temperature Factor
  Kd = 1

  # Reliability Factor
  # Assuming 2 bearings per shaft, 4 gears, 2 shafts
  Ke = 0.702
  

  # Miscellaneous Effect
  Kf = 1

  # Endurance Limit
  Se = Ka*Kb*Kc*Kd*Ke*Kf*Se_prime

  

  # Axial Stresses
  
  sigma_a_ax = 4*Fa/(np.pi*d**2)
  sigma_m_ax = 4*Fm/(np.pi*d**2)

  # Bending Stresses

  sigma_a_bd = 32*Ma/(np.pi*d**3) * 1000 # convert to MPa
  sigma_m_bd = 32*Mm/(np.pi*d**3) * 1000 # convert to MPa

  # Shear Stresses (Torque)
  
  tau_a = 16*Ta/(np.pi*d**3) * 1000 # convert to MPa
  tau_m = 16*Tm/(np.pi*d**3) * 1000 # convert to MPa

  # Fatigue Stress Concentration Factors

  Kf = 1 + q*(Kt-1) # For bending and axial
  Kfs = 1 + qs*(Kts - 1) # For Torque

  # Effective Stresses
  sigma_prime_a = ((Kf*sigma_a_bd + Kf*sigma_a_ax**2/0.85)**2 + 3*(Kfs*tau_a)**2)**(0.5)

  sigma_prime_m = ((Kf*sigma_m_bd + Kf*sigma_m_ax**2)**2 + 3*(Kfs*tau_m)**2)**(0.5)

  # Fatigue Safety Factor
  nf = (sigma_prime_a/Se + sigma_prime_m/Sut)**(-1)

  # Static Safety Factor
  ny = Sy/(sigma_prime_m + sigma_prime_a)

  if (nf > ny):
    n = ny
    #print("Critical in Static Loading")
  else:
    n = nf
    #print("Critical in Fatigue")
  
  # Checks
  print("Surface Factor: ", Ka)
  print("Size Factor: ", Kb)
  print("Loading Factor: ", Kc)
  print("Temperature Factor: ", Kc)
  print("Reliability Factor: ", Ke)
  print("Endurance Limit: ", Se)
  print("Alternating Axial Stress: ", sigma_a_ax, " MPa")
  print("Mean Axial Stress: ", sigma_m_ax, " MPa")
  print("Alternating Bending Stress: ", sigma_a_bd, " MPa")
  print("Mean Bending Stress: ", sigma_m_bd, " MPa")
  print("Alternating Torsion Stress: ", tau_a, " MPa")
  print("Mean Torsion Stress: ", tau_m, " MPa")
  print("Bending Stress Concentration Factor: ", Kt)
  print("Torsion Stress Concentration Factor: ", Kfs)
  print("Notch Sensitivity: ", q)
  print("Shear Notch Sensitivity: ", qs)
  print("Fatigue Concentration Factor: ", Kf)
  print("Shear Fatigue Concentration Factor: ", Kfs)
  print("DE-Goodman Alternating Stress: ", sigma_prime_a, " MPa")
  print("DE-Goodman Mean Stress: ", sigma_prime_m, " MPa")
  print("Safety Factor in Fatigue: ", nf)
  print("Safety Factor in Yield: ", ny)

  return n