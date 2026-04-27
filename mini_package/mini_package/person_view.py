

def format_person(person: dict) -> str:
    name = person.get("name", "Unknown")
    age = person.get("age", "N/A")
    return f"Name: {name}, Age: {age}"
