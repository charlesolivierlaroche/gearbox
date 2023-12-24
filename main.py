# %% 
# Imports

import numpy as np

from models.spline import Spline
np.set_printoptions(suppress=True)

from matplotlib import pyplot as plt
plt.rc('lines', linewidth=2)
plt.rc('axes', grid=True)
plt.rc('grid', linestyle='--')

from gears.gear_analysis import run_analysis
from shafts.shaft_analysis import  shaft_analysis_metric
from shafts.asme_code import ASMECode
import shafts.diagrams as sd
import data.gearsdata as gd
from splines.spline_analysis import spline_analysis

# %%
# AGMA

dtire = 0.499

# AGMA 2101
Sc = 1895
St = 515 

Tmotor = 172
nmin = 110*1000/60*(1/(np.pi*dtire))

# last gear
index = 4

combinations = run_analysis(gd.SpurPinion, gd.SpurGear, St, Sc, nmin, Tmotor, index)

print("Combinations: \n")
print("Module \t Pinion  Gear")
for combination in combinations:
  print(combination[0].mod, "\t", combination[0].N, "\t", combination[1].N )

# %%
# Spline Analysis
m = 1
N = 24
D = 24
do = 25
di = 22.5
ds = 35
F = 15
phi = 30
n = 6367.143
T = 172

spline = Spline(m, N, D, do, di, ds, F, phi)

sf = spline_analysis(spline, n=n, T=T)

sf.print()


# %% 
# Force Equilibrium and Free Body Diagram

# distance between elements
dele = 10/1000 # m

# gear width
w_gear = 50/1000 # m

# Bearing Width 
w_bear = 21/1000 # m

# motor width
w_motor = (31.1 - 10 - 6.1)/1000

# %% 
# Input Shaft
dg1 = 150/1000
Wtg1 = 2293.3
Wrg1 = 837.7
dmotor = 24/1000

input_param = sd.input_diagrams(dele=dele, w_gear=w_gear, w_bear=w_bear, w_motor=w_motor, dg1=dg1, Wtg1=Wtg1, Wrg1=Wrg1)

print("Combined Reaction Force on Bearing 1: ", input_param[0], "N")
print("Combined Reaction Force on Bearing 2: ", input_param[1], "N")
print("Maximum Moment in Input Shaft: ", input_param[2], "N*m")
print("Maximum Torque in Input Shaft: ", input_param[3], "N*m")

# %% 
# Idler Shaft 

# Gears Properties
dg2 = 350/1000 # m
Wtg2 = 2293.33 # N
Wrg2 = 837.7 # N

dg3 = 175/1000 # m
Wtg3 = 4586.66 # N
Wrg3 =  1669.40 # N

idler_param = sd.idler_diagrams(dele=dele, w_gear=w_gear, w_bear=w_bear, dg2=dg2, Wtg2=Wtg2, Wrg2=Wrg2, dg3=dg3, Wtg3=Wtg3, Wrg3=Wrg3)

print("Combined Reaction Force on Bearing 1: ", idler_param[0], "N")
print("Combined Reaction Force on Bearing 2: ", idler_param[1], "N")
print("Maximum Moment in Idler Shaft: ", idler_param[2], "N*m")
print("Maximum Torque in Idler Shaft: ", idler_param[3], "N*m")

# %% 
# ASME Code

# Safety Factor
n = 2

# Shaft Material Strengths
# AISI 4140 https://www.matweb.com/search/DataSheet.aspx?MatGUID=8b43d8b59e4140b88ef666336ba7371a
Sut = 1020
Sy = 655

# Input Shaft
M_input = input_param[2]
T_input = input_param[3]

# Idler Shaft
M_idler = idler_param[2]
T_idler = idler_param[3]

# starting diameter for iteration 
d_input = round(ASMECode(Sy, Sut, n, M=M_input, T=T_input))
d_idler = round(ASMECode(Sy, Sut, n, M=M_idler, T=T_idler))

print("Input Shaft ASME Diameter (mm) :", d_input)
print("Idler Shaft ASME Diameter (mm): ", d_idler)

# %% 
# Fatigue Analysis, Input Shaft @ Bearing 1

# shaft surface finish
sf = "ground"

# Forces
Fa = 0 # alternating axial force
Fm = 0 # mean axial force

# Moments
Mm = 0 # mean moment
Ma = 0 # alternating moment

# Torques
Tm = input_param[3] # mean torque
Ta = 0 # alternating torque

# Notch Radius
r = 2.5
# Groove
# dia = 33

# Notch Sensitivity (depends on radius, read from tables, L4S3)
q = 0.83 # notch sensitivity
qs = 1 # shear notch sensitivity

# Stress Concentration Factors, Shoulder
Kt = 1.7
Kts = 1.3

# diameter defined
d_input = 35

# Iteration
d_iter = np.arange(d_input, d_input+1)
m = d_iter.shape[0] 
d_iter = d_iter.reshape(m,1)
s = np.zeros(m).reshape(m,1)
ds = np.hstack((d_iter, s))

for i in range(m):
  ds[i, 1] = shaft_analysis_metric(d_iter[i], Sy, Sut, q, qs, Kt, Kts, sf, Fa, Fm, Ma, Mm, Ta, Tm)[0]

print(ds)
# %%
# Fatigue Analysis, Input Shaft @ Gear 1, Shoulder

# shaft surface finish
sf = "ground"

# Forces
Fa = 0 # alternating axial force
Fm = 0 # mean axial force

# Moments
Mm = 0 # mean moment
Ma = input_param[2] # alternating moment

# Torques
Tm = input_param[3] # mean torque
Ta = 0 # alternating torque

# Notch Radius
r = 5
# Shoulder
# dia = 45

# Notch Sensitivity (depends on radius, read from tables, L4S3)
q = 1 # notch sensitivity
qs = 1 # shear notch sensitivity

# Stress Concentration Factors, Shoulder
Kt = 1.5
Kts = 1.3

# diameter defined
d_input = 35

# Iteration
d_iter = np.arange(d_input, d_input+1)
m = d_iter.shape[0] 
d_iter = d_iter.reshape(m,1)
s = np.zeros(m).reshape(m,1)
ds = np.hstack((d_iter, s))

for i in range(m):
  ds[i, 1] = shaft_analysis_metric(d_iter[i], Sy, Sut, q, qs, Kt, Kts, sf, Fa, Fm, Ma, Mm, Ta, Tm)[0]


# %%
# Fatigue Analysis, Input Shaft @ Gear 1, Groove

# shaft surface finish
sf = "ground"

# Forces
Fa = 0 # alternating axial force
Fm = 0 # mean axial force

# Moments
Mm = 0 # mean moment
Ma = input_param[2] # alternating moment

# Torques
Tm = input_param[3] # mean torque
Ta = 0 # alternating torque

# Notch Radius
r = 0.925
# groove
# dia = 37.5

# Notch Sensitivity (depends on radius, read from tables, L4S3)
q = 0.75 # notch sensitivity
qs = 0.9 # shear notch sensitivity

# Stress Concentration Factors, Shoulder
Kt = 2.7
Kts = 2

# diameter defined
d_input = 37.5

# Iteration
d_iter = np.arange(d_input, d_input+1)
m = d_iter.shape[0] 
d_iter = d_iter.reshape(m,1)
s = np.zeros(m).reshape(m,1)
ds = np.hstack((d_iter, s))

for i in range(m):
  ds[i, 1] = shaft_analysis_metric(d_iter[i], Sy, Sut, q, qs, Kt, Kts, sf, Fa, Fm, Ma, Mm, Ta, Tm)[0]

# %% 
# Spline Analysis, Input Shaft @ Gear 1
m = 1
N = 39
D = 39
do = 40
di = 37.5
ds = 0
F = 50
phi = 30
n = 6367.143
T = 172

spline = Spline(m, N, D, do, di, ds, F, phi)

sf = spline_analysis(spline, n=n, T=T)

sf.print()

# %%
# Fatigue Analysis, Idler Shaft @ Gear 3, Shoulder

# shaft surface finish
sf = "ground"

# Forces
Fa = 0 # alternating axial force
Fm = 0 # mean axial force

# Moments
Mm = 0 # mean moment
Ma = idler_param[2] # alternating moment

# Torques
Tm = idler_param[3] # mean torque
Ta = 0 # alternating torque

# Notch Radius
r = 2.5
# Shoulder
# dia = 45

# Notch Sensitivity (depends on radius, read from tables, L4S3)
q = 0.83 # notch sensitivity
qs = 1 # shear notch sensitivity

# Stress Concentration Factors, Shoulder
Kt = 1.75
Kts = 1.3

# diameter defined
d_idler = 40

# Iteration
d_iter = np.arange(d_idler, d_idler+1)
m = d_iter.shape[0] 
d_iter = d_iter.reshape(m,1)
s = np.zeros(m).reshape(m,1)
ds = np.hstack((d_iter, s))

for i in range(m):
  ds[i, 1] = shaft_analysis_metric(d_iter[i], Sy, Sut, q, qs, Kt, Kts, sf, Fa, Fm, Ma, Mm, Ta, Tm)[0]

# print(ds)

# %%
# Fatigue Analysis, Idler shaft @ Gear 3, groove
# shaft surface finish
sf = "ground"

# Forces
Fa = 0 # alternating axial force
Fm = 0 # mean axial force

# Moments
Mm = 0 # mean moment
Ma = idler_param[2] # alternating moment

# Torques
Tm = idler_param[3] # mean torque
Ta = 0 # alternating torque

# Notch Radius
r = 0.925
# Groove
# dia = 37.5

# Notch Sensitivity (depends on radius, read from tables, L4S3)
q = 0.75 # notch sensitivity
qs = 0.95 # shear notch sensitivity

# Stress Concentration Factors, Groove
Kt = 2.6
Kts = 2

# diameter defined
d_idler = 37.5

# Iteration
d_iter = np.arange(d_idler, d_idler+1)
m = d_iter.shape[0] 
d_iter = d_iter.reshape(m,1)
s = np.zeros(m).reshape(m,1)
ds = np.hstack((d_iter, s))

for i in range(m):
  ds[i, 1] = shaft_analysis_metric(d_iter[i], Sy, Sut, q, qs, Kt, Kts, sf, Fa, Fm, Ma, Mm, Ta, Tm)[0]

 # %% 
# Spline Analysis, Idler Shaft @ Gear 3
m = 1
N = 39
D = 39
do = 40
di = 37.5
ds = 87.5
F = 50
phi = 30
n = 2728.775
T = idler_param[3]

spline = Spline(m, N, D, do, di, ds, F, phi)

sf = spline_analysis(spline, n=n, T=T)

sf.print()
