# this code cannot be run directly
# do 'source /users/smp24dhl/cosmo/code/planck/clik/bin/clik_profile.csh' from your csh shell or put it in your profile

 

if !($?PATH) then
setenv PATH /users/smp24dhl/cosmo/code/planck/clik/bin
else
set newvar=$PATH
set newvar=`echo ${newvar} | sed s@:/users/smp24dhl/cosmo/code/planck/clik/bin:@:@g`
set newvar=`echo ${newvar} | sed s@:/users/smp24dhl/cosmo/code/planck/clik/bin\$@@` 
set newvar=`echo ${newvar} | sed s@^/users/smp24dhl/cosmo/code/planck/clik/bin:@@`  
set newvar=/users/smp24dhl/cosmo/code/planck/clik/bin:${newvar}                     
setenv PATH /users/smp24dhl/cosmo/code/planck/clik/bin:${newvar} 
endif
if !($?PYTHONPATH) then
setenv PYTHONPATH /users/smp24dhl/cosmo/code/planck/clik/lib/python3.9/site-packages
else
set newvar=$PYTHONPATH
set newvar=`echo ${newvar} | sed s@:/users/smp24dhl/cosmo/code/planck/clik/lib/python3.9/site-packages:@:@g`
set newvar=`echo ${newvar} | sed s@:/users/smp24dhl/cosmo/code/planck/clik/lib/python3.9/site-packages\$@@` 
set newvar=`echo ${newvar} | sed s@^/users/smp24dhl/cosmo/code/planck/clik/lib/python3.9/site-packages:@@`  
set newvar=/users/smp24dhl/cosmo/code/planck/clik/lib/python2.7/site-packages:${newvar}                     
setenv PYTHONPATH /users/smp24dhl/cosmo/code/planck/clik/lib/python2.7/site-packages:${newvar} 
endif
if !($?LD_LIBRARY_PATH) then
setenv LD_LIBRARY_PATH /usr/lib
else
set newvar=$LD_LIBRARY_PATH
set newvar=`echo ${newvar} | sed s@:/usr/lib:@:@g`
set newvar=`echo ${newvar} | sed s@:/usr/lib\$@@` 
set newvar=`echo ${newvar} | sed s@^/usr/lib:@@`  
set newvar=/usr/lib:${newvar}                     
setenv LD_LIBRARY_PATH /usr/lib:${newvar} 
endif
if !($?LD_LIBRARY_PATH) then
setenv LD_LIBRARY_PATH /users/smp24dhl/cosmo/code/planck/clik/lib
else
set newvar=$LD_LIBRARY_PATH
set newvar=`echo ${newvar} | sed s@:/users/smp24dhl/cosmo/code/planck/clik/lib:@:@g`
set newvar=`echo ${newvar} | sed s@:/users/smp24dhl/cosmo/code/planck/clik/lib\$@@` 
set newvar=`echo ${newvar} | sed s@^/users/smp24dhl/cosmo/code/planck/clik/lib:@@`  
set newvar=/users/smp24dhl/cosmo/code/planck/clik/lib:${newvar}                     
setenv LD_LIBRARY_PATH /users/smp24dhl/cosmo/code/planck/clik/lib:${newvar} 
endif
if !($?LD_LIBRARY_PATH) then
setenv LD_LIBRARY_PATH /opt/apps/testapps/el7/software/staging/OpenBLAS/0.3.9-GCC-9.3.0/lib
else
set newvar=$LD_LIBRARY_PATH
set newvar=`echo ${newvar} | sed s@:/opt/apps/testapps/el7/software/staging/OpenBLAS/0.3.9-GCC-9.3.0/lib:@:@g`
set newvar=`echo ${newvar} | sed s@:/opt/apps/testapps/el7/software/staging/OpenBLAS/0.3.9-GCC-9.3.0/lib\$@@` 
set newvar=`echo ${newvar} | sed s@^/opt/apps/testapps/el7/software/staging/OpenBLAS/0.3.9-GCC-9.3.0/lib:@@`  
set newvar=/opt/apps/testapps/el7/software/staging/OpenBLAS/0.3.9-GCC-9.3.0/lib:${newvar}                     
setenv LD_LIBRARY_PATH /opt/apps/testapps/el7/software/staging/OpenBLAS/0.3.9-GCC-9.3.0/lib:${newvar} 
endif
if !($?LD_LIBRARY_PATH) then
setenv LD_LIBRARY_PATH /opt/apps/testapps/el7/software/staging/CFITSIO/3.48-GCCcore-9.3.0/lib
else
set newvar=$LD_LIBRARY_PATH
set newvar=`echo ${newvar} | sed s@:/opt/apps/testapps/el7/software/staging/CFITSIO/3.48-GCCcore-9.3.0/lib:@:@g`
set newvar=`echo ${newvar} | sed s@:/opt/apps/testapps/el7/software/staging/CFITSIO/3.48-GCCcore-9.3.0/lib\$@@` 
set newvar=`echo ${newvar} | sed s@^/opt/apps/testapps/el7/software/staging/CFITSIO/3.48-GCCcore-9.3.0/lib:@@`  
set newvar=/opt/apps/testapps/el7/software/staging/OpenBLAS/0.3.9-GCC-9.3.0/lib:${newvar}                     
setenv LD_LIBRARY_PATH /opt/apps/testapps/el7/software/staging/OpenBLAS/0.3.9-GCC-9.3.0/lib:${newvar} 
endif

setenv CLIK_PATH /users/smp24dhl/cosmo/code/planck/clik
setenv CLIK_DATA /users/smp24dhl/cosmo/code/planck/clik/share/clik

setenv CLIK_PLUGIN rel2015

