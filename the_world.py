from time import sleep

import pygame
from stand_powers import StandPowerType

from sounds.make_sounds import *

class TheWorld(StandPowerType):
    """替身能力：“世界”"""
    
    def __init__(self, ai_settings, screen, stats):
        """初始化“世界”的属性"""
        super().__init__(ai_settings, screen, stats)
        #重写属性：阐明图标的路径，并设置热键
        self.icon_path = r'images\the_world.jpg'
        self.hotbar_mark = 'z'
        self.hotbar_key = pygame.K_z
        
        #表明“世界”不在使用
        self.stats.sp_occupation['the_world'] = False

        #设置单次时停时长
        self.duration = 5
        
        #设置标志，以判断是否时停
        self.time_flows = True
               
        #重写属性：设置技能CD
        self.cool_down = self.duration * 6
         
        #初始化替身能力开始时间
        self.start_time = -1
        
    def effect(self):
        """
        为重写方法
        设置替身能力效果
        """
        #暂停时间，并为计算剩余时长而初始化一些值
        self.time_freezing()
        self.time_left = self.duration
        
    def update(self):
        """
        为重写方法
        更新时停的剩余时间
        """
        if not self.time_flows:
            self.countdown()
            self.prep_left_time()
            
    def screen_update_event(self):
        """
        为重写方法
        重绘时停的剩余时间
        """
        if not self.time_flows:
            self.draw_left_time()

    def countdown(self):
        """计算剩余时长"""
        #获得剩余秒数
        passed_secs = (pygame.time.get_ticks() - self.start_time) / 1000
        
        if passed_secs <= self.duration:
            self.time_left = self.duration - int(passed_secs)
        else:
            self.time_flowing()
            
    def time_freezing(self):
        """将时间冻结"""
        #停顿0.1秒
        sleep(0.1)
        
        #以5-15的音量随机播放DIO1-5（咋瓦鲁多）
        random_play('DIO', 1, 5, 5, 15)
        
        #表明已经时停
        self.time_flows = False
        
        #表明“世界”正在使用
        self.stats.sp_occupation['the_world'] = True
        
        #将外星人的速度置零
        self.temp_alien_speed = self.ai_settings.alien_speed_factor
        self.ai_settings.alien_speed_factor = 0
        
        #外星人贴图变化
        self.temp_alien_image_path = self.ai_settings.alien_image_path
        self.ai_settings.alien_image_path = r'images/theworlded_alien.bmp'
        
        #背景颜色变化
        self.temp_bg_color = self.ai_settings.bg_color
        self.ai_settings.bg_color =(180, 181, 176)
        
        #子弹颜色变化
        self.temp_bullet_color = self.ai_settings.bullet_color
        self.ai_settings.bullet_color = (225, 211, 0)
        
    def time_flowing(self):
        """时间继续流动"""
        #表明时间继续流动
        self.time_flows = True
        
        #表明“世界”不在使用
        self.stats.sp_occupation['the_world'] = False
        
        #将外星人的速度和贴图、背景颜色、子弹颜色变为原样
        self.ai_settings.alien_speed_factor = self.temp_alien_speed
        self.ai_settings.alien_image_path = self.temp_alien_image_path
        self.ai_settings.bg_color = self.temp_bg_color
        self.ai_settings.bullet_color = self.temp_bullet_color
            
    def prep_left_time(self):
        """将剩余时停时间渲染成图像"""
        #字体设置
        self.text_color = (255, 236, 16)
        self.font = pygame.font.SysFont('jokerman', 48)
        
        self.lt_image = self.font.render(str(self.time_left), True,
            self.text_color)
        self.lt_image_rect = self.lt_image.get_rect()
        screen_rect = self.screen.get_rect()
        self.lt_image_rect.center = screen_rect.center
        
    def draw_left_time(self):
        """绘制剩余时间"""
        self.screen.blit(self.lt_image, self.lt_image_rect)

