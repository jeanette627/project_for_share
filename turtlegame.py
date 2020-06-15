from turtle import *
import tkinter.messagebox
import tkinter
import random
import math
import datetime

screenMinX = -500
screenMinY = -500
screenMaxX = 500
screenMaxY = 500

class LaserBeam(RawTurtle): # Task4
    def __init__(self,canvas,x,y,direction,dx,dy):
        super().__init__(canvas)
        self.penup()
        self.goto(x,y)
        self.setheading(direction)
        self.color("Green")
        self.__lifespan = 200
        self.__dx = math.cos(math.radians(direction))*2+dx #this is Task 4A
        self.__dy = math.sin(math.radians(direction))*2+dy  #this is Task 4A
        self.shape("laser")

    def getdx(self):
        return self.__dx

    def getdy(self):
        return self.__dy

    def getlifespan(self):
        return self.__lifespan

    def getRadius(self):
        return 4

    def move(self):
        x = self.xcor()
        y = self.ycor()

        x = (self.__dx + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.__dy + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)

        self.__lifespan-=1


class Ghost(RawTurtle): # all attributes has been set as private and create appropriate accessor and mutator
    def __init__(self,canvasobj,dx,dy,x,y,size):
        RawTurtle.__init__(self,canvasobj)
        self.penup()
        self.goto(x,y)
        self.__dx = dx
        self.__dy = dy
        self.__size = size
        if self.__size==3:
            self.shape("blueghost.gif")
        elif self.__size==2:
            self.shape("pinkghost.gif")
    def getdx(self):
        return self.__dx

    def getdy(self):
        return self.__dy

    def setnewdx(self,newdx):
        self.__dx=newdx

    def setnewdy(self,newdy):
        self.__dy=newdy

    def getsize(self): # used in my way to do Task10
        return self.__size



    #Moves the ghost from its current position to a new position
    def move(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.__dx + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.__dy + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)

    #returns the apprximate "radius" of the Ghost object
    def getRadius(self):
        return self.__size * 10 - 5

class FlyingTurtle(RawTurtle): # all attributes has been set as private and create appropriate accessor and mutator
    def __init__(self,canvasobj,dx,dy,x,y, size):
        RawTurtle.__init__(self,canvasobj)
        self.penup()
        self.color("purple")
        self.goto(x,y)
        self.__dx = dx
        self.__dy = dy
        self.__size = size
        self.shape("turtle")

    def getdx(self):
        return self.__dx

    def getdy(self):
        return self.__dy

    def setnewdx(self,newdx):
        self.dx=newdx

    def setnewdy(self,newdy):
        self.dy=newdy

    def move(self):
        screen = self.getscreen()
        x = self.xcor()
        y = self.ycor()

        x = (self.__dx + x - screenMinX) % (screenMaxX - screenMinX) + screenMinX
        y = (self.__dy + y - screenMinY) % (screenMaxY - screenMinY) + screenMinY

        self.goto(x,y)

    def turboBoost(self):
        angle = self.heading()
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))

        self.__dx = self.__dx + x
        self.__dy = self.__dy + y

    def stopTurtle(self):
        angle = self.heading()
        self.__dx = 0
        self.__dy = 0

    def getRadius(self):
        return 2

def intersect(obj1,obj2): #this is Task 5A
    r1= obj1.getRadius()
    r2= obj2.getRadius()
    distance = math.sqrt((obj2.xcor() - obj1.xcor()) ** 2 + (obj2.ycor() - obj1.ycor()) ** 2)
    if distance <= r1+r2:
        return True
    else:
        return False

def main():
    # Start by creating a RawTurtle object for the window.
    firstwindow = tkinter.Tk()
    firstwindow.title("Turtle Saves the World!")
    canvas = ScrolledCanvas(firstwindow,600,600,600,600)
    canvas.pack(side = tkinter.LEFT)
    t = RawTurtle(canvas)

    screen = t.getscreen()
    screen.setworldcoordinates(screenMinX,screenMinY,screenMaxX,screenMaxY)
    screen.register_shape("blueghost.gif")
    screen.register_shape("pinkghost.gif")
    screen.register_shape("laser",((-2,-4),(-2,4),(2,4),(2,-4)))
    frame = tkinter.Frame(firstwindow)
    frame.pack(side = tkinter.RIGHT,fill=tkinter.BOTH)
    scoreVal = tkinter.StringVar()
    scoreVal.set("0")
    scoreTitle = tkinter.Label(frame,text="Score")
    scoreTitle.pack()
    scoreFrame = tkinter.Frame(frame,height=2,bd=1,relief=tkinter.SUNKEN)
    scoreFrame.pack()
    score = tkinter.Label(scoreFrame,height=2,width=20,textvariable=scoreVal,fg="Yellow",bg="black")
    score.pack()
    livesTitle = tkinter.Label(frame, text="Extra Lives Remaining")
    livesTitle.pack()
    livesFrame = tkinter.Frame(frame,height=30,width=60,relief=tkinter.SUNKEN)
    livesFrame.pack()
    livesCanvas = ScrolledCanvas(livesFrame,150,40,150,40)
    livesCanvas.pack()
    livesTurtle = RawTurtle(livesCanvas)
    livesTurtle.ht()
    livesScreen = livesTurtle.getscreen()
    life1 = FlyingTurtle(livesCanvas,0,0,-35,0,0)
    life2 = FlyingTurtle(livesCanvas,0,0,0,0,0)
    life3 = FlyingTurtle(livesCanvas,0,0,35,0,0)
    lives = [life1, life2, life3]
    t.ht()

    screen.tracer(10)

    #Tiny Turtle!
    flyingturtle= FlyingTurtle(canvas,0,0,(screenMaxX-screenMinX)/2+screenMinX,(screenMaxY-screenMinY)/2 + screenMinY,3)


    #A list to keep track of all the ghosts
    #all list needed for track
    ghosts = []
    active_laser=[]
    dead_lasers=[]
    been_hit_ghost=[]

    #Create some ghosts and randomly place them around the screen
    for numofghosts in range(6):
        dx = random.random()*6  - 4
        dy = random.random()*6  - 4
        x = random.random() * (screenMaxX - screenMinX) + screenMinX
        y = random.random() * (screenMaxY - screenMinY) + screenMinY

        ghost = Ghost(canvas,dx,dy,x,y,3)

        ghosts.append(ghost)



    def play():
        #start counting time for the play function
        ##LEAVE THIS AT BEGINNING OF play()
        start = datetime.datetime.now()
        if len(ghosts)==0:
            tkinter.messagebox.showinfo("You Win!!", "You saved theworld!")
            return
        # Move the turtle
        flyingturtle.move()


        #Move the ghosts
        for each_ghost in ghosts:
            each_ghost.move()
            if intersect(flyingturtle,each_ghost):
                new_Tiny=lives.pop()
                new_Tiny.ht()
                if len(lives)>=1:
                    #if each_ghost not in been_hit_ghost:
                    tkinter.messagebox.showwarning( "Uh-Oh","You Lost a Life!")
                    been_hit_ghost.append(each_ghost)
                    ghosts.remove(each_ghost)
                    each_ghost.ht()
                    if each_ghost.getsize()==3:
                        int_score=int(scoreVal.get())+20
                        for pink_num in range(2):
                            dx = random.random()*6  - 4
                            dy = random.random()*6  - 4
                            pink_ghost=Ghost(canvas,dx,dy,each_ghost.xcor()+30,each_ghost.ycor()+30,2)
                            ghosts.append(pink_ghost)
                    else:
                        int_score=int(scoreVal.get())+30
                    scoreVal.set(str(int_score))
                else:
                    tkinter.messagebox.showinfo("You lose!!", "you lost all lives!")
                    return

            for each_laser in active_laser:
                if each_laser.getlifespan()==0:
                    active_laser.remove(each_laser)
                    dead_lasers.append(each_laser)
                    each_laser.goto(-screenMinX*2, -screenMinY*2)
                else:
                    each_laser.move()

                if intersect(each_ghost,each_laser):
                    if each_ghost not in been_hit_ghost:
                        ghosts.remove(each_ghost)
                    else:
                        been_hit_ghost.append(each_ghost)
                        ghosts.remove(each_ghost)

                    each_ghost.ht()
                    each_laser.ht()
                    active_laser.remove(each_laser)
                    dead_lasers.append(each_laser)
                    if each_ghost.getsize()==3:
                        int_score=int(scoreVal.get())+20
                        for pink_num in range(2):
                            dx = random.random()*6  - 4
                            dy = random.random()*6  - 4
                            pink_ghost=Ghost(canvas,dx,dy,each_ghost.xcor()+30,each_ghost.ycor()+30,2)
                            ghosts.append(pink_ghost)
                    else:
                        int_score=int(scoreVal.get())+30
                    scoreVal.set(str(int_score))
                    #

        #stop counting time for the play function
        ##LEAVE THIS AT END OF ALL CODE IN play()
        end = datetime.datetime.now()
        duration = end - start

        millis = duration.microseconds / 1000.0

        # Set the timer to go off again
        screen.ontimer(play,int(10-millis))


    # Set the timer to go off the first time in 5 milliseconds
    screen.ontimer(play, 5)

    #Turn turtle 7 degrees to the left
    def turnLeft():
        flyingturtle.setheading(flyingturtle.heading()+7)

    def turnRight():#this is Task 3
        flyingturtle.setheading(flyingturtle.heading()-7)

    #turboBoost turtle
    def forward():
        flyingturtle.turboBoost()

    #stop Turtle
    def stop():
        flyingturtle.stopTurtle()

    #shoot lasers
    def fireLaser():# use flyingturtle's dx,dy and x,y to initialize the laser
        l_dx=flyingturtle.getdx()
        l_dy=flyingturtle.getdy()
        l_x=flyingturtle.xcor()
        l_y=flyingturtle.ycor()
        laserbeam = LaserBeam(canvas,l_x,l_y,flyingturtle.heading(),l_dx,l_dy)
        active_laser.append(laserbeam)

    #Call functions above when pressing relevant keys
    screen.onkeypress(turnLeft,"Left")
    screen.onkeypress(turnRight,"Right")
    screen.onkeypress(forward,"Up")
    screen.onkeypress(stop, "Down")
    screen.onkeypress(fireLaser, "space")

    screen.listen()
    tkinter.mainloop()

if __name__ == "__main__":
    main()
