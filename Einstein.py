GlowScript 2.7 VPython

pixel = 8

G = 6.67384 * 10 ** (19) * (1/149597870) ** 3
ms = 1.9891
rs = 6.955 * 10 ** 5
c = 299792458 * 1/149597870

class Planet:
    def __init__(self, mass, rad, pose):
        self.mass = mass
        self.planet = sphere(pos = pose, radius = rad) 
        
    def field(self, x, y):
        if (x - self.planet.pos.x) ** 2 + (y - self.planet.pos.z) ** 2 >= self.planet.radius ** 2:
            return -G * self.mass / ((x - self.planet.pos.x) ** 2 + (y - self.planet.pos.z) ** 2)
        return -G * self.mass / self.planet.radius ** 2

class plot3D:
    def __init__(self, f, xmin, xmax, ymin, ymax, zmin, zmax):
        self.f = f
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
        
        self.vertices = []
        cookie = []
        for y in range(ymin * pixel, ymax * pixel + 1):
            for x in range(xmin * pixel, xmax * pixel + 1):
                val = self.f(float(x) / pixel, float(y) / pixel)
                cookie.append(self.make_vertex(x / pixel, y / pixel, min(zmax, max(val, zmin))))
            self.vertices.append(cookie)
            cookie = []
        self.make_quads()
        self.make_normals()
    
    def make_quads(self):
        for x in range(self.xmin * pixel, self.xmax * pixel):
            for y in range(self.ymin  * pixel, self.ymax  * pixel):
                v0 = self.get_vertex(x / pixel, y / pixel)
                v1 = self.get_vertex((x + 1) / pixel, y / pixel)
                v2 = self.get_vertex((x + 1) / pixel, (y + 1) / pixel)
                v3 = self.get_vertex(x / pixel, (y + 1) / pixel)
                quad(vs=[v0, v1, v2, v3])
                
    def make_normals(self):
        for x in range(self.xmin * pixel, self.xmax * pixel):
            for y in range(self.ymin  * pixel, self.ymax  * pixel):
                v = self.get_vertex(x / pixel, y / pixel)
                a = self.get_vertex(x / pixel, (y + 1) / pixel).pos - v.pos
                b = self.get_vertex((x + 1) / pixel, y / pixel).pos - v.pos
                v.normal = cross(a,b)
        
    def replot(self):
        for x in range(self.xmin * pixel, self.xmax * pixel + 1):
            for y in range(self.ymin * pixel, self.ymax * pixel + 1):
                v = self.get_vertex(x / pixel, y / pixel)
                v.pos.y = min(self.zmax, max(self.f(x / pixel, y / pixel), self.zmin))
        self.make_normals()
                
    def make_vertex(self,x,y,value):
        return vertex(pos=vec(y,value,x), color=color.white)
        
    def get_vertex(self,x,y):
        return self.vertices[round((x - self.xmin) * pixel)][round((y - self.ymin) * pixel)]
        
    def get_pos(self,x,y):
        return self.get_vertex(x,y).pos

t = 0
dt = 0.001

sun = Planet(ms * 480000, rs * 1/149597870, vector(0, 0, 0))

def f(x, y):
    return sun.field(x, y)
    
def ag(x, y):
    return sun.field(x, y) * norm(vector(x, 0, y) - sun.planet.pos)

p = plot3D(f, -15, 15, -15, 15, -20, 4)

photon = sphere(pos=vector(-15, 0, -10), radius=0.0001, make_trail=True)
photon.vel =vector(1, 0, 0) * c

run = True
def running(ev):
    global run
    run = not run

scene.bind('mousedown', running)

while True:
    rate(10)
    if run:
        if mag(vector(photon.pos.x, 0, photon.pos.z) - sun.planet.pos) > sun.planet.radius:
            if mag(vector(photon.pos.x, 0, photon.pos.z) - sun.planet.pos) < 20:
                photon.pos = photon.pos + photon.vel
                photon.vel = photon.vel + ag(photon.pos.x, photon.pos.z)
                photon.pos.y = f(photon.pos.x, photon.pos.z)
        p.replot()
        t += dt
