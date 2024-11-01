#! /users/smp24dhl/.conda/envs/cosmos/bin/python3
import sys
sys.path = ["/users/smp24dhl/cosmo/code/planck/clik/lib/python3.9/site-packages"]+sys.path

import clik
import clik.hpy as hpy
import clik.parobject as php


def main(argv):
  pars = clik.miniparse(argv[1])

  outhf,lkl_grp = php.copy_and_get_0(pars)
  php.add_free_calib(lkl_grp,pars.str.parname)

  php.remove_selfcheck(root_grp=outhf["clik"])

    
  outhf.close()

    
import sys
if __name__=="__main__":
  main(sys.argv)