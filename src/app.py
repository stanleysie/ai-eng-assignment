from __future__ import annotations

from ast import Dict
import json
import os
import glob
from llm_pipeline.pipeline import LLMAnalysisPipeline
from flask import Flask, jsonify


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
        return jsonify(read_all_recipes()), 200

    @app.get("/recipe/<id>")
    def recipe(id: str):
        return jsonify(read_recipe(id)), 200

    @app.post("/recipe/<id>/enhance")
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
            return jsonify({"message": "Failed to enhance recipe"}), 500
        return jsonify(enhanced_recipe.model_dump()), 200

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
