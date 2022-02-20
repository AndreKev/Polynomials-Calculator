from os import system as command
import sys
#import Screen
import glob
print(glob.glob("*"))

def main():
    # importing the Screen application
    sys.path.insert(0, "widgets")
    sys.path.append("assets")
    try:
        import screen
        print("Sucessfuly imported Screen Widget")
        screen.main()
    except ModuleNotFoundError:
        print("Could not found de module *screen*")

if __name__ == "__main__":
    main()
