# Sparq Programming Language

Sparq is a lightweight, easy-to-understand programming language designed for simplicity and flexibility. Inspired by languages like JavaScript and C++, Sparq aims to be intuitive while maintaining robust features.

## Features
- **Explicit Typing**: Declare variable types explicitly for clarity.
- **Dynamic Objects**: Use generic declarations like `let` or `var` when types are unknown.
- **Constants**: Immutable variables with `const`.
- **Functions**: Clear and concise syntax using the `function` keyword.
- **Classes**: Object-oriented programming with class support.
- **Imports**: Modular programming with an `import` system.

---

## Sparq Syntax

### Variables
```sparq
int x = 10;         // Integer variable
str y = "Hello";    // String variable
bool cool = true;   // Boolean variable
let z = 42;         // Generic variable (type inferred)
const pi = 3.1415;  // Immutable constant
```

### Functions
```sparq
function greet(str name) {
    print("Hello, " + name);
}
```

### Conditionals
```sparq
if (x > 5) {
    print("x is greater than 5");
} else {
    print("x is 5 or less");
}
```

### Loops
```sparq
for (int i = 0; i < 10; i++) {
    print(i);
}
```
```sparq
while (x > 0) {
    x = x - 1;
    print(x);
}
```

### Objects
```sparq
let person = {
    name: "DaPSL",         // string
    age: 14,                // int
    hobbies: ["coding", "gaming"] // array of strings
};
print(person.name);
```

### Classes
```sparq
class Animal {
    str name;

    function init(str name) {
        this.name = name;
    }

    function speak() {
        print(this.name + " makes a sound");
    }
}
```

## Built-in Libraries
Sparq includes built-in libraries for common tasks, such as:
- **Math**: ```Math.PI```, ```Math.sqrt(x)```, ```Math.pow(x, y)```, etc.
- **String utilities**: Built-in methods like ```.length()```, ```.toUpperCase()```, ```.toLowerCase()``
- **Basic I/O**: Functions like ```print()``` and ```input()```

## Example with Built-in Libraries
```sparq
let radius = 5;
let area = Math.PI * (radius * radius); // Built-in Math library
print("Area: " + area);
```

## Importing Modules
For extended functionality, Sparq allows importing external or user-defined modules.
```sparq
import "utils.sq"; // importing user-defined moduled

function main() {
    let result = utils.add(5, 10); // using a function from the imported module
    print(result);
}
```


## Getting Started
1. Clone the Repository:
```bash
git clone https://github.com/IAmThePSL/Sparq
cd sparq
```
2. Build the project:
```bash
make
```
3. Run example Sparq programs:
```bash
./sparq examples/hello_world.sq
```

## Contribution
Contributors are welcome! Feel free to submit pull requests or open issues to help improve Sparq

## License
This project is licensed under the [MIT License](https://github.com/IAmThePSL/Sparq/blob/main/LICENSE)