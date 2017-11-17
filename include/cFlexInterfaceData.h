/*!
 * Header for CFlexInterfaceData.
 * Authors : D. THOMAS.
 *
 * COPYRIGHT (C) University of Liège, 2017.
 */

#pragma once

#include <vector>

#ifdef HAVE_MPI
#include "petscvec.h"
#endif  //HAVE_MPI

#include "cMpi.h"

class CFlexInterfaceData{
#ifdef HAVE_MPI
  std::vector<Vec> dataContainer;
#else //HAVE_MPI
  std::vector< std::vector<double> > dataContainer;
#endif //HAVE_MPI
public:
  CFlexInterfaceData(int const& val_nPoint, int const& val_nDim);
  virtual ~CFlexInterfaceData();
  std::vector<int> getOwnershipRange() const;
  int nPoint, nDim;
};
