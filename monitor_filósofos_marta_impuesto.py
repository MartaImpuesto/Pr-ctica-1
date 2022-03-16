# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:32:53 2022

@author: Marta Impuesto
"""
from multiprocessing import Array, Manager
from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Array, Manager
import time
import random

NPHIL = 5

class Table:
    def __init__(self, NPHIL, manager):
        self.NPHIL = NPHIL
        self.mutex = Lock()
        self.comensales = manager.list([False for i in range(NPHIL)])
        self.free_fork = Condition(self.mutex)
        self.phil = None
        
    def set_current_phil(self, num):
        self.phil = num

    # no comen lados   
    def are_free_fork(self):
        return (not self.comensales[(self.phil-1)%self.NPHIL]) and (not self.comensales[(self.phil+1)%self.NPHIL])
       
    def wants_eat(self, num):
        self.mutex.acquire()
        self.free_fork.wait_for(self.are_free_fork)
        self.comensales[self.phil] = True
        self.mutex.release()
       
    def wants_think(self, num):
       self.mutex.acquire()
       self.comensales[self.phil] = False
       self.free_fork.notify()
       self.mutex.release()