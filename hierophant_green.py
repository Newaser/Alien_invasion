from time import sleep
from random import randint

import pygame
from pygame.sprite import Group
from ship import Ship
from bullet import Bullet
from stand_powers import StandPowerType

import game_functions as gf
from sounds.make_sounds import *

class HierophantGreen(StandPowerType):
    """替身能力：“绿色法皇”"""
    
    def __init__(self, ai_settings, screen, stats, sb, ship, aliens):
        """初始化“绿色法皇”的属性"""
        super().__init__(ai_settings, screen, stats)
        #共享sb, ship, bullets编组
        self.sb = sb
        self.ship = ship
        self.aliens = aliens
        
        #重写属性：阐明图标的路径，并设置热键
        self.icon_path = r'images\hierophant_green.jpg'
        self.hotbar_mark = 'x'
        self.hotbar_key = pygame.K_x
        
        #表明“绿色法皇”不在使用
        self.stats.sp_occupation['hierophant_green'] = False
        
        #重写属性：设置技能CD
        self.cool_down = 30
        
        #创建绿宝石编组
        self.emeralds = Group()

    def effect(self):
        """
        为重写方法
        发射绿宝石水花
        """
        #表明“绿色法皇”正在使用
        self.stats.sp_occupation['hierophant_green'] = True
        
        #初始化发射次数
        self.splash_times = 0
        
        random_play('emerald_splash_', 1, 2, 7, 9)
        
    def update(self):
        """
        为重写方法
        更新替身能力的状态值
        """
        #获得经过的秒数
        passed_secs = (pygame.time.get_ticks() - self.start_time) / 1000
        
        if self.stats.sp_occupation['hierophant_green'] :
            if passed_secs / 0.1 >= self.splash_times and self.splash_times <= 10:
                self.emerald_splash()
            elif self.splash_times >= 10:
            #表明“绿色法皇”不在使用
                self.stats.sp_occupation['hierophant_green'] = False
        
        for emerald in self.emeralds:
            emerald.update()
            
        for parent_emerald in self.emeralds:
            limit_generation = randint(4, 5)
            if parent_emerald.generation <= limit_generation:
                for son_emerald in range(parent_emerald.multiply_num):
                    son_emerald = Emerald(self.ai_settings, self.screen,
                        parent_emerald)
                    son_emerald.generation = parent_emerald.generation + 1
                    self.emeralds.add(son_emerald)
                    self.emeralds.remove(parent_emerald)
                
        for emerald in self.emeralds.copy():
            if emerald.rect.bottom <= 0:
                self.emeralds.remove(emerald) 

        gf.check_bullet_alien_collisions(self.ai_settings, self.screen,
            self.stats, self.sb, self.ship, self.aliens, self.emeralds)
            
    def screen_update_event(self):
        """
        为重写方法
        将新的状态值更新于屏幕
        """
        for emerald in self.emeralds.sprites():
            emerald.draw_bullet()
            
    def reset(self):
        """
        为重写方法
        重置替身能力的状态值
        """
        self.cd_finnished = True
        self.emeralds.empty()
            
    def emerald_splash(self):
        """发射绿宝石水花"""
        reference_ship = Ship(self.ai_settings, self.screen)
        muzzles = randint(2, 4)
        for i in range(muzzles):
            reference_ship.rect.centerx = self.ship.rect.centerx
            reference_ship.rect.centerx += (((i - 1) / muzzles) * 
                                                self.ship.rect.width)
            emerald = Emerald(self.ai_settings, self.screen, reference_ship)
            self.emeralds.add(emerald)
            
        self.splash_times += 1

class Emerald(Bullet):
    """绿宝石类型"""
    
    def __init__(self, ai_settings, screen, parent_emerald):
        """初始化绿宝石类型"""
        super().__init__(ai_settings, screen, parent_emerald)
        #重写属性：定义绿宝石的大小
        emerald_width = 5
        emerald_height = 10
        self.rect = pygame.Rect(0, 0, emerald_width, 
        emerald_height)
        #重写属性：定义绿宝石的位置
        wave = 20
        self.rect.centerx = parent_emerald.rect.centerx + randint(-wave, wave)
        self.rect.bottom = parent_emerald.rect.top
        
        #重写属性：随机定义绿宝石的颜色
        color_r = randint(0, 32)
        color_g = randint(223, 255)
        color_b = randint(0, 32)
        self.color = (color_r, color_g, color_b)
        
        #重写属性：随机定义绿宝石的速度
        self.speed_factor = 4 + randint(-5, 5) / 10
        
        #重写精算的y，并定义起始距离
        self.y = float(self.rect.y)
        self.start_y = self.y
        
        #初始化应增殖数
        self.multiply_num = -1
        self.generation = 0
        
    def update(self):
        """向上移动绿宝石"""
        #更新绿宝石的位置
        self.y -= self.speed_factor
        #根据拟定值self.y确定绿宝石的纵坐标
        self.rect.y = self.y
        #更新移动距离
        self.dist = self.start_y - self.y
        
        #绿宝石随机0-3增殖
        rand_dist = randint(20, 30)
        if self.dist > rand_dist:
            self.multiply_num = int(randint(1, 6) / 2) - 1
            
        
