import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from memristor import memristor


def wave(a0,f0,t):
    return a0*np.sin(2*np.pi*f0*t)

def get_mem_states(a0,f0,mem,t):

    print "a0",a0
    print "f0",f0
    yw=[]
    yr=[]
    yi=[]
    xv=[]

    for i in t:
        yw.append(mem1.getW())
        yi.append(mem1.getI())
        yr.append(mem1.getR())
        xv.append(mem1.getV())
        mem.updateW()
        mem.setV(wave(a0,f0,i))

    return [yw,yr,yi,xv]

#(w, D, Roff, Ron, v, mu, Tao):
mem1 = memristor(0.1,1.0,10000.0,10.0,10.0,0.1,100.1)
mem2 = memristor(0.1,1.0,10000.0,10.0,10.0,0.1,100.1)

fig, (ax1,ax2,ax3) = plt.subplots(3,1)
plt.subplots_adjust(left=0.25, bottom=0.25)

t = np.arange(0.0, 10.0, 0.001)
a0 = 5
f0 = 3
s = wave(a0,f0,t)


[yw, yr, yi, xv] = get_mem_states(a0,f0,mem1,t)
[yww, yrr, yii, xvv] = get_mem_states(a0,f0,mem2,t)

# l, = plt.plot(t, s, lw=2, color='red')
ln1, = ax1.plot(t, s, lw=2, color='red')
ln2, = ax2.plot(xv, yi, lw=0.5, color='b')
ln3, = ax3.plot(xvv,yii, lw=1.5, color='g')


ax1.set_xlim([0,1])

axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
axamp = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)

sfreq = Slider(axfreq, 'Freq', 0.1, 5.0, valinit=f0)
samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=a0)


def update(val):
    amp = samp.val
    freq = sfreq.val
    [yw, yr, yi, xv] = get_mem_states(amp,freq,mem1,t)
    [yww, yrr, yii, xvv] = get_mem_states(amp,freq,mem2,t)
    ln1.set_ydata(wave(amp,freq,t))
    ln2.set_xdata(xv)
    ln2.set_ydata(yi)
    ln3.set_xdata(xvv)
    ln3.set_ydata(yii)
    ax1.relim()
    ax2.relim()
    ax3.relim()
    ax1.autoscale_view()
    ax2.autoscale_view()
    ax3.autoscale_view()
    # fig.canvas.draw_idle()
    plt.draw()

sfreq.on_changed(update)
samp.on_changed(update)

# resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
# button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
#
#
# def reset(event):
#     sfreq.reset()
#     samp.reset()
# button.on_clicked(reset)
#
# rax = plt.axes([0.025, 0.5, 0.15, 0.15], axisbg=axcolor)
# radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)
#
#
# def colorfunc(label):
#     l.set_color(label)
#     fig.canvas.draw_idle()
# radio.on_clicked(colorfunc)

plt.show()