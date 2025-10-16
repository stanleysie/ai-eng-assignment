from __future__ import annotations

from ast import Dict
import json
import os
import glob
from llm_pipeline.pipeline import LLMAnalysisPipeline
from flask import Flask, jsonify
from flask import request
from flask import make_response
from flask import Response


def _enable_cors(resp: Response) -> Response:
    resp.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = request.headers.get(
        "Access-Control-Request-Headers", "Content-Type, Authorization"
    )
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    return resp


def read_all_recipes() -> list[Dict]:
    recipes = []
    for file in glob.glob("data/recipe_*.json"):
        recipe_id = file.split("_")[1]
        recipe_name = file.split("_")[2].split(".json")[0]
        with open(file, "r") as f:
            recipes.append(
                {
                    "id": recipe_id,
                    "name": recipe_name,
                    "data": json.load(f),
                }
            )
    return recipes


def read_recipe(id: str) -> Dict:
    for file in glob.glob("data/recipe_*.json"):
        if id in file:
            recipe_name = file.split("_")[2].split(".json")[0]
            with open(file, "r") as f:
                return {
                    "id": id,
                    "name": recipe_name,
                    "data": json.load(f),
                }
    return None


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def all():
        return _enable_cors(jsonify(read_all_recipes())), 200

    @app.get("/recipe/<id>")
    def recipe(id: str):
        return _enable_cors(jsonify(read_recipe(id))), 200

    @app.get("/recipe/<id>/enhance")
    def enhance(id: str):
        receipt_file = None
        for file in glob.glob("data/recipe_*.json"):
            if id in file:
                receipt_file = file
                break
        if receipt_file is None:
            return jsonify({"message": "Recipe not found"}), 404

        enhanced_recipe = LLMAnalysisPipeline().process_single_recipe(receipt_file)
        if enhanced_recipe is None:
            return _enable_cors(jsonify({"message": "No modifications found"})), 200
        return _enable_cors(jsonify(enhanced_recipe.model_dump())), 200

    @app.route("/", methods=["OPTIONS"])
    @app.route("/recipe/<id>", methods=["OPTIONS"])
    @app.route("/recipe/<id>/enhance", methods=["OPTIONS"])
    def options(id: str | None = None):
        return _enable_cors(make_response("", 204))

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
