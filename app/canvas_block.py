class CanvasBlock:

    def __init__(self, canvas, x, y):
        self.value = 0
        self.x = x
        self.y = y
        self.canvas = canvas
        self.interface_object = canvas.create_rectangle(
            self.x, self.y, self.x + 100, self.y + 100, fill="#fafafa", outline=""
        )
        self.text = self.canvas.create_text(self.x + 50, self.y + 50, font=("arial", 25, "bold"))

    def set_value(self, value, color):
        self.value = value
        self.canvas.itemconfig(self.interface_object, fill=color[0])
        if self.value != 0:
            self.canvas.itemconfig(self.text, text=str(value), fill=color[1])
        else:
            self.canvas.itemconfig(self.text, text="", fill=color[1])

    def coordinates(self):
        return self.x, self.y
