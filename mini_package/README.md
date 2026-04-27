# Mini Package Example

A simple and basic Python package with multiple modules.

Modules used in the basic example:

- `person.py` to create person data
- `person_view.py` to format person data
- `storage.py` for optional file save/load helpers

## Run the package demo

```bash
python -m mini_package
```

## Use in code

```python
from mini_package import create_person, format_person, is_adult

person = create_person("Sam", 19)
print(format_person(person))
print(is_adult(person))
```
