from json import load, dump
from scripts.settings import saveFileDirectory


def saveLocal(name, score):
    try:
        highscores = load(open(saveFileDirectory, "r"))
    except FileNotFoundError:
        highscores = []

    player_exists = False
    for i in highscores:
        if i['name'] == name:
            if i['score'] <= score:
                i['score'] = score
            player_exists = True
            break

    if not player_exists:
        highscores.append({"name": name, "score": score})

    dump(highscores, open(saveFileDirectory, "w"), indent=4)


def displayLocal():
    try:
        with open(saveFileDirectory, "r") as file:
            highscores = load(file)
            if len(highscores) > 0:
                highscores_sorted = sorted(
                    highscores, key=lambda x: x['score'], reverse=True)
                for i, score in enumerate(highscores_sorted, start=1):
                    print(f"{i}. {score['name']}\t: {score['score']}")
            else:
                print("no highscores yet!")
    except FileNotFoundError:
        print("file not found! check savefiles dir or settings.json")
