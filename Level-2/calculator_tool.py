def calculator(expression: str) -> float:
   
    allowed_chars = "0123456789+-*/(). "
    if not all(char in allowed_chars for char in expression):
        raise ValueError("Expression contains invalid characters.")

    try:
        result = eval(expression)
        return round(result, 4)  # rounded for clean output
    except Exception as e:
        raise ValueError(f"Invalid expression: {expression}. Error: {str(e)}")
