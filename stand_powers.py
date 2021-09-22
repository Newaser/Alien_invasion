import pygame
from pygame.sprite import Sprite

from sounds.make_sounds import play_in_sounds

class StandPower(Sprite):
    """替身能力索引类"""
    
    def __init__(self, ai_settings, screen, stats):
        """初始化替身能力的索引"""
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.sp_type = StandPowerType(ai_settings, screen, stats)
        self.event = None
        
        #初始化替身能力热键的字体和其他属性
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
    def load_icon(self):
        """加载图标"""
        #加载替身能力图标和矩形
        self.image = pygame.image.load(self.sp_type.icon_path)
        self.rect = self.image.get_rect()
        
        #设置替身能力图标的尺寸
        self.width, self.height = 50, 50
        self.rect.width = self.width
        self.rect.height = self.height
        
        #将替身能力图标放在屏幕右侧
        self.rect.right = self.screen_rect.right - 10
        
    def load_hotbar_image(self):
        """加载热键渲染图"""
        self.hotbar_image = self.font.render(self.sp_type.hotbar_mark.upper(),
            True, self.text_color)
        self.hotbar_image_rect = self.hotbar_image.get_rect()
    
    def check_hotbar(self):
        """检测是否响应了热键"""
        return self.sp_type.trigger(self.event)
         
    def update(self):
        """更新替身能力状态"""
        self.sp_type.update_cd()
        self.sp_type.update()
        
    def screen_update_event(self):
        """更新打印入屏幕的状态"""
        self.sp_type.screen_update_event()
        
    def reset(self):
        """重置替身能力的状态值"""
        self.sp_type.reset()
        
def prep_sps(sb, stand_powers):
    """预处理所有替身能力的图标"""
    #将替身能力图标放在游戏等级下方
    ceiling = sb.level_rect.bottom - 50
    #依次确定它们的位置
    for stand_power in stand_powers:
        choose_hotbar_color(stand_power)
        ceiling += stand_power.height + 10
        stand_power.rect.top = ceiling
        stand_power.hotbar_image_rect.center =  stand_power.rect.center
        
def draw_sps(screen, stand_powers):
    """绘制所有替身能力的图标和热键"""
    for stand_power in stand_powers:
        screen.blit(stand_power.image, stand_power.rect)
        screen.blit(stand_power.hotbar_image, stand_power.hotbar_image_rect)
        
def choose_hotbar_color(stand_power):
    """决定热键渲染图颜色"""
    if stand_power.sp_type.cd_finnished:
        stand_power.text_color = (255, 255, 255)
    elif not stand_power.sp_type.cd_finnished:
        stand_power.text_color = (255, 0, 0)
    stand_power.load_hotbar_image()


class StandPowerType():
    """替身能力种类的类"""
    def __init__(self, ai_settings, screen, stats):
        #共享ai_settings、screen和stats
        self.ai_settings = ai_settings
        self.screen = screen
        self.stats = stats
        #设置图标路径
        self.icon_path = 'images\default.jpg'
        #设置热键的标志和按键
        self.hotbar_mark = ''
        self.hotbar_key = None
        #设置技能CD
        self.cool_down = 10
        #判断CD是否冷却
        self.cd_finnished = True
        #初始化替身能力开始时间
        self.start_time = -1
        
    def trigger(self, event):
        """热键触发替身能力"""
        #判断热键是否正确
        hotbar_correct = event.key == self.hotbar_key
        
        if hotbar_correct and self.cd_finnished:
            self.start_time = pygame.time.get_ticks()
            self.effect()
            return True
        elif hotbar_correct and not self.cd_finnished:
            play_in_sounds('forbidden')
            return False
        else:
            return False
            
    def effect(self):
        """设置替身能力的效果"""
        None
        
    def update_cd(self):
        """更新CD是否冷却的状态"""
        self.cd_finnished = (pygame.time.get_ticks() - self.start_time
            >= self.cool_down * 1000) or (self.start_time == -1)
            
    def update(self):
        """更新替身能力的状态值"""
        None
        
    def screen_update_event(self):
        """将新的状态值更新于屏幕"""
        None
        
    def reset(self):
        """重置替身能力的状态值"""
        self.cd_finnished = True
