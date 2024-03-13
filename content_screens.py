from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton

from kivy.clock import Clock
from kivy.utils import get_color_from_hex as chex

from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, DictProperty
from datetime import datetime, time

Clock.max_iteration = 60


# ------------------------ Faculty Screens ----------------------
class FacultySettingsDropDownButton(MDFillRoundFlatButton):
    command: callable = ObjectProperty(None)

    def on_release(self) :
        self.command(self.text)


class SettingPasswordForm(MDBoxLayout):
    username: TextInput = ObjectProperty(None)
    password: TextInput = ObjectProperty(None)

    def comparison(self, passed_username : str , passed_password : str) -> bool:
        if self.username.text == passed_username and passed_password == self.password.text:
            return True
        return False

    def clearInput(self):
        self.username.text = ""
        self.password.text = ""


class FacultyDropDownButton(MDFillRoundFlatButton) :
    command: callable = ObjectProperty(None)

    def on_release(self) :
        self.command(self.text)


class FacultyWarningActionsModalView(ModalView) :
    isUsedToDisplay: bool = BooleanProperty(False)  # Used to check if the modal is used for displaying only or not

    text_displayer: Label = ObjectProperty(None)

    proceed_text : str = StringProperty("PROCCED")
    cancelText: str = StringProperty("CANCEL")

    command: callable = ObjectProperty(None)

    def displayError(self, text_error: str) :
        # TODO: Display the text_error
        self.text_displayer.text = text_error
        self.text_displayer.halign = "center"
        self.isUsedToDisplay = True
        self.cancelText = "CLOSE"
        self.open()

    def displayAddingSchedule(self, start_time: str, end_time: str, room: str, command: callable) :
        self.isUsedToDisplay = False
        self.text_displayer.text = f"Do You Want to add this schedule? \nTime : {start_time} \nTime : {end_time} \nRoom : {room}"
        self.text_displayer.halign = "left"
        self.command = command
        self.proceed_text = "ADD"
        self.open()

    def displayUnfinishedTransactionInTeacherScreen(self, command : callable):
        self.isUsedToDisplay = False
        self.text_displayer.text = f"There is currently Unfinished activities in current screen.\nDo you want to disregard it and continue?"
        self.text_displayer.halign = "left"
        self.proceed_text = "PROCEED"
        self.command = command
        self.open()

    def on_dismiss(self):
        self.text_displayer.text = ""
        self.text_displayer.halign = "center"
        self.isUsedToDisplay = True
        self.cancelText = "CLOSE"
        self.proceed_text = ""
        self.command = ObjectProperty(None)

    def displayResetScheduleWarning(self, command : callable):
        self.isUsedToDisplay = False
        self.text_displayer.text = f"Do you want to clear all the past save schedule and the current schedule created?"
        self.text_displayer.halign = "left"
        self.proceed_text = "PROCEED"
        self.command = command
        self.open()

    def displayApplyingChanges(self, command : callable ):
        self.isUsedToDisplay = False
        self.text_displayer.text = "Do you want to save the new changes in this screen?"
        self.text_displayer.halign = "left"
        self.proceed_text = "APPLY CHANGES"
        self.command = command
        self.open()

    def displayInfoBeforeExiting(self, command : callable):
        self.isUsedToDisplay = False
        self.text_displayer.text = f"Do you want to start the activity of guest inqueries handling? If you want to just click the \'GOTO MAIN SCREEN\' to go back to main screen where the activities executed."
        self.text_displayer.halign = "center"
        self.proceed_text = "GOTO MAIN SCREEN"
        self.command = command
        self.open()

    def displaySavingNewFacultySecurity(self , command : callable):
        self.isUsedToDisplay = False
        self.text_displayer.text = "There is no turning BACK, by changing the system when the faculty member who will enter this screen must use the new security such as USERNAME and PASSWORD. Do you agree the changes of the system security?"
        self.text_displayer.halign = "left"
        self.proceed_text = "I AGREE"
        self.cancelText = "I DON'T AGREE"
        self.command = command
        self.open()


class FacultySelectionLocationDropdownContent(MDBoxLayout) :
    pass


class AddFacultyScheduleModalViewTimeSelections(Widget) :
    holder: BoxLayout = ObjectProperty(None)

    time_start: time = ObjectProperty(None)
    time_end: time = ObjectProperty(None)

    def __init__(self, **kwargs) :
        super(AddFacultyScheduleModalViewTimeSelections, self).__init__(**kwargs)
        self.start_time_picker = MDTimePicker(
            primary_color="brown",
            accent_color="white",
            text_button_color="white", )
        self.end_time_picker = MDTimePicker(
            primary_color="brown",
            accent_color="white",
            text_button_color="white", )

        # Customize the input
        self.start_time_picker.bind(on_save=self.get_start_time)
        self.end_time_picker.bind(on_save=self.get_end_time)

    def get_start_time(self, timer: MDTimePicker, selected_time: time) :
        self.holder.start_time = f"{int(timer.hour):02d}:{int(timer.minute):02d} {str(timer.am_pm).upper()}"
        self.time_start = selected_time

    def get_end_time(self, timer: MDTimePicker, selected_time: time) :
        self.holder.end_time = f"{int(timer.hour):02d}:{int(timer.minute):02d} {str(timer.am_pm).upper()}"
        self.time_end = selected_time

    def checkingIfCorrectSelectionOfTime(self) -> tuple[bool, str] :
        print(f"{self.time_start} >= {self.time_end}")
        if not self.time_end or not self.time_start :
            return False, "Please fill up or select the requested time"

        if self.time_start >= self.time_end :
            return False, "The starting time is greater than end time"

        return True, ""


class AddFacultyScheduleModalView(ModalView) :
    location_dropdown: MDFillRoundFlatButton = ObjectProperty()
    dropdown_list = DropDown()

    day_selection : MDFillRoundFlatButton = ObjectProperty()
    days_dropdown_list = DropDown()

    time_selections: AddFacultyScheduleModalViewTimeSelections = ObjectProperty(None)
    start_time: str = StringProperty("SELECT TIME")
    end_time: str = StringProperty("SELECT TIME")

    isUsedAlready: bool = BooleanProperty(False)

    holder: Screen = ObjectProperty(None)

    numberOfUsed = 0

    def on_kv_post(self, base_widget):
        self.time_selections = AddFacultyScheduleModalViewTimeSelections()
        self.time_selections.holder = self

    def changeLocation(self, location: str) :
        self.location_dropdown.text = location
        self.dropdown_list.dismiss()

    def changeDay(self, day : str):
        self.day_selection.text = day
        self.days_dropdown_list.dismiss()

    def updatingNewSchedule(self) :
        isCorrect, result = self.time_selections.checkingIfCorrectSelectionOfTime()

        if not isCorrect :
            self.holder.warning.displayError(result)
        elif self.location_dropdown.text == "Select Location" :
            self.holder.warning.displayError("Please specify what room you want to stay-in for the time being")
        elif self.day_selection.text == "Select Day" :
            self.holder.warning.displayError("Please specify what day you want to stay-in for the time being")
        else :
            def command():
                schedule_json =  f"{self.time_selections.time_start}-{self.time_selections.time_end}"
                day = self.day_selection.text
                room_schedule = self.holder.parent.parent.parent.getKeyByRoomName(self.location_dropdown.text)
                self.holder.addSchedule(schedule = schedule_json , day = day, room_schedule = room_schedule)
                self.closeModal()
                # self.holder.warning.command = None

            self.holder.warning.displayAddingSchedule(self.start_time, self.end_time, self.location_dropdown.text,
                                                      command)

    def closeModal(self) :
        self.start_time = "SELECT TIME"
        self.end_time = "SELECT TIME"
        self.location_dropdown.text = "Select Location"
        self.day_selection.text = "Select Day"

        self.dismiss()

    def on_open(self) :
        if not self.isUsedAlready :
            # TODO: Get the locations in the parents and display it in the dropdown list
            rooms = self.holder.parent.parent.parent.getAllRooms()  # TeachersScreen > ScreenManager > BoxLayout > FacultyScreen
            content_box = FacultySelectionLocationDropdownContent()
            for room in rooms :
                dropButton = FacultyDropDownButton(text=room)
                dropButton.command = self.changeLocation

                content_box.add_widget(dropButton)

            self.dropdown_list.clear_widgets()
            self.dropdown_list.add_widget(content_box)

            content_box = FacultySelectionLocationDropdownContent()
            for day in self.holder.days:
                dropButton = FacultyDropDownButton(text = day)
                dropButton.command = self.changeDay

                content_box.add_widget(dropButton)

            self.days_dropdown_list.clear_widgets()
            self.days_dropdown_list.add_widget(content_box)
            print(f"Happen in {self.holder.teacher_key}")

            self.isUsedAlready = True


class ChangeFacultyInfoModalView(ModalView) :
    teacher_name: TextInput = ObjectProperty(None)
    teacher_info: TextInput = ObjectProperty(None)

    holder: object = ObjectProperty(None)

    updateInfo: callable = ObjectProperty(None)

    def on_pre_open(self) :
        self.teacher_name.text = self.holder.teacher_name.text
        self.teacher_info.text = self.holder.teacher_info.text

    def updateParentInfo(self) :
        self.updateInfo(self.teacher_name.text, self.teacher_info.text)
        self.dismiss()


class ScheduleContainer(BoxLayout) :
    room: str = StringProperty('')
    schedule: str = StringProperty('')
    day : str = StringProperty('')

    deleteSchedule: callable = ObjectProperty(None)

    json_schedule = ""
    room_schedule = ""

    def updateOnCreate(self, data_info: str, room: str, schedule: str , day : str ) :
        self.json_schedule = data_info
        self.room_schedule = room
        self.room = room.upper()
        self.day = day

        schedule_1, schedule_2 = schedule.split("-")
        schedule_1 = datetime.strptime(schedule_1, "%H:%M:%S")
        schedule_1 = schedule_1.strftime("%I:%M %p")
        schedule_2 = datetime.strptime(schedule_2, "%H:%M:%S")
        schedule_2 = schedule_2.strftime("%I:%M %p")

        self.schedule = f"{schedule_1} - {schedule_2}"


class SettingScreen(Screen):

    isSettings: bool = BooleanProperty(True)

    warning : FacultyWarningActionsModalView = ObjectProperty(None)
    dropdown_button : MDFillRoundFlatButton = ObjectProperty(None)
    data_warning : Label = ObjectProperty(None)
    data_input : TextInput = ObjectProperty(None)
    room_picture : Image = ObjectProperty(None)
    dropdown_list : DropDown = ObjectProperty(None)

    past_security : SettingPasswordForm = ObjectProperty(None)
    new_security : SettingPasswordForm = ObjectProperty(None)

    __room_data : dict = DictProperty({})

    __past_text : str = StringProperty("sdfsd") # Use to check if there is edited happen in textbox
    __selected_room : dict = DictProperty({})

    def on_kv_post(self, base_widget):
        self.warning = FacultyWarningActionsModalView()

    def applyChanges(self):
        # Check if okey to save
        room_key = None
        for key in self.__room_data:
            if self.__room_data[key]['name'] == self.dropdown_button.text:
                room_key : str = key
                break

        if not room_key or self.__past_text == self.data_input.text:
            return

        # Update the room data
        self.__selected_room['brief information'][0] = self.data_input.text

        def command():
            self.parent.parent.parent.applyChanges( room_key, self.__selected_room , True)
            self.data_warning.text = "Successfully saved the new information about the room!"
            self.data_warning.color = chex('0da22e')
            self.warning.dismiss()

        self.warning.displayApplyingChanges(command)

    def changeScreenSecurity(self):
        username, password = self.parent.parent.parent.getSecurity()
        if not self.past_security.comparison(username , password):
            self.warning.displayError("The past security does not matches the faculty system security!")
            return

        def command():
            self.parent.parent.parent.changeSecurity(self.new_security.username.text , self.new_security.password.text )
            self.past_security.clearInput()
            self.new_security.clearInput()
            self.warning.dismiss()

        self.warning.displaySavingNewFacultySecurity(command)

    def checkChanges(self, *args):
        if not self.__past_text:
            return
        if self.__past_text != self.data_input.text:
            self.data_warning.text = "Currently there is a changes in the data, save it!"
            self.data_warning.color = chex('bf0a10')

    def initializedData(self, *args):

        if self.dropdown_list:
            return
        self.__room_data = self.parent.parent.parent.room_data

        self.dropdown_list = DropDown()
        content_box = FacultySelectionLocationDropdownContent()

        for room in self.__room_data:
            dropButton = FacultySettingsDropDownButton(text=self.__room_data[room]['name'])
            dropButton.command = self.changeRoom
            content_box.add_widget(dropButton)
        self.dropdown_list.add_widget(content_box)

    def on_enter(self, *args):
        Clock.schedule_once(self.initializedData)

    def changeRoom(self , name : str):
        self.dropdown_button.text = name
        self.dropdown_list.dismiss()

        def command(*args):
            for key , values in self.__room_data.items():
                if values['name'] == name:
                    self.__past_text = values['brief information'][0]
                    self.data_input.text = values['brief information'][0]
                    self.__selected_room = values
                    self.data_warning.text = ""
                    self.room_picture.source = values['building picture']
                    break
        Clock.schedule_once(command )

    def goBackToMainScreen(self):
        def command():
            self.warning.dismiss()
            self.parent.parent.parent.changeToGuestScreen()
        self.warning.displayInfoBeforeExiting(command)


class TeachersScreen(Screen) :

    isSettings : bool = BooleanProperty(False)

    teacher_schedule: MDGridLayout = ObjectProperty(None)
    teacher_image: Image = ObjectProperty(None)
    teacher_name: Label = ObjectProperty(None)
    teacher_info: Label = ObjectProperty(None)

    teacher_data: dict = DictProperty({})
    teacher_key: str = StringProperty("")

    days = ( "MONDAY" , "TUESDAY" , "WEDNESDAY" , "THURSDAY" , "FRIDAY" , "SATURDAY", "SUNDAY" )

    change_faculty_info : ChangeFacultyInfoModalView = ObjectProperty()
    add_schedule : AddFacultyScheduleModalView = ObjectProperty()
    warning : FacultyWarningActionsModalView = ObjectProperty()

    new_added_schedule : dict = DictProperty({})
    removed_schedules : dict = DictProperty({})

    def on_kv_post(self, base_widget):
        self.change_faculty_info = ChangeFacultyInfoModalView()
        self.add_schedule = AddFacultyScheduleModalView()
        self.warning = FacultyWarningActionsModalView()

        self.change_faculty_info.holder = self
        self.change_faculty_info.updateInfo = self.updateNameAndInfo
        self.add_schedule.holder = self
        # self.warning.holder = self

    def updateDisplay(self, data: dict) :
        # Update the display contain in schedule of each teacher
        self.teacher_info.text = data['information']
        self.teacher_image.source = data['picture']
        self.teacher_name.text = data['person']

        # For debugging
        # if data['person'] == "Justine Aban" :
        #     print(f"Aban Locations : {data['locations']}")

        self.teacher_schedule.clear_widgets()  # Clear the display widgets
        for room in data['locations'] :
            for schedule_time in data['locations'][room] :
                container = ScheduleContainer()
                schedule, day = schedule_time.split("/")
                container.updateOnCreate(schedule_time, room, schedule , self.days[int(day)])
                container.deleteSchedule = self.removeSchedule
                self.teacher_schedule.add_widget(container)

        # TODO: Update the schedule screen
        self.teacher_data = data

    def isThereAnyChanges(self) -> bool:
        if self.new_added_schedule:
            return True
        if self.removed_schedules:
            return True
        if self.teacher_data['person'] != self.teacher_name.text:
            return True
        if self.teacher_data['information'] != self.teacher_info.text:
            return True

        return False

    def removeSchedule(self, schedule_object : ScheduleContainer ) :
        json_schedule = schedule_object.json_schedule
        room_schedule = schedule_object.room_schedule

        if room_schedule in self.removed_schedules:
            self.removed_schedules[room_schedule].append(json_schedule)
        else:
            self.removed_schedules[room_schedule] = [json_schedule,]

        self.teacher_schedule.remove_widget(widget=schedule_object)

    def updateNameAndInfo(self, name: str, info: str) :
        self.teacher_info.text = info if len(info) else self.teacher_info.text
        self.teacher_name.text = name if len(name) else self.teacher_name.text

    def resetSchedule(self) :
        for key, item in self.teacher_data.items():
            if key in self.removed_schedules:
                self.removed_schedules[key].append(item)
            else:
                self.removed_schedules[key] = [item,]
        self.teacher_data['locations'] = {}
        self.teacher_schedule.clear_widgets()
        self.warning.dismiss()

    def addSchedule(self, schedule: str, day : str, room_schedule: str) :
        data_info = f"{schedule}/{self.days.index(day)}"
        if room_schedule in self.new_added_schedule:
            self.new_added_schedule[room_schedule].append(data_info)
        else:
            self.new_added_schedule[room_schedule] = [data_info,]

        container = ScheduleContainer()
        container.updateOnCreate(data_info, room_schedule, schedule, day)
        container.deleteSchedule = self.removeSchedule
        self.teacher_schedule.add_widget(container)
        self.add_schedule.closeModal()
        self.warning.dismiss()

    def applyChanges(self):
        self.teacher_data["person"] = self.teacher_name.text
        self.teacher_data["information"] = self.teacher_info.text

        for key, values in self.removed_schedules.items(): # Use to filter and remove the past value
            self.teacher_data["locations"][key] = [value for value in self.teacher_data["locations"].get(key, []) if value not in values]
        self.teacher_data["locations"] = {key : self.new_added_schedule.get(key, []) + self.teacher_data["locations"].get(key, []) for key in set(self.new_added_schedule) | set(self.teacher_data["locations"])}

        self.new_added_schedule.clear()
        self.removed_schedules.clear()
        self.parent.parent.parent.applyChanges( self.teacher_key, self.teacher_data )
        self.warning.dismiss()

    def disregardActivities(self , changeCommand : callable, screen_name : str):
        def command():
            self.removed_schedules.clear()
            self.new_added_schedule.clear()
            self.warning.dismiss()
            changeCommand(screen_name)
        self.warning.displayUnfinishedTransactionInTeacherScreen(command=command)

    def resetScheduleWarning(self):
        if self.teacher_schedule.children:
            self.warning.displayResetScheduleWarning(self.resetSchedule)

    def applyChangesWarning(self):
        if self.isThereAnyChanges():
            self.warning.displayApplyingChanges(self.applyChanges)


class NavigationButton(Button) :
    activity: callable = ObjectProperty(None)
    activity_colors = {
        "selected" : (chex("ddacae"), "black"),
        "unselected" : (chex("620609"), "white")
    }

    isSelected: bool = BooleanProperty(False)
    name: str = StringProperty("")

    def command(self) :
        if self.activity :
            self.activity(self.name)


class FacultyScreen(Screen) :
    navigation_buttons: MDGridLayout = ObjectProperty(None)
    navigation_screens: ScreenManager = ObjectProperty(None)

    room_data: dict = ObjectProperty()
    instructor_data: dict = ObjectProperty()

    current_screen: str = StringProperty("")
    list_of_screens: dict[str, TeachersScreen] = DictProperty({})

    exit_command : callable = ObjectProperty() # Use to exit the

    warning_view : FacultyWarningActionsModalView = ObjectProperty()

    def on_kv_post(self, base_widget):
        self.warning_view = FacultyWarningActionsModalView()

    def getSecurity(self) -> tuple[str, str]:
        return self.parent.parent.facultySecurity

    def changeSecurity(self, new_username : str , new_password : str):
        self.parent.parent.updateFacultySecurity(new_username , new_password)

    def applyChanges(self , key : str , new_data : dict , isRoom = False):
        if isRoom:
            self.room_data[key] = new_data
            filename, folder = self.parent.parent.room_filename
            self.parent.parent.saveNewData(filename=filename , data=self.room_data , folder=folder)
        else:
            self.instructor_data[key] = new_data
            filename , folder = self.parent.parent.instructor_filename
            self.parent.parent.saveNewData(filename=filename , data=self.instructor_data , folder=folder)
            self.update_navigation_content()

    def displayWindow(self, *args):
        if self.parent :

            self.exit_command = self.parent.switchScreenByName

            if not self.parent.parent.hasData() :  # Check if MainWindow hold the data already
                self.parent.parent.loadScreenData()

            self.room_data = self.parent.parent.getRoomData()
            self.instructor_data = self.parent.parent.getInstructorData()

            self.navigation_buttons.clear_widgets()

            # Create Settings Screen
            settings_screen = SettingScreen()
            self.list_of_screens["setting"] = settings_screen
            # Creating Navigation Button
            navBut = NavigationButton()
            navBut.text = "S E T T I N G S"
            navBut.activity = self.changeScreen
            navBut.name = 'setting'
            self.navigation_buttons.add_widget(navBut)

            for key, values in self.instructor_data.items() :

                # Creating Navigation Button
                navBut = NavigationButton()
                navBut.text = values["person"]
                navBut.activity = self.changeScreen
                navBut.name = key
                self.navigation_buttons.add_widget(navBut)

                # Checking if it has screen used
                if not self.current_screen :
                    # Creating Navigation Screen
                    screen = TeachersScreen(name=key)
                    screen.teacher_key = key
                    screen.updateDisplay(values)
                    self.list_of_screens[key] = screen
                    self.changeScreen(key)

            self.update()

    def on_enter(self, *args) :
        self.displayWindow()

    def getKeyByRoomName(self , room : str ) -> str :
        for key in self.room_data:
            if self.room_data[key]['name'] == room:
                return key

    def getAllRooms(self) -> tuple[str, ...] :
        return tuple(self.room_data[room]['name'] for room in self.room_data)

    def update(self , *args) :
        for child in self.navigation_buttons.children :
            if child.name == self.current_screen :
                child.isSelected = True
            else :
                if child.isSelected :
                    child.isSelected = False

    def changeScreen(self, name: str) :
        # This 3 lines here use to identify if there is any changes in the data of the instructor
        if self.navigation_screens.current_screen:
            if not self.navigation_screens.current_screen.isSettings:
                # Check if there is any changes
                if self.navigation_screens.current_screen.isThereAnyChanges() :
                    # Check if the selected screen is same as clicked
                    if self.current_screen == name :
                        return
                    self.navigation_screens.current_screen.disregardActivities(self.changeScreen , name)
                    return

        self.current_screen = name
        self.update() # Update the navigation's button
        # Check if the screen exist before changing
        if name in self.list_of_screens:
            if not self.list_of_screens[name].isSettings:
                self.list_of_screens[name].updateDisplay(self.instructor_data[name])
        else:
            screen = TeachersScreen(name =name)
            screen.teacher_key = name
            screen.updateDisplay(self.instructor_data[name])
            self.list_of_screens[name] = screen

        print(f"Exist {name}: {name in self.list_of_screens}")
        self.navigation_screens.switch_to(self.list_of_screens[name])
        self.update_navigation_content()

    def update_navigation_content(self) :
        for nav_button in self.navigation_buttons.children :
            if nav_button.text == "S E T T I N G S":
                continue
            nav_button.text = self.instructor_data[nav_button.name]['person']

    def changeToGuestScreen(self):
        if not self.parent:
            return

        self.parent.switchScreenByName("guest")



# ------------------------ Developer Screens ----------------------

class DeveloperScreen(Screen) :
    pass
