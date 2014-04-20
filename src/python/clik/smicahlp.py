import parobject as php
import numpy as nm
import re

def base_smica(root_grp,hascl,lmin,lmax,nT,nP,wq,rqhat,Acmb,rq0=None,bins=None):
  if bins==None:
    nbins = 0
  else:
    bins.shape=(-1,(lmax+1-lmin)*nm.sum(hascl))
    nbins = bins.shape[0]
    bins=bins.flat[:]
  lkl_grp = php.add_lkl_generic(root_grp,"smica",1,hascl,lmax,lmin,nbins = nbins,bins = bins)

  lkl_grp.attrs["m_channel_T"] = nT
  lkl_grp.attrs["m_channel_P"] = nP
  lkl_grp.create_dataset('wq', data=wq)
  lkl_grp.create_dataset("Rq_hat",data=rqhat.flat[:])
     
  if rq0 !=None:
    lkl_grp.create_dataset("Rq_0",data=rq0.flat[:])
  
  lkl_grp.attrs["A_cmb"] = Acmb
  lkl_grp.attrs["n_component"] = 1  
  
  return lkl_grp

def add_component(lkl_grp,typ,position=-1):
  nc = lkl_grp.attrs["n_component"]
  if position ==-1:
    position = nc
  assert position <=nc
  for ic in range(nc,position,-1):
    lkl_grp.copy("component_%d"%(ic-1),"component_%d"%ic)
    del lkl_grp["component_%d"%(ic-1)]
  agrp = lkl_grp.create_group("component_%d"%(position))  
  agrp.attrs["component_type"]=typ
  lkl_grp.attrs["n_component"] = nc+1
  return agrp

def add_cst_component(lkl_grp,rq0,position=-1):
  agrp = add_component(lkl_grp,"cst",position)
  agrp.create_dataset("Rq_0",data=rq0.flat[:])
  return agrp
def add_cst_component_pars(lkl_grp,pars):
  rq0 = php.read_somearray(pars.rq0)
  return add_cst_component(lkl_grp,rq0)

def add_gcal_component(lkl_grp,typ,ngcal,gcaltpl,binned=False,names=[],position=-1):
  if typ.lower() == "log":
    typ = "gcal_log"
  else:
    typ = "gcal_lin"
  agrp = add_component(lkl_grp,typ,position)
  agrp.attrs["ngcal"] = nm.array(ngcal,dtype=nm.int) 
  agrp.create_dataset("gcaltpl",data=nm.array(gcaltpl,dtype=nm.double).flat[:])
  if binned:
    agrp.attrs["binned"]=1
  else:
    agrp.attrs["binned"]=0

  if names:
    setnames(agrp,names)
  return agrp

def get_dnames(lkl_grp):
  if "dnames" in lkl_grp.attrs:
    dnames = [v for v in lkl_grp.attrs["dnames"].split('\0') if v]
    return dnames
  else:
    raise Exception("argl")

def add_calTP_component(lkl_grp,names,position=-1):
  typ = "calTP"
  im = []
  dnames = get_dnames(lkl_grp)
  for i,n in enumerate(names):
    if "calib" in n:
      det = re.findall("calib_(.+)",n)[0]
      idx = dnames.index(det)
      im += [idx]
  if len(im):
    agrp = add_component(lkl_grp,typ,position)
    agrp.create_dataset("im",data=nm.array(im,dtype=nm.int))
    setnames(agrp,names)
    return agrp
  return None

def add_gcal2_component(lkl_grp,names, tpl,position=-1):
  typ = "gcal2"
  agrp = add_component(lkl_grp,typ,position)
  im = []
  jm = []
  tpls = []
  dnames = get_dnames(lkl_grp)
  #compute nq here
  for i,n in enumerate(names):
    if "beammode_" in n:
      det1,det2,mode = re.findall("beammode_(.+)_(.+)_(\d+)",n)[0]
      idx1 = dnames.index(det1)
      idx2 = dnames.index(det2)
      im += [idx1]
      jm += [idx2]
      tpls += [tpl[i]]
  agrp.create_dataset("im",data=nm.array(im,dtype=nm.int))
  agrp.create_dataset("jm",data=nm.array(jm,dtype=nm.int))
  agrp.create_dataset("tpl",data=nm.array(nm.concatenate(tpls),dtype=nm.double))
  setnames(agrp,names)
  return agrp

def read_gcal_data(pars,lkl_grp):
  return read_gcal_data_(pars.str_array.datacal,pars.float_array.ngcal,pars.int_array(default=[-1]).lmax_tpl,lkl_grp)

def read_gcal_data_(datacal,ngcal,lmax_tpl,lkl_grp):
  # returns the dtemplate data
  lmin = lkl_grp.attrs["lmin"]
  lmax = lkl_grp.attrs["lmax"]
  if len(datacal) == 1:
    dat = nm.loadtxt(datacal[0]).flat[:]
  else:
    assert len(datacal)==len(ngcal)
    dat = ()
    i=0
    if len(lmax_tpl)==1:
      lmax_tpl = list(lmax_tpl)*len(ngcal)
    assert len(ngcal)==len(lmax_tpl)
    for ff,lm in zip(datacal,lmax_tpl):
      assert lm>=lmax
      idat = nm.loadtxt(ff).flat[:]
      if lm!=-1:
        idat.shape = (-1,lm+1)
        idat = idat[:ngcal[i],lmin:lmax+1]
        idat = idat.flat[:]
      dat = nm.concatenate((dat,idat))  
  return dat

def add_gcal_component_pars(lkl_grp,pars):
  typ = pars.str.type
  ngcal = pars.float_array.ngcal  
  gcaltpl = read_gcal_data(pars,lkl_grp)
  names = []
  if "name" in pars:
    names = pars.str_array.name
    assert len(names) == nm.sum(ngcal)
  binned = bool(pars.int(default=0).binned!=0)
  return add_gcal_component(lkl_grp,typ,ngcal,galtpl,binned,names)

def setnames(agrp,names):
  agrp.attrs["names"] = php.pack256(*names) 
  
def add_egfs_component(lkl_grp,vpars,defaults,values,lmin,lmax,template_names,tpls,cib_decor_clustering,position=-1):
  import egfs
  agrp = add_component(lkl_grp,"egfs",position)
  egfs.add_xxx(agrp,vpars,defaults,values,lmin,lmax,template_names,tpls,cib_decor_clustering)
  agrp.attrs["A_cmb"] = lkl_grp.attrs["A_cmb"]
  return agrp

def add_from_pars(lkl_grp,parfile):
  import miniparse
  pars = miniparse.miniparse(parfile)
  typ = pars.str.ctype
  return globals()["add_%s_component_pars"](lkl_grp,pars)

def add_parametric_component(lkl_grp,name,dets,vpars,lmin,lmax,defaults={},color=None,rename={},voidmask="",data=None,position=-1):
  import os
  import parametric
  import os.path as osp
  #parametric.register_all(parametric.__dict__,False)
  
  # initialize parameters
  prclass = getattr(parametric,name)
  nT = lkl_grp.attrs["m_channel_T"]
  nP = lkl_grp.attrs["m_channel_P"]
  if issubclass(prclass,parametric.parametric_pol):
    has_cl = lkl_grp.attrs["has_cl"]
    pm = prclass(dets[:nT],dets[nT:],has_cl,vpars,lmin,lmax,defaults,color=color,rename=rename,voidmask=voidmask)
  else:
    dets = dets[:nT]
    if color!=None:
        color = color[:nT]
    pm = prclass(dets,vpars,lmin,lmax,defaults,color=color,rename=rename,voidmask=voidmask)
    
  #filter them out
  npars = [vp for vp in vpars if pm.has_parameter(vp)]
  agrp = add_component(lkl_grp,pm.name,position)
  agrp.attrs["ndim"] = len(npars)
  agrp.attrs["keys"] = php.pack256(*npars)
  nefaults = pm.defaults
  agrp.attrs["ndef"] = len(nefaults)
  defkey = nefaults.keys()
  defval = [nefaults[k] for k in defkey]
  agrp.attrs["defaults"] = php.pack256(*defkey)
  agrp.attrs["values"] = php.pack256(*defval)

  agrp.attrs["lmin"] = lmin
  agrp.attrs["lmax"] = lmax

  agrp.attrs["dfreq"] = [float(d) for d in dets]
  agrp.attrs["A_cmb"] = lkl_grp.attrs["A_cmb"]

  voidmask = pm.voidmask
  if voidmask:
      _voidlist = [i for i in range(len(voidmask)) if not bool(int(voidmask[i]))]
      nvoid = len(_voidlist)
      if nvoid!=0:
        agrp.attrs["nvoid"] = nvoid
        agrp.attrs["voidlist"] = _voidlist
      
  if color is not None:
    agrp.create_dataset("color",data=color.flat[:])  

  template = pm.get_template()
  if template is None:
    pass
  else:
    if data is None:
      agrp.create_dataset("template",data=nm.array(template,dtype=nm.double).flat[:])  
    else:
      agrp.create_dataset("template",data=nm.array(data,dtype=nm.double).flat[:])

  rename = pm.rename
  if rename:
    rename_from = rename.keys()
    rename_to = [rename[k] for k in rename_from]
    agrp.attrs["rename_from"] = php.pack256(*rename_from)
    agrp.attrs["rename_to"] = php.pack256(*rename_to)
    agrp.attrs["nrename"] = len(rename_from)
  return agrp

import numpy as nm

def set_criterion(lkl_grp,typ,**extra):
  if typ.lower()=="classic":
    lkl_grp.attrs["criterion"]="classic"
    return
  if typ.lower()=="eig":
    lkl_grp.attrs["criterion"]="eig"
    if "eig_norm" in extra:
      lkl_grp["criterion_eig_norm"]=extra["eig_nrm"]
    else:
      import numpy.linalg as la
      import numpy as nm
      rqh = lkl_grp["Rq_hat"][:]
      nq = len(lkl_grp["wq"][:])
      m = lkl_grp.attrs["m_channel_T"] + lkl_grp.attrs["m_channel_P"] 
      rqh.shape=(nq,m,m)
      nrm = nm.array([.5*(nm.log(nm.abs(la.det(rqh[i])))+m) for i in range(nq)])
      lkl_grp["criterion_eig_norm"] = nrm
    return 
  if typ.lower()=="gauss":
    import numpy.linalg as la
    import numpy as nm
    if "mask" in extra:
        lkl_grp["criterion_gauss_mask"] = extra["mask"].flat[:]
    if "ordering" in extra:
      lkl_grp["criterion_gauss_ordering"] = extra["ordering"].flat[:]
    lkl_grp["criterion_gauss_mat"]=extra["mat"].flat[:]
    lkl_grp.attrs["criterion"]="gauss"
    return 
  if typ.lower()=="quad":
    import numpy as nm
    if "fid" in extra:
      if "mask" in extra:
        lkl_grp["criterion_quad_mask"] = extra["mask"].flat[:]
        mask = extra["mask"].flat[:]
        rq = extra["fid"]*1.
        n = int(nm.sqrt(mask.size))
        rq.shape=(-1,n,n)
        mask.shape=(n,n)
        sn = int(nm.sum(nm.triu(mask)))
        fq = nm.zeros((len(rq),sn,sn))
        for i in range(len(rq)):
          ifq = build_tensormat(rq[i],mask)
          fq[i] = nm.linalg.inv(ifq)
        lkl_grp["criterion_quad_mat"] = fq.flat[:]
      else:
        lkl_grp["criterion_quad_mat"]=extra["fid"].flat[:]
    lkl_grp.attrs["criterion"]="quad"

  return
  
def build_tensormat(rq ,mask=None):
  n = len(rq)
  if mask==None:
    mask = nm.ones((n,n))
  M = nm.zeros((n**2,n**2))
  for i in range(n):
    for j in range(n):
      for k in range(n):
        for l in range(n):
          M[j*n+k,l*n+i] = rq[i,j]*rq[k,l]
  B = build_vecproj(mask)
  return nm.dot(B.T,nm.dot(M,B))

def build_vecproj(mask):
  n=len(mask)
  p=0
  B = nm.zeros((n**2,nm.sum(nm.triu(mask))))
  for i in range(n):
    for j in range(i,n):
      if mask[i,j]==0:
        continue
      B[i*n+j,p]=.5
      B[j*n+i,p]=.5
      if i==j:
        B[i*n+j,p]=1
      p+=1
  return B


def parametric_from_smica(h5file,lmin=-1,lmax=-1,ilkl=0):
  import hpy
  ff = hpy.File(h5file,"r")
  return parametric_from_smica_group(ff["clik/lkl_%d"%ilkl],lmin,lmax)
  ff.close()

def parametric_from_smica_group(hgrp,lmin=-1,lmax=-1):
  import parametric as prm
  nc = hgrp.attrs["n_component"]
  prms = []
  for i in range(1,nc):
    compot = hgrp["component_%d"%i].attrs["component_type"]
    if not (compot in dir(prm)):
      continue
    key = [v.strip() for v in hgrp["component_%d"%i].attrs["keys"].split("\0") if v.strip() ]
    default = [v.strip() for v in hgrp["component_%d"%i].attrs["defaults"].split("\0") if v.strip() ]
    value = [v.strip() for v in hgrp["component_%d"%i].attrs["values"].split("\0") if v.strip() ]
    defdir = dict(zip(default,value))
    frq = hgrp["component_%d"%i].attrs["dfreq"]
    try:
      rename_from = [v.strip() for v in hgrp["component_%d"%i].attrs["rename_from"].split("\0") if v.strip() ]
      rename_to = [v.strip() for v in hgrp["component_%d"%i].attrs["rename_to"].split("\0") if v.strip() ]
      rename = dict(zip(rename_from,rename_to))
    except Exception,e:
      rename = {}
    #print rename
    #print key
    #print default
    #print value
    try:
      color = hgrp["component_%d/color"%i][:]
    except Exception,e:
      color = None
    try:
      data = hgrp["component_%d/data"%i][:]
    except Exception,e:
      data = None
    if lmin==-1:
      lmin = hgrp["component_%d"%i].attrs["lmin"]
    if lmax==-1:
      lmax = hgrp["component_%d"%i].attrs["lmax"]
    cmpr = getattr(prm,compot)
    if issubclass(cmpr,prm.parametric_pol):
      has_TEB = hgrp["has_cl"]
      detT = frq[:hgrp["m_channel_T"]]
      detP = frq[:hgrp["m_channel_P"]]
      args = [detT,detP,has_TEB[:3],key,lmin,lmax]
    else:
      args = [frq,key,lmin,lmax]
    kargs = {"rename":rename,"defs":defdir,"color":color}
    if data != None:
      kargs["data"]=data
    prms += [cmpr(*args,**kargs)]
  return prms  

def calTP_from_smica(dffile):
  import hpy
  
  fi = hpy.File(dffile)
  hascl = fi["clik/lkl_0/has_cl"]
  nb = fi["clik/lkl_0/nbins"]/hascl.sum()
  mt = fi["clik/lkl_0/m_channel_T"]*hascl[0]
  me = fi["clik/lkl_0/m_channel_P"]*hascl[1]
  mb = fi["clik/lkl_0/m_channel_P"]*hascl[2]
  m = mt+me+mb
  hgrp = fi["clik/lkl_0"]
  nc = hgrp.attrs["n_component"]
  prms = []
  fnd=False
  for i in range(1,nc):
    compot = hgrp["component_%d"%i].attrs["component_type"]
    if not (compot=="calTP"):
      continue
    fnd=True
    break
  if not fnd:
    def cal(vals):
      return nm.ones((nb,m,m))
    cal.varpar = []
    return cal
  names = fi["clik/lkl_0/component_%d/names"%i].replace("\0"," ").split()
  im = fi["clik/lkl_0/component_%d/im"%i]
  def cal(vals):
    vec = nm.ones(m)
    evals = nm.exp(vals)
    vec[im[im<mt]] = evals[im<mt]
    vec[im[im>=mt]] = evals[im>=mt]
    if mb:
      vec[im[im>=mt]+mb] = evals[im>=mt]
    return nm.ones((nb,m,m))*nm.outer(vec,vec)[nm.newaxis,:,:]
  cal.varpar = names
  return cal

def create_gauss_mask(nq,qmins,qmaxs,nT,nP):
  """lmins is a ndetxndet qmins matrix, qmaxs is a ndetxndet matrix of qmax. if qmax[i,j]<=0, the spectrum is ignored
  mask is 1 for q in qmins<=q<qmaxs
  only the upper part (j>=i) of qmins and qmaxs is used"""
  qmins = nm.array(qmins)
  qmaxs = nm.array(qmaxs)
  ndet = qmins.shape[0]
  assert ndet == nT+nP
  mask = nm.zeros((nq,ndet,ndet),dtype=nm.int )
  for i in range(ndet):
    for j in range(i,ndet):
      mask[qmins[i,j]:qmaxs[i,j],i,j]=1
      mask[qmins[i,j]:qmaxs[i,j],j,i]=1
      if i<nT and j>=nT and i>j-nT and i<nP:
        # cas TE dessous
        mask[qmins[i,j]:qmaxs[i,j],i,j]=0
        mask[qmins[i,j]:qmaxs[i,j],j,i]=0

  return mask

def ordering_from_smica(dffile,jac=True):
  import hpy
  
  fi = hpy.File(dffile)
  msk = fi["clik/lkl_0/criterion_gauss_mask"]
  ord = fi["clik/lkl_0/criterion_gauss_ordering"]
  hascl = fi["clik/lkl_0/has_cl"]
  m = fi["clik/lkl_0/m_channel_T"]*hascl[0]+fi["clik/lkl_0/m_channel_P"]*hascl[1]+fi["clik/lkl_0/m_channel_P"]*hascl[2]
  nb = fi["clik/lkl_0/nbins"]/hascl.sum()
  m2 = m*m
  ordr =  nm.concatenate([nm.arange(nb)[msk[iv+jv*m::m2]==1]*m2+iv*m+jv for iv,jv in zip(ord[::2],ord[1::2])])
  if jac==True:
    return ordr,nm.array([ordr/m2==i for i in range(nb)],dtype=nm.int)
  fi.close()

def get_bestfit_and_cl(dffile,bffile):
  import hpy
  import lkl

  fi = hpy.File(dffile)
  bff = nm.loadtxt(bffile)
  lmax = fi["clik/lkl_0/lmax"]
  hascl = fi["clik/lkl_0/has_cl"]
  cls = nm.zeros((6,lmax+1))
  cnt=0
  for i in range(6):
    if hascl[i]:
      cls[i] = bff[cnt:cnt+lmax+1]
      cnt += lmax+1
  lkl = lkl.clik(dffile)
  names = lkl.extra_parameter_names
  bestfit = dict(zip(names,bff[cnt:]))
  return bestfit,cls


def _simu_from_rq(mt,me,mb,rq,nside=2048):
  import healpy as hp
  m = mt+me+mb
  cls = []
  for i in range(m):
    for j in range(m-i):
      cls += [rq[:,j,j+i]]
  print "random alms"
  alms = hp.synalm(cls,new = True)
  rmaps = nm.zeros((m,m,12*nside**2))
  mp = nm.max(me,mb)
        
  mps = []

  for i in range(mp):
    almsr = []
    if mt<=i:
      almsr += [nm.zeros_like(alms[0])]
    else:
      almsr += [cls[i]]
    if me<=i:
      almsr += [nm.zeros_like(alms[0])]
    else:
      almsr += [cls[i+mt]]
    if mb<=i:
      almsr += [nm.zeros_like(alms[0])]
    else:
      almsr += [cls[i+mt+me]]
    print "fg channel %d"%i
    mps += [hp.alm2map(almsr,nside,pol=True)]
  for i in range(mp,m):
    print "fg channel %d"%i
    mps += [[hp.alm2map(alms[i],nside,pol=True),None,None]]
  return mps

def simulate_chanels(dffile,bestfit,cls,calib=True,nside=2048,all=False):
  import hpy
  if isinstance(bestfit,str):
    bestfit,cls = get_bestfit_and_cl(dffile,bestfit)
  fi = hpy.File(dffile)
  cal = calTP_from_smica(dffile)
  cvec = [bestfit[nn] for nn in cal.varpar]
  if not calib:
    cvec = cvec*0
  g = nm.sqrt(cal(cvec)[0].diagonal())
  hascl = fi["clik/lkl_0/has_cl"]
  lmin = fi["clik/lkl_0/lmin"]
  lmax = fi["clik/lkl_0/lmax"]
  nb = fi["clik/lkl_0/nbins"]/hascl.sum()
  mt = fi["clik/lkl_0/m_channel_T"]*hascl[0]
  me = fi["clik/lkl_0/m_channel_P"]*hascl[1]
  mb = fi["clik/lkl_0/m_channel_P"]*hascl[2]
  m = mt+me+mb
  import healpy as hp

  #icls = [-1,-1,-1,-1,-1,-1]
  #if mt!=0:
  #  icls[0] = 0
  #if me!=0:
  #  icls[1] = 1
  #if mt!=[0]:
  #  icls[2] = 2
  #if mt*me != 0:
  #  icls[3] = 3
  #if mt*mb !=0:
  #  icls[4] = 5
  #if me*mb !=0:
  #  icls[5] = 4

  #ncls = [cls[i] if cls[i].sum() else None for i in icls if i!=-1]

  icls = [0,1,2,3,5,4]
  ncls = [cls[i]  for i in icls]

  if me==0 and mb == 0:
    icls = [0]

  print "generate cmb"
  cmb = hp.synfast(ncls,nside,pol=True and len(ncls)>1 ,new=True)

  # got maps  for the cmb !

  prms = parametric_from_smica(dffile)
  oq = []
  nrms = []
  for p in prms:
    pvec = [bestfit[nn] for nn in p.varpar]
    oq += [p(pvec)]
    nrms += [p.__class__.__name__]
  oq = nm.array(oq)
  oq = nm.sum(oq,0)
  print "generate fg"
  fg = _simu_from_rq(mt,me,mb,oq,nside)

  maps = [[None,None,None]]*max(mt,me,mb)
  for i in range(mt):
    maps[i][0] = (cmb[0] + fg[i][0]) *g[i]
  for j in range(max(me,mb)):
    maps[i][1] = (cmb[1] + fg[i][1]) * g[i+mt]
    maps[i][2] = (cmb[2] + fg[i][2]) * g[i+mt]
  if all:
    return maps,cmb,fg,g
  return maps



def get_binned_calibrated_model_and_data(dffile,bestfit,cls=None):
  import hpy
  if isinstance(bestfit,str):
    bestfit,cls = get_bestfit_and_cl(dffile,bestfit)
  fi = hpy.File(dffile)
  cal = calTP_from_smica(dffile)
  cvec = [bestfit[nn] for nn in cal.varpar]
  g = cal(cvec)
  acmb = fi["clik/lkl_0/A_cmb"]
  g *= nm.outer(acmb,acmb)[nm.newaxis,:,:]
  rqh = fi["clik/lkl_0/Rq_hat"]
  rqh.shape = g.shape
  rqh/=g
  prms = parametric_from_smica(dffile)
  oq = []
  nrms = []
  for p in prms:
    pvec = [bestfit[nn] for nn in p.varpar]
    oq += [p(pvec)]
    nrms += [p.__class__.__name__]
  oq = nm.array(oq)
  blmin = fi["clik/lkl_0/bin_lmin"]
  blmax = fi["clik/lkl_0/bin_lmax"]
  b_ws = fi["clik/lkl_0/bin_ws"]
  hascl = fi["clik/lkl_0/has_cl"]
  lmin = fi["clik/lkl_0/lmin"]
  lmax = fi["clik/lkl_0/lmax"]
  nb = fi["clik/lkl_0/nbins"]/hascl.sum()
  mt = fi["clik/lkl_0/m_channel_T"]*hascl[0]
  me = fi["clik/lkl_0/m_channel_P"]*hascl[1]
  mb = fi["clik/lkl_0/m_channel_P"]*hascl[2]
  m = mt+me+mb
  
  oqb = nm.zeros((len(oq),)+rqh.shape)
  lm = nm.zeros(nb)
  for b in range(nb):
    oqb[:,b] = nm.sum(oq[:,blmin[b]:blmax[b]+1]*b_ws[nm.newaxis,blmin[b]:blmax[b]+1,nm.newaxis,nm.newaxis],1)
    lm[b] += nm.sum(nm.arange(lmin+blmin[b],lmin+blmax[b]+1)*b_ws[blmin[b]:blmax[b]+1])
  res = lm,oqb,nrms,rqh
  if cls!=None:
    rq = nm.zeros((nb,m,m))
    for b in range(nb):
      if mt:
        rq[b,:mt,:mt]+=nm.sum(cls[0,lmin+blmin[b]:lmin+blmax[b]+1]*b_ws[blmin[b]:blmax[b]+1])
        if me:
          rq[b,:mt,mt:mt+me]+=nm.sum(cls[3,lmin+blmin[b]:lmin+blmax[b]+1]*b_ws[blmin[b]:blmax[b]+1])
          rq[b,mt:mt+me,:mt]+=nm.sum(cls[3,lmin+blmin[b]:lmin+blmax[b]+1]*b_ws[blmin[b]:blmax[b]+1])
        if mb:
          rq[b,:mt,mt+me:mb+mt+me]+=nm.sum(cls[4,lmin+blmin[b]:lmin+blmax[b]+1]*b_ws[blmin[b]:blmax[b]+1])
          rq[b,mt+me:mb+mt+me,:mt]+=nm.sum(cls[4,lmin+blmin[b]:lmin+blmax[b]+1]*b_ws[blmin[b]:blmax[b]+1])
      if me:
        rq[b,mt:mt+me,mt:mt+me]+=nm.sum(cls[1,lmin+blmin[b]:lmin+blmax[b]+1]*b_ws[blmin[b]:blmax[b]+1])
        if mb:
          rq[b,mt:mt+me,mt+me:mb+mt+me]+=nm.sum(cls[5,lmin+blmin[b]:lmin+blmax[b]+1]*b_ws[blmin[b]:blmax[b]+1])
          rq[b,mt+me:mb+mt+me,mt:mt+me]+=nm.sum(cls[5,lmin+blmin[b]:lmin+blmax[b]+1]*b_ws[blmin[b]:blmax[b]+1])
      if mb:
        rq[b,mt+me:mt+me+mb,mt+me:mb+mt+me]+=nm.sum(cls[2,lmin+blmin[b]:lmin+blmax[b]+1]*b_ws[blmin[b]:blmax[b]+1])
    res = lm,oqb,nrms,rqh,rq
  return res

  
def plot_1d_residual(lm,oqb,nrms,rqh,rq,m1,m2,**extra):
  import pylab as plt  
  plt.figure()
  plt.semilogy(lm,rqh[:,m1,m2]*lm*(lm+1.)/2./nm.pi,label="data")
  plt.semilogy(lm,rq[:,m1,m2]*lm*(lm+1.)/2./nm.pi,label="cmb")
  if extra.get("abs",False):
    plt.semilogy(lm,-rqh[:,m1,m2]*lm*(lm+1.)/2./nm.pi,label="-data")
    plt.semilogy(lm,-rq[:,m1,m2]*lm*(lm+1.)/2./nm.pi,label="-cmb")
  for oq,nn in zip(oqb,nrms):
    plt.semilogy(lm,oq[:,m1,m2]*lm*(lm+1.)/2./nm.pi,label=nn)
  plt.semilogy(lm,nm.abs(rqh[:,m1,m2]-(rq[:,m1,m2]+nm.sum(oqb[:,:,m1,m2],0)))*lm*(lm+1.)/2./nm.pi,label="|data-model|")
  plt.legend(loc="upper right",frameon=False,ncol=3,prop=plt.matplotlib.font_manager.FontProperties(size="x-small"))
  if extra.get("title",""):
    plt.suptitle(extra["title"])
  plt.ylabel(extra.get("ylabel","$D_{\\ell}\\ \\mu K^2$"))
  plt.xlabel(extra.get("xlabel","$\\ell$"))
  #plt.xscale=("linear")
  #plt.xaxis = (0,lm[-1]+100)

def best_fit_cmb(dffile,bestfit):
  import parobject as php
  import hpy

  oo,Jt = ordering_from_smica(dffile)

  fi = hpy.File(dffile)

  siginv = fi["clik/lkl_0/criterion_gauss_mat"]
  siginv.shape=(len(oo),len(oo))

  lm,oqb,nrms,rqh = get_binned_calibrated_model_and_data(dffile,bestfit)

  Yo = nm.sum(oqb,0)-rqh
  Yo = Yo.flat[oo]
  Jt_siginv = nm.dot(Jt,siginv)
  Jt_siginv_Yo = nm.dot(Jt_siginv,Yo)
  Jt_siginv_J = nm.dot(Jt_siginv,Jt.T)
  return lm,-nm.linalg.solve(Jt_siginv_J,Jt_siginv_Yo),1./nm.sqrt(Jt_siginv_J.diagonal())
