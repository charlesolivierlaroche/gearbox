from numpy import pi
from numpy import tan

class Spline:

  def __init__(self, m, N, D, do, di, ds, F, phi):
    '''
    create spline object

    m: module
    N: number of teeth mm
    D: pitch diameter mm
    do: major diameter mm
    di: minor diameter mm
    ds: sleeve outer diameter mm
    F: Face width mm
    phi: pressure angle Deg
    
    Dre: minor external diameter
    L: length of engagement
    t: actual tooth thickness
    h: depth of engagement
    tw: wall thickness of internal spline
    Dri: major internal diameter
    '''

    # Convert to meters
    self.m = m/1000
    self.N = N
    self.D = D/1000
    self.do = do/1000
    self.di = di/1000
    self.ds = ds/1000
    self.F = F/1000
    self.phi = phi*pi/180

    # pitch
    self.P = 1/self.m
  
    # minor external diameter
    self.Dre = (N-1.35)/self.P
    # Length of engagement
    self.L = self.F
    # Actual tooth thickness
    self.t = (self.do - self.di)/2
    # depth of engagement
    self.h = 0.9/self.P
    # Wall thickness of internal spline
    self.tw = (self.ds - self.do)/2
    # Major internal diameter
    self.Dri = (self.N+1.35)/self.P

  def rootShearStress(self, T, Ka, Kf):
    '''
    Return shear stress under the roots of external teeth

    T: applied torque N*m
    Ka: Spline application factor (default 1)
    Kf: Fatigue-Life Factor (default 1)
    '''
    Ss = 16*T*Ka/(pi*self.Dre**3*Kf)
    return Ss
  
  def pDShearStress(self, T, Ka, Km, Kf):
    '''
    Return shear stress at pitch diameter

    T: applied torque N*m
    Ka: Spline application factor (default 1)
    Km: Spline Load-distribution factor (default 1)
    Kf: Fatigue-Life Factor (default 1)
    '''
    Ss = 4*T*Ka*Km/(self.D*self.N*self.L*self.t*Kf)
    return Ss

  def compressiveStress(self, T, Ka, Km, Kw):
    '''
    Return compressive stress

    T: applied torque N*m
    Ka: Spline application factor (default 1)
    Km: Spline Load-distribution factor (default 1)
    Kw: Wear Life factor (default 1)
    '''
    Sc = 2*T*Km*Ka/(9*self.D*self.N*self.L*self.h*Kw)
    return Sc

  def burstingStresses(self, T, n, Y, Ka, Km, Kf):
    '''
    Return Bursting stresses

    T: applied torque N*m
    n: rotation speed rpm
    Y: Lewis Form Factor (default 1.5)
    Ka: Spline application factor (default 1)
    Km: Spline Load-distribution factor (default 1)
    Kf: Fatigue-Life Factor (default 1)
    '''

    # Radial load tensile stress
    S1 = T*tan(self.phi)/(pi*self.D*self.tw*self.L)

    # Centrifugal tensile stress
    S2 = 1.656*n**2*(self.ds**2+0.212*self.Dri**2)

    # beam loading tensile stress
    S3 = 4*T/(self.D**2*self.L*Y)

    St = (Ka*Km*(S1+S3)+S2)/Kf
    return St
  
  def safetyFactor(self, T, n, Ka, Km, Kw, Kf, Y, shear, compression, tension):
    '''
    Return safety factors in shear, compression and tension

    T: applied torque N*m
    n: rotation speed rpm 
    Ka: Spline application factor
    Km: Spline Load-distribution factor
    Kw: Wear Life factor
    Kf: Fatigue-Life Factor
    Y: Lewis Form Factor
    shear: allowable shear stress MPa
    compression: allowable compressive stress MPa
    tension: allowable tensile stress MPa
    '''
    Ss1 = self.rootShearStress(T, Ka, Kf)
    Ss2 = self.pDShearStress(T, Ka, Km, Kf)
    Sc = self.compressiveStress(T, Ka, Km, Kw)
    St = self.burstingStresses(T, n, Y, Ka, Km, Kf)

    ns = min((shear*1e6)/Ss1, (shear*1e6)/Ss2)
    nc = (compression*1e6)/Sc
    nt = (tension*1e6)/St

    return ns, nc, nt



