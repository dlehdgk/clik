#! /users/smp24dhl/.conda/envs/cosmos/bin/python3
import sys
sys.path = ["/users/smp24dhl/cosmo/code/planck/clik/lib/python3.9/site-packages"]+sys.path

import numpy as nm
import clik.parobject as php
import clik



def main(argv):
	if len(argv)==3:
		cls = nm.loadtxt(argv[2])
		res = php.add_selfcheck(argv[1],cls)
	else:
	  pars = clik.miniparse(argv[1])
	  cls = nm.loadtxt(pars.input_cl)
	  res = php.add_selfcheck(pars.input_object,cls)
	print("lkl for init cl %g"%res) 
    
import sys
if __name__=="__main__":
  main(sys.argv)