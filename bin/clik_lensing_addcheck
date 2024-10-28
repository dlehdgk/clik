#! /users/smp24dhl/.conda/envs/cosmos/bin/python3
import sys
sys.path = ["/users/smp24dhl/cosmo/code/planck/clik/lib/python3.9/site-packages"]+sys.path

import numpy as nm
import clik.parobject as php
import clik
import os.path as osp
import clik.hpy as hpy

lkl = clik.clik_lensing(sys.argv[1])
pp = lkl.get_clpp_fid()
cmb = lkl.get_clcmb_fid()
chk = lkl(nm.concatenate((pp,cmb,[1])))

del(lkl)

f = hpy.File(sys.argv[1],"r+")
f["clik_lensing/check"] = chk[0]
f.close()