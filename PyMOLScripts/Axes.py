from pymol import cmd
from chempy import cpv
 
class PutCenterCallback(object):
    prev_v = None
 
    def __init__(self, name, corner=0):
        self.name = name
        self.corner = corner
        self.cb_name = cmd.get_unused_name('_cb')
 
    def load(self):
        cmd.load_callback(self, self.cb_name)
 
    def __call__(self):
        if self.name not in cmd.get_names('objects'):
            cmd.delete(self.cb_name)
            return
 
        v = cmd.get_view()
        if v == self.prev_v:
            return
        self.prev_v = v
 
        t = v[12:15]
 
        if self.corner:
            vp = cmd.get_viewport()
            R_mc = [v[0:3], v[3:6], v[6:9]]
            off_c = [0.15 * v[11] * vp[0] / vp[1], 0.15 * v[11], 0.0]
            if self.corner in [2,3]:
                off_c[0] *= -1
            if self.corner in [3,4]:
                off_c[1] *= -1
            off_m = cpv.transform(R_mc, off_c)
            t = cpv.add(t, off_m)
 
        z = -v[11] / 30.0
        m = [z, 0, 0, t[0] / z, 0, z, 0, t[1] / z, 0, 0, z, t[2] / z, 0, 0, 0, 1]
        cmd.set_object_ttt(self.name, m, homogenous=1)
 
def axes(name='axes'):
    '''
DESCRIPTION
 
    Puts coordinate axes to the lower left corner of the viewport.
    '''
    from pymol import cgo
 
    cmd.set('auto_zoom', 0)
 
    w = 0.06 # cylinder width
    l = 0.75 # cylinder length
    h = 0.25 # cone hight
    d = w * 1.618 # cone base diameter
 
    obj = [cgo.CYLINDER, 0.0, 0.0, 0.0,   l, 0.0, 0.0, w, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
           cgo.CYLINDER, 0.0, 0.0, 0.0, 0.0,   l, 0.0, w, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
           cgo.CYLINDER, 0.0, 0.0, 0.0, 0.0, 0.0,   l, w, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
           cgo.CONE,   l, 0.0, 0.0, h+l, 0.0, 0.0, d, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
           cgo.CONE, 0.0,   l, 0.0, 0.0, h+l, 0.0, d, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
           cgo.CONE, 0.0, 0.0,   l, 0.0, 0.0, h+l, d, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0]
 
    PutCenterCallback(name, 1).load()
    cmd.load_cgo(obj, name)
 
cmd.extend('axes', axes)
