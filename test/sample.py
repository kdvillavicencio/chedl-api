from thermo.chemical import Chemical
tol = Chemical('toluene')
tol.calculate(T=360, P=200000)
print(tol.rho)
print(tol.mu)
print(tol.Cp)