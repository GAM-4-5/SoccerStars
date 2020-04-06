import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock

Window.size = (600, 950)

class Lopta(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x,velocity_y)

    def move(self): 
        self.pos = Vector(*self.velocity) + self.pos    
        self.velocity_x *= 0.4
        self.velocity_y *= 0.4

class Igrac(Widget):
    score = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
                
        #stalno smanjivanje brzine igrača
        self.velocity_x *= 0.9
        self.velocity_y *= 0.9

    #def player_collide(self, player):
        #if self.collide_widget(player):
            #offset = (player.center_y)

    
class Igra(Widget):
    lopta = ObjectProperty(None)

    igrac1 = ObjectProperty(None)
    igrac2 = ObjectProperty(None)

    slijed = BooleanProperty(None)

    velocity_xp = NumericProperty(0)
    velocity_yp = NumericProperty(0)
    
    def on_touch_down(self, touch):
        if self.igrac1.collide_point(*touch.pos):
            print("Kliknuo si prvog igraca")
            self.slijed = True
            print(self.slijed)
        elif self.igrac2.collide_point(*touch.pos):
            print("Kliknuo si drugog igraca")
            self.slijed = False
            print(self.slijed)

    #def on_touch_move(self, touch):
    #    if self.slijed == True:
    #        print("prvi igrač igra ", touch.x, " ",touch.y)
    #    elif abs(self.igrac2.y - touch.y) < 100 and abs(self.igrac2.x - touch.x) < 100:
    #        print("drugi igrač igra")
        
    def on_touch_up(self, touch):
        if self.slijed == True:
            self.igrac1.velocity_x = int((self.igrac1.center_x - touch.x)/2)
            self.igrac1.velocity_y = int((self.igrac1.center_y - touch.y)/2)
            self.igrac1.velocity = (self.igrac1.velocity_x, self.igrac1.velocity_y)
        else:
            self.igrac2.velocity_x = int((self.igrac2.center_x - touch.x)/2)
            self.igrac2.velocity_y = int((self.igrac2.center_y - touch.y)/2)
            self.igrac2.velocity = (self.igrac2.velocity_x, self.igrac2.velocity_y)

    def update(self, dt):
        #pokretanje funkcije kretanja igraca
        self.igrac1.move()
        self.igrac2.move()

        #Odbijanje od zidova terena, treba jos malo doraditi
        if (self.igrac1.x <= 0) or (self.igrac1.right >= 600):
            self.igrac1.velocity_x *= -1
            print("igrac 1 je pogdio lijevo ili desno")
        if (self.igrac2.x <= 0) or (self.igrac2.right >= 600):
            self.igrac2.velocity_x *= -1
            print("igrac 2 je pogdio lijevo ili desno")
        if (self.igrac1.y <= 0) or (self.igrac1.top >= 908):
            self.igrac1.velocity_y *= -1
            if (self.igrac1.top >= 908):
                self.igrac1.score += 1
            print("igrac 1 je pogdio gore ili dolje")
        if (self.igrac2.y <= 0) or (self.igrac2.top >= 908):
            self.igrac2.velocity_y *= -1
            if (self.igrac2.y <= 0):
                self.igrac2.score += 1
            print("igrac 2 je pogdio gore ili dolje")

class SoccerStars(App):
    def build(self):
        igra = Igra()
        Clock.schedule_interval(igra.update, 1.0 / 60.0)
        return igra

if __name__ == "__main__":
    SoccerStars().run()

