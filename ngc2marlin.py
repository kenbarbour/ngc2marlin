#!/usr/bin/python
# ngc2marlin
# Converts PyCAM's NGC gcode output to a Marlin flavor for Reprap 3d printers
# @Author Kenneth Barbour

import sys, getopt, os

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      showhelp()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         showhelp()
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   if inputfile == '':
      print 'Empty input file, exiting.'
      sys.exit()
   if outputfile == '':
      outputfile = os.path.splitext(inputfile)[0]+'.gcode'

   print 'Input file is ', inputfile
   print 'Output file is ', outputfile

   outfile = open(outputfile,'w+')

   outfile.write('; Marlin GCode converted from Pycam ngc with ngc2marlin.py')
   outfile.write("\n")

   with open(inputfile, 'r') as f:
      for line in f:
         outfile.write(getValidMarlinCode(line))

   outfile.close()

def getValidMarlinCode(gcode):
   line = gcode.rstrip("\n")
   if line[0] == ' ': # Pycam shorthand
      line = 'G1'+line
   if line[0] == ';': # GCode Comment
      return ''
   if line[0] == 'F': # Feedrate
      line = 'G1 '+line
   line = line + "\n"
   return line

def showhelp():
   print 'ngc2marlin.py -i <inputfile> [-o <outputfile>]'
   return 0

if __name__ == "__main__":
   main(sys.argv[1:])
