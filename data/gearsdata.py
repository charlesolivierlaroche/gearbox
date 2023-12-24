import numpy as np
from models.gear import Gear

Ep = 190*10**3
Eg = 190*10**3

vp = 0.3
vg = 0.3

Hbp = 183
Hbg = 183

Qv = 12

# Create Objects, Module 4
p41 = Gear(module=4, number_of_teeth=45, pitch_diameter=180, bore=25, face_width=40, E=Ep, v=vp, H=Hbp, Qv=Qv)
p42 = Gear(module=4, number_of_teeth=48, pitch_diameter=192, bore=25, face_width=40, E=Ep, v=vp, H=Hbp, Qv=Qv)
p43 = Gear(module=4, number_of_teeth=50, pitch_diameter=200, bore=25, face_width=40, E=Ep, v=vp, H=Hbp, Qv=Qv)

g41 = Gear(module=4, number_of_teeth=110, pitch_diameter=440, bore=25, face_width=40, E=Eg, v=vg, H=Hbg, Qv=Qv)
g42 = Gear(module=4, number_of_teeth=114, pitch_diameter=456, bore=25, face_width=40, E=Eg, v=vg, H=Hbg, Qv=Qv)

# Create Objects, Module 5
p51 = Gear(module=5, number_of_teeth=30, pitch_diameter=150, bore=25, face_width=50, E=Ep, v=vp, H=Hbp, Qv=Qv)
p52 = Gear(module=5, number_of_teeth=32, pitch_diameter=160, bore=25, face_width=50, E=Ep, v=vp, H=Hbp, Qv=Qv)
p53 = Gear(module=5, number_of_teeth=35, pitch_diameter=175, bore=25, face_width=50, E=Ep, v=vp, H=Hbp, Qv=Qv)
p54 = Gear(module=5, number_of_teeth=36, pitch_diameter=180, bore=25, face_width=50, E=Ep, v=vp, H=Hbp, Qv=Qv)
p55 = Gear(module=5, number_of_teeth=38, pitch_diameter=190, bore=25, face_width=50, E=Ep, v=vp, H=Hbp, Qv=Qv)
p56 = Gear(module=5, number_of_teeth=40, pitch_diameter=200, bore=25, face_width=50, E=Ep, v=vp, H=Hbp, Qv=Qv)
p57 = Gear(module=5, number_of_teeth=42, pitch_diameter=210, bore=25, face_width=50, E=Ep, v=vp, H=Hbp, Qv=Qv)
p58 = Gear(module=5, number_of_teeth=45, pitch_diameter=225, bore=25, face_width=50, E=Ep, v=vp, H=Hbp, Qv=Qv)

# Create Gear Objects
g51 = Gear(module=5, number_of_teeth=70, pitch_diameter=350, bore=30, face_width=50, E=Eg, v=vg, H=Hbg, Qv=Qv)
g52 = Gear(module=5, number_of_teeth=75, pitch_diameter=375, bore=30, face_width=50, E=Eg, v=vg, H=Hbg, Qv=Qv)
g53 = Gear(module=5, number_of_teeth=76, pitch_diameter=380, bore=30, face_width=50, E=Eg, v=vg, H=Hbg, Qv=Qv)
g54 = Gear(module=5, number_of_teeth=80, pitch_diameter=400, bore=30, face_width=50, E=Eg, v=vg, H=Hbg, Qv=Qv)
g55 = Gear(module=5, number_of_teeth=85, pitch_diameter=425, bore=25, face_width=50, E=Eg, v=vg, H=Hbg, Qv=Qv)
g56 = Gear(module=5, number_of_teeth=90, pitch_diameter=450, bore=30, face_width=50, E=Eg, v=vg, H=Hbg, Qv=Qv)
g57 = Gear(module=5, number_of_teeth=95, pitch_diameter=475, bore=30, face_width=50, E=Eg, v=vg, H=Hbg, Qv=Qv)
g58 = Gear(module=5, number_of_teeth=100, pitch_diameter=500, bore=30, face_width=50, E=Eg, v=vg, H=Hbg, Qv=Qv)
g59 = Gear(module=5, number_of_teeth=110, pitch_diameter=550, bore=30, face_width=50, E=Eg, v=vg, H=Hbg, Qv=Qv)

# Create Gear Objects, Module 6
p61 = Gear(module=6, number_of_teeth=15, pitch_diameter=90, bore=20, face_width=60, E=Eg, v=vg, H=Hbg, Qv=Qv)
p62 = Gear(module=6, number_of_teeth=16, pitch_diameter=96, bore=20, face_width=60, E=Eg, v=vg, H=Hbg, Qv=Qv)
p63 = Gear(module=6, number_of_teeth=18, pitch_diameter=108, bore=20, face_width=60, E=Eg, v=vg, H=Hbg, Qv=Qv)

g61 = Gear(module=6, number_of_teeth=38, pitch_diameter=220, bore=25, face_width=60, E=Eg, v=vg, H=Hbg, Qv=Qv)
g62 = Gear(module=6, number_of_teeth=40, pitch_diameter=240, bore=25, face_width=60, E=Eg, v=vg, H=Hbg, Qv=Qv)

SpurPinion = np.array([
  p41, p42, p43, p51, p52, p53, p54, p55, p56, p57, p58, p61, p62, p63
])
SpurGear = np.array([
  g41, g42, g51, g52, g53, g54, g55, g56, g57, g58, g59, g61, g62
])
