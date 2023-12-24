import numpy as np

from models.spline import Spline
from models.spline_results import SplineResults

def spline_analysis(spline: Spline, T, n, Y=1.5, Ka=1, Km=1, Kw=1, Kf=1, shear=275.79, compression=27.57, tension=310):
  '''
  performs stress analysis on a spline, outputs parameters

  spline: spline object
  T: applied torque N*m
  n: rotation speed rpm
  Ka: Spline application factor (default 1)
  Km: Spline Load-distribution factor (default 1)
  Kw: Wear Life factor (default 1)
  Kf: Fatigue-Life Factor (default 1)
  Y: Lewis-Form factor (default 1.5)
  shear: allowable shear stress MPa
  compression: allowable compressive stress MPa
  tension: allowable tensile stress MPa
  '''

  Ss1 = spline.rootShearStress(T, Ka, Kf)
  Ss2 = spline.pDShearStress(T, Ka, Km, Kf)
  Sc = spline.compressiveStress(T, Ka, Km, Kw)
  St = spline.burstingStresses(T, n, Y, Ka, Km, Kf)

  sf = spline.safetyFactor(T, n, Ka, Km, Kw, Kf, Y, shear, compression, tension)

  results = SplineResults(T, n, Ka, Km, Kw, Kf, Y, max(Ss1, Ss2), Sc, St, shear, compression, tension, sf) 
  
  return results


  