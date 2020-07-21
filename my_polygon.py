import turtle
import math

def polygon(t,n,length):
    angle = 360/n
    polyline(t,n,length,angle)


def circle(t,r):
    arc(t,r,360)

# def arc(t,r,angle):
#     arc_length = 2*math.pi*r*angle/360
#     n = int(arc_length/3)+1
#     step_length = arc_length/n
#     step_angle = float(angle)/n
#     polyline(t,n,length=step_length,angle=step_angle)
def arc(t, r, angle):
    """Draws an arc with the given radius and angle.
    t: Turtle
    r: radius
    angle: angle subtended by the arc, in degrees
    """
    arc_length = 2 * math.pi * r * abs(angle) / 360
    n = int(arc_length / 4) + 3
    step_length = arc_length / n
    step_angle = float(angle) / n

    # making a slight left turn before starting reduces
    # the error caused by the linear approximation of the arc
    t.lt(step_angle/2)
    polyline(t, n, step_length, step_angle)
    t.rt(step_angle/2)
    
def polyline(t,n,length,angle):
    """Draws n line segments with the given length and 
    angle (in degrees) between them. t is a tutle."""
    for i in range(n):
        t.fd(length)
        t.lt(angle)
    

bob = turtle.Turtle()
l = 50
n = 20
r = 200
angle = 360
arc(bob,r,angle)
turtle.mainloop()