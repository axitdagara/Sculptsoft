# My Project

A simple Python project that demonstrates a small package with math and string utility modules.

## Project Structure

```text
my_project/
├── README.md
└── src/
    ├── main.py
    └── mypackage/
        ├── __init__.py
        ├── math_utils.py
        └── string_utils.py
```

## Available Functions

### `mypackage/math_utils.py`
- `add(a, b)`: Returns the sum of two numbers.
- `multiply(a, b)`: Returns the product of two numbers.

### `mypackage/string_utils.py`
- `to_upper(text)`: Converts text to uppercase.
- `to_lower(text)`: Converts text to lowercase.

## Run the Example

From the `my_project` directory:

```bash
python src/main.py
```

Expected output:

```text
5
HARSH
```

## Usage in Code

```python
from mypackage import math_utils, string_utils

print(math_utils.add(2, 3))            # 5
print(math_utils.multiply(2, 3))       # 6
print(string_utils.to_upper("hello")) # HELLO
print(string_utils.to_lower("HELLO")) # hello
```
