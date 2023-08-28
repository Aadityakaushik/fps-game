import pygame as pg
from setting import *
import os
from collections import deque

class sprite:
    def __init__(self,game,path='resources/sprites/static_sprites/candlebra.png',pos=(10.5,3.5),scale=0.7,shift=0.27):
        self.game=game
        self.player=game.player
        self.x,self.y=pos
        self.image=pg.image.load(path).convert_alpha()
        self.IMG_WIDTH=self.image.get_width()
        self.IMG_HALF_WIDTH=self.image.get_width() // 2
        self.IMG_RATIO = self.IMG_WIDTH/self.image.get_height()
        self.dx,self.dy,self.theta,self.screen_x,self.dist,self.norm_dist=0,0,0,0,1,1
        self.sprite_half_width=0
        self.SPRITE_SCALE=scale
        self.SPRITE_SHIFT=shift

    def get_sprite_proj(self):
        proj = SCREEN_DIST/self.norm_dist * self.SPRITE_SCALE
        proj_width,proj_height = proj*self.IMG_RATIO,proj

        image=pg.transform.scale(self.image,(proj_width,proj_height))
        self.sprite_half_width = proj_width//2
        height_shift = self.SPRITE_SHIFT * proj_height
        pos = self.screen_x-self.sprite_half_width,HALF_HEIGHT-proj_height//2+height_shift

        self.game.ray.object_to_render.append((self.norm_dist,image,pos))


    def get_sprite(self):
        dx=self.x-self.player.x
        dy=self.y-self.player.y
        self.dx,self.dy = dx,dy
        self.theta = math.atan2(dy,dx)

        delta = self.theta - self.player.angle

        if(dx>0 and self.player.angle>math.pi ) or (dx < 0 and dy < 0):
            delta+=math.tau

        delta_rays = delta/DELTA_ANGLE

        self.screen_x = (HALF_NUM_RAYS+delta_rays)*SCALE
        self.dist=math.hypot(dx,dy)
        self.norm_dist = self.dist*math.cos(delta)

        if -self.IMG_HALF_WIDTH<self.screen_x<(WIDTH+self.IMG_HALF_WIDTH) and self.norm_dist>0.5:
            self.get_sprite_proj()

            
    def update(self):
        self.get_sprite()


class animatedsprite(sprite):
    def __init__(self, game, path='resources/sprites/animated_sprite/villian/1.png', 
                 pos=(11.5, 7.5), scale=0.8,shift=0.16,animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/',1)[0]
        self.images=self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger=False

    
    def update(self): 
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self,images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image=images[0]

    def check_animation_time(self):
        self.animation_trigger=False
        time_now = pg.time.get_ticks()
        if time_now-self.animation_time_prev>self.animation_time:
            self.animation_time_prev=time_now
            self.animation_trigger=True

    def get_images(self,path):
        images=deque()
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path,file)):
                img=pg.image.load(path+'/'+file).convert_alpha()
                images.append(img)
        return images


