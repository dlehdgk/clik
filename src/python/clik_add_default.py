#! $PYTHONEXE
import sys
sys.path = ["$REPLACEPATH"]+sys.path

import numpy as nm
import numpy.random as ra
import numpy.linalg as la
import clik.parobject as php
import clik
import re
import os.path as osp
import os
import shutil
import clik.hpy as h5py
import clik.egfs



def main(argv):
  pars = clik.miniparse(argv[1])
  name = pars.str_array.name
  clikl = clik.clik(pars.input_object)
  extn = clikl.extra_parameter_names
  print extn
  for n in name:
    if n not in extn:
      raise Exception("extra parameter %s does not exist in likelihood file %s"%(n,pars.input_object))

  shutil.copyfile(pars.input_object,pars.res_object)
  outhf = h5py.File(pars.res_object,"r+")
  loc = pars.float_array.loc
  
  assert len(name)==len(loc)
  if "clik/default" in outhf:
    prid = outhf["clik/default"]
  else:
    prid = outhf.create_group("clik/default")
  
  prid.attrs["name"] = php.pack256(*name)
  prid.create_dataset("loc", data=loc.flat[:])
    
  
  if "check_param" in outhf["clik"]:
    cls = outhf["clik/check_param"]
    del(outhf["clik/check_param"])
    del(outhf["clik/check_value"])
    outhf.close()
    #php.add_selfcheck(pars.res_object,cls)
  else:
    outhf.close()

    
import sys
if __name__=="__main__":
  main(sys.argv)