#expertmm forked this from https://gist.github.com/tshirtman/6222891

from kivy.app import App
#from kivy.properties import NumericProperty
#from kivy.lang import Builder
from kivy.clock import Clock

from kivy.uix.label import Label
from kivy.uix.widget import Widget

from spritewidget import SpriteWidget

import random

def getRandomPos(lessThanX, lessThanY):
    return float(random.randrange(0,int(lessThanX))), float(random.randrange(0,int(lessThanY)))
        

#the variables marked with underscores should not be touched except internally


class MainForm(Widget):
    imperativeWidgets = None
    lastCreatedWidget = None
    
    imperativeLabel = None
    
    def __init__(self, **kwargs):
        super(MainForm, self).__init__(**kwargs)
        self.imperativeWidgets = list()

        self.imperativeLabel = Label(text="Tap if you like bunnies!")
        self.add_widget(self.imperativeLabel)
        #self.imperativeLabel.size = self.imperativeLabel.texture_size

    def update(self, dt, *args):
        #self.generateWidgetAt(random.randrange(0,self.width),random.randrange(0,self.height))
        self.imperativeLabel.set_center_y(self.height/2.0)
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


    def getRandomFormPos(self):
        return float(random.randrange(0,int(self.size[0]))), float(random.randrange(0,int(self.size[1])))

    def on_touch_down(self, touch):
        self.generateWidgetAt( touch.x, touch.y )
        
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
        
        return self.mainForm
    
        
        

if __name__ == '__main__':
    SpinningBunniesApp().run()