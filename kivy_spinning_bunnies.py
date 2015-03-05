#expertmm forked this from https://gist.github.com/tshirtman/6222891

from kivy.app import App
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.clock import Clock

from kivy.uix.label import Label
from kivy.graphics import PushMatrix
from kivy.graphics import PopMatrix
from kivy.graphics import Rotate
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

import math
import random

def getRandomPos(lessThanX, lessThanY):
    return float(random.randrange(0,int(lessThanX))), float(random.randrange(0,int(lessThanY)))
        

#the variables marked with underscores should not be touched except internally
class FreeWidget(Widget):
    freeAngle = None
    freePos = None
    _rotation_instruction = None
    _rectangle_instruction = None
    
    degreesPerSecond = None
    speedPixelsPerFrameXYPair = None
    
    def __init__(self, **kwargs):
        super(FreeWidget, self).__init__(**kwargs)
        self.freeAngle = 0.0
        self.degreesPerSecond = 0.0
        self.freePos = (10.0,100.0)
        self._rotation_instruction = Rotate(angle=self.freeAngle, origin=self.freePos)
        self._rectangle_instruction = Rectangle(source="bunny.png", pos=self.freePos, size=(41.0,41.0))
#         with self.canvas.before:
#             PushMatrix()
#             Rotate(angle=self.freeAngle, origin = self.freePos)
        self.canvas.add(PushMatrix())
        self.canvas.add(self._rotation_instruction)  #self.canvas.add(Rotate(angle=self.freeAngle, origin = self.freePos))
        self.canvas.add(Color(1.0,1.0,1.0,1.0))
        self.canvas.add(self._rectangle_instruction)  #self.canvas.add(Rectangle(pos=self.freePos, size=(10.0,20.0)))
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
        self._rectangle_instruction.pos = self.freePos[0]-self._rectangle_instruction.size[0]/2.0, self.freePos[1]-self._rectangle_instruction.size[1]/2.0
        self._rotation_instruction.origin = self.freePos
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

class MainForm(Widget):
    imperativeWidgets = None
    lastCreatedWidget = None
    imperativeLabel = None
    
    def __init__(self, **kwargs):
        super(MainForm, self).__init__(**kwargs)
        self.imperativeWidgets = list()

    def on_touch_down(self, touch):
        self.generateWidgetAt( touch.x, touch.y )
        
    def getRandomFormPos(self):
        return float(random.randrange(0,int(self.size[0]))), float(random.randrange(0,int(self.size[1])))
        
    def generateWidgetAt(self, x, y):
        self.lastCreatedWidget = FreeWidget()
        self.lastCreatedWidget.set_center_x(x)
        self.lastCreatedWidget.set_center_y(y)
        self.lastCreatedWidget.degreesPerSecond = float(random.randrange(0,3))
        self.lastCreatedWidget.speedPixelsPerFrameXYPair = getRandomPos(5,5)
        self.add_widget(self.lastCreatedWidget)
        self.imperativeWidgets.append(self.lastCreatedWidget)
        self.imperativeLabel.text = "Tap if you like "+str(len(self.imperativeWidgets)+1)+" bunnies!"
        
    def update(self, dt, *args):
        self.imperativeLabel.set_center_y(self.height/3.0*2.0)
        self.imperativeLabel.set_center_x(self.width/2.0)
        for widgetIndex in range(0,len(self.imperativeWidgets)):
            thisWidget = self.imperativeWidgets[widgetIndex]
            thisWidget.refresh()
            if thisWidget.speedPixelsPerFrameXYPair is not None:
                if thisWidget.get_center_x()<0 and thisWidget.speedPixelsPerFrameXYPair[0]<0:
                    thisWidget.bounce_x()
                    thisWidget.set_center_x(0)
                elif thisWidget.get_center_x()>=self.size[0] and thisWidget.speedPixelsPerFrameXYPair[0]>0:
                    thisWidget.bounce_x()
                    thisWidget.set_center_x(self.size[0]-1.0)
                if thisWidget.get_center_y()<0 and thisWidget.speedPixelsPerFrameXYPair[1]<0:
                    thisWidget.bounce_y()
                    thisWidget.set_center_y(0)
                elif thisWidget.get_center_y()>=self.size[1] and thisWidget.speedPixelsPerFrameXYPair[1]>0:
                    thisWidget.bounce_y()
                    thisWidget.set_center_y(self.size[1]-1.0)

class SpinningBunniesApp(App):
    mainForm = None
    
    def build(self):
        self.mainForm = MainForm()
        Clock.schedule_interval(self.mainForm.update, 0)
        
#         self.freeWidget1 = FreeWidget()
#         self.lastCreatedWidget = self.freeWidget1
#         self.freeWidget1.degreesPerSecond = (1.0)
#         self.mainForm.add_widget(self.freeWidget1)
#         self.imperativeWidgets.append(self.freeWidget1)
        
        self.freeWidget2 = FreeWidget()
        self.lastCreatedWidget = self.freeWidget2
        self.freeWidget2.degreesPerSecond = (3.0)
        self.freeWidget2.speedPixelsPerFrameXYPair = 2.0,5.0
        self.mainForm.add_widget(self.freeWidget2)
        self.mainForm.imperativeWidgets.append(self.freeWidget2)
        
        self.mainForm.imperativeLabel = Label(text="Tap if you like bunnies!")
        
        self.mainForm.imperativeLabel.size = self.mainForm.imperativeLabel.texture_size
        self.mainForm.add_widget(self.mainForm.imperativeLabel)
        
        return self.mainForm
    
        
        

if __name__ == '__main__':
    SpinningBunniesApp().run()