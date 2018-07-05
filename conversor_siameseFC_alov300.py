import argparse
import os

def getArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument("frame", action='store', type=int)
	parser.add_argument('input', action='store', type=str)
	parser.add_argument('path_output', action='store', type=str)
	parser.add_argument('namefile', action='store', type=str)
	return parser.parse_args()

if __name__ == '__main__':
	args = getArgs()
	
	output = os.path.join(args.path_output,args.namefile + ".txt")
	
	with open (args.input) as i, open (output, "wt") as o:
		for line in i:
			line = line.replace("\n", "")
			coord = line.split()		
			o.write("%d " %args.frame + "%f " %float(coord[0]) + "%f " %float(coord[1]) + "%f " %(float(coord[0]) + float(coord[2])) + "%f\n" %(float(coord[1]) + float(coord[3])))
			args.frame+=1
