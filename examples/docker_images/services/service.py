'''
Sample long running service
'''

import time


def main():
    '''
    Main function
    -> Run a loop forever times and print out the current time
    -> Between each iteration wait 10 seconds
    '''
    while True:
        print(time.time())
        time.sleep(10)

if __name__ == "__main__":
    main()
