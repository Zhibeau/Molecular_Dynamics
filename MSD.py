import numpy#引用python自带的numpy库


def modify(frame, input, output):
	#位移是储存在input.particle_properties.displacement_magnitude.array
	#这个数组中的，这个数组储存了每个原子的位移量
	displacement_magnitudes = input.particle_properties.displacement_magnitude.array

	#计算msd
	msd = numpy.sum(displacement_magnitudes ** 2) / len(displacement_magnitudes)

	#用output.attributesp[]函数输出计算结果到MSD
	output.attributes["MSD"] = msd 
	print('MSD = ',msd)

