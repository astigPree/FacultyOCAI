import re, pickle, json, os, typing, random , datetime


def whatScreen(self, system_data : dict[str : [str , str]] , user_input : tuple[str, str] ) -> typing.Union[None , str]:
    """ Use to change screen in the main content window by checking the user input and system secured data """
    for key , values in system_data.items():
        if values[0] == user_input[0] and values[1] == user_input[1] :
            return key
    return None


def saveText(file, tag, text, header=('tags', 'text')) -> typing.NoReturn :
    folder = os.path.join(os.path.dirname(__file__), 'Training Data', file)
    if not os.path.exists(folder) :
        with open(folder, 'w') as f :
            f.write(f"{header[0]},{header[1]}\n")

    with open(folder, 'a') as f :
        f.write(f"{tag},{text}\n")


def loadNeededData(filename: str, folder=None, isBytes=False) -> dict :
    filepath = os.path.join(os.path.dirname(__file__), folder, filename) if folder else os.path.join(
        os.path.dirname(__file__), filename)
    with open(filepath, 'rb' if isBytes else 'r') as file :
        return json.load(file) if not isBytes else pickle.load(file)


def recognizeAlgo(self: object) -> typing.NoReturn :

    import ctypes
    # Prevent Windows from going to sleep
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)  # ES_CONTINUOUS | ES_SYSTEM_REQUIRED

    # threading.stack_size() # Pinaka importante sa lag

    # return  # TODO: Debugging Only For UI

    from .recognizer import AIMouth, AIEar
    ear = AIEar()
    mouth = AIMouth()

    print("[/] LOAD ALL NEEDED OBJECTS")

    # TODO: Load The Model
    model = loadNeededData('model.pkl', isBytes=True)
    print("[/] LOAD ALL NEEDED MODEL")

    # TODO: Load All Patterns
    rooms_patterns = loadNeededData('rooms_pattern.json', 'wise_data')
    persons_patterns = loadNeededData('instructors_patterns.json', 'wise_data')
    cant_find_responses = loadNeededData( 'cant_find_responses.json' , 'wise_data')
    print("[/] LOAD ALL NEEDED DATA")

    # TODO: create filename for incoming new training data
    file = f"new_data {datetime.datetime.now().strftime('%m-%d-%Y')}.csv"

    # TODO: create a loop variables
    person_found = []
    room_found = []

    print("Start Main Activity".center(40, "-"))
    while not self.stop_all_running :  # Main Loop

        self.activity.text = "LISTENING"
        # TODO: Capture the voice
        text = ear.captureVoice(holder = self)
        print(f"The text : {text}")

        if self.stop_all_running: # Use to stop the program activity
            break

        # TODO:  Check if the text is not error
        if not text :
            continue

        text = text + " "  # Add Space for identifying what room it is

        # TODO:  Check if the finding in the text using NLP and Regex Operation

        # TODO: Check if what the text means using machine learning
        predicted = model.predict([text])
        self.okeyToChangeScreen() # Use to delay the changing screen
        if predicted[0] == 1 :
            print(f"Predicted -------------------------")

            # TODO:  Check if the finding in the text

            for location, pattern in persons_patterns.items() :
                if re.findall(rf"{pattern}", text) :
                    person_found.append(location)

            if person_found :
                for person in person_found :
                    # TODO: tell the current location of instructor based on the where instructor time in
                    # Updating The UI
                    self.location_selected = person
                    while self.location_selected: # Use to wait till the screen is show then it will talk
                        pass
                    self.activity.text = "TALKING"
                    data = self.getGuestScreenData(person)
                    print(f"Person : {person}")
                    self.updateAITalking(data['directions'][0], data['directions'][1])
                    # BackEnd action
                    mouth.talk(data["directions"][0])

            for location, pattern in rooms_patterns.items() :
                if re.findall(rf"{pattern}", text) :
                    room_found.append(location)

            if room_found :
                for location in room_found :
                    # TODO: tell the current location of instructor based on the where instructor time in
                    # Updating The UI
                    self.location_selected = location
                    while self.location_selected: # Use to wait till the screen is show then it will talk
                        pass
                    self.activity.text = "TALKING"
                    data = self.getGuestScreenData(location)
                    print(f"Room : {location}")
                    self.updateAITalking(data['directions'][0], data['directions'][1])
                    # BackEnd action
                    mouth.talk(data["directions"][0])

            if not room_found and not person_found:
                response = random.sample(cant_find_responses, k=1)[0]
                self.activity.text = "TALKING"
                self.updateAITalking(response[0], response[1])
                mouth.talk(response[0])

            # Clear the findings
            person_found.clear()
            room_found.clear()

            # TODO: Save new data for new learning
            intent = "wheres"
            saveText(file, intent, text)

        else :
            # TODO: tell the user can't understand what user talking
            print(f"Not Predicted -------------------------")
            self.activity.text = "TALKING"
            self.updateAITalking(
                "My functions only guiding the location in this building, I cant understand what are you talking.", 5)
            mouth.talk("My functions only guiding the location in this building, I cant understand what are you talking")

            intent = "invalid"
            saveText(file, intent, text)

    ear.closeMicrophone()