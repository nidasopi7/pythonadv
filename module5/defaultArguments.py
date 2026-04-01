def greet_person(name, greeting="Hello"): 2usages
    message = f"{greeting},{name}"
    return message

default_greeting = greet_person("Alice")
print(default_greeting)

custom_greeting = greet_person( name:"Alice", greeting: "Hi")
print(custom_greeting)