from clik.parametric cimport c_parametric, error, doError, parametric, parametric_template, parametric_pol, parametric_pol_template

cdef extern c_parametric *galactic_component_init(int ndet, double *detlist, int ndef, char** defkey, char **defvalue, int nvar, char **varkey, int lmin, int lmax, error **err)
cdef extern c_parametric *gpe_dust_init(int ndet, double *detlist, int ndef, char** defkey, char **defvalue, int nvar, char **varkey, int lmin, int lmax, error **err)
cdef extern double c_dust_spectrum "dust_spectrum" (double nu, double T_dust, double beta_dust, double nu0)
cdef extern double c_non_thermal_spectrum "non_thermal_spectrum" (double nu, double alpha_non_thermal, double nu0)
cdef extern double c_dBdT "dBdT" (double nu, double nu0)
cdef extern c_parametric *gal_TE_init(int ndet_T, int ndet_P, int *has_TEB, double *detlist, int ndef, char** defkey, char **defvalue, int nvar, char **varkey, int lmin, int lmax, error **err)
cdef extern c_parametric *gal_EE_init(int ndet_T, int ndet_P, int *has_TEB, double *detlist, int ndef, char** defkey, char **defvalue, int nvar, char **varkey, int lmin, int lmax, error **err)


def dust_spectrum(nu,T_dust=18.0,beta_dust=1.8,nu0=143.0):
  return c_dust_spectrum(<double>nu,<double>T_dust,<double>beta_dust,<double>nu0)

def non_thermal_spectrum(nu,alpha_non_thermal=-1.0,nu0=143.0):
  return c_non_thermal_spectrum(<double>nu,<double>alpha_non_thermal,<double>nu0)

def dBdT(nu,nu0=143.0):
  return c_dBdT(<double>nu,<double>nu0)


cdef class galametric(parametric):
  def __cinit__(self):
    self.initfunc = <void*>galactic_component_init

cdef class gal_TE(parametric_pol):
  def __cinit__(self):
    self.initfunc = <void*>gal_TE_init

cdef class gal_EE(parametric_pol):
  def __cinit__(self):
    self.initfunc = <void*>gal_EE_init

cdef class gpe_dust(parametric):
  def __cinit__(self):
    self.initfunc = <void*> gpe_dust_init;

    
component_list = ["galametric","gpe_dust","gal_EE","gal_TE"]
