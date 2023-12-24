
class AGMA:
  def __init__(self, J, I, Cp, Kv, Ko, Cf, Ks, Km, Ch, Yn, Zn, Kr, Kt, Kb, Wt, Wr, sigma, sigma_all_bending, sigma_c, sigma_all_c, Sf, Sh, exceeded):
    '''
    Initialize AGMA object containing analysis results

    J: Geometry Factor
    I: Surface Strength Geometry Factor
    Cp: Elastic Coefficient
    Kv: Dynamic Factor
    Ko: Overload Factor
    Cf: Surface Factor
    Ks: Size Factor
    Km: Load Distribution Factor
    Ch: Hardness-Ratio Factor
    Yn: Bending Stress-Cycle Factor
    Zn: Contact Stress Cycle Factor
    Kr: Reliability Factor
    Kt: Temperature Factor
    Kb: Rim-Thickness Factor
    Wt: Tangential Force [N/lbf]
    Wr: Radial Force [N/lbf]
    Wa: Axial Force [N/lbf]
    sigma: Bending Stress [Pa/psi]
    sigma_all_bending: Allowable Bending Stress [Pa]
    sigma_c: Contact Stress [Pa/psi]
    sigma_all_c: Allowable contact stress [Pa/psi]
    Sf: Safety Factor in Bending
    Sh: Safety Factor in Shear
    exceeded: True if recommeded gear velocity is exceeded
    '''

    self.J = J
    self.I = I
    self.Cp = Cp
    self.Kv = Kv
    self.Ko = Ko
    self.Cf = Cf
    self.Ks = Ks
    self.Km = Km
    self.Ch = Ch
    self.Yn = Yn
    self.Zn = Zn
    self.Kr = Kr
    self.Kt = Kt
    self.Kb = Kb
    self.Wt = Wt
    self.Wr = Wr
    # self.Wa = Wa
    self.sigma = sigma
    self.sigma_all_bending = sigma_all_bending
    self.sigma_c = sigma_c
    self.sigma_all_c = sigma_all_c
    self.Sf = Sf
    self.Sh = Sh
    self.exceeded = exceeded
  
  def safety_factor(self):
    '''
    return the minimum safety factor
    '''
    if (self.Sf > self.Sh):
      return self.Sh
    else:
      return self.Sf
    
  def valid_safety(self, thresh):
    '''
    Return True if the safety factor is above a certain threshold
    '''
    s = self.safety_factor()
    if (s >= thresh):
      return True
    else:
      return False
  
  def valid_velocity(self):
    if (self.exceeded == True):
      return False
    else:
      return True
    
  def valid(self, thresh):
    if (self.valid_safety(thresh) == True and self.valid_velocity() == True):
      return True
    else:
      return False
    
  def print(self):
    print("AGMA Analysis Results \n\n")
    print("Geometry Factor J: ", self.J)
    print("Surface Strength Geometry Factor I: ", self.I)
    print("Elastic Coefficient Cp: ", self.Cp)
    print("Dynamic Factor Kv: ", self.Kv)
    print("Overload Factor Ko: ", self.Ko)
    print("Surface Factor Cf: ", self.Cf)
    print("Size Factor Ks: ", self.Ks)
    print("Load Distribution Factor Km: ", self.Km)
    print("Hardness-Ratio Factor Ch: ", self.Ch)
    print("Bending Stress-Cycle Factor Yn: ", self.Yn)
    print("Contact Stress-Cycle Factor Zn: ", self.Zn)
    print("Reliability Factor Kr: ", self.Kr)
    print("Temperature Factor Kt: ", self.Kt)
    print("Rim-Thickness Factor Kb: ", self.Kb)
    print("Tangential Force: ", self.Wt)
    print("Radial Force: ", self.Wr)
    print("Bending Stress: ", self.sigma)
    print("Allowable Bending Stress: ", self.sigma_all_bending)
    print("Contact Stress: ", self.sigma_c)
    print("Allowable Contact Stress: ", self.sigma_all_c)
    print("Safety Factor in Bending: ", self.Sf)
    print("Safety Factor in Contact: ", self.Sh)