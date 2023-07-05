import gradio as gr
import os
import cv2
import PIL
import numpy as np


from UI import Generate



class Candidate:
    def __init__(self, imgpath, iteration_num, num):
        self.imgpath = imgpath
        self.iteration_num = iteration_num
        self.num = num

    def getImgpath(self):
        return self.imgpath

    def setScore(self, style, layout):
        self.style = style
        self.layout = layout

    def setPrompts(self, prompts):
        self.prompts = prompts

    def setParemeters(self, parameters):
        self.parameters = parameters


