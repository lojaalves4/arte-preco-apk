from kivy.app import App
from kivy.uix.label import Label

class ArtePreco(App):
    def build(self):
        return Label(text="Arte Preço Pro Offline - OK")

if __name__ == "__main__":
    ArtePreco().run()
