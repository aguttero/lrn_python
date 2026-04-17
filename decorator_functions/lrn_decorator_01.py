from ast import arg
import time

def tictoc (func):
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time() - t1
        print(f"Func {func.__name__} took {t2} seconds")
    return wrapper

def add_sprinkles(func):
    def wrapper(*args, **kwargs):
        print ("You add sprinkles!!")
        func(*args, **kwargs)
    return wrapper

def add_fudge(func):
    def wrapper(*args, **kwargs):
        print ("You add fudge!!")
        func(*args, **kwargs)
    return wrapper


@add_fudge
@add_sprinkles
def get_ice_cream(flavor):
    print(f"Here is your {flavor} ice cream!!")


@tictoc
def do_this():
    # simulate time running code
    time.sleep(1.3)

@tictoc
def do_that():
    # simulate time running code
    time.sleep(0.4)

def main():
    do_this()
    do_that()
    print ("- - -")
    get_ice_cream("chocolate")
    print ("done")
    return 0

if __name__ == "__main__":
    exit_code: int = main()
    print("EXIT CODE: ",exit_code)
    exit(exit_code)

