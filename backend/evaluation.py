from backend.severity_engine import analyze_severity

def evaluate_text(text: str):
    result = analyze_severity(text)
    result["is_cyberbullying"] = result["severity"] >= 3
    return result
