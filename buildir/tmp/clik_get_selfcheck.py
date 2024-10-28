#! /users/smp24dhl/.conda/envs/cosmos/bin/python3
import sys
sys.path = ["/users/smp24dhl/cosmo/code/planck/clik/lib/python3.9/site-packages"]+sys.path

import clik.parobject as php
import clik
import clik.hpy as hpy
import numpy as nm

def main_lensing(argv):
  lkl = clik.clik_lensing(argv[1])
  n = len(lkl.get_extra_parameter_names())
  cls = nm.concatenate((lkl.get_clpp_fid(),lkl.get_clcmb_fid(),nm.ones(n)))
  if len(argv)==2:
    clfile = argv[1]+".cls"
  else:
    clfile = argv[2]
  cls.tofile(clfile,sep=" ")
  

def main(argv):
  

  if clik.lkl_lensing.try_lensing(argv[1]):
    return main_lensing(argv)

  lkl = hpy.File(sys.argv[1],"r")
  cls = lkl["clik/check_param"][:]
  if len(argv)==2:
  	clfile = argv[1]+".cls"
  else:
  	clfile = argv[2]
  cls.tofile(clfile,sep=" ")
    
import sys
if __name__=="__main__":
  main(sys.argv)