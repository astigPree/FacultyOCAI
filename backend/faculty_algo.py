import os, pickle, json, random


def loadNeededData(filename: str, folder=None, isBytes=False) -> dict :
    filepath = os.path.join(os.path.dirname(__file__), folder, filename) if folder else os.path.join(
        os.path.dirname(__file__), filename)
    with open(filepath, 'rb' if isBytes else 'r') as file :
        return json.load(file) if not isBytes else pickle.load(file)


def screenActions(self: object) :
    action_responses = loadNeededData('faculty_actions_command.json', 'wise_data')  # Load the responses

    from .recognizer import AIMouth

    mouth = AIMouth()

    # TODO: talk for every actions make in faculty
    while not self.stop_all_running :

        if not self.algo_action :  # Do nothing if there is no actions in faculty screen
            continue

        action = self.algo_action
        self.algo_action = ""  # Set to empty after using it

        responses = action_responses.get(action, None)
        if not responses :
            print(f"Can't Find This Action : {action}")
        else :
            response = random.sample(responses, k=1)[0]

            self.updateAITalking(response[0], response[1])  # For UI
            mouth.talk(response[0])  # For Backend Action
