from models.agma_results import AGMA
import numpy as np
import gears.agma_factors as af
from models.gear import Gear

def agma(R, pinion: Gear, gear: Gear, nmin, Tmotor, St, Sc, index, psi=0, phi_t=20, S1 = 1, S = 1, arg: str = 'metric'):
  '''
  Returns the AGMA analysis results

  R: Geometry Factor
  phi_t: Tangential Pressure Angle (mfr listed pressure angle, deg). default: 20-deg
  psi = 0: helix angle (deg). default: 0, spur gear
  m: module (mm or in)
  dp: pinion pitch diameter (mm or in)
  dg: gear pitch diameter (mm or in)
  Np: Number of teeth of the pinion
  Ng: Number of teeth of the gear
  vp: Pinion material poisson's ratio (unitless)
  vg: Gear material poisson's ratio (unitless)
  Ep: Pinion material Young's Modulus (Pa)
  Eg: Gear material Young's Modulus (Pa)
  Hbp: Pinion Brinell Hardness
  Hbg: Gear Brinell Hardness
  n: analyzed gear rotation speed (rpm)
  Qv = 10: AGMA quality number, JIS N5 Equivalent
  F: Face width (mm or in)
  bore: bore diameter (mm or in)
  T: Torque (N*m or lbf*in)
  St: allowable bending stress (MPa or lbf/in^2)
  Sc: allowable contact stress (MPa or lbf/in^2)
  index: position of gear in geartrain
  S1: Offset from shaft centerline (mm)
  S: Shaft length (mm)
  '''
  m = pinion.mod
  F = pinion.F
  Np = pinion.N
  dp = pinion.dp
  borep = pinion.bore
  Ng = gear.N
  dg = gear.dp
  boreg = gear.bore
  vp = pinion.v
  vg = gear.v
  Ep = pinion.E
  Eg = gear.E
  Hbp = pinion.H
  Hbg = gear.H
  Qvp = pinion.Qv
  Qvg = gear.Qv

  # Convert angles to rad
  phi_t = phi_t*np.pi/180
  psi = psi*np.pi/180

  if (index == 1 or index == 3):
    N = Np
    d = dp
    Qv = Qvp
  else:
    N = Ng
    d = dg
    Qv = Qvg
  
  # Geometry Factor
  J = af.geometry_factor(R)
  

  # Calculations for ss geometry factor
  pn = np.pi*m
  rp = dp/2
  rg = dg/2
  a = m

  # ss geometry factor
  I = af.ss_geometry_factor(phi_t, psi, pn, rp, rg, a, Ng, Np)
  

  # Elastic Coefficient
  Cp = af.elastic_coefficient(vp, vg, Ep, Eg)
  

  # Pitch-Line velocity
  V = af.pitch_line_velocity(Np, Ng, d, nmin, index, arg)

  # Max recommended velocity
  Vmax = af.max_recommended_velocity(Qv, arg)

  # Check if max velocity is exceeded
  exceeded = False
  if (V > Vmax):
    exceeded = True

  # Dynamic Factor
  Kv = af.dynamic_factor(V, Qv, arg)
  

  # Overload Factor
  Ko = af.overload_factor()
  

  # Surface Condition Factor
  Cf = af.surface_condition_factor()
  

  # Size factor
  Ks = af.size_factor(F, N, d)
  

  # Load Distribution Factor
  Km = af.load_distribution_factor(F, d, S1, S)
  

  # Hardness Ratio Factor
  Ch = af.hardness_ratio_factor(Np, Ng, Hbp, Hbg, index)
  

  # Stress-Cycle Factor
  factors = af.stress_cycle_factors(Np, Ng, index)
  
  Yn = factors[0]
  
  
  Zn = factors[1]
  

  # Reliability Factor
  Kr = af.reliability_factor(10)
  

  # Temperature Factor
  Kt = af.temperature_factor()
  

  # Rim Thickness Factor
  if (index == 1 or index == 3):
    bore = borep
  else:
    bore = boreg
  
  Kb = af.rim_thickness_factor(d, m, bore)
  

  # Tangential Force
  Wt = af.tangential_force(Np, Ng, Tmotor, d, index)

  # Radial Force
  Wr = Wt*np.tan(phi_t)
  

  # Stresses
  sigma = af.bending_stress(Wt, Ko, Kv, Ks, 1/m, F, Km, Kb, J)
  
  sigma_all_bending  = af.allowable_bending_stress(St, Yn, Kt, Kr)
  
  sigma_c = af.contact_stress(Cp, Wt, Ko, Kv, Ks, Km, dp, F, Cf, I)
  
  sigma_all_c = af.allowable_contact_stress(Sc, Zn, Ch, Kt, Kr)
  
  # Safety Factors
  Sf = af.safety_factor(sigma,sigma_all_bending)

  Sh = af.safety_factor(sigma_c,sigma_all_c)

  results = AGMA(J, I, Cp, Kv, Ko, Cf, Ks, Km, Ch, Yn, Zn, Kr, Kt, Kb, Wt, Wr, sigma, sigma_all_bending, sigma_c, sigma_all_c, Sf, Sh, exceeded)

  return results