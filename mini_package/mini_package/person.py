

def create_person(name: str, age: int) -> dict:
    return {"name": name, "age": age}


def is_adult(person: dict) -> bool:
    return person.get("age", 0) >= 18
