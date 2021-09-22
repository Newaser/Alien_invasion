import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self, ai_settings, screen):
        """初始化外星人，并设置其初始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载外星人图像，并设置其rect属性
        self.image = pygame.image.load(ai_settings.alien_image_path)
        self.rect = self.image.get_rect()

        #设置初始位置，为左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #存储外星人的准确位置
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """如果外星人处于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if (self.rect.right >= screen_rect.right or
            self.rect.left <= screen_rect.left):
            return True
        
    def update(self, ai_settings):
        """更新外星人"""
        #更新外星人贴图
        self.image = pygame.image.load(ai_settings.alien_image_path)
        #将外星人向左或右移动
        self.x += (self.ai_settings.alien_speed_factor *
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x
        
    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)
