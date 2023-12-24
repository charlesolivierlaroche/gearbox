class Gear:
  def __init__(self, module, number_of_teeth, pitch_diameter, bore, face_width, E, v, H, Qv, weight=0):
    '''
    module: gear module (mm or in)
    number_of_teeth: No. Teeth
    pitch_diameter = gear pitch diameter (mm or in)
    bore: Bore diameter (mm or in)
    face_width Face Width (mm or in)
    E: Elastic Modulus (MPa)
    v: Poisson's Ratio
    H: Brinell Hardness
    Qv: AGMA quality number
    Weight: gear weight (Kg)
    
    '''
    self.mod = module
    self.N = number_of_teeth
    self.dp = pitch_diameter
    self.bore = bore
    self.F = face_width
    self.E = E
    self.v = v
    self.H = H
    self.weight = weight
    self.Qv = Qv

  def print(self):
    print("Gear Specifications \n\n")
    print("Modulus: ", self.mod)
    print("Number of Teeth: ", self.N)
    print("Pitch Diameter: ", self.dp)
    print("Bore: ", self.bore)
    print("Face Width: ", self.F)
    print("Elastic Modulus: ", self.E)
    print("Poisson's Ratio: ", self.v)
    print("Brinell Hardness: ", self.H)
    print("Gear Weight: ", self.weight)


  