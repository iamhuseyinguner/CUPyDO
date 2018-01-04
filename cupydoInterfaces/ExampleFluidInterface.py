#!/usr/bin/env python
# -*- coding: latin-1; -*-

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# Import whatever you want here, e.g.:
# import fluidWrapper
# import math

# Those are mandatory
import numpy as np
from cupydo.genericSolvers import FluidSolver

# ----------------------------------------------------------------------
#  ExampSolver class
# ----------------------------------------------------------------------
               
class ExampSolver(FluidSolver):
    def __init__(self, config): # You are free to add any arguments here
        """
        Des.
        """
        
        print '\n***************************** Initializing Example *****************************'
        

        #self.nNodes =                              # number of nodes (physical + ghost) at the f/s boundary
        #self.nHaloNode =                           # number of ghost nodes at the f/s boundary
        #self.nPhysicalNodes =                      # number of physical nodes at the f/s boundary
        
        FluidSolver.__init__(self)
        self.coreSolver = fluidWrapper.solverDriver(config)
        
        self.initRealTimeData()

    def run(self, t1, t2):
        """
        Des.
        """

        #Run the solver for one iteration, e.g. :
        #self.coreSolver.run()

        self.__setCurrentState()       # use to fill the arrays with nodal values after each run

    def __setCurrentState(self):
        """
        Des.
        """

        #This is an example, you are free to do it your own way
        #for iVertex in range(self.nPhysicalNodes):
            #self.nodalLoad_X[iVertex] = self.coreSolver.getLoadX(iVertex)
            #self.nodalLoad_Y[iVertex] = self.coreSolver.getLoadY(iVertex)
            #self.nodalLoad_Z[iVertex] = self.coreSolver.getLoadZ(iVertex)

    def getNodalInitialPositions(self):
        """
        Des.
        """

        #nodalInitialPos_X = np.zeros(self.nPhysicalNodes)
        #nodalInitialPos_Y = np.zeros(self.nPhysicalNodes)
        #nodalInitialPos_Z = np.zeros(self.nPhysicalNodes)

        #for ii in range(self.nPhysicalNodes):
            #nodalInitialPos_X[ii] =   
            #nodalInitialPos_Y[ii] = 
            #nodalInitialPos_Z[ii] = 

        #return (nodalInitialPos_X, nodalInitialPos_Y, nodalInitialPos_Z)

    def getNodalIndex(self, iVertex):
        """
        Des.
        """

        #no = 

        #return no

    def applyNodalDisplacements(self, disp_X, disp_Y, disp_Z):
        """
        Des.
        """

        #This is just an example again
        #for iVertex in range(self.nPhysicalNodes):
            #self.coreSolver.applyNodalDispX(disp_X[iVertex], iVertex)
            #self.coreSolver.applyNodalDispY(disp_Y[iVertex], iVertex)
            #self.coreSolver.applyNodalDispZ(disp_Z[iVertex], iVertex)

    def update(self):
        """
        Des.
        """

        FluidSolver.update(self)

        #overload here

    def bgsUpdate(self):
        """
        Des.
        """

        #overload here

        return

    def save(self):
        """
        Des.
        """

        #overload here

        return

    def initRealTimeData(self):
        """
        Des.
        """
        
        solFile = open('ExampleSolution.ascii', "w")
        solFile.write("Time\tnIter\tValue\n")
        solFile.close()

    def saveRealTimeData(self, time, nFSIIter):
        """
        Des.
        """
        
        solFile = open('ExampleSolution.ascii', "a")
        solFile.write(str(time) + '\t' + str(nFSIIter) + str(1.0) + '\n')
        solFile.close()

    def printRealTimeData(self, time, nFSIIter):
        """
        Des.
        """
        
        toPrint = 'RES-FSI-' + 'ExampleSolution' + ': ' + str(1.0) + '\n'
        print toPrint
    
    def exit(self):
        """
        Des.
        """

        print("***************************** Exit Example solver *****************************")
