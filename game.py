import pygame as pg
import math
import time



def jeux():
    pg.init()

    pixel_per_cm = 3
    fps = 60
    m_per_s = (100 * pixel_per_cm)/fps    #pixels /cm divded by fps is cm per second
    m_per_s2 = (100 * pixel_per_cm)/(fps**2)
    w = 356.9 * pixel_per_cm
    h = 177.8 * pixel_per_cm

    screen = pg.display.set_mode((int(w), int(h)))
    clock = pg.time.Clock()
    running = True

    def dist(x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def text_objectss(text,font,color):
        textSurface = (font.render(text,True,color))
        return textSurface, textSurface.get_rect()

    def buttonn(msg, x, y, w, h, activeColor, inactiveColor,colorText, action=None):
        '''This is the basic button function template'''
        mouse = pg.mouse.get_pos()

        click = pg.mouse.get_pressed()

        # checking if mouse is on button
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pg.draw.rect(screen, activeColor, (x, y, w, h))
            if click[0] == 1 and action != None:
                action()

        else:
            pg.draw.rect(screen, inactiveColor, (x, y, w, h))

        smallText = pg.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = text_objectss(msg, smallText,colorText)
        textRect.center = (x + (w / 2), y + (h / 2))
        screen.blit(textSurf, textRect)


    def scoreboard(stripesIN, solidsIN,player):
        smallText = pg.font.Font("freesansbold.ttf", 20)

        word = f"Stripes: {stripesIN} Solids: {solidsIN}"
        textSurf, textRect = text_objectss(word, smallText,(0,0,0))
        textRect.center = ((w-350), (h-20))
        screen.blit(textSurf, textRect)

        word = f"Turn: {player}"
        textSurf, textRect = text_objectss(word, smallText,(0,0,0))
        textRect.center = ((w/4), (h-20))
        screen.blit(textSurf, textRect)





    class Hole:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y
            self.r = 3.7 * pixel_per_cm
            self.caught = [] #list of all balls in teh hole
        def catch(self, balls):
            for ball in balls: #checks if ball is in the hole, not like a collision, IT HAS TO BE 5/3rds in the hole
                if dist(self.x, self.y, ball.x, ball.y) < 5/3 * self.r:
                    ball.x = self.x #centers the ball inside the hole
                    ball.y = self.y
                    pg.mixer.music.load('Ta Da.mp3')
                    pg.mixer.music.play(0)
                    self.caught.append(ball)
                    balls.remove(ball) #removes from ball list so it doesnt check for missing ball during collisions
        def display(self):
            pg.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), int(self.r), 0)
            if len(self.caught):
                self.caught[-1].display() #displays most recent ball on hole



    class Ball:
        def __init__(self, x, y, index):
            self.x = x
            self.y = y
            self.r = 2.7 * pixel_per_cm
            self.vel = 0
            self.angle = 0
            self.index = index
            self.color = [(255, 255, 255), (255, 255, 0), (0, 0, 255),
                          (255, 0, 0), (127, 0, 127), (255, 127, 0),
                          (0, 255, 0), (255, 0, 63), (0, 0, 0),
                          (255, 255, 0), (0, 0, 255), (255, 0, 0),
                          (127, 0, 127), (255, 127, 0), (0, 255, 0),
                          (255, 0, 63)][index]
            self.accel = -1.5 * m_per_s2 #friction
            self.Cr = 0.0 #physics if zero then both balls are knocked back by same amount if 1, all momentum of one object is transfered into the other one, as cr goes up knockback goes down
        def roll(self):
            self.x += self.vel * math.cos(self.angle) #roll is moving the ball by the given velocity and direction #moving in the x
            self.y += self.vel * math.sin(self.angle) #moving in the y

            if self.vel > 0: #if the velocity is bigger than zero, then its gonna start to decelerate due to friciton
                self.vel += self.accel
            if self.vel < 0: #if velocity is less than zero then its stops the ball, so it doesnt continually go backwards
                self.vel = 0
        def check_collide(self, balls):
            if self.x + self.r > w or self.x - self.r < 0 or self.y + self.r > h or self.y - self.r < 0: #checking colliusions against walls
                self.wall_bounce()
            for ball in balls: #checking collisions for balls
                if ball != self: #not gonna check if its colliding with itself
                    if dist(self.x, self.y, ball.x, ball.y) < self.r * 2: #if theyre touching, distance between them is the sum of both their radii
                        self.collide(ball) #collinging if distance is less than contact point
        def wall_bounce(self):
            if self.x + self.r > w:
                self.x = w - self.r
                self.angle = math.pi - self.angle
            if self.x - self.r < 0:
                self.x = self.r
                self.angle = math.pi - self.angle
            if self.y + self.r > h:
                self.y = h - self.r
                self.angle = 2 * math.pi - self.angle
            if self.y - self.r < 0:
                self.y = self.r
                self.angle = 2 * math.pi - self.angle
        def collide(self, ball): #balls are bouncing back along the line connecting their origins (perpendicular bisector to tangent)
            pg.mixer.music.load('billiards+2.mp3')
            pg.mixer.music.play(1)
            rise = self.y - ball.y#finding angle connecting two balls
            run = self.x - ball.x
            try:
                slope = rise/run
                self.angle = math.atan(slope) #angle is the inverse tan of the slope artan only gives angles in quadrant 1 and 3 (CAST rule) ARCTAN DOESNT GIVE NEGATIVE NUMBERS 1 and 4 have positive runs
                if run < 0: #since run has a small chance of being zero cant divide anything by zero, so if its zero, the angle will just be 90
                    self.angle += math.pi #increasing the angle by 180 degrees if angle is in quadrant 2 or 4 where tan is negative
            except:#except happens if run is zero flipping the direction
                self.angle = math.pi/2 * abs(rise)/rise #use math.pi/2 cuz its in radians, if rise is negative multiply by -1, changing the direction of the ball setting the angle to 90 degrees

            vi = self.vel #initial velocity, since youre changing velocity but youre gonna need velocity before chaning
            self.vel = (self.Cr * (ball.vel - self.vel) + self.vel + ball.vel) / 2 #inelastic collision formulas modified for same mass
            ball.vel = (self.Cr * (vi - ball.vel) + ball.vel + vi) / 2 #velocity of other ball
                #both balls velocities are changed in this method so you dont have to go around to the other ball and change it
            #cr is the coefficient of restitution so whether its elastic or inelastic, look at wikipedia inelastic collisions for more

            ball.angle = self.angle + math.pi #adding 180 degrees to second balls angle cuz theyre going in opposite direction

            self.x -= (ball.x - self.x) / 4
            self.y -= (ball.y - self.y) / 4 #moves the balls away from eachother so program doesnt recognize them as having collided for a second time so it doesnt recalculate again just because the balls are inside eachother, makes them not touch
            ball.x += (ball.x - self.x) / 4 #to avoid collisions that arent there, because the balls would still be inside eachother because in collisions they go inside eachother
            ball.y += (ball.y - self.y) / 4
        def display(self): #drawing the balls on the screen
            if self.index <= 8: #drawing fully colored balls
                pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.r), 0)
            if self.index > 8: # drawing striped circles
                pg.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), int(self.r), 0)
                pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.r - 1 * pixel_per_cm), 0)

    class WhiteBall(Ball): #inheritence from ball adding extra methods
        def point(self, mousepos): #calculates angle to mouse curosr
            rise = mousepos[1] - self.y #first coordinate is what youre pointing towards
            run = mousepos[0] - self.x
            try: #if run is zero slope is gonna be an error
                slope = rise/run
                self.angle = math.atan(slope)
                if run < 0:
                    self.angle += math.pi
            except:
                if rise != 0:#sets angle to 90 and multiply depending on direction of rise, zero is asymptote so if run is zero it means its either straight up or straight down
                    self.angle = math.pi/2 * abs(rise)/rise
        def place(self, mousepos): #When you get whiteball in hole it sets the balls position to the mouse position
            self.x = mousepos[0]
            self.y = mousepos[1]
        def hit(self, mousepos):#when you click down, fac is distance from cursor to white ball and youre diving by a hundred
            fac = dist(self.x, self.y, mousepos[0], mousepos[1]) / (100 * pixel_per_cm) #magnitude of the hit
            self.vel = 5 * fac * m_per_s #making the velocity depend on the distance of cursor from ball
        def display(self): #display overridden
            pg.draw.line(screen, (255, 0, 0), (self.x, self.y), (30* pixel_per_cm*math.cos(self.angle) + self.x, 30* pixel_per_cm*math.sin(self.angle)+self.y), 2) #make sit so that the length of the line stays the same not go all teh way to the mouse
            pg.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), int(self.r), 0) #drawing the ball


    white_ball = WhiteBall(w/(1.3), h/2, 0)
    balls = [white_ball, Ball(w/3.5-30, h/2+15, 1), Ball(w/3.5 -66, h/2 - 13, 2), Ball(w/3.5 - 49, h/2 +4, 3), Ball(w/3.5 -66, h/2 + 12, 4),
             Ball(w/3.5 - 66, h/2 +36, 5), Ball(w/3.5 - 49, h/2 - 27, 6), Ball(w/3.5 - 10, h/2 -5, 7),
             Ball(w/3.5 - 30, h/2-3, 8), Ball(w/3.5 -1, h/2, 9), Ball(w/3.5 - 49, h/2 - 4, 10),
             Ball(w/3.5-66, h/2 - 36, 11), Ball(w/3.5 - 10, h/2 +5, 12), Ball(w/3.5 - 66, h/2 , 13),
             Ball(w/3.5 - 49, h/2 + 27, 14), Ball(w/3.5 - 30, h/2 - 12, 15)] #list of all the balls
    holes = [Hole(w - Hole().r, h-Hole().r), Hole(Hole().r, Hole().r), Hole(Hole().r, h-Hole().r), Hole(w - Hole().r, Hole().r), Hole(w/2, Hole().r), Hole(w/2, h-Hole().r)]
    #center of holes is the radius away from the edge

    turn = "p1"

    def endgame():
        end = True

        def scoreboardd(word):
            smallText = pg.font.Font("freesansbold.ttf", 50)
            textSurf, textRect = text_objectss(word, smallText,(255,255,255))
            textRect.center = ((w/2), (h//2.5))
            screen.blit(textSurf, textRect)

        while end:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            background = pg.image.load('end-bg.jpg')

            screen.blit(background,[0,-80])

            buttonn('Play again?', w/2-100, h//2+50, 200, 100, (255,153,51), (204,104,0),(255,255,255),jeux)



            if winners[0] == 7 and winners[1] != 7:
                scoreboardd("Stripes win!")
            elif winners[1] == 7 and winners[0] != 7:
                (scoreboardd('Solids win!'))
            else:
                if turn == 'p1':
                    (scoreboardd('Player 1 wins!'))
                elif turn == 'p2':
                    (scoreboardd('Player 2 wins!'))

            pg.display.update()





    while running:


        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1: #if you press left mouse button
                    in_hole = False
                    for hole in holes: #check every hole to see if the white ball is in any of the holes
                        if white_ball in hole.caught:
                            in_hole = True
                            balls.append(white_ball) #reappend to balls list and remove from hole
                            hole.caught.remove(white_ball)
                            white_ball.vel = 0
                            break
                    print(in_hole)
                    if white_ball.vel == 0 and in_hole == False:
                        white_ball.hit(pg.mouse.get_pos()) #if you click on the screen you shoul donly be able to hit the white ball if its not in a hole

                        if turn == "p1":
                            turn = "p2"
                        else:
                            turn = "p1"

        screen.fill((0, 50, 0))

        for hole in holes:
            hole.catch(balls) #chekcs if balls are in holes and catches them checks all balls for going in holes
            hole.display()

        for ball in balls:
            ball.check_collide(balls) #for every ball you check the collision to evry ball, you roll every ball and then you display it
            ball.roll()
            ball.display()

        if white_ball not in balls:
            white_ball.place(pg.mouse.get_pos()) #if white ball is not in the balls list, its caught in the hole, we take it out of the balls list and we call teh place mathod
        else:
            if white_ball.vel == 0: #you cant point while the ball is moving
                white_ball.point(pg.mouse.get_pos())

        def checker(holesF):

            solids = 0
            stripes = 0

            for j in holesF:
                for k in j.caught:
                    if k.index in [1,2,3,4,5,6,7]:
                        solids +=1
                    if k.index in [9,10,11,12,13,14,15]:
                        stripes += 1
            return (stripes, solids)


        def blackChecker(holesF): # return true if the black ball is in oine of the holees
            for j in holesF:
                for k in j.caught:
                    if k.index in [8]:
                        return True
            return False


        if blackChecker(holes):
            winners = list(checker(holes))
            break



        scoreboard(checker(holes)[0],checker(holes)[1], turn)

        if checker(holes)[0] == 7:
            time.sleep(3)
        elif checker(holes)[1] == 7:
            time.sleep(3)


        #sets specific time interval for loop
        clock.tick(fps) #update the screen by this amount
        pg.display.update()

    endgame()


jeux()


