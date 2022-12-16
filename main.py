import sys, argparse, configparser

parser = argparse.ArgumentParser(description='Corretor.')
parser.add_argument('infile', help='Path to input image')
parser.add_argument('outfile', help='Path to output image')
parser.add_argument('-t', '--transparent', action='store_true', 
	help='')
parser.add_argument('-o', '--optimize', action='store_true', 
	help='')
parser.add_argument('-d', '--deduplicate', action='store_true', 
	help='')
args = parser.parse_args()
