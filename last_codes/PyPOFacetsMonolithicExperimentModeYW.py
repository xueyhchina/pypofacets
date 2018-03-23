
import sys
import math
import numpy as np

from datetime import datetime

# @begin PyPOFacetsMonolithicExperimentModeYW
# @in  input_model  @as InputModel
# @in  input_data_file  @as InputDataFile
# @in  fname @as CoordinatesFile  @URI file:{input_model}/coordinates.m
# @in  fname2 @as FacetsFile  @URI file:{input_model}/facets.m
# @out fileE0 @as FileE0
# @out T1 @as T1
# @out fileR @as FileR
input_model = sys.argv[1]
input_data_file = sys.argv[2]

# @begin ReadInputParameters
# @in  input_data_file @as InputDataFile
# @out freq @as Frequency
# @out corr @as CorrelationDistance
# @out delstd @as StandardDeviation
# @out ipol @as IncidentWavePolarization
# @out pstart @as StartPhiAngle
# @out pstop @as StopPhiAngle
# @out delp @as PhiIncrement
# @out tstart @as StartThetaAngle
# @out tstop @as StopThetaAngle
# @out delt @as ThetaIncrement
params = open(input_data_file, 'r')
param_list = []
for line in params:
    if not line.startswith("#"):
        param_list.append(int(line))
freq, corr, delstd, ipol, pstart, pstop, delp, tstart, tstop, delt = param_list
params.close()
# @end ReadInputParameters

# @begin CalculateWaveLength
# @in  freq @as Frequency
# @out waveL @as WaveLength
c = 3e8
waveL = c / freq
# @end CalculateWaveLength

corel = corr / waveL
delsq = delstd ** 2
bk = 2 * math.pi / waveL
cfact1 = math.exp(-4 * bk ** 2 * delsq)
cfact2 = 4 * math.pi * (bk * corel) ** delsq
rad = math.pi / 180
Lt = 0.05
Nt = 5

# @begin CalculateIncidentWavePolarization
# @in ipol @as InputPolarization
# @out Et
# @out Ep
if ipol == 0:
    Et = 1 + 0j
    Ep = 0 + 0j
elif ipol == 1:
    Et = 0 + 0j
    Ep = 1 + 0j
Co = 1
# @end CalculateIncidentWavePolarization

# @begin ReadModelCoordinates
# @in  input_model @as InputModel
# @in  fname @as CoordinatesFile  @URI file:{input_model}/coordinates.m
# @out xpts @as XPoints
# @out ypts @as YPoints
# @out zpts @as ZPoints
fname = input_model + "/coordinates.m"
coordinates = np.loadtxt(fname)
xpts = coordinates[:, 0]
ypts = coordinates[:, 1]
zpts = coordinates[:, 2]
nverts = len(xpts)
# @end ReadModelCoordinates

# @begin ReadFacetsModel
# @in  input_model @as InputModel
# @in  fname2 @as FacetsFile  @URI file:{input_model}/facets.m
# @out facets @as Facets
fname2 = input_model + "/facets.m"
facets = np.loadtxt(fname2)
# @end ReadFacetsModel

# @begin GenerateTransposeMatrix
# @in  facets @as Facets
# @out node1 @as Node1
# @out node1 @as Node2
# @out node3 @as Node3
# @out ntria @as NTria
nfcv = facets[:, 0]
node1 = facets[:, 1]
node2 = facets[:, 2]
node3 = facets[:, 3]
iflag = 0
ilum = facets[:, 4]
Rs = facets[:, 5]
ntria = len(node3)

vind = [[node1[i], node2[i], node3[i]]
        for i in range(ntria)]
# @end GenerateTransposeMatrix

# @begin GenerateCoordinatesPoints
# @in  xpts @as XPoints
# @in  ypts @as YPoints
# @in  zpts @as ZPoints
# @out r @as Points
x = xpts
y = ypts
z = zpts
r = [[x[i], y[i], z[i]]
     for i in range(nverts)]
# @end GenerateCoordinatesPoints

# @begin CalculateRefsGeometryModel
# @in  pstart @as StartPhiAngle
# @in  pstop @as StopPhiAngle
# @in  delp @as PhiIncrement
# @in  tstart @as StartThetaAngle
# @in  tstop @as StopTethaAngle
# @in  delt @as ThetaIncrement
# @in  rad @as Radians
# @out it @as ITHorizontalRotations
# @out ip @as IPVerticalRotations
# @out delp @as PhiIncrement
# @out delt @as ThetaIncrement
if delp == 0:
    delp = 1
if pstart == pstop:
    phr0 = pstart*rad
if delt == 0:
    delt = 1
if tstart == tstop:
    thr0 = tstart*rad
it = math.floor((tstop-tstart)/delt)+1
ip = math.floor((pstop-pstart)/delp)+1
# @end CalculateRefsGeometryModel

# @begin CalculateEdgesAndNormalTriangles
# @in  node1 @as Node1
# @in  node1 @as Node2
# @in  node3 @as Node3
# @in  r @as Points
# @out areai @as AreaI
# @out beta @as Beta
# @out alpha @as Alpha
areai = []
beta = []
alpha = []
for i in range(ntria):
    A0 = ((r[int(vind[i][1])-1][0]) - (r[int(vind[i][0])-1][0]))
    A1 = ((r[int(vind[i][1])-1][1]) - (r[int(vind[i][0])-1][1]))
    A2 = ((r[int(vind[i][1])-1][2]) - (r[int(vind[i][0])-1][2]))
    A = [int(A0), int(A1), int(A2)]
    B0 = ((r[int(vind[i][2]) - 1][0]) - (r[int(vind[i][1]) - 1][0]))
    B1 = ((r[int(vind[i][2]) - 1][1]) - (r[int(vind[i][1]) - 1][1]))
    B2 = ((r[int(vind[i][2]) - 1][2]) - (r[int(vind[i][1]) - 1][2]))
    B = [int(B0), int(B1), int(B2)]
    C0 = ((r[int(vind[i][0]) - 1][0]) - (r[int(vind[i][2]) - 1][0]))
    C1 = ((r[int(vind[i][0]) - 1][1]) - (r[int(vind[i][2]) - 1][1]))
    C2 = ((r[int(vind[i][0]) - 1][2]) - (r[int(vind[i][2]) - 1][2]))
    C = [int(C0), int(C1), int(C2)]
    N = -(np.cross(B,A))
    d = [np.linalg.norm(A), np.linalg.norm(B), np.linalg.norm(C)]
    ss = 0.5*sum(d)
    areai.append(math.sqrt(ss*(ss-np.linalg.norm(A))*(ss-np.linalg.norm(B))*(ss-np.linalg.norm(C))))
    Nn = np.linalg.norm(N)
    N = N/Nn
    beta.append(math.acos(N[2]))
    alpha.append(math.atan2(N[1],N[0]))
# @end CalculateEdgesAndNormalTriangles

# @begin AssembleGenerateOutputFile
# @in freq @as Frequency
# @in corr @as CorrelationDistance
# @in delstd @as StandardDeviation
# @in ipol @as IncidentWavePolarization
# @in pstart @as StartPhiAngle
# @in pstop @as StopPhiAngle
# @in delp @as PhiIncrement
# @in tstart @as StartThetaAngle
# @in tstop @as StopThetaAngle
# @in delt @as ThetaIncrement
# @out fileR @as FileR
# @out fileE0 @as FileE0
phi = []
theta = []
D0 = []
R = []
e0 = []
now = datetime.now().strftime("%Y%m%d%H%M%S")
filename_R = "R_PyPOFacetsMonolithicExperimentMode_"+sys.argv[1]+"_"+sys.argv[2]+"_"+now+".dat"
filename_E0 = "E0_PyPOFacetsMonolithicExperimentMode_"+sys.argv[1]+"_"+sys.argv[2]+"_"+now+".dat"
fileR = open(filename_R, 'w')
fileE0 = open(filename_E0, 'w')
r_data = [
    now, sys.argv[0], sys.argv[1], sys.argv[2],
    freq, corr, delstd, ipol, pstart, pstop,
    delp, tstart, tstop, delt
]
text = '\n'.join(map(str, r_data)) + '\n'
fileR.write(text)
fileE0.write(text)
# @end AssembleGenerateOutputFile
for i1 in range(0, int(ip)):
    for i2 in range(0, int(it)):
        # @begin CalculateGlobalAnglesAndDirections
        # @in  ip @as IPVerticalRotations
        # @in  it @as ITHorizontalRotations
        # @in  pstart @as StartPhiAngle
        # @in  delp @as PhiIncrement
        # @in  rad @as Radians
        # @in  tstart @as StartThetaAngle
        # @in  delt @as ThetaIncrement
        # @in  phi @as Phi
        # @in  theta @as Theta
        # @out u @as U
        # @out v @as V
        # @out w @as W
        # @out uu @as UU
        # @out vv @as VV
        # @out ww @as WW
        # @out sp @as SP
        # @out cp @as CP
        # @out D0 @as D0
        phi.append(pstart+i1*delp)
        phr = phi[i2]*rad
        theta.append(tstart+i2*delt)
        thr = theta[i2]*rad
        st = math.sin(thr)
        ct = math.cos(thr)
        cp = math.cos(phr)
        sp = math.sin(phr)
        u = st*cp
        v = st*sp
        w = ct
        D0.append([u, v, w])
        U = u
        V = v
        W = w
        uu = ct*cp
        vv = ct*sp
        ww = -st
        # @end CalculateGlobalAnglesAndDirections

        # @begin CalculateSphericalCoordinateSystemRadialUnitVector
        # @in  u @as U
        # @in  v @as V
        # @in  w @as W
        # @in fileR @as FileR
        # @out fileR @as FileR
        fileR.write(str(i2))
        fileR.write(" ")
        fileR.write(str([u, v, w]))
        fileR.write("\n")
        R.append([u, v, w])
        # @end CalculateSphericalCoordinateSystemRadialUnitVector

        # @begin CalculateIncidentFieldInGlobalCartesianCoordinates
        # @in  uu @as UU
        # @in  vv @as VV
        # @in  ww @as WW
        # @in  Et @as Et
        # @in  Ep @as Ep
        # @in  sp @as SP
        # @in  cp @as CP
        # @in fileE0 @as FileE0
        # @out fileE0 @as FileE0
        fileE0.write(str(i2))
        fileE0.write(" ")
        fileE0.write(str([(uu*Et-sp*Ep), (vv*Et+cp*Ep), (ww*Et)]))
        fileE0.write("\n")
        e0.append([(uu*Et-sp*Ep), (vv*Et+cp*Ep), (ww*Et)])
        # @end CalculateIncidentFieldInGlobalCartesianCoordinates
fileR.close()
fileE0.close()

# @end PyPOFacetsMonolithicExperimentModeYW