import sys
import json
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien
from stand_powers import StandPower
from stand_powers import prep_sps, draw_sps

from sounds.make_sounds import *

pygame.mixer.init()

def check_keydown_events(event, ai_settings, screen, stats, sps, ship,
    bullets):
    """响应按下"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
        ship.moving_left = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
        ship.moving_right = False
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        save_and_quit(stats)
    elif not sp_occupying(stats):
        #响应所有替身能力事件
        for sp in sps:
            sp.event = event
            if sp.check_hotbar():
                break
            
def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, sps, ship,
        aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                save_and_quit(stats)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sps, ship,
                bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, sps,
                ship, aliens, bullets, mouse_x, mouse_y)

def update_screen(ai_settings, screen, stats, sb, sps, ship, aliens, bullets,
        play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    #每次循环时重绘屏幕
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    #重绘计分板
    sb.show_score()
    
    #重绘所有替身能力的图标和热键
    if stats.game_active:
        draw_sps(screen, sps)
    
    #重绘替身能力的改变
    for stand_power in sps:
        stand_power.screen_update_event()
    
    #若游戏不在进行，绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
            
    #让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship,
        aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    #更新子弹的位置
    bullets.update()
        
    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets)
    

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果子弹数未达上限，发射一颗新的子弹"""
    #创建一颗子弹，并将其加入编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        play_in_sounds('shooting')
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
    
def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                            (3*alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其加入当前行"""
    alien = Alien(ai_settings, screen)
    #获得外星人长和宽
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    #计算外星人的坐标
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien_height + 2 * alien_height * row_number
    #生成外星人
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    #创建一个外星人，并计算一行可容纳多少个外星人，一共可以存在多少这样的行
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)
    
    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """
    检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update(ai_settings)
    
    #检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        play_in_sounds('ship_crash')
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    #检测外星人与是否到达屏幕底部
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达屏幕边缘时应采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets):
    """响应子弹和外星人的碰撞"""
    #删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            #播放音效
            play_in_sounds('alien_shot')
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        #如果外星人团灭，并提升游戏等级
        
        bullets.empty()
        ai_settings.increase_speed()
        
        #暂停0.3秒并播放音效
        sleep(0.3)
        play_in_sounds('annihilation')
        
        #提升游戏等级
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        #生命值-1
        stats.ships_left -= 1
        
        #更新记分牌
        sb.prep_ships()
        
        #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        
        #生成一群新外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        #暂停
        sleep(1.0)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """检测是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #添加音效，并暂停3秒
            play_in_sounds('invasion_success')
            sleep(3.0)
            #像飞船碰撞一样处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def check_play_button(ai_settings, screen, stats, sb, play_button, sps, 
        ship, aliens, bullets, mouse_x, mouse_y):
    """响应Play按钮点击事件"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #隐藏光标
        pygame.mouse.set_visible(False)
        
        #重置游戏动态配置和统计信息，让游戏开始
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True
        
        #更新记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        
        #重置所有替身能力
        for sp in sps:
            sp.reset()
        
        #生成一群新外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_high_score(stats, sb):
    """检测是否诞生了最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        #若没破纪录且最高分不为0，可破记录
        if stats.high_score == 0:
            stats.record_break_available = False
        elif stats.record_break_available:
            play_in_sounds('break_record')
            stats.record_break_available = False

def save_and_quit(stats):
    """保存并退出"""
    file_path = 'logs\history.json'
    with open(file_path, 'w') as f_obj:
        json.dump(stats.high_score, f_obj)
    
    sys.exit()

def load_stand_powers(ai_settings, types, sps):
    """加载替身能力"""
    for num in range(ai_settings.sp_limit):
        stand_power = StandPower(types[num].ai_settings, types[num].screen,
            types[num].stats)
        stand_power.sp_type = types[num]
        stand_power.load_icon()
        stand_power.load_hotbar_image()
        sps.add(stand_power)

def update_sps(ai_settings, screen, sb, sps):
    """更新所有替身能力"""
    #预处理替身能力的状态
    for stand_power in sps:
        stand_power.update()
    #预处理替身能力的图标
    prep_sps(sb, sps)

def sp_occupying(stats):
    occupied = False
    for value in stats.sp_occupation.values():
        occupied += value
    return occupied
    
