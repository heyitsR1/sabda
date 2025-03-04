from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import requests
import random
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from threading import Thread


def pick_word(n, length, frequency):
    all_words = []
    i = 0
    for i in range(0, n):
        freq = 0
        found = False
        while freq < frequency or not found:
            api1_url = f"https://random-word-api.herokuapp.com/word?number=1&length={length}&lang=en"
            response = requests.get(api1_url).json()  # word as a list
            word = response[0]
            # second api to get frequency, or how popular the word is
            try:
                api2_url = f"https://api.datamuse.com/words?sp={word}&md=f&max=1"
                response2 = requests.get(api2_url).json()
                freq = (
                    0.0 if len(response2) == 0 else float(response2[0]["tags"][0][2:]) #just the way API returns things
                )
                found = True
            # just the way API returns things, you can print(response) to further understand
            # print (word,freq)
            except:
                found = False
            meaning_is = meaning(word)
            if meaning_is == "not found":
                found = False
            # print(word,freq,found,meaning_is)
        all_words.append(word)
    return all_words


def meaning(word):
    # third api to get definition
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(api_url).json()
        meaning = response[0]["meanings"][0]["definitions"][0]["definition"]
        # read the api call, this gives the first meaning
        return meaning
    except:
        return "not found"


def jumble(word):
    word_list = list(word)
    random.shuffle(word_list)
    jumbled_word = " ".join(word_list)
    return jumbled_word


def update_cache(difficulty):
    global cache
    if not cache[difficulty]:
        match difficulty:
            case "Easy":
                # print("filling in")
                cache["Easy"] = pick_word(5, 5, 1)
            case "Try-Hard":
                # print("filling in x2")
                cache["Try-Hard"] = pick_word(5, 6, 0.5)
            case "God-Mode":
                # print("filling in x3")
                cache["God-Mode"] = pick_word(5, 7, 0.3)
            case _:
                cache["Easy"] = pick_word(5, 5, 1)


app = Flask("__name__")
app.secret_key = "secret key"
words = []
db = SQL("sqlite:///final.db")
answered = 0
difficulty = None
score = 0
high_score = 0
name = None
cache = {
    "Easy": [],
    "Try-Hard": [],
    "God-Mode": [],
}

#update_cache("Easy")
update_cache("Try-Hard")
#update_cache("God-Mode")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    name = request.form.get("name")
    names = db.execute("SELECT name FROM users")
    password = request.form.get("password")
    password_confirmation = request.form.get("password_confirmation")
    for x in range(0, len(names)):
        if name == names[x]["name"]:
            error_name = "Unavailable username. Try a different one"
            return redirect(url_for("apology", error=error_name))
    if not name or len(name) < 2:
        error_name = "Invalid username. Try a different one"
        return redirect(url_for("apology", error=error_name))
    if password != password_confirmation:
        error_name = "Passwords dont match"
        return redirect(url_for("apology", error=error_name))
    hashed = generate_password_hash(password)
    db.execute("INSERT INTO users (name,hashed_password) VALUES (?,?)", name, hashed)
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    global name
    if request.method == "GET":
        return render_template("login.html")
    else:
        name = request.form.get("name")
        password = request.form.get("password")
        try:
            hash = db.execute("SELECT hashed_password FROM users WHERE name = ?", name)
            uid = db.execute("SELECT id FROM users WHERE name = ?", name)
            hash_is = hash[0]["hashed_password"]  # selecting from a list
        except:
            hash_is = "Empty"  # user doesn't exist
        match = check_password_hash(hash_is, password)
        session["user_id"] = uid
        if match is True:
            return render_template("settings.html")
        error = "Username/Password Error"
    return render_template("apology.html", error_name=error)


@app.route("/apology")
def apology():
    error = request.args.get("error")
    return render_template("apology.html", error_name=error)


@app.route("/game", methods=["POST", "GET"])
def doall():
    global words
    global answered
    global difficulty
    global score
    if request.method == "GET":
        answered = 0
        score = 0
        difficulty = request.args.get("difficulty")
        words = cache[difficulty]
        cache[difficulty] = []  # empty cache for difficulty key
        # print(words)
        if not words:
            error = "Loading words takes a lot of magic, please choose a different mode while we fill up"
            return render_template("apology.html", error_name=error)
        session["question_number"] = 0
        hint = meaning(words[session["question_number"]])
        Thread(target=update_cache, args=(difficulty,)).start()  # tuple things?
        return render_template(
            "test.html",
            word=jumble(words[session["question_number"]]),
            hint=hint,
            difficulty=difficulty,
        )
    if request.method == "POST":
        data = request.get_json()
        answer = data.get("answer")
        status = "Incorrect"
        if session["question_number"] < len(words):
            current_word = words[session["question_number"]]
        else:
            current_word = "complete"
        if answer == current_word and session["question_number"] < len(words):
            answered += 1
            match difficulty:
                case "Easy":
                    score += 100
                case "Try-Hard":
                    score += 150
                case "God-Mode":
                    score += 200
                case _:
                    score += 100
            # print(f"score is {score}")
            status = "Correct"
            if session["question_number"] == (
                len(words) - 1
            ):  # we are at the very last question
                new_question = "Complete"
                hint = "Complete"
                current_word = "complete"
                session[
                    "question_number"
                ] += 1  # this is shitty verbose code but basically passing filler parameters to not cause errors
            elif session["question_number"] < len(words) - 1:
                session["question_number"] += 1
                new_question = jumble(words[session["question_number"]])
                hint = meaning(words[session["question_number"]])
            else:
                new_question = "GameOver"  # just filler, status is incorrect
                hint = "GameOver"
        elif current_word == "complete":
            new_question = "Complete"
            hint = "Complete"
        else:
            # print(f"answer is {answer}")
            new_question = "GameOver"  # just filler, status is incorrect
            hint = "GameOver"

        return jsonify(
            {
                "new_question": new_question,
                "status": status,
                "hint": hint,
                "question_number": session["question_number"],
            }
        )


@app.route("/gameover")
def gameover():
    global name, high_score, score
    # print(words[session["question_number"]])
    # print(score,high_score)
    if score > high_score:
        high_score = score
        db.execute("UPDATE users SET high_score = ? where name = ?", high_score, name)
    return render_template(
        "gameover.html",
        word=words[session["question_number"]],
        meaning=meaning(words[session["question_number"]]),
        score=score,
    )


@app.route("/complete")
def complete():
    global score, high_score
    # print(words[session["question_number"]])
    # print(score,high_score)
    if score > high_score:
        high_score = score
        db.execute(
            "UPDATE users SET high_score = ? where id = ?",
            high_score,
            session["user_id"][0]["id"],
        )
    return render_template("complete.html", score=score, high_score=high_score)


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/leaderboards", methods=["POST", "GET"])
def leaderboards():
    list = db.execute(
        "SELECT name,high_score FROM users ORDER BY high_score DESC LIMIT 10"
    )
    try:
        p = db.execute(
            "SELECT name FROM users WHERE id = ?", session["user_id"][0]["id"]
        )
        player = p[0]["name"]
    except KeyError:
        player = None
    return render_template("leaderboards.html", list=list, player=player)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
