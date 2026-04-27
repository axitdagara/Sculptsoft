

from .person import create_person, is_adult
from .person_view import format_person


def main() -> None:
    person = create_person("Alex", 21)
    print(format_person(person))
    print("Adult:", is_adult(person))


if __name__ == "__main__":
    main()
