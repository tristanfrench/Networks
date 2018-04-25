# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 13:45:20 2018
@author: JamesDL

file is a repository of obstacle presets 
to be called from a simulation program.
"""

#2x2 coords set top-left piece
def sqcol(xcoord,ycoord):
    squareColumn = [[ycoord,xcoord],[ycoord+1,xcoord],[ycoord,xcoord+1],[ycoord+1,xcoord+1]]
    return squareColumn

#3x3 coords set left piece
def crcol(xcoord,ycoord):
    crossColumn = [[ycoord,xcoord],[ycoord,xcoord+1],[ycoord-1,xcoord+1],[ycoord+1,xcoord+1],[ycoord,xcoord+2]]
    return crossColumn

#3x3 coords set top-left piece
def vcor(xcoord,ycoord):
    verticalCorridor = [[ycoord,xcoord],[ycoord+1,xcoord],[ycoord+2,xcoord],
                        [ycoord,xcoord+2],[ycoord+1,xcoord+2],[ycoord+2,xcoord+2]]
    return verticalCorridor

#3x3 coords set top-left piece
def hcor(xcoord,ycoord):
    horizontalCorridor = [[ycoord,xcoord],[ycoord,xcoord+1],[ycoord,xcoord+2],
                        [ycoord+2,xcoord],[ycoord+2,xcoord+1],[ycoord+2,xcoord+2]]
    return horizontalCorridor

#10x10 coords are top-left piece. Roads are parallel lines of obstacles with 2 empty spaces between them.
def hroad(xcoord,ycoord):
    horizontalRoad = [[ycoord,xcoord],[ycoord,xcoord+1],[ycoord,xcoord+2],[ycoord,xcoord+3],[ycoord,xcoord+4],[ycoord,xcoord+5],[ycoord,xcoord+6],[ycoord,xcoord+7],[ycoord,xcoord+8],[ycoord,xcoord+9],
                      [ycoord+3,xcoord],[ycoord+3,xcoord+1],[ycoord+3,xcoord+2],[ycoord+3,xcoord+3],[ycoord+3,xcoord+4],[ycoord+3,xcoord+5],[ycoord+3,xcoord+6],[ycoord+3,xcoord+7],[ycoord+3,xcoord+8],[ycoord+3,xcoord+9]]
    return horizontalRoad

#10x10 coords are top-left piece. Roads are parallel lines of obstacles with 2 empty spaces between them.
def vroad(xcoord,ycoord):
    verticalRoad = [[ycoord,xcoord],[ycoord+1,xcoord],[ycoord+2,xcoord],[ycoord+3,xcoord],[ycoord+4,xcoord],[ycoord+5,xcoord],[ycoord+6,xcoord],[ycoord+7,xcoord],[ycoord+8,xcoord],[ycoord+9,xcoord],
                      [ycoord,xcoord+3],[ycoord+1,xcoord+3],[ycoord+2,xcoord+3],[ycoord+3,xcoord+3],[ycoord+4,xcoord+3],[ycoord+5,xcoord+3],[ycoord+6,xcoord+3],[ycoord+7,xcoord+3],[ycoord+8,xcoord+3],[ycoord+9,xcoord+3]]
    return verticalRoad


    
    
    
    
    