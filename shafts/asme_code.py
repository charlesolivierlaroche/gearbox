# ASME Code

def ASMECode(Sy, Sut, n, M, T, Cm=3, Ct=3):
  '''
  Return ASME diameter estimate for a shaft 

  Sy: material yield strength (MPa)
  Sut: material ultimate strength (MPa)
  n: Safety Factor
  Cm, Ct: Load Factors = 3: default max possible value
  '''

  b = 0.75
  if (0.18*Sut > 0.30*Sy):
    Sp = b*0.30*Sy
  else:
    Sp = b*0.18*Sut

  # Convert from MPa to Pa (N/m^2)
  Sp = Sp*1e6

  # Safety Factor of 2 applied
  d = (5.1*n/Sp*((Cm*M)**2 + (Ct*T)**2)**(1/2))**(1/3)
  
  # return d in mm
  return d*1000
