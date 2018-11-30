from ovito.modifiers import *
from ovito.data import *
import math
T = 900
A = [3.5510,3.5583,3.5654,3.5723,3.5794,3.5865,3.5938,3.6014,3.6120,3.6178,3.6284]
A = A[int((T-300)/100)]/2

def modify(frame, input, output):
	K = 0
	X = [0,A,A,0,A,0,0,A]
	Y = [0,A,0,A,0,A,0,A]
	Z = [0,0,A,A,0,0,A,A]
	P1 = [0,1,2,3]
	P2 = [4,5,6,7]

	Position = input.particle_properties.position.array
	Defect_property = output.create_user_particle_property("Defect", "float").marray
	nparticles = input.number_of_particles
	for i in range(nparticles) :
		PositioX = Position[i,0]//A%2
		PositioY = Position[i,1]//A%2
		PositioZ = Position[i,2]//A%2
		Distance0 = []
		if PositioX == 1 :
			if PositioY == 1:
				if PositioZ == 1:
					for j in P2:
						Distance0.append(math.sqrt((Position[i,0]%A-X[j])**2 + (Position[i,1]%A-Y[j])**2 + (Position[i,2]%A-Z[j])**2))
					Distance = min(Distance0)
				elif PositioZ == 0:
					for j in P1:
						Distance0.append(math.sqrt((Position[i,0]%A-X[j])**2 + (Position[i,1]%A-Y[j])**2 + (Position[i,2]%A-Z[j])**2))
					Distance = min(Distance0)
			elif PositioY == 0:
				if PositioZ == 1:
					for j in P1:
						Distance0.append(math.sqrt((Position[i,0]%A-X[j])**2 + (Position[i,1]%A-Y[j])**2 + (Position[i,2]%A-Z[j])**2))
					Distance = min(Distance0)
				elif PositioZ == 0:
					for j in P2:
						Distance0.append(math.sqrt((Position[i,0]%A-X[j])**2 + (Position[i,1]%A-Y[j])**2 + (Position[i,2]%A-Z[j])**2))
					Distance = min(Distance0)
		elif PositioX == 0 :
			if PositioY == 1:
				if PositioZ == 1:
					for j in P1:
						Distance0.append(math.sqrt((Position[i,0]%A-X[j])**2 + (Position[i,1]%A-Y[j])**2 + (Position[i,2]%A-Z[j])**2))
					Distance = min(Distance0)
				elif PositioZ == 0:
					for j in P2:
						Distance0.append(math.sqrt((Position[i,0]%A-X[j])**2 + (Position[i,1]%A-Y[j])**2 + (Position[i,2]%A-Z[j])**2))
					Distance = min(Distance0)
			elif PositioY == 0:
				if PositioZ == 1:
					for j in P2:
						Distance0.append(math.sqrt((Position[i,0]%A-X[j])**2 + (Position[i,1]%A-Y[j])**2 + (Position[i,2]%A-Z[j])**2))
					Distance = min(Distance0)
				elif PositioZ == 0:
					for j in P1:
						Distance0.append(math.sqrt((Position[i,0]%A-X[j])**2 + (Position[i,1]%A-Y[j])**2 + (Position[i,2]%A-Z[j])**2))
					Distance = min(Distance0)
	
		if Distance > 0.27*A*2 :
			Defect_property[i] = 1
			K = K + 1
		else :
			Defect_property[i] = 0
	output.attributes["Number of Interstitials"] = K
	print("Number of Interstitials = ",K)