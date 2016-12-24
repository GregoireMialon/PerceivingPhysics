###############################################################################
"""
doublependulum.py

desc: A pygame animated simulation of two tandem double pendula.

auth: Craig Wm. Versek (cversek@gmail.com) circa 2008?
"""
###############################################################################
import sys,os
from math import sin,cos,pi,atan2,sqrt
import pygame
from pygame.locals import *
import pygame.surfarray

COLOR = {'black' : (0,0,0),
         'red'   : (255,0,0),
         'green' : (0,255,0),
         'blue'  : (0,0,255)}

SCREEN_WIDTH  = 1200
SCREEN_HEIGHT = 800
SCREEN_DIM    = (SCREEN_WIDTH,SCREEN_HEIGHT)
SCREEN_CENTER = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2) 

def gen_doublependulum_physics_RK4(dt,theta1_0,theta2_0,theta1_dot0,theta2_dot0,m1,m2,l1,l2,g):
    #aggregate some constants
    M     = float(m1 + m2)
    L1L2  = float(l1*l2)
    L1sqr = float(l1*l1)
    L2sqr = float(l2*l2)
    L1M   = float(l1*M)
    L2M2  = float(l2*m2)
    GL1M  = float(g*L1M)
    GM2L2 = float(g*m2*l2)
    L2sqrM2 = float(L2sqr*m2)
    L1sqrM  = float(L1sqr*M)
    L1L2M2  = float(L1L2*m2)
    #initialize generalized coordinates
    q1        = theta1_0
    q2        = theta2_0
    p1        = L1sqrM*theta1_dot0 + L1L2M2*theta2_dot0*cos(theta1_0 - theta2_0)
    p2        = L2sqrM2*theta2_dot0 + L1L2M2*theta1_dot0*cos(theta1_0 - theta2_0)
    #the Equations of Motion
    def EOM(q1,q2,p1,p2):
        #compute common parts
        delta_q = q1 - q2
        sin_delq = sin(delta_q)
        cos_delq = cos(delta_q)
        A = L1L2*(m1 + m2*sin_delq*sin_delq)
        B = p1*p2*sin_delq/A
        C = sin(2*delta_q)*(L2sqrM2*p1*p1 + L1sqrM*p2*p2 - L1L2M2*p1*p2*cos_delq)/(2*A*A)
        #equations of motion
        q1_dot = (l2*p1 - l1*p2*cos_delq)/(l1*A)
        q2_dot = (L1M*p2 - L2M2*p1*cos_delq)/(l2*A)
        p1_dot = -GL1M*sin(q1)  - B + C
        p2_dot = -GM2L2*sin(q2) + B - C    
        return (dt*q1_dot,dt*q2_dot,dt*p1_dot,dt*p2_dot)
    #loop forever
    while True:
        #integrate using Runge-Kutta 4th order
        k1_1,k2_1,n1_1,n2_1 = EOM(q1         ,q2         ,p1         ,p2         )
        k1_2,k2_2,n1_2,n2_2 = EOM(q1+k1_1/2.0,q2+k2_1/2.0,p1+n1_1/2.0,p2+n2_1/2.0)
        k1_3,k2_3,n1_3,n2_3 = EOM(q1+k1_2/2.0,q2+k2_2/2.0,p1+n1_2/2.0,p2+n2_2/2.0)
        k1_4,k2_4,n1_4,n2_4 = EOM(q1+k1_3    ,q2+k2_3    ,p1+n1_3    ,p2+n2_3    )
        q1 += ((k1_1+k1_4)/2.0 + k1_2+k1_3)/3.0
        q2 += ((k2_1+k2_4)/2.0 + k2_2+k2_3)/3.0
        p1 += ((n1_1+n1_4)/2.0 + n1_2+n1_3)/3.0
        p2 += ((n2_1+n2_4)/2.0 + n2_2+n2_3)/3.0
        yield (q1,q2)

def gen_doublependulum_physics_Steomer_Verlet(dt,
                                              theta1_0,
                                              theta2_0,
                                              theta1_dot0,
                                              theta2_dot0,
                                              m1,m2,l1,l2,g):
    #aggregate some constants
    M     = float(m1 + m2)
    L1L2  = float(l1*l2)
    L1sqr = float(l1*l1)
    L2sqr = float(l2*l2)
    L1M   = float(l1*M)
    L2M2  = float(l2*m2)
    GL1M  = float(g*L1M)
    GM2L2 = float(g*m2*l2)
    L2sqrM2 = float(L2sqr*m2)
    L1sqrM  = float(L1sqr*M)
    L1L2M2  = float(L1L2*m2)
    #initialize generalized coordinates
    q1        = theta1_0
    q2        = theta2_0
    p1        = L1sqrM*theta1_dot0 + L1L2M2*theta2_dot0*cos(theta1_0 - theta2_0)
    p2        = L2sqrM2*theta2_dot0 + L1L2M2*theta1_dot0*cos(theta1_0 - theta2_0)
    #the Equations of Motion
    def EOM(q1,q2,p1,p2):
        #compute common parts
        delta_q = q1 - q2
        sin_delq = sin(delta_q)
        cos_delq = cos(delta_q)
        A = L1L2*(m1 + m2*sin_delq*sin_delq)
        B = p1*p2*sin_delq/A
        C = sin(2*delta_q)*(L2sqrM2*p1*p1 + L1sqrM*p2*p2 - L1L2M2*p1*p2*cos_delq)/(2*A*A)
        #equations of motion
        q1_dot = (l2*p1 - l1*p2*cos_delq)/(l1*A)
        q2_dot = (L1M*p2 - L2M2*p1*cos_delq)/(l2*A)
        p1_dot = -GL1M*sin(q1)  - B + C
        p2_dot = -GM2L2*sin(q2) + B - C
        return (dt*q1_dot,dt*q2_dot,dt*p1_dot,dt*p2_dot)
    #loop forever
    while True:
        #integrate using Runge-Kutta 4th order
        k1_1,k2_1,n1_1,n2_1 = EOM(q1         ,q2         ,p1         ,p2         )
        k1_2,k2_2,n1_2,n2_2 = EOM(q1+k1_1/2.0,q2+k2_1/2.0,p1+n1_1/2.0,p2+n2_1/2.0)
        k1_3,k2_3,n1_3,n2_3 = EOM(q1+k1_2/2.0,q2+k2_2/2.0,p1+n1_2/2.0,p2+n2_2/2.0)
        k1_4,k2_4,n1_4,n2_4 = EOM(q1+k1_3    ,q2+k2_3    ,p1+n1_3    ,p2+n2_3    )
        q1 += k1_1
        q2 += ((k2_1+k2_4)/2.0 + k2_2+k2_3)/3.0
        p1 += ((n1_1+n1_4)/2.0 + n1_2+n1_3)/3.0
        p2 += ((n2_1+n2_4)/2.0 + n2_2+n2_3)/3.0
        yield (q1,q2)


class DoublePendulum(pygame.sprite.Sprite):
    """renders a fixed pivot pendulum and updates motion according to differential equation"""
    def __init__(self,pivot_vect=SCREEN_CENTER,
                      length1=200,length2=100,
                      bob_radius1=20,bob_radius2=10,
                      bob_mass1=1,  bob_mass2=0.5,
                      init_angle1=pi/4,init_angularspeed1=0,
                      init_angle2=pi/4,init_angularspeed2=0,
                      gravity=9.8,dt=0.01):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.phys_gen = gen_doublependulum_physics_Steomer_Verlet(dt,
                                                                  init_angle1,
                                                                  init_angle2,
                                                                  init_angularspeed1,
                                                                  init_angularspeed2,
                                                                  bob_mass1,bob_mass2,
                                                                  length1/1000.0,length2/1000.0,
                                                                  gravity)
        self.length     = (length1    ,length2    )
        self.bob_radius = (bob_radius1,bob_radius2)
        self.bob_mass   = (bob_mass1  ,bob_mass2  )
        self.angle      = (init_angle1,init_angle2)
        #positioning attributes
        self.pivot_vect = pivot_vect                     #vector from topleft to pivot of pendulum
        swinglen = length1 + length2 + bob_radius2       #whole swing arc
        #these next two attributes are used by the RenderPlain container class
        self.image  = pygame.Surface((swinglen*2,swinglen*2)).convert()          #create surface just big enough to fit swing
        self.image.set_colorkey(COLOR['black'])
        self.rect   = self.image.get_rect()
        self.rect.topleft = (pivot_vect[0] - swinglen, pivot_vect[1] - swinglen) #place so that pivot is at center
        self.image_center = (self.rect.width//2,self.rect.height//2)
        #calculate the initial relative bob position in the image
        self.bob1_X    = int(length1*sin(init_angle1)+self.rect.width//2)
        self.bob1_Y    = int(length1*cos(init_angle1)+self.rect.height//2)
        self.bob2_X    = int(length2*sin(init_angle2)+self.bob1_X)
        self.bob2_Y    = int(length2*cos(init_angle2)+self.bob1_Y)
        #render the pendulum from the parameters
        self._render()
        
    def _render(self):
        #clear the pendulum surface
        self.image.fill(COLOR['black'])
        bob1_pos = (self.bob1_X,self.bob1_Y)
        bob2_pos = (self.bob2_X,self.bob2_Y)
        bob_radius1, bob_radius2 = self.bob_radius
        #draw the tethers
        pygame.draw.aaline(self.image,COLOR['red'],self.image_center,bob1_pos,True)
        pygame.draw.aaline(self.image,COLOR['red'],bob1_pos         ,bob2_pos,True)
        #draw the bob2
        pygame.draw.circle(self.image,COLOR['blue'] ,bob1_pos,bob_radius1,0)
        pygame.draw.circle(self.image,COLOR['green'],bob2_pos,bob_radius2,0)
        
    def update(self):
        #coords relative to pivot
        self.angle = self.phys_gen.next()
        angle1 ,angle2  = self.angle
        length1,length2 = self.length
        self.bob1_X = int(length1*sin(angle1)) + self.rect.width//2
        self.bob1_Y = int(length1*cos(angle1)) + self.rect.height//2
        self.bob2_X = int(length2*sin(angle2)  + self.bob1_X)
        self.bob2_Y = int(length2*cos(angle2)  + self.bob1_Y)
        self._render()


def main():
    """this function is called when the program starts.
    it initializes everything it needs, then runs in
    a loop until a stop event (escape or window closing) is recognized.
    """
    #Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption('Double Pendulum Simulation')
    #pygame.mouse.set_visible(0)

    #Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(COLOR['black'])
    #Prepare Objects
    clock = pygame.time.Clock()
    p1 = DoublePendulum(pivot_vect=(  SCREEN_WIDTH//4,SCREEN_HEIGHT//2),
                        init_angle1=pi,init_angle2=pi+0.001,dt=0.01,
                        #bob_mass1=0.5,bob_radius1=10,
                        #bob_mass2=0.5,bob_radius2=1
                       )
    p2 = DoublePendulum(pivot_vect=(3*SCREEN_WIDTH//4,SCREEN_HEIGHT//2),
                        init_angle1=pi,init_angle2=pi+0.002,dt=0.01)
    free_group = pygame.sprite.RenderPlain((p1,p2))
    #Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #Main Loop
    while True:
        clock.tick(30)
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                return
        free_group.update()
        #send the mouse position to the held bobs so we can move them
        screen.blit(background,(0,0))
        free_group.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()