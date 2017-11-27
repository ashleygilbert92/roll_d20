import os

accepted_list = ["cleanup.py", "encounters.PNG", "favicon.ico", "feedback.PNG",
                 "loading.gif", "play_sessions.PNG", "probability.PNG"]
dir_path = os.path.dirname(os.path.realpath(__file__))
for file in os.listdir(dir_path):
    if file not in accepted_list:
        remove_path = os.path.join(dir_path, file)
        os.remove(remove_path)
