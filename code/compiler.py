import sys

def main():
	if(len(sys.argv) != 2):
		print 'Usage: python compilter.py filename.txt'
                sys.exit()

	fname = sys.argv[1]

	with open(fname) as f:
		content = [x.strip('\n') for x in f.readlines()]

	content = [x.strip('\t') for x in content]

	instructions = []
	pc_values = []
	pc = 0
	routines = {}

	for y in content:
		instructions.append(y.split())
	for z in instructions:
		pc_values.append(hex(pc))
		pc += 0x4
	for y, z in zip(pc_values, instructions):
		if len(z) == 1:
			routines[y] = z

	print content
	print instructions
	print pc_values
	print routines

"""
	routines = {}
	keys = []
	for z in instructions:
		if len(z) == 1:
			routines[z] = []
		keys = routines.keys()
		if z not in routines:
			routines[keys[-1]].append(z)
"""
	
if __name__ == '__main__':
	main()
