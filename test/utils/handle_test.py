def handle_test(func, init, finish):

    def wrapper(*args, **kwargs):
        try:
            init()
            func(*args, **kwargs)
        except BaseException as e:
            raise e
        finally:
            finish()

    return wrapper
