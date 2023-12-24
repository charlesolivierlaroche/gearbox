import numpy as np
import data.lewisfactors as lf

def bending_stress(Wt, Ko, Kv, Ks, Pd, F, Km, Kb, J):
  '''
  Wt: Tangential Force (N or lbf)
  Ko: Overload Factor
  Kv: Dynamic Factor
  Ks: Size Factor
  Pd: transverse diametral pitch = 1/mt (transverse metric mod.)
  F: Face width (in or mm)
  Km: Load-distribution factor
  Kb: Rim-thickness factor
  J: Geometry Factor 
  '''
 
  
  sigma = Wt*Ko*Kv*Ks*Pd*Km*Kb/(F*J)
  
  return sigma

def contact_stress(Cp, Wt, Ko, Kv, Ks, Km, dp, F, Cf, I):
  '''
  Cp: Elastic Coefficient
  Wt: Tangential Force (N or lbf)
  Ko: Overload Factor
  Kv: Dynamic Factor
  Ks: Size Factor
  Km: Load-distribution factor
  dp: pinion pitch diameter (in or mm)
  F: Face width (in or mm)
  Cf: Surface condition factor
  I: Geometry Factor for pitting resistance 
  '''

  sigma_c = Cp*np.sqrt(Wt*Ko*Kv*Ks*Km*Cf/(dp*F*I))

  return sigma_c

def allowable_bending_stress(St, Yn, Kt, Kr):
  '''
  St: allowable bending stress (lbf/in^2 or N/mm^2)
  Yn: Stress cycle factor for bending stress
  Kt: temperature factor
  Kr: reliability factor
  '''

  sigma_bending_allowable = St*Yn/(Kt*Kr)

  return sigma_bending_allowable

def allowable_contact_stress(Sc, Zn, Ch, Kt, Kr):
  '''
  Sc: allowable contact stress (lbf/in^2 or N/mm^2)
  Zn: Stress cycle life factor 
  Kt: temperature factor
  Kr: reliability factor
  '''

  sigma_contact_allowable = Sc*Zn*Ch/(Kt*Kr)

  return sigma_contact_allowable

def geometry_factor(J, Jprime = 1):
  '''
  Jprime: Helical-Gear Geometry Factor (=1 for spur) L11 Fig. 14-7
  J: Helical or spur geometry factor L11 Fig. 14-6 (Spur) Fig. 14-8 (Helical)
  '''
  return J*Jprime

def ss_geometry_factor(phi_t, psi, pn, rp, rg, a, Ng, Np):
  '''
  phi_t: transverse pressure angle
  psi: helix angle
  pn: normal circular pitch
  rp: pinion pitch radius
  rg: gear pitch radius
  a: addendum
  Np: number of teeth of pinion
  Ng: number of teeth of gear
  '''
  # transverse pressure angle
  phi_n = np.arctan(np.tan(phi_t)/np.cos(psi))

  # Speed Ratio
  mg = Ng/Np

  # base-circle radii
  rbp = rp*np.cos(phi_t)
  rbg = rg*np.cos(phi_t)

  # Z
  Z = ((rp + a)**2 - rbp**2)**.5 + ((rg + a)**2 - rbg**2)**.5 - (rp + rg)*np.sin(phi_t)

  # 
  # Load Sharing Ratio
  # spur gear
  if (psi == 0):
    mn = 1
  else:
    PN = pn*np.cos(phi_n)
    mn = PN/(0.95*Z)
  
  # external gears
  I = np.cos(phi_t)*np.sin(phi_t)*mg/(2*mn*(mg + 1))

  return I

def elastic_coefficient(vp, vg, Ep, Eg):
  '''
  vp: Poisson's Ratio, pinion
  vg: Poisson's Ratio, gear
  Ep: Young's Modulus, pinion
  Eg: Young's Modulus, gear
  '''
  x1 = (1-vp**2)/Ep
  x2 = (1-vg**2)/Eg

  Cp = (1/(np.pi*(x1 + x2)))**.5

  return Cp

def pitch_line_velocity(Np, Ng, d, nmin, index, arg: str = 'metric'):
  if (index == 4):
    n = nmin
  
  elif (index == 2 or index == 3):
    n = Ng/Np*nmin
  
  elif (index == 1):
    n = (Ng/Np)**2*nmin

  if (arg == 'metric'):
    V = np.pi*d*n/60000
  elif (arg == 'us'):
    V = np.pi*d*n/12

  return V

def dynamic_factor(V, Qv, arg: str = 'metric'):
  '''
  d: pitch diameter (mm or in)
  n: rotation speed (rpm)
  Qv: AGMA quality number
  arg: specify if metric or US calc.
  '''
  B = 0.25*(12-Qv)**(2/3)
  A = 50+56*(1-B)

  if (arg == 'metric'):
    Kv = ((A + np.sqrt(200*V))/A)**B
  elif (arg == 'us'):
    Kv = ((A + np.sqrt(V))/A)**B
  
  return Kv

def max_recommended_velocity(Qv, arg: str = 'metric'):
  '''
  Qv: AGMA quality number
  '''
  B = 0.25*(12-Qv)**(2/3)
  A = 50+56*(1-B)

  if (arg == 'metric'):
    Vtmax = (A+Qv-3)**2/200
  elif (arg == 'us'):
    Vtmax = (A+Qv-3)**2

  return Vtmax

def overload_factor():
  return 1

def surface_condition_factor():
  return 1

def size_factor(F, N, d, lf: np.ndarray = lf.lewisFactors):
  '''
  F: face width (mm or in)
  N: Number of teeth
  d: pitch diameter (mm or in)
  lf: Lewis Factors table
  '''
  # diametral pitch
  P = N/d

  # Lewis Factor Interpolation
  if (N < 12 or N > 400):
    return None
  else:
    i = np.where(lf == N)[0] 

    if (len(i) == 0):
      Y = np.interp(N, lf[:, 0], lf[:, 1])
    else:
      Y = lf[i, 1].item()

  Ks = 1.192*(F*np.sqrt(Y)/P)**0.05035

  return Ks

def load_distribution_factor(F, d, S1, S, arg: str = 'metric'):
  '''
  F: Face width (mm or in)
  d: pitch diameter (mm or in)
  S1: Gear centerline offset distance from shaft center (mm or in)
  S: Shaft length (mm or in)
  A, B, C: Tabulated Factors
  '''

  # Lead Correction Factor
  Cmc = 1 # uncrowned teeth

  # mesh alignment correction factor
  Ce = 1 # no adjustment at assembly or lapping

  # pinion proportion modifier
  if (S1/S < 0.175):
    Cpm = 1
  else:
    Cpm = 1.1

  if (arg == 'metric'):
    # metric pinion-proportion Factor
    x = F/(10*d)
    if (F <= 25):
      Cpf = x - 0.025
    elif (F > 25 and F <= 432):
      Cpf = x - 0.0375 + 0.000492*F
    elif (F > 432 and F <= 1020):
      Cpf = x - 0.1109 + 0.000815*F -0.000000353*F**2
    else:
      return None
    
    # metric mesh alignment factor
    A = 0.274 # from  L11 Table 14-9
    B = 0.657e-3
    C = -1.186e-7
    Cma = A + B*F + C*F**2
  
  elif (arg == 'us'):
    # imperial pinion-proportion Factor
    x = F/(10*d)
    if (F <= 1):
      Cpf = x - 0.025
    elif (F > 1 and F <= 17):
      Cpf = x - 0.0375 + 0.000492*F
    elif (F > 17 and F <= 40):
      Cpf = x - 0.1109 + 0.000815*F -0.000000353*F**2
    else:
      return None
    
    # imperial mesh alignment factor
    A = 0.274 # from AGMA 2101-D04 Table 2
    B = 0.0167
    C = -0.765e-4
    Cma = A + B*F + C*F**2

  Km = 1 + Cmc*(Cpf*Cpm+Cma*Ce)
  
  return Km

def hardness_ratio_factor(Np, Ng, Hbp, Hbg, index):
  '''
  Hbp: Brinell Hardness of the pinion
  Hbg: Brinell Hardness of the gear
  arg: specify if the analyzed gear is pinion or gear
  '''
  
  if (index == 1 or index == 3):
    return 1
  
  r = Hbp/Hbg
  if (r >= 1.2 and r <= 1.7):
    A = 8.98e-3*r-8.29e-3
  elif (r <1.2):
    return 1
  else:
    return None
  
  mg = Ng/Np

  Ch = 1.0 + A*(mg - 1)

  return Ch

def stress_cycle_factors(Np, Ng, index = 4):
  '''
  Np: Number of teeth of the pinion
  Ng: number of teeth of the gear
  index: position of the gear in the gear train. 1 = nearest to motor
  '''
  # tire diameter
  dtire = 0.499 # m

  # Vehicle Life
  L = 300000
  
  # Driving Cycles specs
  drv_cycle = np.array([[20, 600], [40, 400], [60, 500], [110, 300]])
  
  # Distance per driving cycle
  dist_per_cycle = 1/3600*drv_cycle[:, 0] @ drv_cycle[:, 1]
  
  # Number of driving cycles
  N_cycles = L/dist_per_cycle

  # minimum number of cycles
  M_min = N_cycles*1000/(np.pi*dtire)*dist_per_cycle

  # Scale minimum number of cycles based on gear in the geartrain
  if (index == 1):
    N = (Ng/Np)**2*M_min
  elif (index == 2 or index == 3):
    N = (Ng/Np)**2*M_min
  else:
    N = M_min

  # Factors (e8 cycles or greater)
  YN = 1.3558*N**(-0.0178)
  ZN = 1.4488*N**(-0.023)

  return YN, ZN

def reliability_factor(num_components):
  '''
  num_components: number of components in the assembly
  '''
  R_total = 2999/3000 # = 0.9996666...
  Ri = R_total**(1/num_components)

  if (Ri >= 0.99 and Ri <= 0.9999):
    Kr = 0.50-0.109*np.ln(1-Ri)
  elif (Ri > 0.9999):
    Kr = 1.5
  else:
    return None # other cases not tackled here
  
  return Kr

def temperature_factor():
  return 1

def rim_thickness_factor(d, m, bore):
  '''
  d: pitch diameter (in or mm)
  m: module (in or mm)
  bore: diameter of bore (in or mm)
  '''
  tr = d/2 - 1.25*m - bore/2 
  ht = 2.25*m

  mb = tr/ht

  if (mb >= 1.2):
    Kb = 1
  else:
    Kb = 1.6*np.log(2.242/mb)

  return Kb

def safety_factor(sigma, sigma_all):
  '''
  sigma: observed stress (MPa or Psi)
  sigma_all: allowable stress (MPa or Psi)
  '''
  return sigma_all/sigma

def tangential_force(Np, Ng, Tmotor, d, index):
  '''
  Np: Number of teeth of the pinion
  Ng: Number of teeth of the gear
  T: Motor power output
  d: gear pitch diameter (mm)
  index: position of the gear in the geartrain
  '''
  # After 1st gearset selection, define values
  d1 = 150/1000
  d2 = 350/1000


  # convert diameter to m
  d = d/1000

  if (index == 1):
    # d = d1
    Wt = 2*Tmotor/(d)
  
  elif (index == 2):
    # d = d2, Wt same as for Gear 1
    # dg/dp = Ng/Np
    Wt = 2*Tmotor/(d*(Np/Ng))
  
  elif (index == 3):
    # At first, assume d = d1 = d3
    # After 1st gearset selection, use values
    Wt1 = 2*Tmotor/(d1) 
    # After 1st gearset selection, use Ng, Np values
    T = Wt1*(d2)/2
    Wt = 2*T/(d)

  elif (index == 4):
    # d = d2 = d4
    # After 1st gearset selection, use d1
    Wt1 = 2*Tmotor/(d1)
    # Torque on Gear 3
    T = Wt1*(d2)/2
    # Wt same as for Gear 3
    Wt = 2*T/(d*Np/Ng)
  
  return Wt