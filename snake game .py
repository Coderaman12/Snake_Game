import pygame
import math
import os 
import sys
import random


pygame.init()
pygame.display.set_caption("Snake Game")
pygame.font.init()
random.seed()

# declare global constant 

speed=0.36
snake_size=9
apple_size=snake_size      
separation=10
screen_width=800
screen_height=600
fps=25
key={"UP":1,"DOWN":2,"LEFT":3,"RIGHT":4}

# INITILIZING screen 
screen=pygame.display.set_mode((screen_width,screen_height),pygame.HWSURFACE)
# we have to use hwsurface for hardware surface to using memory on video card for storing draws as opposed to main memory

# resources 
score_font=pygame.font.Font(None,38)
score_numb_font=pygame.font.Font(None,28)
game_over_font=pygame.font.Font(None,46)
play_again_font=score_numb_font
score_msg=score_font.render("score : ",1,pygame.Color("green"))
score_msg_size=score_font.size('Score')
background_color=pygame.Color(0,0,0)  # for black color
black=pygame.Color(0,0,0)

# for clock at the left corner 
gameclock=pygame.time.Clock()

def checkCollision(posA,As,posB,Bs): # As is the size of a and Bs is the size of b
   if(posA.x<posB.x+Bs and posA.x+As>posB.x and posA.y<posB.y+Bs and posA.y+As > posB.y):
      return True
   return False

# to check the boundries here we are not limiting the boundries like it can pass thourgh screen and come from the other side

def checkLimits(snake):
   if snake.x > screen_width:
      snake.x=snake_size
   if snake.x < 0:       # this will check the snake some part is on other side and some is on other opposite side
      snake.x = screen_width-snake_size
   if snake.y > screen_height:
      snake.y=snake_size
   if snake.y < 0:    # this will do same as half half
      snake.y = screen_height-snake_size
    
    
# we will make class for food of the snake named as apple

class Apple:
   def __init__(self,x,y,state):
      self.x=x
      self.y=y
      self.state=state
      self.color=pygame.color.Color("orange") # color of the food
   
   def draw(self,screen):
      pygame.draw.rect(screen,self.color,(self.x,self.y,apple_size,apple_size),0)

class segment:
   # initially snake is move up direction
   def __init__(self,x,y):
      self.x=x
      self.y=y
      self.direction=key["UP"]
      self.color="white"
      
class Snake:
   def __init__(self,x,y):
      self.x=x
      self.y=y
      self.direction=key["UP"]
      self.stack=[]  # initially it will be empty
      self.stack.append(self)
      blackBox=segment(self.x,self.y+separation)
      blackBox.direction=key["UP"]
      blackBox.color="NULL"
      self.stack.append(blackBox)
      
   # we will define move of the snake 
   
   def move(self):
      last_element=len(self.stack)-1
      while(last_element != 0):
         self.stack[last_element].direction = self.stack[last_element-1].direction
         self.stack[last_element].x = self.stack[last_element-1].x
         self.stack[last_element].y = self.stack[last_element-1].y      
         last_element-=1
      if len(self.stack) < 2 :
         last_segment =self
      else:
         last_segment=self.stack.pop(last_element)
      last_segment.direction=self.stack[0].direction
      if(self.stack[0].direction == key["UP"]):
         last_segment.y = self.stack[0].y - (speed*fps)
      elif(self.stack[0].direction == key["DOWN"]):
         last_segment.y = self.stack[0].y + (speed*fps)
      elif(self.stack[0].direction == key["LEFT"]):
         last_segment.x = self.stack[0].x - (speed*fps)
      elif(self.stack[0].direction == key["RIGHT"]):
         last_segment.x = self.stack[0].x + (speed*fps)
      self.stack.insert(0,last_segment)
      
   def getHead(self):
      return (self.stack[0])
   
   # now snake increase when it take the food
   def grow(self):
      last_element=len(self.stack)-1
      self.stack[last_element].direction = self.stack[last_element].direction
      if(self.stack[last_element].direction == key["UP"]):
         newSegment = segment(self.stack[last_element].x,self.stack[last_element].y - snake_size)
         blackBox = segment(newSegment.x , newSegment.y-separation)
         
      elif(self.stack[last_element].direction == key["DOWN"]):
         newSegment = segment(self.stack[last_element].x,self.stack[last_element].y + snake_size)
         blackBox = segment(newSegment.x , newSegment.y+separation)
         
      elif(self.stack[last_element].direction == key["LEFT"]):
         newSegment = segment(self.stack[last_element].x - snake_size,self.stack[last_element].y)
         blackBox = segment(newSegment.x-separation , newSegment.y)
         
      elif(self.stack[last_element].direction == key["RIGHT"]):
         newSegment = segment(self.stack[last_element].x + snake_size,self.stack[last_element].y)
         blackBox = segment(newSegment.x+separation , newSegment.y)
      blackBox.color = "NULL"
      self.stack.append(newSegment)
      self.stack.append(blackBox)
      
   def iterateSegment(self,delta):
      pass
   
   def setDirection(self,direction):
      if(self.direction == key["RIGHT"] and direction == key["LEFT"] or self.direction == key["LEFT"] and direction == key["RIGHT"]):
         pass
      elif(self.direction == key["RIGHT"] and direction == key["LEFT"] or self.direction == key["LEFT"] and direction == key["RIGHT"]):
         pass
      else:
         self.direction = direction
   def get_rect(self):  # to get the rectangle shape
      rect = (self.x,self.y)
      return rect
   
   def getX(self):
      return self.x
   
   def getY(self):
      return self.y
   
   def setX(self,x):
      self.x=x
   def setY(self,y):
      self.y=y
   
   # we will make the function of crashing when snake eats itself
   
   def checkCrashing(self):
      counter=1
      while (counter < len(self.stack)-1):
         if (checkCollision(self.stack[0],snake_size,self.stack[counter],snake_size) and self.stack[counter].color != 'Null'):
            return True
         counter+=1
      return False
   
   # we will draw the snake
   def draw(self,screen):
      pygame.draw.rect(screen,pygame.color.Color("green"),(self.stack[0].x,self.stack[0].y,snake_size,snake_size),0)
      counter=1
      while(counter < len(self.stack)):
         if(self.stack[counter].color == "NULL"):
            counter+=1
            continue
         pygame.draw.rect(screen,pygame.color.Color("yellow"),(self.stack[counter].x,self.stack[counter].y,snake_size,snake_size),0)
         counter+=1


# we will define keys

def getKey():
   for event in pygame.event.get():
      if event.type==pygame.KEYDOWN:
         if event.key == pygame.K_UP:
            return key["UP"]
         elif event.key == pygame.K_DOWN:
            return key["DOWN"]
         elif event.key == pygame.K_LEFT:
            return key["LEFT"]
         elif event.key == pygame.K_RIGHT:
            return key["RIGHT"]
         # for exit
         elif event.key == pygame.K_ESCAPE:
            return "exit"
         # for continue playing
         elif event.key == pygame.K_y:
            return "yes"
         # if we dont want to play game
         if event.key == pygame.K_n:
            return "no"
      if event.type == pygame.QUIT:
         sys.exit(0)
         
         
def endGame():
   message=game_over_font.render("Game Over",1,pygame.Color("white"))
   message_play_again =play_again_font.render("Play Again ?(Y/N)",1,pygame.Color("green"))
   screen.blit(message,(320,240))
   screen.blit(message_play_again(320+12,240+40))

   pygame.display.flip()
   pygame.display.update()
   
   mkey=getKey()
   while(mkey != "exit"):
      if(mkey == "yes"):
         main()
      elif(mkey == "no"):
         break
      mkey=getKey()
      gameclock.tick(fps)
   sys.exit(0)

def drawScore(score):
   score_numb=score_numb_font.render(str(score),1,pygame.Color("red"))
   screen.blit(score_msg,(screen_width-score_msg_size[0]-60,10))
   screen.blit(score_numb,(screen_width-45,14))

def drawGameTime(gameTime):
   game_time=score_font.render("Time : ",1,pygame.Color("white"))
   game_time_numb=score_numb_font.render(str(gameTime/1000),1,pygame.Color("white"))
   screen.blit(game_time,(30,10))
   screen.blit(game_time_numb,(105,14))
   
def exitScreen():
   pass
   
def respawnApple(apples,index,sx,sy):
   radius = math.sqrt(screen_width/2*screen_width/2 + screen_height/2*screen_height/2)/2
   angle=999
   while(angle > radius):
      angle=random.uniform(0,800)*math.pi*2
      x=screen_width/2 + radius * math.cos(angle)
      y=screen_height/2 + radius * math.sin(angle)
      if (x==sx and y==sy):
         continue
   newApple = Apple(x,y,1)
   apples[index]=newApple
   
def respawnApples(apples,quantity,sx,sy):
   counter=0
   del apples[:]
   radius=math.sqrt((screen_width/2*screen_width/2 + screen_height/2*screen_height/2))/2
   angle=999
   while(counter < quantity):
      while(angle > radius):
         angle = random.uniform(0,800)*math.pi*2
         x=screen_width/2 + radius * math.cos(angle)
         y=screen_height/2 + radius * math.sin(angle)
         if (x-apple_size == sx or x+apple_size == sx) and (y-apple_size==sy or y+apple_size==sy) or radius-angle <10:
            continue
      apples.append(Apple(x,y,1))
      angle=999
      counter+=1
   
   
def main():
   score =0
   
   
   # initialization of snake 
   
   mySnake =Snake(screen_width/2,screen_height/2)
   mySnake.setDirection(key["UP"])
   mySnake.move()
   start_segment = 3
   while(start_segment > 0):
      mySnake.grow()
      mySnake.move()
      start_segment-=1
   
   # food
   max_apples=1
   eaten_apple = False
   apples = [Apple(random.randint(60,screen_width),random.randint(60,screen_height),1)]
   respawnApples(apples,max_apples,mySnake.x,mySnake.y)
   
   startTime = pygame.time.get_ticks()
   endGame=0
   
   while(endGame !=1):
      gameclock.tick(fps)
      
      # input
      keypress=getKey()
      if keypress == "exit":
         endGame = 1
         
      # to check collision 
      
      checkLimits(mySnake)
      if mySnake.checkCrashing() == True:
         endGame()
         
      for myApple in apples:
         if (myApple.state == 1):
            if checkCollision(mySnake.getHead(),snake_size,myApple,apple_size) == True:
               mySnake.grow()
               myApple.state=0
               score+=10
               eaten_apple=True
      
      # update position
      if (keypress):
         mySnake.setDirection(keypress)
      mySnake.move()
      
      # respawning food
      if (eaten_apple == True):
         eaten_apple = False
         respawnApple(apples,0,mySnake.getHead().x , mySnake.getHead().y)
         
      # drawing 
      screen.fill(background_color)
      for myApple in apples:
         if myApple.state == 1:
            myApple.draw(screen)
      
      mySnake.draw(screen)
      drawScore(score)
      gameTime=pygame.time.get_ticks()-startTime
      drawGameTime(gameTime)
           
      pygame.display.flip()
      pygame.display.update()
            
main()
            