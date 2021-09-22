class Settings():
    """存储《外星人入侵》的所有设置的类"""
    
    def __init__(self):
        """初始化游戏静态设置"""
        #界面的设置
        self.screen_width = 1200
        self.screen_height = 800
        
        
        #飞船的设置
        self.ship_limit = 3
        
        #替身能力数量设置
        self.sp_limit = 2
        
        #子弹的设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        
        #外星人的设置
        self.fleet_drop_speed = 10
        self.alien_image_path = r'images/alien.bmp'
        
        #游戏节奏加快的度量
        self.speedup_scale = 1.1
        
        #外星人点数提高的度量
        self.score_scale = 1.5
        
        #初始化游戏动态设置
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """初始化游戏动态配置"""
        self.bg_color_r = 230
        self.bg_color_g = 230
        self.bg_color_b = 230
        self.bg_color = (self.bg_color_r, self.bg_color_g, self.bg_color_b)
        
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        
        #fleet_direction为1时表示右移，为-1时表示左移
        self.fleet_direction = 1
        
        #计分
        self.alien_points = 50
        
    def increase_speed(self):
        """加快游戏节奏，提高外星人点数"""
        # ~ self.bg_color_r /= self.speedup_scale
        # ~ self.bg_color_g /= self.speedup_scale
        # ~ self.bg_color_b /= self.speedup_scale
        # ~ self.bg_color = (self.bg_color_r, self.bg_color_g, self.bg_color_b)
        
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
