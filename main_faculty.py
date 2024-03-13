from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivymd.uix.relativelayout import MDRelativeLayout

from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.clock import Clock

from threading import Thread
import os, pickle, json , typing , random

os.environ['KIVY_TEXT'] = 'pil' # Use to handle big font size

from content_screens import FacultyScreen, DeveloperScreen


class AIImageActions(MDRelativeLayout):
    image : str = StringProperty(os.path.join(os.path.dirname(__file__), 'pictures', 'oc robot.png'))
    action : Image = ObjectProperty(None)
    face : MDRelativeLayout = ObjectProperty(None)
    emoji : Label = ObjectProperty(None)
    info : Label = ObjectProperty(None)

    activities = {
        'sleep' : (
            ('s' , 'SLEEPING') ,("T", "STILL SLEEP" ), ('3' , "TIRED" ),
            ('z' , "WAKING UP")
        ),
        'talk' : (
            ('y' , 'HAPPY TALKING') , ('w' , 'DOUBTING') , ('l', "YOUR RIGHT"),
            ('n' , 'CORRECT') , ("7" , "HAHA") , ("L", "THAT'S RIGHT"),
            ('Z' , "MAYBE")
        ),
        'listen' : (
            ( 'O' , 'LISTENING') , ('p' , 'UNDERSTAND') , ('d' , "WOW"),
            ('h' , 'SERIOUSLY') , ('j' , "WHAT!!") , ('5' , "OKEY.."),
            ("8", "I LISTEN.") , ("E" , "SHOCK"), ("D", "BLUSH") ,
            ("F", "RIGHT"),("J", "CAN'T BELIEVE"), ("X" , "SURE?"),
            ("M" , "WHAT EVER")
        ),
        'nothing' : (
            ('4' , "NOTHING") , ( '6' , "SILENT") , ("0", "QUITE"),
            ("W", "CRAZY") , ("R", "LAUGHING"), ("U", "BLEEE") ,
            ('A', "GLAD"), ("G","GREEEE!!") , ("V", "SHHHHHH")
        )
    }
    __speed = 3
    __mood = "sleep"

    emotions = { '' : 'sleep' , 'TALKING' : 'talk' , 'LISTENING' : 'listen' , 'SILENT' : 'nothing' }

    def changeFace(self, mood : str ):

        mood = self.emotions.get(mood , None)

        if mood is None:
            return

        self.__mood = mood

    def animateFace(self , *args):
        pos = random.randint(1 , len(self.activities[self.__mood])) - 1
        emoji , info = self.activities[self.__mood][pos]
        # print(f"{self.__mood} : {pos} = {emoji},{info}")
        self.emoji.text = emoji
        self.info.text = info
        Clock.schedule_once(self.animateFace , self.__speed)


class LogInView(ModalView):
    duration = 10 # Duration of login

    username: TextInput = ObjectProperty()
    password: TextInput = ObjectProperty()

    command : callable = ObjectProperty()

    # Checking variable
    isOpen : bool = BooleanProperty(False)

    warning_label : Label = ObjectProperty(None)
    holder : object = ObjectProperty(None) # hold the parent reference

    def on_dismiss(self):
        self.isOpen = False

    def on_open(self):
        self.isOpen = True
        Thread(target=self.holder.screenActions).start()

    def displayWarningForPassword(self):
        self.warning_label.color = "red"


class ContentWindow(ScreenManager) :
    listOfScreen = { 'faculty' : FacultyScreen , 'dev' : DeveloperScreen}
    selected_screen : str = StringProperty("")

    def loading(self, *args):
        screen = self.listOfScreen['faculty'](name='faculty')
        self.selected_screen = screen.name
        self.switch_to(screen)

    def on_parent(self, *args) :
        screen = self.listOfScreen['dev'](name='dev')
        self.selected_screen = screen.name
        self.switch_to(screen)
        Clock.schedule_once(self.loading)

    def switchScreenByName(self, name : str):
        self.selected_screen = name
        current_screen = self.current_screen
        self.switch_to(self.listOfScreen[name](name=name))
        self.remove_widget(current_screen)

    def isGuestScreen(self) -> bool:
        return self.selected_screen == "guest"

    def isFacultyScreen(self) -> bool:
        return self.selected_screen == "faculty"

    def isDevScreen(self) -> bool:
        return self.selected_screen == "dev"


class MainWindow(FloatLayout) :
    display_talking_scroller : ScrollView = ObjectProperty(None)
    display_talking: Label = ObjectProperty(None)
    content: ContentWindow = ObjectProperty(None)
    activity : Label = ObjectProperty(None)
    action : AIImageActions = ObjectProperty(None)

    size_effect = NumericProperty(5.0)
    stop_all_running = BooleanProperty(False)
    __ai_talking: str = StringProperty("")

    algo_action : str = StringProperty("") # Used to identify what actions did the user do

    __instructor_data : dict = ObjectProperty(None)
    __room_data : dict = ObjectProperty(None)
    __system_data : dict = ObjectProperty(None)

    __room_filename= ( "locations_data.json", "locations_informations")
    __instructor_filename = ("instructors_data.json", "locations_informations")
    __system_filename = ("system_data.ai" , "locations_informations")

    from backend import whatScreen , screenActions

    def __init__(self , **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        # Login View Widget & Logic
        self.login = LogInView()
        self.login.command = self.changeScreen
        self.login.holder = self

    @property
    def room_filename(self) -> tuple[str , str]:
        return self.__room_filename

    @property
    def instructor_filename(self) -> tuple[str, str]:
        return self.__instructor_filename

    @property
    def facultySecurity(self) -> tuple[str , str]:
        return self.__system_data['faculty']

    @staticmethod
    def loadNeededData( filename: str, folder=None, isBytes=False) -> dict :
        filepath = os.path.join(os.path.dirname(__file__), folder, filename) if folder else os.path.join(
            os.path.dirname(__file__), filename)
        with open(filepath, 'rb' if isBytes else 'r') as file :
            return json.load(file) if not isBytes else pickle.load(file)

    @staticmethod
    def saveNewData( filename : str, data : dict, folder = None , isBytes = False):
        filepath = os.path.join(os.path.join(os.path.dirname(__file__),folder) ,filename) if folder else os.path.join(
            os.path.dirname(__file__), filename)
        with open(filepath, 'wb' if isBytes else 'w') as file :
            return json.dump(data, file, indent=4) if not isBytes else pickle.dump(data, file)

    def loadScreenData(self) :
        # TODO: Load the teachers and rooms data and System
        self.__instructor_data = self.loadNeededData(filename=self.__instructor_filename[0], folder=self.__instructor_filename[1])
        self.__room_data = self.loadNeededData(filename=self.__room_filename[0], folder=self.__room_filename[1])
        self.__system_data = self.loadNeededData(filename = self.__system_filename[0] , folder=self.__system_filename[1] , isBytes=True)

    def updateFacultySecurity(self, username : str , password : str ):
        self.__system_data['faculty'] = (username , password)
        print(self.__system_data)

    def saveImportantData(self):
        self.saveNewData(filename=self.__system_filename[0] , data=self.__system_data , folder=self.__system_filename[1] , isBytes=True)

    def on_kv_post(self, base_widget):
        self.ids['picture'].ids['picture'].source = os.path.join(os.path.dirname(__file__), 'pictures', 'building.jpg')
        self.action.animateFace()

    def close(self):
        self.stop_all_running = True

    def updateScrolling(self, interval : int):
        if self.display_talking_scroller.children[0].height > self.display_talking_scroller.height:
            self.display_talking_scroller.scroll_y = 0
        else:
            self.display_talking_scroller.scroll_y = 1

    def animateDisplayTalking(self, talking_time: int) :
        def Animate(speed: float) :
            if not len(self.__ai_talking) :
                return None

            self.display_talking.text = self.display_talking.text + self.__ai_talking[0]
            self.__ai_talking = self.__ai_talking[1 :]

            Clock.schedule_once(lambda x : Animate(speed), speed)

        try:
            speed = talking_time / len(self.__ai_talking)
        except ZeroDivisionError:
            speed = 5
        else:
            Clock.schedule_once(lambda x : Animate(speed), speed)

    def updateAITalking(self, text : str , talking_speed : int):
        # TODO: before changing the ai_talking , check if the AI is done talking by checking if the ai_talking is empty string
        self.display_talking.text = ""
        self.__ai_talking = text
        Clock.schedule_once(lambda x : self.animateDisplayTalking(int(talking_speed)))

    def changeScreen(self, username : str , password : str):
        """Use to change screen with login modal view """
        screen = self.whatScreen( self.__system_data.copy() , (username , password) )

        if not screen:
            self.login.displayWarningForPassword()
            return

        if screen == "faculty":
            self.login.dismiss()
            self.action.changeFace('SILENT')
            self.activity.text = "WATCHING"

            self.algo_action = "opening"

    # ---------------------- WRITING DATA ------------------------------

    def updateNewCommand(self, command : typing.Union[None , str]):
        if command is None or not command :
            return
        else:
            print(f"Command : {command}")
        self.__current_command = command

    def updateAIText(self, text : str):
        self.__ai_talking = text

    def doneTalking(self):
        if self.content.isGuestScreen() :
            self.content.current_screen.okeyToChangeScreen()

    # ---------------------- READING DATA ------------------------------
    @property
    def COMMAND(self) -> str:
        return self.__current_command

    def hasData(self) -> bool:
        if self.__room_data and self.__instructor_data:
            return True
        return False

    def getInstructorData(self) -> dict:
        return self.__instructor_data

    def getRoomData(self) -> dict :
        return self.__room_data

    def getCommandPattern(self) -> dict:
        return self.__commands_pattern

    def getSpecificRoom(self, key : str) -> typing.Union[dict , None]:
        for room in self.__room_data:
            if room == key:
                return self.__room_data[key]
        return None

    def getGuestScreenData(self, name : str):
        return self.content.current_screen.screens_handler.get_screen(name).getScreenInformation()



class RoomAIApp(MDApp) :

    def on_stop(self):
        self.root.close()
        self.root.saveImportantData()

        # self.profile.disable()
        # self.profile.dump_stats('oc ai.profile')
        # self.root.close()

    def on_start(self):
        # import cProfile
        # self.profile = cProfile.Profile()
        # self.profile.enable()
        Clock.schedule_once(self.root.login.open)

    def build(self) :
        Builder.load_file("faculty_design.kv")
        return Builder.load_file("design.kv")


if __name__ == "__main__" :
    LabelBase.register(name="ai_font", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'OpenSans-Semibold.ttf'))
    LabelBase.register(name="title_font" , fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'OpenSans-Bold.ttf'))
    LabelBase.register(name="content_font" , fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'OpenSans-Regular.ttf'))
    LabelBase.register(name="ai_eye" , fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'Kablokhead-xxY5.ttf'))
    LabelBase.register(name="emoji_font", fn_regular=os.path.join(os.path.dirname(__file__), 'fonts', 'GoogleEmojis-Regular.ttf'))
    try :
        RoomAIApp().run()
    except Exception as e:
        print(f"Main Error : {e.with_traceback(Exception)}")
    except RuntimeError as r:
        print(f"Runtime Error : {r.with_traceback(RuntimeError)}")
    except MemoryError as m:
        print(f"Memory Error : {m.with_traceback(MemoryError)}")
    except OverflowError as o:
        print(f"Overflow Error : {o.with_traceback(OverflowError)}")
