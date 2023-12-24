import numpy as np
import gears.agma as ag
from gears.reduction import valid_reduction
from gears.interference import interference

def run_analysis(pinions: np.ndarray, gears: np.ndarray, St, Sc, n, Tmotor, index):
  
  combinations = np.empty((1, 2))

  if (index == 1 or index == 2):
    # Analyze first gearset
    i = 1

  elif (index == 3 or index == 4):
    # Analyze second gearset
    i = 3

  for pinion in pinions:
    
    # Define parameters
    Np = pinion.N

    # First Iteration, Np = 15
    # Rp = 0.25
    
    # 2nd interation min Geometry Factor, Np = 30
    # Rp = 0.385
    
    # Third iteration min Geometry Factor
    Rp = 0.41
    
    # For Helical Gears, min geometry factor
    # Rp = 0.56

    # Try to match each pinion with every possible gear
    for gear in gears:
      
      if (pinion.mod != gear.mod):
        continue
      
      # Define Parameters
      Ng = gear.N

      # Check for reduction & interference
      reduce = valid_reduction(Np, Ng)
      k = 1 # full depth teeth
      phi = 20 # typical pressure angle
      interf = interference(Ng, Np, phi, k)

      if (reduce == False or interf == False):
        continue
      
      # First Iteration, Ng = 30
      # Rg = 0.37

      # 2nd Interation Define Min Geometry Factor Ng = 70
      # Rg = 0.43

      # 3rd Iteration
      Rg = 0.45

      # Helical Gear, min geometry factor
      # Rg = 0.5238

      # 1) Check Pinion
      validp = ag.agma(Rp, pinion, gear, n, Tmotor, St, Sc, index=i)

      # 2) Check Gear
      validg = ag.agma(Rg, pinion, gear, n, Tmotor, St, Sc, index=i+1)

      if (validp.valid(thresh=2) == True and validg.valid(thresh=2) == True):
        combination = np.array([[pinion, gear]])
        combinations = np.vstack([combinations, combination])

  combinations = combinations[1:, :]
  return combinations