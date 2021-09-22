import pygame
import pygame.time

from stand_powers import StandPowerType

class TheWorld(StandPowerType):
    """替身能力：“世界”"""
    def __init__(self, ai_settings, screen):
        """初始化“世界”的属性"""
        super().__init__()
        self.screen = screen
        #选择图标的路径，并设置热键
        self.icon_path = (r'C:\Users\25410\Desktop\python_work\
            alien_invasion_copy\images\the_world.bmp')
        self.hotbar = 'z'
        
        #设置单次时停时长
        self.duration = 5
        
        #设置标志，以判断是否时停
        self.time_flows = True
        
    def trigger(self, event):
        """热键触发替身能力"""
        if event.key == pygame.K_z:
            #暂停时间，并为计算剩余时长而初始化一些值
            self.ai_settings.time_freezing(ai_settings)
            self.start_time = pygame.time.get_tick()
            self.time_left = self.duration
            return True
        else:
            return False
            
    def countdown(self):
        """计算剩余时长"""
        #获得剩余秒数
        passed_secs = (pygame.time.get_tick() - self.start_time) / 1000
        if passed_secs <= self.duration:
            self.time_left = self.duration - int(passed_time)
        else:
            self.ai_settings.time_flowing(ai_settings)
            
    def time_freezing(self, ai_settings):
        """冻结时间"""
        #表明已经时停
        self.time_flows = False
        
        #将外星人的速度置零
        self.temp_alien_speed = ai_settings.alien_speed_factor
        ai_settings.alien_speed_factor = 0
        
    def time_flowing(self, ai_settings):
        """时间继续流动"""
        #表明时间继续流动
        self.time_flows = True
        
        #将外星人的速度变为原样
        ai_settings.alien_speed_factor = self.temp_alien_speed
            
    def prep_left_time(self, ai_settings, screen):
        """将剩余时停时间渲染成图像"""
        #字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        
        self.lt_image = self.font.render(str(self.time_left), True,
            self.text_color, self.ai_settings.bg_color)
        self.lt_image_rect = self.lt_image.get_rect()
        self.lt_image_rect.center = screen.center
        
    def draw_left_time(self):
        """绘制剩余时间"""
        self.screen.blit(self.lt_image, self.lt_image_rect)

    def update(self, ai_settings, screen):
        """
        接口函数，与StandPower类相接
        更新时停的状态
        """
        if not self.time_flows:
            countdown()
            prep_left_time(ai_settings, screen)
            
    def screen_update_event(self, ai_settings, screen):
        """
        接口函数，与StandPower类相接
        更新时停时间
        """
        if not self.time_flows:
            draw_left_time()
