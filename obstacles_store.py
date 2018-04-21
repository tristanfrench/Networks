# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 13:45:20 2018
@author: JamesDL

file is a repository of obstacle presets 
to be called from a simulation program.
"""



#coords set top-left piece
def sqcol(xcoord,ycoord):
    squareColumn = [[ycoord,xcoord],[ycoord+1,xcoord],[ycoord,xcoord+1],[ycoord+1,xcoord+1]]
    return squareColumn

#coords set left piece
def crcol(xcoord,ycoord):
    crossColumn = [[ycoord,xcoord],[ycoord,xcoord+1],[ycoord-1,xcoord+1],[ycoord+1,xcoord+1],[ycoord,xcoord+2]]
    return crossColumn

#coords set top-left piece
def vcor(xcoord,ycoord):
    verticalCorridor = [[ycoord,xcoord],[ycoord+1,xcoord],[ycoord+2,xcoord],
                        [ycoord,xcoord+2],[ycoord+1,xcoord+2],[ycoord+2,xcoord+2]]
    return verticalCorridor

#coords set top-left piece
def hcor(xcoord,ycoord):
    horizontalCorridor = [[ycoord,xcoord],[ycoord,xcoord+1],[ycoord,xcoord+2],
                        [ycoord+2,xcoord],[ycoord+2,xcoord+1],[ycoord+2,xcoord+2]]
    return horizontalCorridor
