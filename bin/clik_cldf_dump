#! /users/smp24dhl/.conda/envs/cosmos/bin/python3
import sys
sys.path = ["/users/smp24dhl/cosmo/code/planck/clik/lib/python3.9/site-packages"]+sys.path

import numpy as nm
import clik.cldf as cldf
import os.path as osp

def main(argv):

  base = osp.dirname(argv[1])
  f = cldf.File(base)
  print(f[osp.basename(argv[1])])

import sys
if __name__=="__main__":
  main(sys.argv)