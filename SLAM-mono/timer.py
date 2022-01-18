
from tabnanny import verbose
import pygame


class Timer(object):
    def __init__(self, verbose=True):
        self.t0 = pygame.time.get_ticks()
        self.t1 = 0.0
        self.delta = 0.0
        self.verbose = verbose

    def get(self):
        self.t1 = pygame.time.get_ticks()
        self.delta = self.t1 - self.t0
        
        if self.verbose:
            print(f'delta_t = {self.delta}')