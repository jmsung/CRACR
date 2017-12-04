# Analysis of CRACR data from Yuxiao

from __future__ import division, print_function, absolute_import
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

class CRACR(object):
    def __init__(self):
        self.path = os.getcwd()
        self.path_split = self.path.split('\\')
        self.data_name = self.path_split[len(self.path_split)-1]
        
        self.dir_list = os.listdir(self.path)
        self.dir_num = len(self.dir_list)
        
        for self.dir_name in self.dir_list:
            self.file_list = os.listdir(self.path+'\\'+self.dir_name)
            self.file_num = len(self.file_list)
            
            for self.file_name in self.file_list:
                print(self.file_name)
                self.img = Image.open(self.path+'\\'+self.dir_name+'\\'+self.file_name)
                

# Start  
data = CRACR()