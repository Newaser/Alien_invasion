import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship

import game_functions as gf

#导入所有替身能力类
from the_world import TheWorld
from hierophant_green import HierophantGreen

def run_game():
    #初始化游戏
    pygame.init()
    
    #初始化游戏设置和屏幕
    ai_settings = Settings()
    screen = pygame.display.set_mode((
        ai_settings.screen_width,ai_settings.screen_height))
        
    #初始化标题字样
    pygame.display.set_caption("Alien Invasion")
    
    #创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    
    #创建并初始化游戏统计数据，创建计分板
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    #创建一艘飞船，创建一个子弹的编组，创建一个外星人编组，创建一个替身能力编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    sps = Group()
    
    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    #加载所有替身能力
    types = []
    types.append(TheWorld(ai_settings, screen, stats))
    types.append(HierophantGreen(ai_settings, screen, stats, sb, ship, aliens))
    gf.load_stand_powers(ai_settings, types, sps)
    
    #开始主游戏循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, sps, ship,
            aliens, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens,
                bullets)
            
            gf.update_sps(ai_settings, screen, sb, sps)
            
        gf.update_screen(ai_settings, screen, stats, sb, sps, ship, aliens,
            bullets, play_button)

run_game()
