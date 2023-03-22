'''
Sample short running job
'''

import time


def main():
    '''
    Main function
    -> Run a loop 10 times and print out the current time
    -> Between each iteration wait 10 seconds
    '''
    for i in range(10):
        print(time.time())
        time.sleep(10)

if __name__ == "__main__":
    main()