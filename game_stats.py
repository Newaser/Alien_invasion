import json

class GameStats():
    """跟踪游戏信息"""
    
    def __init__(self, ai_settings):
        """初始化游戏信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = self.get_high_score()
        self.sp_occupation = {}
        
    def reset_stats(self):
        """重置游戏信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        self.sp_num = 0
        self.record_break_available = True
        
    def get_high_score(self):
        """读取历史最高分"""
        file_path = 'logs\history.json'
        with open(file_path) as f_obj:
            high_score = int(json.load(f_obj))
        return high_score
