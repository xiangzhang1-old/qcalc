#
hidden = {'hidden', 'phi0', 'rho0', 'rho'}
#
if phi0 == 0:
    istart = 0
elif phi0:
    istart = 1
if rho0 == 0:
    icharg = 2
elif rho0:
    icharg = 1
elif rho:
    icharg = 11
#
assert None not in [istart, icharg]
#