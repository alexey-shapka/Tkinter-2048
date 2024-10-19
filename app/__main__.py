import sys
from tkinter import Tk
from pathlib import Path

if "-m" not in sys.argv:
    sys.path.append(str(Path(__file__).parent.parent))

from app.interface import Interface


if __name__ == "__main__":
    root = Tk()
    q = Interface(root)
    root.mainloop()
