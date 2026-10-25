"""Небольшой веб-сервис для демонстрации контроля качества в CI/CD."""
from flask import Flask, jsonify, request

from app.storage import TaskStore


def create_app():
    app = Flask(__name__)
    store = TaskStore()

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/api/sum")
    def api_sum():
        try:
            a = float(request.args["a"])
            b = float(request.args["b"])
        except (KeyError, ValueError):
            return jsonify(error="Нужны числовые параметры a и b"), 400
        return jsonify(result=a + b)

    @app.get("/api/tasks")
    def list_tasks():
        return jsonify(store.all())

    @app.post("/api/tasks")
    def create_task():
        data = request.get_json(silent=True) or {}
        try:
            task = store.add(data.get("title"))
        except ValueError as exc:
            return jsonify(error=str(exc)), 400
        return jsonify(task), 201

    @app.post("/api/tasks/<int:task_id>/done")
    def complete_task(task_id):
        try:
            return jsonify(store.complete(task_id))
        except KeyError:
            return jsonify(error="Задача не найдена"), 404

    return app
