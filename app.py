from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

dataset_path = "AirQualityUCI.xlsx"
df = pd.read_excel(dataset_path)

df.replace(-200, np.nan, inplace=True)
df.dropna(inplace=True)

def air_quality_score(row):
    co = row["CO(GT)"] / 100
    c6h6 = row["C6H6(GT)"]
    nox = row["NOx(GT)"] / 10
    no2 = row["NO2(GT)"] / 10
    temp = row["T"] / 10
    rh = row["RH"] / 10

    return (
        0.4 * co +
        0.3 * c6h6 +
        0.2 * nox +
        0.1 * no2 -
        0.05 * temp -
        0.05 * rh
    )

df["Score"] = df.apply(air_quality_score, axis=1)

def get_air_quality(score):
    min_s = df["Score"].min()
    max_s = df["Score"].max()
    step = (max_s - min_s) / 4

    if score <= min_s + step:
        return "GOOD"
    elif score <= min_s + 2 * step:
        return "MODERATE"
    elif score <= min_s + 3 * step:
        return "POOR"
    else:
        return "VERY POOR"

states = [0, 1, 2, 3]
actions = [0, 1, 2, 3]

q_table = np.zeros((4, 4))

def reward(state, action):
    return 1 if state == action else -1

for s in states:
    for a in actions:
        q_table[s][a] = reward(s, a)

def score_to_state(score):
    mapping = {
        "GOOD": 0,
        "MODERATE": 1,
        "POOR": 2,
        "VERY POOR": 3
    }
    return mapping[get_air_quality(score)]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    co = float(data.get("co", 0))
    c6h6 = float(data.get("c6h6", 0))
    nox = float(data.get("nox", 0))
    no2 = float(data.get("no2", 0))
    temp = float(data.get("temp", 0))
    rh = float(data.get("rh", 0))
    ah = float(data.get("ah", 0))

    score = (
        0.4 * (co / 100) +
        0.3 * c6h6 +
        0.2 * (nox / 10) +
        0.1 * (no2 / 10) -
        0.05 * (temp / 10) -
        0.05 * (rh / 10)
    )

    state = score_to_state(score)
    action_index = int(np.argmax(q_table[state]))

    actions_map = {
        0: "No Action",
        1: "Fan",
        2: "Ventilation",
        3: "Air Purifier"
    }

    return jsonify({
        "air_quality": get_air_quality(score),
        "score": round(score, 2),
        "action": actions_map[action_index],
        "details": {
            "CO(GT)": co,
            "C6H6(GT)": c6h6,
            "NOx(GT)": nox,
            "NO2(GT)": no2,
            "Temperature": temp,
            "RH": rh,
            "AH": ah
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
