from kivy.uix.screenmanager import Screen



class HomeScreen(Screen):   # EOD page, Extended Care,
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def changeToEOD(self):
        self.manager.current = 'EOD'