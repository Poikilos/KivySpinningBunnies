
from kivy.graphics import PushMatrix
from kivy.graphics import PopMatrix
from kivy.graphics import Rotate
from kivy.graphics import Translate
from kivy.graphics import Rectangle
from kivy.graphics import Scale
from kivy.graphics import Color
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

class SpriteWidget(Widget):
    freeAngle = None
    freePos = None
    _rotation_instruction = None
    _rectangle_instruction = None
    _scale_instruction = None
    _translate_instruction = None
    
    degreesPerSecond = None
    speedPixelsPerFrameXYPair = None
    
    def __init__(self, **kwargs):
        super(SpriteWidget, self).__init__(**kwargs)
        self.freeAngle = 0.0
        self.degreesPerSecond = 0.0
        self.freePos = (10.0,100.0)
        self._rectangle_instruction = Rectangle(source="bunny.png", pos=(0,0), size=(41.0,41.0))
        self._rotation_instruction = Rotate(angle=self.freeAngle, origin=(self._rectangle_instruction.size[0]/2.0,self._rectangle_instruction.size[1]/2.0))
        self._scale_instruction = Scale(1.0,1.0,1.0)
        self._translate_instruction = Translate(0,0)
        
        self.canvas.add(PushMatrix())
        self.canvas.add(self._translate_instruction)
        self.canvas.add(self._rotation_instruction)
        self.canvas.add(self._scale_instruction)
        self.canvas.add(Color(1.0,1.0,1.0,1.0))
        self.canvas.add(self._rectangle_instruction)
        self.canvas.add(PopMatrix())
        
        self.refresh()
#         with self.canvas.after:
#             PopMatrix()
    
    def refresh(self):
        if (self.speedPixelsPerFrameXYPair is not None):
            self.freePos = self.freePos[0] + self.speedPixelsPerFrameXYPair[0], self.freePos[1] + self.speedPixelsPerFrameXYPair[1]
        self.freeAngle += self.degreesPerSecond
        self._change_instructions()
    
    def _change_instructions(self):
        self._translate_instruction.x = self.freePos[0]-self._rectangle_instruction.size[0]*self._scale_instruction.x/2
        self._translate_instruction.y = self.freePos[1]-self._rectangle_instruction.size[1]*self._scale_instruction.y/2
        #self._rectangle_instruction.pos = self.freePos[0]-self._rectangle_instruction.size[0]*self._scale_instruction.x/2.0, self.freePos[1]-self._rectangle_instruction.size[1]*self._scale_instruction.y/2.0
        self._rotation_instruction.origin = self._rectangle_instruction.size[0]*self._scale_instruction.x/2.0, self._rectangle_instruction.size[1]*self._scale_instruction.x/2.0 
        self._rotation_instruction.angle = self.freeAngle
        
        
    def set_center_x(self, x):
        self.freePos = float(x), self.freePos[1]
        self._change_instructions()

    def set_center_y(self, y):
        self.freePos = self.freePos[0], float(y)
        self._change_instructions()
    
        
    def get_center_x(self):
        return self.freePos[0]
    
    def get_center_y(self):
        return self.freePos[1]
    
    def load_image_file(self, fileName):
        self._rectangle_instruction.source=fileName
    
    def bounce_x(self):
        if self.speedPixelsPerFrameXYPair is not None:
            self.speedPixelsPerFrameXYPair = self.speedPixelsPerFrameXYPair[0]*-1.0, self.speedPixelsPerFrameXYPair[1]

    def bounce_y(self):
        if self.speedPixelsPerFrameXYPair is not None:
            self.speedPixelsPerFrameXYPair = self.speedPixelsPerFrameXYPair[0], self.speedPixelsPerFrameXYPair[1]*-1.0
            
    def setScale(self, multiplier):
        self._scale_instruction.x = float(multiplier)
        self._scale_instruction.y = float(multiplier)
        self._change_instructions()

    def setScaleXY(self, xMultiplier, yMultiplier):
        self._scale_instruction.x = float(xMultiplier)
        self._scale_instruction.y = float(yMultiplier)
        self._change_instructions()