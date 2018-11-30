from ovito.io import *
from ovito.data import *
from ovito.modifiers import *
import numpy
import math
Ngroup = 30
T = 900
A0 = [3.5510,3.5583,3.5654,3.5723,3.5794,3.5865,3.5938,3.6014,3.6120,3.6178,3.6284]
A = A0[int(T/100-3)]
for i in range(Ngroup) :
   j = i+1
   node0 = import_file("C:/Users/Gregory/Desktop/行观晓/毕设/模拟/批量模拟900K1ns1SIAMSD/group%d/relax.0.xyz"%j,columns =
   ["Particle Type", "Position.X", "Position.Y", "Position.Z"])
   cell = node0.source.cell
   cell.pbc = (True, True, True)
   mod = WignerSeitzAnalysisModifier()
   ref = 50500+i*500
   mod.reference.load("C:/Users/Gregory/Desktop/行观晓/毕设/模拟/批量模拟900K1ns1SIAMSD/弛豫/relax.%d.xyz"%ref,columns =
   ["Particle Type", "Position.X", "Position.Y", "Position.Z"])
   node0.modifiers.append(mod)
   node0.modifiers.append(SelectExpressionModifier(expression = 'Occupancy == 1'))
   node0.modifiers.append(DeleteSelectedParticlesModifier())
   node0.compute()
   export_file(node0, "C:/Users/Gregory/Desktop/行观晓/毕设/模拟/批量模拟900K1ns1SIAMSD/弛豫/dref%d.xyz"%j, "xyz", columns= 
   ["Particle Type", "Position.X", "Position.Y", "Position.Z"])
   
   node = import_file("C:/Users/Gregory/Desktop/行观晓/毕设/模拟/批量模拟900K1ns1SIAMSD/group%d/relax.*.xyz"%j,columns =
   ["Particle Type", "Position.X", "Position.Y", "Position.Z"])
   cell = node.source.cell
   cell.pbc = (True, True, True)
   mod.reference.load("C:/Users/Gregory/Desktop/行观晓/毕设/模拟/批量模拟900K1ns1SIAMSD/弛豫/relax.%d.xyz"%ref,columns =
   ["Particle Type", "Position.X", "Position.Y", "Position.Z"])
   node.modifiers.append(mod)
   node.compute()
   node.modifiers.append(SelectExpressionModifier(expression = 'Occupancy == 1'))
   node.compute()
   node.modifiers.append(DeleteSelectedParticlesModifier())
   modifier = CalculateDisplacementsModifier()
   modifier.reference.load("C:/Users/Gregory/Desktop/行观晓/毕设/模拟/批量模拟900K1ns1SIAMSD/弛豫/dref%d.xyz"%j,columns =
   ["Particle Type", "Position.X", "Position.Y", "Position.Z"])
   node.modifiers.append(modifier)
   node.compute()
   Position = input.particle_properties.position.array
   for i in range(input.number_of_particles):
      if abs(Position[i,0]) > 30 :
         DeltaX = Position[i,0]-Position[i+1,0]
         if abs(DeltaX) > 50 :
            Position.marray[i+1,0] = Position.marray[i+1,0] + 20*A*sign(DeltaX)
      if abs(Position[i,1]) > 30 :
         DeltaY = Position[i,1]-Position[i+1,1]
         if abs(DeltaY) > 50 :
            Position.marray[i+1,1] = Position.marray[i+1,1] + 20*A*sign(DeltaY)
      if abs(Position[i,2]) > 30 :
         DeltaZ = Position[i,2]-Position[i+1,2]
         if abs(DeltaY) > 50 :
            Position.marray[i+1,2] = Position.marray[i+1,2] + 20*A*sign(DeltaZ)
   def modify(frame, input, output):
                     
    # Access the per-particle displacement magnitudes computed by an existing 
    # Displacement Vectors modifier that precedes this custom modifier in the 
    # data pipeline:
      displacement_magnitudes = input.particle_properties.displacement_magnitude.array

    # Compute MSD:
      msd = numpy.sum(displacement_magnitudes ** 2) / len(displacement_magnitudes)

    # Output MSD value as a global attribute: 
      output.attributes["MSD"] = msd 
   node.modifiers.append(PythonScriptModifier(function = modify))
   node.compute()
   export_file(node, "C:/Users/Gregory/Desktop/行观晓/毕设/模拟/批量模拟900K1ns1SIAMSD/MSD/msd%d.txt"%j, "txt", columns= 
   ["Frame","MSD"], multiple_frames = True)


   

  