def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Done wth the function.")
    return wrapper

@announce
def hello():
    print("Hello, world!")

hello()