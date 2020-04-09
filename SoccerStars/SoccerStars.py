import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

Window.size = (600, 950)

class Lopta(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x,velocity_y)

    def move(self): 
        self.pos = Vector(*self.velocity) + self.pos    
        self.velocity_x *= 0.9
        self.velocity_y *= 0.9

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
    
    #sudar dva igraca
    def player_collide(self, player):
        if self.collide_widget(player):
            print("sudaraju se", self.velocity_x, self.velocity_y)
            vx = self.velocity_x
            vy = self.velocity_y

            player.velocity_x = vx*3/4
            player.velocity_y = vy*3/4
            
            self.velocity_x = -vx/3
            self.velocity_y = -vy/3
            
            player.move()
            self.move()
    
class Igra(Widget):
    lopta = ObjectProperty(None)

    igrac1 = ObjectProperty(None)
    igrac2 = ObjectProperty(None)

    slijed = BooleanProperty(None)
    red = NumericProperty(1)

    zvuk = SoundLoader.load("source/sound1.mp3").play()

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
        if self.slijed and self.red % 2 == 1:
            self.igrac1.velocity_x = int((self.igrac1.center_x - touch.x)/2)
            self.igrac1.velocity_y = int((self.igrac1.center_y - touch.y)/2)
            self.igrac1.velocity = (self.igrac1.velocity_x, self.igrac1.velocity_y)
            self.slijed = BooleanProperty(None)
            self.red += 1
        elif self.red % 2 == 0 and not self.slijed:
            self.igrac2.velocity_x = int((self.igrac2.center_x - touch.x)/2)
            self.igrac2.velocity_y = int((self.igrac2.center_y - touch.y)/2)
            self.igrac2.velocity = (self.igrac2.velocity_x, self.igrac2.velocity_y)
            self.slijed = BooleanProperty(None)
            self.red += 1

    def restart(self):
        self.lopta.center = (300, 454)
        self.lopta.velocity = (0,0)
        self.igrac1.center = (300, 200)
        self.igrac1.velocity = (0,0)
        self.igrac2.center = (300, self.parent.height - 242)
        self.igrac2.velocity = (0,0)

    def update(self, dt):
        #pokretanje funkcije kretanja igraca, 60x u sekundi provodi micanje igraca
        self.igrac1.move()
        self.igrac2.move()
        self.lopta.move()
        
        #provjerava i provodi odbijanje između igrača i igrača s loptom
        self.igrac1.player_collide(self.igrac2)
        self.igrac2.player_collide(self.igrac1)
        self.igrac1.player_collide(self.lopta)
        self.igrac2.player_collide(self.lopta)

        #Odbijanje od zidova terena, treba jos malo doraditi, nekada dolazi do nekih grešaka
        if (self.igrac1.x <= 0) or (self.igrac1.right >= 600):
            self.igrac1.velocity_x *= -1
            self.igrac1.move()
        if (self.igrac1.y <= 0) or (self.igrac1.top >= 908):
            self.igrac1.velocity_y *= -1
            self.igrac1.move()
        if (self.igrac2.x <= 0) or (self.igrac2.right >= 600):
            self.igrac2.velocity_x *= -1
            self.igrac2.move()
        if (self.igrac2.y <= 0) or (self.igrac2.top >= 908):
            self.igrac2.velocity_y *= -1
            self.igrac2.move()
        
        #Odbijanje lopte od zidova i restartanje igre u slučaju gola
        if  (self.lopta.x <= 0) or (self.lopta.right >= 600):
            self.lopta.velocity_x *= -1
            self.lopta.move()
        if (self.lopta.y <= 0):
            self.igrac2.score += 1
            self.restart
        elif (self.lopta.top >= 908):
            self.igrac1.score +=1
            self.restart

class SoccerStars(App):
    def build(self):
        igra = Igra()
        Clock.schedule_interval(igra.update, 1.0 / 60.0)
        return igra

if __name__ == "__main__":
    SoccerStars().run()

