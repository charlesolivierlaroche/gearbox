
class SplineResults:
  def __init__(self, T, rpm,  Ka, Km, Kw, Kf, Y, Ss, Sc, St, shear, compression, tension, n):
    '''
    initialize result object

    T: Applied Torque N*m
    rpm: rotation speed rpm
    Ka: Spline application factor (default 1)
    Km: Spline Load-distribution factor (default 1)
    Kw: Wear Life factor (default 1)
    Kf: Fatigue-Life Factor (default 1)
    Y: Lewis-Form factor (default 1.5)
    Ss: shear stress Pa
    Sc: compressive stress Pa
    St: tensile stress Pa
    shear: allowable shear stress MPa
    compression: allowable compressive stress MPa
    tension: allowable tensile stress MPa
    T: applied torque N*m
    n: safety factors
    '''

    self.T = T
    self.rpm = rpm
    self.Ka = Ka
    self.Km = Km
    self.Kw = Kw
    self.Kf = Kf
    self.Y = Y
    self.Ss = Ss/1e6
    self.Sc = Sc/1e6
    self.St = St/1e6
    self.shear = shear
    self.compression = compression
    self.tension = tension
    self.ns = n[0]
    self.nc = n[1]
    self.nt = n[2]

  def print(self):
    print("Spline Analysis Results: \n")
    print("Applied Torque: ", self.T, "N*m")
    print("Rotation Speed: ", self.rpm, "rpm")
    print("Spline Application Factor: ", self.Ka)
    print("Spline Load-Distribution Factor: ", self.Km)
    print("Spline Wear Life Factor: ", self.Kw)
    print("Spline Fatigue-Life Factor: ", self.Kf)
    print("Lewis Form Factor: ", self.Y)
    print("Maximum Shear Stress: ", self.Ss, "MPa")
    print("Compressive Stress: ", self.Sc, "MPa")
    print("Tensile Stress: ", self.St, "MPa")
    print("Allowable Shear Stress: ", self.shear, "MPa")
    print("Allowable Compressive Stress: ", self.compression, "MPa")
    print("Allowable Tensile Stress: ", self.tension, "MPa")
    print("Safety Factor in Shear: ", self.ns)
    print("Safety Factor in Compression: ", self.nc)
    print("Safety Factor in Tension: ", self.nt)