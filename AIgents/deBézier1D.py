# Interactive de Casteljau / Bézier curve explorer
'''
Claude (Sonnet 5 Medium) — a prompt for a better visualization of Bézier curves. De Casteljau's algorithm (and its animation)was added by Claude).
Today we have a simple job to do: a better visualization.

1. Here is a script (of mine): [AppliedPythonology/deBézier1D.py at master · Bahrd/AppliedPythonology](https://github.com/Bahrd/AppliedPythonology/blob/master/deB%C3%A9zier1D.py)
2. I believe you can help making the visual presentation much more dynamic, interactive and thus mor entertaining and informative.

Could you?
'''
# Extends deBézier1D.py: https://github.com/Bahrd/AppliedPythonology/blob/master/deB%C3%A9zier1D.py
# https://matplotlib.org/stable/gallery/widgets/slider_demo.html
# https://en.wikipedia.org/wiki/B%C3%A9zier_curve
# https://en.wikipedia.org/wiki/De_Casteljau%27s_algorithm

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, CheckButtons
from sys import argv as controlPoints

# --- Bernstein-form evaluation, used only to draw the finished curve ------
def bézier(P, p=128):
    binomial = lambda n, k: 1 if k == 0 or n == k else binomial(n - 1, k - 1) + binomial(n - 1, k)
    n, u = len(P), np.linspace(0, 1, p)
    B = sum(binomial(n - 1, i) * np.outer((1 - u) ** (n - i - 1) * u ** i, P[i]) for i in range(n))
    return B[:, 0], B[:, 1]

# --- de Casteljau's algorithm, the actual construction we animate --------
def deCasteljau(P, t):
    levels, cur = [np.array(P, dtype=float)], np.array(P, dtype=float)
    while len(cur) > 1:
        cur = (1 - t) * cur[:-1] + t * cur[1:]
        levels.append(cur)
    return levels                                    # levels[-1][0] == point on curve

# --- Default control points (the wavy example from the original script) --
P = ([[0, 0], [1/8, -1], [1/4, 1], [1/2, -2], [3/4, 1], [7/8, -1], [1, 0]]
     if len(controlPoints) < 2 else eval(controlPoints[1]))
P0, t0 = [list(p) for p in P], 0.4                     # remember the reset state

fig, ax = plt.subplots(num="[de]* Bézier curve demo — interactive")
fig.subplots_adjust(top=0.92, right=0.97, left=0.08, bottom=0.28)
ax.set_xlabel('X'), ax.set_ylabel('Y')

curve, = ax.plot([], [], '-', color='#1D9E75', lw=2, zorder=2)
polygon, = ax.plot([], [], 'k:', lw=1, zorder=1)
points, = ax.plot([], [], 'o', color='#378ADD', ms=9, picker=8, zorder=4)
marker, = ax.plot([], [], 'o', color='#D85A30', ms=9, zorder=5, visible=False)
level_lines, level_dots = [], []                        # construction artists, built lazily
labels = []

state = {'t': t0, 'drag': None, 'playing': False, 'dir': 1, 'show': True}

def redraw_labels():
    for l in labels: l.remove()
    labels.clear()
    for i, (x, y) in enumerate(P):
        labels.append(ax.annotate(f'P{i}', (x, y), textcoords="offset points",
                                   xytext=(0, 10), ha='center', fontsize=9, color='0.4'))

def redraw_construction():
    for l in level_lines + level_dots: l.remove()
    level_lines.clear(); level_dots.clear()
    if not (state['show'] and len(P) > 2):
        marker.set_visible(len(P) > 1)
        if len(P) > 1:
            fx, fy = deCasteljau(P, state['t'])[-1][0]
            marker.set_data([fx], [fy])
        return
    marker.set_visible(False)
    colors = ['#7F77DD', '#F0997B', '#EF9F27', '#D4537E', '#5DCAA5']
    levels = deCasteljau(P, state['t'])
    for lv, pts in enumerate(levels[1:], start=1):
        c = colors[(lv - 1) % len(colors)]
        final = lv == len(levels) - 1
        if len(pts) > 1:
            line, = ax.plot(pts[:, 0], pts[:, 1], '-', color=c, lw=1.5, alpha=0.85, zorder=3)
            level_lines.append(line)
        dots, = ax.plot(pts[:, 0], pts[:, 1], 'o', color='#D85A30' if final else c,
                         ms=8 if final else 4.5, zorder=6 if final else 3)
        level_dots.append(dots)

def update(_=None):
    pp = bézier(P)
    curve.set_data(*pp)
    cp = tuple(zip(*P))
    polygon.set_data(*cp)
    points.set_data(*cp)
    redraw_labels()
    redraw_construction()
    ax.relim(); ax.autoscale_view()
    fig.canvas.draw_idle()

# --- t slider --------------------------------------------------------------
t_ax = fig.add_axes([0.15, 0.14, 0.7, 0.03])
t_slider = Slider(ax=t_ax, label='t', valmin=0, valmax=1, valinit=t0, valstep=0.01)
def on_t(val):
    state['t'] = val
    redraw_construction()
    fig.canvas.draw_idle()
t_slider.on_changed(on_t)

# --- checkbox: show construction -------------------------------------------
chk_ax = fig.add_axes([0.15, 0.19, 0.18, 0.05]); chk_ax.axis('off')
check = CheckButtons(chk_ax, ['Show construction'], [True])
def on_check(_):
    state['show'] = not state['show']
    redraw_construction(); fig.canvas.draw_idle()
check.on_clicked(on_check)

# --- buttons: reset / add / remove / play -----------------------------------
def make_button(rect, label):
    b = Button(fig.add_axes(rect), label, hovercolor='0.9')
    return b

reset_btn  = make_button([0.15, 0.06, 0.12, 0.05], 'Reset')
add_btn    = make_button([0.29, 0.06, 0.14, 0.05], 'Add point')
remove_btn = make_button([0.45, 0.06, 0.18, 0.05], 'Remove point')
play_btn   = make_button([0.65, 0.06, 0.20, 0.05], 'Animate ▶')

def reset(_):
    global P
    P = [list(p) for p in P0]
    state['t'] = t0; t_slider.set_val(t0)
    state['playing'] = False; play_btn.label.set_text('Animate ▶')
    update()
reset_btn.on_clicked(reset)

def add_point(_):
    if len(P) >= 12: return
    i = max(1, len(P) // 2)
    mid = [(P[i-1][0] + P[i][0]) / 2, (P[i-1][1] + P[i][1]) / 2]
    P.insert(i, mid)
    update()
add_btn.on_clicked(add_point)

def remove_point(_):
    if len(P) <= 2: return
    P.pop(len(P) // 2)
    update()
remove_btn.on_clicked(remove_point)

# --- animate t back and forth via a canvas timer ----------------------------
timer = fig.canvas.new_timer(interval=20)
def tick():
    state['t'] += state['dir'] * 0.008
    if state['t'] >= 1: state['t'] = 1; state['dir'] = -1
    if state['t'] <= 0: state['t'] = 0; state['dir'] = 1
    t_slider.set_val(round(state['t'], 2))            # triggers on_t -> redraw
timer.add_callback(tick)

def toggle_play(_):
    state['playing'] = not state['playing']
    play_btn.label.set_text('Pause ⏸' if state['playing'] else 'Animate ▶')
    (timer.start if state['playing'] else timer.stop)()
play_btn.on_clicked(toggle_play)

# --- dragging control points -------------------------------------------------
def on_pick(event):
    if event.artist is points:
        state['drag'] = event.ind[0]

def on_motion(event):
    i = state['drag']
    if i is None or event.xdata is None: return
    P[i][0], P[i][1] = event.xdata, event.ydata
    update()

def on_release(_):
    state['drag'] = None

fig.canvas.mpl_connect('pick_event', on_pick)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

update()
plt.show()
