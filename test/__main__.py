from test.test_zone import main as test_zone
from test.local.test_record import main as test_record


def main():
    test_zone()
    
    test_record()
    
    
if __name__ == "__main__":
    main()