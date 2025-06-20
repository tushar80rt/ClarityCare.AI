from camel.toolkits.math_toolkit import MathToolkit

math_tool = MathToolkit()

def calculate_mood_score(inputs: list) -> float:
    if not inputs:
        return 0.0
    total = inputs[0]
    for val in inputs[1:]:
        total = math_tool.add(total, val)
    return math_tool.divide(total, len(inputs))
