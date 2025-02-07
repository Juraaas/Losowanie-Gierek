import os
from flask import Flask, render_template, request, jsonify, Response
from functools import wraps
import random

app = Flask(__name__)

USERNAME = os.getenv("AUTH_USERNAME")
PASSWORD = os.getenv("AUTH_PASSWORD")

games = [
    {"nazwa": "Siedem cudów pojedynek", "typ": ["Versus"], "players": [2], "dlugosc": [30, 45]},
    {"nazwa": "Gejsze", "typ": ["Versus", "Przekminy", "Luzne"], "players": [2], "dlugosc": [15, 30]},
    {"nazwa": "Gejsze 2", "typ": ["Strategiczne", "Versus"], "players": [2], "dlugosc": [15, 30]},
    {"nazwa": "Cięcie", "typ": ["Deckbuilding", "Versus"], "players": [2,3,4,5], "dlugosc": [45, 60]},
    {"nazwa": "Eter", "typ": ["Luzne", "Karciane", "Strategiczne", "Versus"], "players": [2], "dlugosc": [15, 30]},
    {"nazwa": "Stwory z obory", "typ": ["Deckbuilding", "Karciane", "OFA"], "players": [2,3,4,5], "dlugosc": [30, 45]},
    {"nazwa": "DBD", "typ": ["Coop", "Przekminy", "Strategiczne"], "players": [3,4,5], "dlugosc": [90, 120]},
    {"nazwa": "Nokaut", "typ": ["Karciane", "Strategiczne"], "players": [2,4], "dlugosc": [30, 45]},
    {"nazwa": "Sen", "typ": ["Luzne", "Karciane"], "players": [2,3,4,5], "dlugosc": [15, 30]},
    {"nazwa": "Mindbug", "typ": ["Karciane", "Versus"], "players": [2], "dlugosc": [15, 30]},
    {"nazwa": "Bang!", "typ": ["Karciane", "OFA", "Towarzyskie", "Alkoholowe"], "players": [4,5,6], "dlugosc": [30, 45]},
    {"nazwa": "W pył zwrot", "typ": ["Karciane", "Strategiczne", "Luzne"], "players": [3,4,5,6], "dlugosc": [30, 45]},
    {"nazwa": "Tajniacy", "typ": ["Coop", "Przekminy", "Towarzyskie", "Luzne", "Karciane"], "players": [4,5,6], "dlugosc": [30, 45]},
    {"nazwa": "Spór o bór 2", "typ": ["Versus", "Karciane", "Strategiczne"], "players": [2], "dlugosc": [15, 30]},
    {"nazwa": "Kotki", "typ": ["Luzne", "Karciane", "Towarzyskie", "Alkoholowe", "OFA"], "players": [3,4,5,6], "dlugosc": [15, 30]},
    {"nazwa": "Carcassonne", "typ": ["Luzne", "Strategiczne"], "players": [2,3,4,5], "dlugosc": [30, 45]},
    {"nazwa": "Craftsmen", "typ": ["Przekminy", "Ekonomia", "Deckbuilding"], "players": [2,3,4,5], "dlugosc": [120, 150]},
    {"nazwa": "Podaj dalej", "typ": ["Luzne", "Towarzyskie"], "players": [4,5,6], "dlugosc": [30, 45]},
    {"nazwa": "Leśne rozdanie", "typ": ["Deckbuilding", "Karciane", "Przekminy", "Ekonomia"], "players": [2,3,4], "dlugosc": [60, 120]},
    {"nazwa": "Warchest", "typ": ["Strategiczne", "Versus"], "players": [2,4], "dlugosc": [45, 60]},
    {"nazwa": "Ryzyko", "typ": ["OFA", "Ekonomia", "Strategiczne"], "players": [3,4,5], "dlugosc": [90, 120]},
    {"nazwa": "Arnak", "typ": ["Przekminy", "Ekonomia"], "players": [2,3,4], "dlugosc": [90, 120]},
    {"nazwa": "Wojny klonów", "typ": ["Coop", "Przekminy", "Strategiczne"], "players": [2,3,4,5], "dlugosc": [90, 120]},
    {"nazwa": "Karak", "typ": ["Strategiczne", "OFA", "Deckbuilding"], "players": [2,3,4,5], "dlugosc": [45, 60]},
    {"nazwa": "Terraformacja Marsa", "typ": ["Przekminy", "Deckbuilding", "Ekonomia", "Strategiczne"], "players": [2,3,4,5], "dlugosc": [90, 120]},
    {"nazwa": "Szachy", "typ": ["Przekminy", "Versus", "Strategiczne"], "players": [2], "dlugosc": [30, 45]},
    {"nazwa": "Slay the spire", "typ": ["Deckbuilding", "Strategiczne", "Coop"], "players": [2,3,4], "dlugosc": [120, 150]},
    {"nazwa": "Wiedźmin", "typ": ["Coop", "Karciane", "OFA", "Deckbuilding", "Strategiczne"], "players": [2,3,4], "dlugosc": [120, 150]},
    {"nazwa": "Catan", "typ": ["Przekminy", "Ekonomia", "Strategiczne"], "players": [2,3,4,5], "dlugosc": [90, 120]},
    {"nazwa": "Monopoly", "typ": ["Ekonomia", "OFA", "Luzne"], "players": [2,3,4,5,6], "dlugosc": [90, 120]},
    {"nazwa": "Na skrzydłach", "typ": ["Przekminy", "Ekonomia", "Deckbuilding"], "players": [2,3,4], "dlugosc": [60, 90]},
    {"nazwa": "Zaklinacze cienia", "typ": ["OFA", "Strategiczne", "Ekonomia"], "players": [2,3,4], "dlugosc": [45, 60]},
    {"nazwa": "Ekosystem", "typ": ["Deckbuilding", "Przekminy", "Karciane"], "players": [2,3,4,5], "dlugosc": [15, 30]},
    {"nazwa": "Ekosystem 2", "typ": ["Deckbuilding", "Przekminy", "Karciane"], "players": [2,3,4,5], "dlugosc": [15, 30]},
    {"nazwa": "Ekosystem 3", "typ": ["Deckbuilding", "Przekminy", "Karciane"], "players": [2,3,4,5], "dlugosc": [15, 30]},
    {"nazwa": "Card Wars", "typ": ["Coop", "Deckbuilding", "Strategiczne", "Karciane"], "players": [2,4], "dlugosc": [60, 120]},
    {"nazwa": "Latające Burrito", "typ": ["Luzne", "Alkoholowe", "Towarzyskie", "OFA"], "players": [3,4,5,6], "dlugosc": [15, 30]},
    {"nazwa": "Qwirkle", "typ": ["Przekminy", "Luzne"], "players": [2,3,4], "dlugosc": [30, 60]},
    {"nazwa": "Karty Dżentelmenów", "typ": ["Luzne", "Karciane", "Towarzyskie", "Alkoholowe"], "players": [4,5,6], "dlugosc": [30, 45]},
    {"nazwa": "Mikstura", "typ": ["Luzne", "Karciane", "Alkoholowe", "Towarzyskie", "OFA"], "players": [4,5,6], "dlugosc": [15, 30]},
    {"nazwa": "Jednorożce", "typ": ["Luzne", "Karciane", "OFA", "Deckbuilding", "Strategiczne"], "players": [2,3,4,5,6], "dlugosc": [45, 60]},
    {"nazwa": "Sabotażysta", "typ": ["Luzne", "Karciane", "Coop", "Towarzyskie", "OFA", "Przekminy"], "players": [3,4,5,6], "dlugosc": [60, 120]},
    {"nazwa": "Shit happens", "typ": ["Alkoholowe", "Towarzyskie"], "players": [4,5,6], "dlugosc": [15, 30]},
    {"nazwa": "Wirus", "typ": ["Towarzyskie", "Luzne", "Karciane", "OFA"], "players": [2,3,4,5], "dlugosc": [15, 30]},
    {"nazwa": "Boss Monster", "typ": ["Ekonomia", "Karciane", "OFA", "Deckbuilding", "Strategiczne"], "players": [2,3,4], "dlugosc": [30, 60]},
    {"nazwa": "Księga Czarów", "typ": ["Versus", "Ekonomia", "Przekminy"], "players": [2], "dlugosc": [45, 60]},
    {"nazwa": "Munchkin", "typ": ["OFA", "Karciane", "Deckbuilding"], "players": [3,4,5], "dlugosc": [45, 60]},
    {"nazwa": "Gwint", "typ": ["Versus", "Karciane", "Deckbuilding", "Strategiczne"], "players": [2], "dlugosc": [30, 60]},
    {"nazwa": "Lotr Pojedynek", "typ": ["Versus", "Ekonomia", "Deckbuilding", "Strategiczne"], "players": [2], "dlugosc": [45, 60]},
    {"nazwa": "Ewolucja", "typ": ["OFA", "Ekonomia", "Deckbuilding", "Karciane", "Strategiczne"], "players": [2,3,4], "dlugosc": [45, 60]},
    {"nazwa": "Trucizna", "typ": ["Towarzyskie", "Alkoholowe", "Luzne", "OFA", "Karciane"], "players": [3,4,5,6], "dlugosc": [15, 30]},
    {"nazwa": "Miasto", "typ": ["Ekonomia", "Deckbuilding", "Strategiczne", "Karciane"], "players": [2,3,4,5], "dlugosc": [30, 45]},
    {"nazwa": "Splendor", "typ": ["Strategiczne", "Ekonomia", "Deckbuilding"], "players": [2,3,4], "dlugosc": [30, 60]},
    {"nazwa": "Szkoła Alchemii", "typ": ["Ekonomia", "Przekminy", "Karciane", "Alkoholowe"], "players": [2,3,4,5,6], "dlugosc": [60, 120]},
    {"nazwa": "Smoki", "typ": ["Luzne", "Przekminy", "Karciane"], "players": [2,3,4,5], "dlugosc": [15, 30]},
    {"nazwa": "Isaac", "typ": ["Luzne", "Alkoholowe", "Karciane", "Coop", "OFA", "Deckbuilding", "Strategiczne"], "players": [2,3,4], "dlugosc": [30, 60]},
    {"nazwa": "Scrabble", "typ": ["Przekminy"], "players": [2,3,4], "dlugosc": [45, 60]},
    {"nazwa": "Siedem Cudów", "typ": ["Ekonomia", "Deckbuilding", "Strategiczne"], "players": [3,4,5,6], "dlugosc": [30, 60]},
    {"nazwa": "Dżenga", "typ": ["Luzne", "Alkoholowe", "Towarzyskie"], "players": [2,3,4,5,6], "dlugosc": [15, 30]},
    {"nazwa": "Poker kościany", "typ": ["Luzne", "Towarzyskie"], "players": [2,3,4], "dlugosc": [15, 30]},
    {"nazwa": "Karty classic", "typ": ["Luzne", "Karciane", "Alkoholowe", "Towarzyskie"], "players": [2,3,4,5,6], "dlugosc": [15, 30]},
    {"nazwa": "Moze isaac?", "typ": ["Wildcard"], "players": [2,3,4,5,6], "dlugosc": [15, 150]}
]

def filter_games(game_types, min_players, max_playtime):
    return [
        game for game in games
        if (not game_types or any(typ in game["typ"] for typ in game_types))
           and any(p >= min_players for p in game["players"])
           and game["dlugosc"][0] <= max_playtime
    ]

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        "Nieautoryzowany dostęp. Podaj login i hasło.",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route("/")
@requires_auth
def home():
    return render_template("kolo.html")

@app.route("/filter", methods=["POST"])
@requires_auth
def filter_route():
    data = request.json
    game_types = data.get("game_types", [])
    min_players = max(data.get("min_players", [1]))
    max_playtime = min(data.get("playtime", [999]))

    print(f"Wybrane typy gier: {game_types}")
    print(f"Minimalna liczba graczy: {min_players}")
    print(f"Maksymalny czas gry: {max_playtime}")

    filtered_games = filter_games(game_types, min_players, max_playtime)

    print(f"Przefiltrowane gry: {filtered_games}")

    return jsonify(filtered_games)


@app.route("/spin", methods=["POST"])
def spin():
    data = request.json
    selected_game = data.get("selected_game")

    if not selected_game:
        return jsonify({"error": "Brak wylosowanej gry"}), 400

    print(f"Wylosowana gra: {selected_game}")

    return jsonify({"message": f"Wylosowano: {selected_game}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
