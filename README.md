# Staticc

Static analysis toolkit for Python AST.

## `staticc.delta`

Delta between the original and the transformed trees.

```py
import ast
from staticc.delta import ChangeType, ast_delta

original_tree = ast.parse("""
def foo(a: int, b: int) -> str:
    if a < 5:
        return foo(a + 1, b)
    else:
        return str(a + b)

def main():
    print(foo(1, 2))

if __name__ == "__main__":
    main()
""")

transformed_tree = ast.parse("""
def bar(a: int, b: int) -> str:
    print("new statement on a new function")
    if a < 5:
        return bar(a + 1, b)
    else:
        return str(a + b)

def main():
    print(bar(1, 2))

if __name__ == "__main__":
    main()
""")

for change in ast_delta(original_tree, transformed_tree):
    if change.on_field is not None:
        original_field = getattr(change.original_node, change.on_field)
        new_field = getattr(change.new_node, change.on_field)

    if change.change_type is ChangeType.FIELD_VALUE:
        if change.on_index is not None:
            original_field = original_field[change.on_index]
            new_field = new_field[change.on_index]

        print(f"(Line: {change.original_node.lineno}) Value of {change.on_field}: {original_field} -> {new_field}")
    elif change.change_type is ChangeType.FIELD_SIZE:
        print(f"(Line: {change.original_node.lineno}) Size of {change.on_field}: {len(original_field)} -> {len(new_field)}")
```
