#!/usr/bin/env python

# Author: Sarah Denny, Stanford University 

# Provides modular tools for making a helix-junction
# helix DNA library

# This function calls dependent functions to make the subset of
# final library that is all three by three junctions and less


##### IMPORT #####
import numpy as np
import os
import sys

# load custom libraries
import create_library
import globalvars
parameters = globalvars.Parameters()
from hjh.helix import Helix
from hjh.junction import Junction
import create_library

##### MODULE #####
"""
SETUP
set working directory, create filename to save all subsequent
sequences to.
Initialize count.
"""
#wd = os.path.join(os.getcwd(), 'libraries') # working directory
wd = parameters.wd

# check if working directory exists and if not, creates it
if not os.path.exists(wd):
    os.mkdir(wd)
    
# initialize file
filename = os.path.join(wd, 'all3x3junctions.02_alonghelix.txt')
print 'saving to %s'%filename
f = open(filename, 'w')

# initalize log file
logfile = open(os.path.join(wd, '%s.log'%os.path.splitext(filename)[0]), 'w')

# initialize counts
count = 1

"""
JUNCTIONS IN ALL 20 POSITIONS
Save subset of junctions located in 'along' set. Also do different loop for all of these.
"""
# save one helix context, many junctions, in many different locations
print 'Doing 20 different positions of subset of junctions'
junctionMotifs = parameters.alongJunctions
receptorName = 'R1'
loopNames     = ['goodLoop', 'badLoop']
helixName    = parameters.standardHelixNames
cutOffNumber = 24
for junctionMotif in junctionMotifs:
    junction = Junction(junctionMotif)
    
    # if junction is 'W', do it in all different helix contexts. Everything else, do in two
    if junctionMotif == ('W',):
        helixNames = parameters.allHelixNames
    else:
        helixNames = parameters.standardHelixNames
    
    # take subset of junctions if greater than cutoff number
    if junction.howManyPossibilities() > cutOffNumber:
        subsetIndex = np.around(np.linspace(0, junction.howManyPossibilities()-1, cutOffNumber)).astype(int)
        junction.sequences = junction.sequences[subsetIndex]
        
    # save all different loops
    for loopName in loopNames:
    
        # save with all different helices
        for helixName in helixNames:
            helices = Helix(parameters.helixDict[helixName], junction.length).alongHelix()
            count = create_library.saveSet(junction, helices, helixName, receptorName, loopName, f, logfile, count)
   

# close
f.close()
logfile.close()
