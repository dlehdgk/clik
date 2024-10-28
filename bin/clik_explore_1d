#! /users/smp24dhl/.conda/envs/cosmos/bin/python3
import sys
sys.path = ["/users/smp24dhl/cosmo/code/planck/clik/lib/python3.9/site-packages"]+sys.path

import numpy as nm
import clik

def main(argv):
  pars = clik.miniparse(argv[1])
  cl = nm.loadtxt(pars.initdata)

  lkl = clik.clik(pars.input_object)

  offset = nm.sum(nm.array(lkl.lmax)+1)
  offset += lkl.extra_parameter_names.index(pars.parameter)

  ps = nm.linspace(pars.float.beg,pars.float.end,pars.float.step)
  res = ps*0.
  for i,v in enumerate(ps):
    cl[offset] = v
    res[i] = lkl(cl)
  res = nm.array([ps,res]).T

  res.tofile(pars.res, sep = "\n")

import sys
if __name__=="__main__":
  main(sys.argv)