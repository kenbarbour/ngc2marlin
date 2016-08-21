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
      print 'Unspecified input file, exiting.'
      sys.exit()
   if outputfile == '':
      outputfile = getDefaultOutputFilename(inputfile)

   print 'Input file is ', inputfile
   print 'Output file is ', outputfile

   outfile = open(outputfile,'w+')

   outfile.write("; Marlin GCode converted from Pycam ngc with ngc2marlin.py\n")
   outfile.write("G21\n")
   outfile.write("G90\n")
   outfile.write("G92 X0 Y0 Z0\n")
   outfile.write("G1 F6000\n")

   with open(inputfile, 'r') as f:
      for line in f:
         outfile.write(getValidMarlinCode(line))

   outfile.close()

def getValidMarlinCode(gcode):
   line = gcode.rstrip("\n")
   if len(line) == 0:
      return ''
   if line[0] == ' ': # Unsupported move in early Marlin
      line = 'G1'+line
   if line[0] == ';': # GCode Comment
      return ''
   clauses = line.split(' ')
   if clauses[0] in ['G2','G02']:
      return getArcCode(line,1)
   elif clauses[0] in ['G3','G03']:
      return getArcCode(line,0)
   elif clauses[0] in ['G1','G01','G0','G00']:
      return line + "\n"
   else:
      return 'G1 '+line

def getDefaultOutputFilename(inputfile):
   outputfile = os.path.splitext(inputfile)[0]+'.gcode'
   if outputfile == inputfile:
      outputfile = os.path.splitext(inputfile)[0]+'_marlin.gcode'
   return outputfile

def getArcCode(code, cw):
   out = ''
   clauses = code.split(' ')
   if arcIsIJK(code):
      print('ijk arc: ' + code)
      for c in clauses:
         if c[0] == 'X':
            x = c[1:]
         elif c[0] == 'Y':
            y = c[1:]
         elif c[0] == 'Z':
            z = c[1:]
         elif c[0] == 'I':
            i = c[1:]
         elif c[0] == 'J':
            j = c[1:]
         elif c[0] == 'K':
            k = c[1:]
         elif c[0] == 'F':
            out += 'G1 F'+c[1:]+"\n"
      #out += 'G1
      out += 'G1 X'+x+' Y'+y+' Z'+z+"\n" # Finish
      return out
   else:
      print('r arc: ' + code)
      for c in clauses:
         if c[0] == 'X':
            x = c[1:]
         elif c[0] == 'Y':
            y = c[1:]
         elif c[0] == 'R':
            R = c[1:]
      return "\n"

def arcIsIJK(code):
   if 'R' in code:
      return False
   return True

def showhelp():
   print 'ngc2marlin.py -i <inputfile> [-o <outputfile>]'
   return 0

if __name__ == "__main__":
   main(sys.argv[1:])
