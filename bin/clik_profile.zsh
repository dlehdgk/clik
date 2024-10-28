# this code cannot be run directly
# do 'source /users/smp24dhl/cosmo/code/planck/clik/bin/clik_profile.sh' from your sh shell or put it in your profile

add_path_element() {
    local tmp="${1//:${2}:/:}"
    tmp="${tmp/#${2}:/}"
    tmp="${tmp/%:${2}/}"
    echo -n "${tmp}:${2}"
} 

if [ -z "${PATH}" ]; then 
PATH=/users/smp24dhl/cosmo/code/planck/clik/bin
export PATH
else
export PATH=$(add_path_element "$PATH" /users/smp24dhl/cosmo/code/planck/clik/bin)
fi
if [ -z "${PYTHONPATH}" ]; then 
PYTHONPATH=/users/smp24dhl/cosmo/code/planck/clik/lib/python3.9/site-packages
export PYTHONPATH
else
export PYTHONPATH=$(add_path_element "$PYTHONPATH"  /users/smp24dhl/cosmo/code/planck/clik/lib/python3.9/site-packages)
fi
if [ -z "${LD_LIBRARY_PATH}" ]; then 
LD_LIBRARY_PATH=/usr/lib
export LD_LIBRARY_PATH
else
export LD_LIBRARY_PATH=$(add_path_element "$LD_LIBRARY_PATH"  /usr/lib)
fi
if [ -z "${LD_LIBRARY_PATH}" ]; then 
LD_LIBRARY_PATH=/users/smp24dhl/cosmo/code/planck/clik/lib
export LD_LIBRARY_PATH
else
export LD_LIBRARY_PATH=$(add_path_element "$LD_LIBRARY_PATH"  /users/smp24dhl/cosmo/code/planck/clik/lib)
fi
if [ -z "${LD_LIBRARY_PATH}" ]; then 
LD_LIBRARY_PATH=/opt/apps/testapps/el7/software/staging/OpenBLAS/0.3.9-GCC-9.3.0/lib
export LD_LIBRARY_PATH
else
export LD_LIBRARY_PATH=$(add_path_element "$LD_LIBRARY_PATH"  /opt/apps/testapps/el7/software/staging/OpenBLAS/0.3.9-GCC-9.3.0/lib)
fi
if [ -z "${LD_LIBRARY_PATH}" ]; then 
LD_LIBRARY_PATH=/opt/apps/testapps/el7/software/staging/CFITSIO/3.48-GCCcore-9.3.0/lib
export LD_LIBRARY_PATH
else
export LD_LIBRARY_PATH=$(add_path_element "$LD_LIBRARY_PATH"  /opt/apps/testapps/el7/software/staging/CFITSIO/3.48-GCCcore-9.3.0/lib)
fi

CLIK_PATH=/users/smp24dhl/cosmo/code/planck/clik
export CLIK_PATH

CLIK_DATA=/users/smp24dhl/cosmo/code/planck/clik/share/clik
export CLIK_DATA

CLIK_PLUGIN=rel2015
export CLIK_PLUGIN

