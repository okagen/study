# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 19:29:07 2019

@author: 10007434
"""

### conda install -c cogsci pygame

import pygame
from pygame.locals import MOUSEBUTTONDOWN, QUIT

import sys
import random

class Agent:
    def __init__(self, x, y, vx, vy):
        self.x, self.y = x, y # position 
        self.vx, self.vy = vx, vy # velocity
        
    def update(self, WINDOW_W, WINDOW_H):
        self.x += self.vx
        self.y += self.vy
        
        #Right edge.
        if self.x > WINDOW_W:
            self.vx, self.x = -self.vx, WINDOW_W
            return
        
        #Left edge.
        if self.x < 0:
            self.vx, self.x = -self.vx, 0
            return
        
        #Upper edge.
        if self.y > WINDOW_H:
            self.vy, self.y = -self.vy, WINDOW_H
            return
        #Lower edge.
        
        if self.y < 0:
            self.vy, self.y = -self.vy, 0
            return

    def draw(self, screen):
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, (255,0,0),(x,y),5)

#main
WINDOW_W, WINDOW_H = 1000, 700
pygame.init()
#Create window.
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)
agent_list = []

while True:
    clock.tick(60)
    
    # Fill screen with white.
    screen.fill((255, 255, 255))
    
    # Process each agent.
    for a in agent_list:
        a.update(WINDOW_W, WINDOW_H)
        a.draw(screen)
    
    # Show the number of the agent.
    sl = "agents : " + str(len(agent_list))
    text = font.render(sl, True, (0,0,0))
    screen.blit(text, (1, 1))

    # Process events.
    for e in pygame.event.get():
        # When clicked the left button on mouse.
        if e.type == MOUSEBUTTONDOWN and e.button==1:
            # Set velocity by use a random number.
            vx = random.uniform(-1.5,1.5)
            vy = random.uniform(-1.5,1.5)
            # create agents.
            a = Agent(e.pos[0], e.pos[1], vx, vy)
            # Add created agent into the agent list.
            agent_list.append(a)
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        
    pygame.display.update()
    
        

        




