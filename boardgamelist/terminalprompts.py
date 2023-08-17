""" A module to wrap the data-strucure based PyInquirer
into a function call based API.

Limited to list prompts, confirmation prompts, and text input.
"""


from InquirerPy import prompt


def list_prompt(message="", items=None):
    """Display a list and allow selection."""
    if not items:
        raise ValueError("Please enter some items")

    question = [
        {"type": "list", "name": "prompt", "message": message, "choices": items}
    ]
    return prompt(question)["prompt"]


def confirmation_prompt(message=""):
    """Display a confirmation prompt (returns True or False)."""
    question = [
        {"type": "confirm", "name": "prompt", "message": message, "default": True}
    ]
    return prompt(question)["prompt"]


def input_prompt(message="", validation_function=None):
    """Allow user input."""
    question = [{"type": "input", "name": "prompt", "message": message}]
    if validation_function:
        question[0]["validate"] = validation_function

    return prompt(question)["prompt"]
