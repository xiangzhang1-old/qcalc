#
hidden = {'hidden', 'phi0', 'rho0', 'rho'}
#
if phi0 == 0:
    istart = 0
elif isinstance(phi0, str):
    istart = 1
if rho0 == 0:
    icharg = 2
elif isinstance(rho0, str):
    icharg = 1
elif isinstance(rho, str):
    icharg = 11
#
istart; icharg;
#