# 🚀 Sparq Programming Language 🌟

Welcome to **Sparq**—a lightweight, beginner-friendly programming language designed for simplicity and power! Inspired by **JavaScript** and **C++**, Sparq makes coding intuitive without sacrificing robust features.

---

## ✨ Features
✅ **Explicit Typing**: Easily declare variable types for clarity.  
✅ **Dynamic Objects**: Use `let` or for type inference when needed.  
✅ **Constants**: Keep values immutable with `const`.  
✅ **Functions**: Clean, readable syntax with the `function` keyword.  
✅ **Classes**: Enjoy object-oriented programming support.  
✅ **Modular Imports**: Keep your code clean with an `import` system.  

---

## 🧠 Sparq Syntax Cheat Sheet

### 🔢 Variables
```sparq
int x = 10;         // Integer variable
str y = "Hello";    // String variable
bool cool = true;   // Boolean variable
let z = 42;         // Generic variable (type inferred)
const pi = 3.1415;  // Immutable constant
```

### 🎉 Functions
```sparq
function greet(str name) {
    print("Hello, " + name);
}
```

### 🛤️ Conditionals
```sparq
if (x > 5) {
    print("x is greater than 5");
} else {
    print("x is 5 or less");
}
```

### 🔁 Loops
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

### 🧍 Objects
```sparq
let person = {
    name: "DaPSL",         // string
    age: 14,                // int
    hobbies: ["coding", "gaming"] // array of strings
};
print(person.name);
```

### 🏛️ Classes
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

## 🛠️ Built-in Libraries
### 📚 Standard Libraries Included
Sparq has built-in tools for everyday coding tasks:
- **Math**: Handy constants like Math.PI and functions like Math.sqrt(x).
- **Strings**: Utilities like .length(), .toUpperCase(), and .toLowerCase().
- **Basic I/O**: Use print() and input() for quick input/output tasks.

### Example:
```sparq
let radius = 5;
let area = Math.PI * (radius * radius); // Built-in Math library
print("Area: " + area);
```

## 📦 Importing Modules
Take it further with external or custom modules:
```sparq
import "utils.sq"; // importing user-defined moduled

function main() {
    let result = utils.add(5, 10); // using a function from the imported module
    print(result);
}
```


## 🚀 Getting Started
1️⃣ Clone the Repository
```bash
git clone https://github.com/IAmThePSL/Sparq
cd sparq
```
2️⃣ Build the Project
```bash

```
3️⃣ Run Sparq Programs
```bash
./sparq examples/hello.sprq
```

## 🤝 Contribution
We ❤️ contributors!
Found a bug? Have a cool feature idea? Feel free to open an issue or submit a pull request. Let’s make Sparq even better together! ✨

## 📜 License
This project is licensed under the [MIT License](https://github.com/IAmThePSL/Sparq/blob/main/LICENSE)

Let’s spark your coding journey with Sparq! 💡


### NOTE:
**Sparq is currently under active development. Some features listed in this document may not yet be available. Thank you for your patience and support!**
