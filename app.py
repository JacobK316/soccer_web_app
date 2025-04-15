from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# List of players
list_players = [
    "Anthony", "Brandon", "Carter", "Gavin", "Henry", "Jackson",
    "Jacob", "Kayde", "M.J.", "Movlud", "Patrick", "Simir"
]
scores_file = "player_scores.json"

def load_scores():
    try:
        with open(scores_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {player: 0 for player in list_players}

def save_scores(scores):
    with open(scores_file, "w") as file:
        json.dump(scores, file)

@app.route('/')
def homepage():
    player_scores = load_scores()
    sorted_scores = dict(sorted(player_scores.items(), key=lambda x: x[1], reverse=True))
    return render_template('index.html', player_scores=sorted_scores)

@app.route('/update', methods=['POST'])
def update_scores():
    player = request.form.get('player')
    score = int(request.form.get('score'))
    player_scores = load_scores()
    if player in player_scores:
        player_scores[player] += score
        save_scores(player_scores)
    return jsonify(player_scores)

if __name__ == '__main__':
    app.run()