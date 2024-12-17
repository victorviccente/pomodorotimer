# app.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

class PomodoroState:
    def __init__(self):
        self.tasks = []
        self.timer = {
            "time_left": 1500,
            "is_running": False,
            "is_break": False,
            "start_time": None
        }

state = PomodoroState()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/timer/status', methods=['GET'])
def get_timer_status():
    return jsonify(state.timer)

@app.route('/api/timer/toggle', methods=['POST'])
def toggle_timer():
    state.timer["is_running"] = not state.timer["is_running"]
    if state.timer["is_running"]:
        state.timer["start_time"] = datetime.now().timestamp()
    return jsonify(state.timer)

@app.route('/api/timer/reset', methods=['POST'])
def reset_timer():
    state.timer["time_left"] = 300 if state.timer["is_break"] else 1500
    state.timer["is_running"] = False
    state.timer["start_time"] = None
    return jsonify(state.timer)

@app.route('/api/timer/toggle-break', methods=['POST'])
def toggle_break():
    state.timer["is_break"] = not state.timer["is_break"]
    state.timer["time_left"] = 300 if state.timer["is_break"] else 1500
    state.timer["is_running"] = False
    return jsonify(state.timer)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(state.tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = {
        "id": len(state.tasks),
        "text": data["text"],
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    state.tasks.append(task)
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in state.tasks:
        if task["id"] == task_id:
            if "completed" in data:
                task["completed"] = data["completed"]
            if "text" in data:
                task["text"] = data["text"]
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for i, task in enumerate(state.tasks):
        if task["id"] == task_id:
            state.tasks.pop(i)
            return jsonify({"success": True})
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
