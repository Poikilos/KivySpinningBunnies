#expertmm forked this from https://gist.github.com/tshirtman/6222891

from kivy.app import App
#from kivy.properties import NumericProperty
#from kivy.lang import Builder
from kivy.clock import Clock

from kivy.uix.label import Label
<<<<<<< HEAD
=======
from kivy.graphics import PushMatrix
from kivy.graphics import PopMatrix
from kivy.graphics import Rotate
from kivy.graphics import Translate
from kivy.graphics import Rectangle
from kivy.graphics import Scale
from kivy.graphics import Color
>>>>>>> origin/master
from kivy.uix.widget import Widget

from spritewidget import SpriteWidget

import random

def getRandomPos(lessThanX, lessThanY):
    return float(random.randrange(0,int(lessThanX))), float(random.randrange(0,int(lessThanY)))
        

#the variables marked with underscores should not be touched except internally
<<<<<<< HEAD

=======
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
>>>>>>> origin/master

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
        self.lastCreatedWidget = SpriteWidget()
        self.lastCreatedWidget.set_center_x(x)
        self.lastCreatedWidget.set_center_y(y)
        self.lastCreatedWidget.degreesPerSecond = float(random.randrange(0,3))
        self.lastCreatedWidget.speedPixelsPerFrameXYPair = getRandomPos(5,5)
        self.lastCreatedWidget.setScale( float(random.randrange(5,20))/10.0 )
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
                #ordered pairs (size is also an ordered pair in Kivy):
                #index 0 contains the x value
                #index 1 contains the y value
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
        framesPerSecond = 60.0
        Clock.schedule_interval(self.mainForm.update, 1.0/framesPerSecond)
        
#         self.spriteWidget1 = SpriteWidget()
#         self.lastCreatedWidget = self.spriteWidget1
#         self.spriteWidget1.degreesPerSecond = (1.0)
#         self.mainForm.add_widget(self.spriteWidget1)
#         self.imperativeWidgets.append(self.spriteWidget1)
        
        self.spriteWidget2 = SpriteWidget()
        self.lastCreatedWidget = self.spriteWidget2
        self.spriteWidget2.degreesPerSecond = (3.0)
        self.spriteWidget2.speedPixelsPerFrameXYPair = 2.0,5.0
        self.mainForm.add_widget(self.spriteWidget2)
        self.mainForm.imperativeWidgets.append(self.spriteWidget2)
        
        self.mainForm.imperativeLabel = Label(text="Tap if you like bunnies!")
        
        self.mainForm.imperativeLabel.size = self.mainForm.imperativeLabel.texture_size
        self.mainForm.add_widget(self.mainForm.imperativeLabel)
        
        return self.mainForm
    
        
        

if __name__ == '__main__':
    SpinningBunniesApp().run()
