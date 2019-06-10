GlowScript 2.7 VPython
scene.width = scene.height = 600

L = 50
G = 6.67384 * 10**(-11) 
scene.center = vec(0.05*L,0.2*L,0)
scene.range = 1.3*L

class plot3D:
    def __init__(self, f, xmin, xmax, ymin, ymax, zmin, zmax):
        # The x axis is labeled y, the z axis is labeled x, and the y axis is labeled z.
        # This is done to mimic fairly standard practive for plotting
        #     the z value of a function of x and y.
        self.f = f
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
        
        R = L/100
    
        self.vertices = []
        for x in range(L):
            for y in range(L):
                val = self.evaluate(x,y)
                self.vertices.append(self.make_vertex( x, y, val ))
        
        self.make_quads()
        self.make_normals()
        
    def evaluate(self, x, y):
        d = L-2
        return (d/(self.zmax-self.zmin)) * (self.f(self.xmin+x*(self.xmax-self.xmin)/d, self.ymin+y*(self.ymax-self.ymin)/d)-self.zmin)
    
    def make_quads(self):
        # Create the quad objects, based on the vertex objects already created.
        for x in range(L-2):
            for y in range(L-2):
                v0 = self.get_vertex(x,y)
                v1 = self.get_vertex(x+1,y)
                v2 = self.get_vertex(x+1, y+1)
                v3 = self.get_vertex(x, y+1)
                quad(vs=[v0, v1, v2, v3])
        
    def make_normals(self):
        # Set the normal for each vertex to be perpendicular to the lower left corner of the quad.
        # The vectors a and b point to the right and up around a vertex in the xy plance.
        for i in range(L*L):
            x = int(i/L)
            y = i % L
            if x == L-1 or y == L-1: continue
            v = self.vertices[i]
            a = self.vertices[i+L].pos - v.pos
            b = self.vertices[i+1].pos - v.pos
            v.normal = cross(a,b)
    
    def replot(self):
        for i in range(L*L):
            x = int(i/L)
            y = i % L
            v = self.vertices[i]
            v.pos.y = self.evaluate(x,y)
        self.make_normals()
                
    def make_vertex(self,x,y,value):
        return vertex(pos=vec(y,value,x), color=color.cyan, normal=vec(0,1,0))
        
    def get_vertex(self,x,y):
        return self.vertices[x*L+y]
        
    def get_pos(self,x,y):
        return self.get_vertex(x,y).pos

t = 0
dt = 0.02
def f(x, y):
    # Return the value of the function of x and y:
    return -0.1 / ((x + cos(t))**2 + (y + sin(t))**2) + 1

p = plot3D(f, -1, 1, -1, 1, -1, 1) # function, xmin, xmax, ymin, ymax (defaults 0, 1, 0, 1, 0, 1)

run = True
def running(ev):
    global run
    run = not run

scene.bind('mousedown', running)
scene.forward = vec(-0.7,-0.5,-1)

while True:
    rate(30)
    if run:
        p.replot()
        t += dt