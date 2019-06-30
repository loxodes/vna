#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Script for KiCad Pcbnew to clone a part of a layout. The scipt clones a row or a matrix
# of similar layouts.
#
# For now, there are no command line parameters given for the script, instead all the settings
# are written in this file. Before using this script, you must have your schema ready.
#
# 1. Use hierarchical sheets for the subschemas to be cloned and annotate them 
#    so that each sheet has module references starting with a different hundred.
# 2. Import a netlist into Pcbnew and place all the components except the ones to be cloned.
#    Also create an optimal layout for the subschema to be used as the template for the clones.
#    Surround the layout of the subchema with a zone in the comment layer.
# 3. Save the .kicad_pcb file. Modify SETTINGS at the top of this script to match your board.
#    Run this script.
#
# The script has three main parts:
# First, the script moves the modules, which are already imported into the board file. They are
# moved by a predetermined offset amount compared to the template module. (A module with the same
# reference, except starting with a different hundred, eg. templatemodule = D201, clones = D301, D401, D501 etc.)
# Second, the script clones the zones inside the comment layer zone. It seems the zone to be cloned must
# be completely inside the comment zone. Zones have a net defined for them. The script searches for any
# pads inside the cloned zone and sets their net for the zone. So you may get a wrong zone for the net if
# there are pads with different nets inside the zone.
# Third, the script clones the tracks inside the comment zone. Any track touching the zone will be cloned.
# Tracks do not have nets defined for them so they should connect nicely to the modules they will be touching
# after the cloning process.
#
# This script has been tested with KiCad versions 4 and 5.


from __future__ import print_function
import sys            
import re # regexp
from pcbnew import *


# :: SETTINGS ::
# Modify these to suit your project.

# Reference designators for the components you want cloned. Replace these.
templateReferences = ['C501', 'C502', 'C503', 'C504', 'C505', 'C506', 'C507',\
                      'L501', 'L502', 'L503',\
                      'R501', 'R502', 'R503', 'R504', 'R505', 'R506', 'R507', 'R508', 'R509', 'R510', 'R511', 'R512',\
                      'T501', 'T502']

# Path to the board with one hierarchical sheet laid out, ready to be cloned.
# Must be surrounded by a (square) zone in the comment layer.
inputBoardFile = u'./adc344x.kicad_pcb'
# Output file. Original file remains unmodified.
outputBoardFile = u'./adc344x_cloned.kicad_pcb'

templateRefModulo = -100;  # Difference in the reference numbers between hierarchical sheets
templateRefStart = 500;     # Starting point of numbering in the first hierarchical sheet
move_dx = FromMM(00.0)    # Spacing between clones in x direction
move_dy = FromMM(30.0)    # Spacing between clones in y direction
clonesX = 1               # Number of clones in x direction
clonesY = 3               # Number of clones in y direction

# :: END SETTINGS ::


numberOfClones = clonesX * clonesY
print('Loading board', inputBoardFile ,'...')
board = LoadBoard(inputBoardFile)

# Cloning the modules
print('Cloning component positions and orientations...')
for templateRef in templateReferences: # For each module in the template subschema
    templateModule = board.FindModuleByReference(templateRef) # Find the corresponding module in the input board
    if templateModule is None:
        print('Module', templateRef, 'was not found in the template board!')
        continue

    templateReferenceNumber = (re.findall(r"\d+", templateRef)).pop(0) # Extract reference number as string

    # Create list of reference designator strings. Corresponding modules will be repositioned and reoriented.
    cloneReferences = []
    for i in range(0, numberOfClones-1):
        cloneRefNumber = int(templateReferenceNumber) + (i+1)*templateRefModulo
        cloneReferences.append(re.sub(templateReferenceNumber, "", templateRef) + str(cloneRefNumber))
    print("Cloning '", templateRef, "' to ", cloneReferences, "...", sep='')

    for counter, cloneRef in enumerate(cloneReferences): # Move each of the clones to appropriate location
        templatePosition = templateModule.GetPosition()
        cloneModule = board.FindModuleByReference(cloneRef)
        if cloneModule is None:
            print('Module', cloneRef, 'was not found in the board!')
            continue

        # If the cloned module is not on the same layer as the template
        if cloneModule.GetLayer() is not templateModule.GetLayer():
            cloneModule.Flip(wxPoint(1,1)) # Flip it around any point to change the layer
        vect = wxPoint(templatePosition.x + (counter+1) % clonesX * move_dx,
                       templatePosition.y + (counter+1) // clonesX * move_dy) # Calculate new position
        cloneModule.SetPosition(vect)
        cloneModule.SetOrientation(templateModule.GetOrientation())
print('Components moved and oriented according to template.')

# Cloning zones inside the template area.
print('Cloning zones and connecting pads...')
# First use the comment zone to define the area to be cloned.
import pdb
pdb.set_trace()
for i in range(0, board.GetAreaCount()):
    zone = board.GetArea(i)                
    if zone.GetLayer() == 41: # Find the comment zone encasing the template board area
        templateRect = zone.GetBoundingBox()
        #board.RemoveArea(zone)   # Removing comment zone does not work
        print('Comment zone left top:', templateRect.GetOrigin(),
              'width:', templateRect.GetWidth(),
              'height:', templateRect.GetHeight())

modules = board.GetModules()
for i in range(0, board.GetAreaCount()): # For each zone in the board
    zone = board.GetArea(i)
    
    # If the zone is inside the area to be cloned (the comment zone) and it is not the comment zone (layer 41)
    if templateRect.Contains(zone.GetPosition()) and zone.GetLayer() is not 41:
        for i in range(1, numberOfClones): # For each target clone areas
            zoneClone = zone.Duplicate()
            zoneClone.Move(wxPoint(i % clonesX * move_dx, i // clonesX * move_dy))
            for module in modules: # Iterate through all the pads (also the cloned ones) in the board...
                for pad in module.Pads():
                    # Find the (last) pad inside the cloned zone. Maybe pad.GetZoneConnection() would be better.
                    if zoneClone.HitTestInsideZone(pad.GetPosition()) and pad.IsOnLayer(zoneClone.GetLayer()):
                        zoneClone.SetNetCode(pad.GetNet().GetNet()) # set the (maybe) correct net for the zone
            board.Add(zoneClone)
print('Zones cloned.')

print('Cloning tracks...')
# Clone tracks inside the template area
tracks = board.GetTracks()
cloneTracks = []
for track in tracks:
    if track.HitTest(templateRect):                             # Find tracks which touch the comment zone
        for i in range(1, numberOfClones):                      # For each area to be cloned
            cloneTrack = track.Duplicate()                      # Copy track
            cloneTrack.Move(wxPoint(i%clonesX*move_dx, i//clonesX*move_dy)) # Move it
            cloneTracks.append(cloneTrack)                        #Add to temporary list
for track in cloneTracks: # Append the temporary list to board
    tracks.Append(track)
print('Tracks cloned.')

# Save output file
print('Saving to', outputBoardFile, '...')
board.Save(outputBoardFile)
print('All done.')
