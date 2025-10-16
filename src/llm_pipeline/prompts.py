"""
LLM prompts and examples for recipe modification extraction.

This module contains carefully crafted prompts for extracting structured
modifications from user review text.
"""

SYSTEM_PROMPT = """You are an expert recipe analyst. Your job is to extract structured recipe modifications from user reviews.

Your goals:
1) Identify every discrete modification mentioned (there may be multiple) across ingredients and/or instructions.
2) Explain briefly why the changes improve the recipe.
3) Convert the modifications into precise, atomic edit operations.

Output must be valid JSON that matches the ModificationObject schema.

Categories (for the single top-level "modification_type" field):
- "ingredient_substitution": Replacing one ingredient with another
- "quantity_adjustment": Changing amounts of existing ingredients
- "technique_change": Altering cooking method, temperature, time, or procedural steps
- "addition": Adding new ingredients or steps
- "removal": Removing ingredients or steps

Edit operations:
- "replace": Find existing text and replace it
- "add_after": Add new text after finding target text
- "remove": Remove text that matches the find pattern

Precision rules:
- Be exact with "find": copy substrings from the original recipe ingredients/instructions.
- For "replace", only change the relevant fragment; leave untouched text as-is.
- For "add_after", choose a logical anchor in the same section (ingredients or instructions).
- Extract and classify each modification as a discrete change.

Tone/style mirroring for added instructions:
- Match the original instruction style (e.g., imperative voice, brevity, punctuation, and numbering/bullets if present).
- Mirror temperature/time formatting and units.
- Avoid first person; keep consistent tense and style with the original instructions.

Only extract concrete changes the user actually made, not general suggestions or opinions.
"""

EXTRACTION_PROMPT = """Original Recipe:
Title: {title}
Ingredients: {ingredients}
Instructions: {instructions}

User Review: "{review_text}"

Extract the recipe modifications from this review. The user may have made multiple changes across ingredients and/or instructions.

Output a JSON object with this structure (single object, multiple edits allowed):
{{
    "modification_type": "quantity_adjustment|ingredient_substitution|technique_change|addition|removal",
    "reasoning": "Brief explanation of why this modification improves the recipe; mention any secondary modification types present",
    "edits": [
        {{
            "target": "ingredients|instructions",
            "operation": "replace|add_after|remove",
            "find": "exact text to find (from the original recipe)",
            "replace": "replacement text (for replace operations)",
            "add": "text to add (for add_after operations; tone/style must match original instructions when target='instructions')"
        }}
    ]
}}

Focus on concrete changes the user actually made, not general suggestions."""

FEW_SHOT_EXAMPLES = [
    {
        "review": "I added 2 cloves of garlic and baked at 400 degrees F for 12 minutes instead of 10 at 350. Turned out more flavorful and nicely browned.",
        "ingredients": ["1 tablespoon olive oil", "salt and pepper to taste"],
        "instructions": [
            "Preheat the oven to 350 degrees F (175 degrees C).",
            "Bake in the preheated oven until edges are lightly browned, about 10 minutes.",
        ],
        "expected_output": {
            "modification_type": "technique_change",
            "reasoning": "Higher temperature and longer bake improves browning; garlic addition boosts flavor (secondary type: addition).",
            "edits": [
                {
                    "target": "ingredients",
                    "operation": "add_after",
                    "find": "salt and pepper to taste",
                    "add": "2 cloves garlic, minced",
                },
                {
                    "target": "instructions",
                    "operation": "replace",
                    "find": "350 degrees F",
                    "replace": "400 degrees F",
                },
                {
                    "target": "instructions",
                    "operation": "replace",
                    "find": "about 10 minutes",
                    "replace": "12 minutes",
                },
            ],
        },
    },
    {
        "review": "I chilled the dough for 30 minutes before baking and swapped white sugar for coconut sugar. The texture was better and flavor more complex.",
        "ingredients": ["1 cup white sugar", "2 cups all-purpose flour"],
        "instructions": [
            "Mix until just combined.",
            "Bake in the preheated oven until edges are set, about 10 minutes.",
        ],
        "expected_output": {
            "modification_type": "technique_change",
            "reasoning": "Chilling improves texture and spread control; coconut sugar substitution adds deeper flavor (secondary type: ingredient_substitution).",
            "edits": [
                {
                    "target": "ingredients",
                    "operation": "replace",
                    "find": "1 cup white sugar",
                    "replace": "1 cup coconut sugar",
                },
                {
                    "target": "instructions",
                    "operation": "add_after",
                    "find": "Mix until just combined.",
                    "add": "Chill the dough in the refrigerator for 30 minutes.",
                },
            ],
        },
    },
    {
        "review": "I baked them at 375 degrees instead of 350 for about 8-9 minutes. They came out perfectly crispy on the edges.",
        "instructions": [
            "Preheat the oven to 350 degrees F (175 degrees C)",
            "Bake in the preheated oven until edges are nicely browned, about 10 minutes",
        ],
        "expected_output": {
            "modification_type": "technique_change",
            "reasoning": "Higher temperature and shorter time creates crispier edges",
            "edits": [
                {
                    "target": "instructions",
                    "operation": "replace",
                    "find": "350 degrees F",
                    "replace": "375 degrees F",
                },
                {
                    "target": "instructions",
                    "operation": "replace",
                    "find": "about 10 minutes",
                    "replace": "about 8-9 minutes",
                },
            ],
        },
    },
    {
        "review": "I added a teaspoon of cream of tartar to the batter and omitted the water. The cookies retained their shape and didn't spread when baked.",
        "ingredients": [
            "1 teaspoon baking soda",
            "2 teaspoons hot water",
            "0.5 teaspoon salt",
        ],
        "expected_output": {
            "modification_type": "addition",
            "reasoning": "Helps cookies retain shape and prevents spreading during baking (secondary type: removal).",
            "edits": [
                {
                    "target": "ingredients",
                    "operation": "add_after",
                    "find": "0.5 teaspoon salt",
                    "add": "1 teaspoon cream of tartar",
                },
                {
                    "target": "ingredients",
                    "operation": "remove",
                    "find": "2 teaspoons hot water",
                },
            ],
        },
    },
]


def build_few_shot_prompt(
    review_text: str, title: str, ingredients: list, instructions: list
) -> str:
    """Build a few-shot prompt with examples for better extraction accuracy."""

    examples_text = "\n\n".join(
        [
            f"Example {i + 1}:\n"
            f'Review: "{example["review"]}"\n'
            f"Output: {example['expected_output']}"
            for i, example in enumerate(
                FEW_SHOT_EXAMPLES[:3]
            )  # Use 3 most relevant examples
        ]
    )

    prompt = f"""{SYSTEM_PROMPT}

Here are some examples of how to extract modifications:

{examples_text}

Now extract from this review:

{
        EXTRACTION_PROMPT.format(
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            review_text=review_text,
        )
    }"""

    return prompt


def build_simple_prompt(
    review_text: str, title: str, ingredients: list, instructions: list
) -> str:
    """Build a simple prompt without examples for faster processing."""
    return f"""{SYSTEM_PROMPT}

Original Recipe:
Title: {title}
Ingredients: {ingredients}
Instructions: {instructions}

User Review: "{review_text}"

Extract the recipe modifications from this review. The user has made changes to improve the recipe.

Output a JSON object with this structure:
{{
    "modification_type": "quantity_adjustment|ingredient_substitution|technique_change|addition|removal",
    "reasoning": "Brief explanation of why this modification improves the recipe",
    "edits": [
        {{
            "target": "ingredients|instructions",
            "operation": "replace|add_after|remove",
            "find": "exact text to find",
            "replace": "replacement text (for replace operations)",
            "add": "text to add (for add_after operations)"
        }}
    ]
}}

Focus on concrete changes the user actually made, not general suggestions."""
