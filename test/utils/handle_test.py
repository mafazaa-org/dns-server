def handle_test(func, init, finish):

    def wrapper(*args, **kwargs):
        try:
            init()
            func(*args, **kwargs)
        except:
            ...
        finally:
            finish()

    return wrapper
