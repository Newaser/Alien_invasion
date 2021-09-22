from random import randint

import pygame.mixer

pygame.mixer.init()

def play_in_sounds(filename):
    """播放sounds目录下的音频文件"""
    path = r'sounds\\' + filename + '.ogg'
    sound = pygame.mixer.Sound(path)
    sound.set_volume(0.2)
    sound.play()
    
def random_play(filename_sort, start_1=None, end_1=None, start_2=5, end_2=5):
    """以随机的音量随机播放sounds目录下的若干个音频文件"""
    random_num_1 = randint(start_1, end_1)
    random_num_2 = randint(start_2, end_2)
    sound_path = r"sounds\\" + filename_sort + str(random_num_1) + ".ogg"
    sound = pygame.mixer.Sound(sound_path)
    sound.set_volume(random_num_2 / 10)
    sound.play()
