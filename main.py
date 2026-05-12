from pymata4 import pymata4
import time
import config
import ss4
import ss1
import ss2
import shift_register

board = pymata4.Pymata4()

def main():
    try:
        while True:

            ss2.update()
            ss4.update()
            ss1.update()

            ss1.apply_outputs()
            ss2.apply_outputs()
            ss4.apply_outputs()

            shift_register.apply()

            time.sleep(0.05)


    except KeyboardInterrupt:
        print("Shutting down...")
        board.shutdown()

if __name__ == "__main__":
    main()