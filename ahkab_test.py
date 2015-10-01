__author__ = 'nfrik'

from ahkab import *;
from ahkab.circuit import Circuit
from ahkab.plotting import plot_results
import numpy as np

cir = Circuit('asdf')
cir.add_vsource('V1','n1',cir.gnd,dc_value=1.,ac_value=0.)
cir.add_resistor('R1','n1','n2',50.)
cir.add_resistor('R2','n2','n3',1100)
cir.add_resistor('R4','n3',cir.gnd,10)

# ac1 = new_ac(2.*np.pi*.97e3, 2.*np.pi*1.03e3,1e2,x0=None)
opa = new_op()
r = run(cir,opa)['op']
print r['VN2'][0][0]
print r

# res = run(cir, ac1)
#
# # plot_results('asdf',[('|Vn8|',"")],res['ac'],outfilename='dccircuit.png')
#
# plot_results('5th order 1kHz Butterworth filter', [('|Vn3|',"")], res['ac'],
#              outfilename='bpf_transfer_fn.png')