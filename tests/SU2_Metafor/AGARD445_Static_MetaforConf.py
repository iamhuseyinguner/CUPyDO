# -*- coding: latin-1; -*-

from wrap import *
from  math import *

metafor = None

def params(q={}):
    """ default model parameters
    """
    p={}
    p['tolNR']      = 1.0e-8        # Newton-Raphson tolerance
    #p['tolNR']      = 1.0e-6        # Newton-Raphson tolerance
    p['tend']       = 0.05           # final time
    p['dtmax']      = 0.05          # max time step
    
    # BC type
    #p['bctype']     = 'pressure'     # uniform pressure
    #p['bctype']     = 'deadload'     # uniform nodal load
    #p['bctype']     = 'pydeadload1'  # uniform nodal load (python)  
    #p['bctype']     = 'pydeadloads'  # variable loads
    #p['bctype']     = 'slave'     # variable loads (mpi)

    p['bndno'] = 177
    p['extractNode'] = 180
    p['unsteady'] = False
                                       
    p.update(q)
    return p

def getMetafor(p={}): 
  global metafor
  if metafor : return metafor
  metafor = Metafor()

  p = params(p)

  domain = metafor.getDomain()
  geometry = domain.getGeometry()

  # --- Define the type of computation (3D, plane stress, plane strain, ...)
  geometry.setDim3D()

  # -- Import the geometry .geo and mesh it with GMSH ---
  from toolbox.gmsh import GmshImport
  f = os.path.join(os.path.dirname(__file__), "AGARD445_solidMesh_bis_coarse_opti.geo")
  importer = GmshImport(f, domain)
  importer.execute()

  groupset = domain.getGeometry().getGroupSet()

  # -- Define solid elements and material ---
  interactionset = domain.getInteractionSet()

  app1 = FieldApplicator(1)
  app1.push( groupset(179) )	#physical group 179 = volumic mesh of the wing
  interactionset.add( app1 )

  materset = domain.getMaterialSet()
  materset.define(1, OrthoElastHypoMaterial)
  mater1 = materset(1)
  mater1.put(MASS_DENSITY, 381.98)		#kg/m3
  mater1.put(YOUNG_MODULUS_1, 3.151e9)		#Pa
  mater1.put(YOUNG_MODULUS_2, 0.4162e9)		#Pa
  mater1.put(YOUNG_MODULUS_3, 0.4162e9)		#Pa
  mater1.put(POISSON_RATIO_12, 0.31)		#-
  mater1.put(POISSON_RATIO_13, 0.31)		#-
  mater1.put(POISSON_RATIO_23, 0.31)		#-
  mater1.put(SHEAR_MODULUS_12, 0.4392e9)	#Pa
  mater1.put(SHEAR_MODULUS_13, 0.4392e9)	#Pa
  mater1.put(SHEAR_MODULUS_23, 0.4392e9)	#Pa
  sweepOrtho = pi/4.0
  #sweepOrtho = 0.0
  mater1.put(ORTHO_AX1_X, sin(sweepOrtho))
  mater1.put(ORTHO_AX1_Y, cos(sweepOrtho))
  mater1.put(ORTHO_AX1_Z, 0.0)
  mater1.put(ORTHO_AX2_X, cos(sweepOrtho))
  mater1.put(ORTHO_AX2_Y, -sin(sweepOrtho))
  mater1.put(ORTHO_AX2_Z, 0.0)

  prp = ElementProperties(Volume3DElement)
  app1.addProperty(prp)
  prp.put(MATERIAL, 1)
  #prp.put(CAUCHYMECHVOLINTMETH,VES_CMVIM_STD)
  prp.put(CAUCHYMECHVOLINTMETH,VES_CMVIM_EAS)
  #prp.put(CAUCHYMECHVOLINTMETH,VES_CMVIM_SRI)
  prp.put(PEAS, 1e-11)

  # --- Boundary conditions ---
  loadingset = domain.getLoadingSet()
  #Clamped face of the wing = physical 176
  loadingset.define(groupset(176), Field1D(TX,RE))
  loadingset.define(groupset(176), Field1D(TY,RE))
  loadingset.define(groupset(176), Field1D(TZ,RE))

  mim = metafor.getMechanicalIterationManager()
  mim.setMaxNbOfIterations(20)
  mim.setResidualTolerance(p['tolNR'])

  #ti = AlphaGeneralizedTimeIntegration(metafor)
  #metafor.setTimeIntegration(ti)

  # --- Used solver ---
  #Blas.setBlasNumThreads(14)
  #solman = metafor.getSolverManager()
  #solman.setSolver(MUMPSolver())

  vmgr = metafor.getValuesManager()
  vmgr.add(1, DbNodalValueExtractor(groupset(183), Field1D(TZ,RE)), 'LE_dz')
  vmgr.add(2, DbNodalValueExtractor(groupset(184), Field1D(TZ,RE)), 'TE_dz')
  vmgr.add(3, DbNodalValueExtractor(groupset(183), Field1D(TY,AB)), 'LE_Y')
  vmgr.add(4, DbNodalValueExtractor(groupset(184), Field1D(TY,AB)), 'TE_Y')
  
  return metafor

def getRealTimeExtractorsList(Mtf):

    extractorsList = list()
    domain = Mtf.getDomain()
    groupset = domain.getGeometry().getGroupSet()  

    # --- Extractors list starts --- #
    extractor1 = DbNodalValueExtractor(groupset(180), Field1D(TZ,RE))
    extractorsList.append(extractor1)
    extractor2 = DbNodalValueExtractor(groupset(181), Field1D(TZ,RE))
    extractorsList.append(extractor2)
    # --- Extractors list ends --- #

    return extractorsList

