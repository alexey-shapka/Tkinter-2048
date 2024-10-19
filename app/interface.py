import random
import time

from tkinter import Menu, Canvas, messagebox

from app.canvas_block import CanvasBlock


class Interface:

    def __init__(self, root):
        self.main_window = root
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.main_window.resizable(False, False)
        self.main_window.title("2048")
        self.main_window.geometry("450x450+" + str(500) + "+" + str(int(self.screen_height / 2 - 708 / 2)))
        self.main_window["bg"] = "#776e65"

        self.menu_bar = Menu(self.main_window)
        self.main_window["menu"] = self.menu_bar
        self.menu_bar.add_command(label="New game", command=lambda: self.reset())
        self.menu_bar.add_command(label="Score", command=lambda: self.score())
        self.menu_bar.add_command(label="Time", command=lambda: self.time())

        self.speed_bar = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Speed", menu=self.speed_bar)
        self.speed_bar.add_command(label="1", command=lambda: self.change_speed(1))
        self.speed_bar.add_command(label="2", command=lambda: self.change_speed(2))
        self.speed_bar.add_command(label="3", command=lambda: self.change_speed(3))
        self.speed_bar.add_command(label="4", command=lambda: self.change_speed(4))
        self.speed_bar.add_command(label="5", command=lambda: self.change_speed(5))
        self.speed_bar.add_command(label="6", command=lambda: self.change_speed(6))

        self.main_window.bind("<Up>", lambda *_: self.button_event("up"))
        self.main_window.bind("<Down>", lambda *_: self.button_event("down"))
        self.main_window.bind("<Left>", lambda *_: self.button_event("left"))
        self.main_window.bind("<Right>", lambda *_: self.button_event("right"))

        self.canvas = Canvas(
            self.main_window, bg="#776e65", bd=0, highlightthickness=0, relief="ridge", width=450, height=450
        )
        self.canvas.place(x=0, y=0)

        self.blocks = [[] for _ in range(4)]
        self.colors = {
            "0": ["#fafafa", "#776e65"],
            "2": ["#eee4da", "#776e65"],
            "4": ["#ede0c8", "#776e65"],
            "8": ["#f2b179", "#f9f6f2"],
            "16": ["#f59563", "#f9f6f2"],
            "32": ["#f67c5f", "#f9f6f2"],
            "64": ["#f65e3b", "#f9f6f2"],
            "128": ["#edcf72", "#f9f6f2"],
            "256": ["#edcc61", "#f9f6f2"],
            "512": ["#edc850", "#f9f6f2"]
        }

        self.speed_scale = {1: 55, 2: 22, 3: 10, 4: 5, 5: 2, 6: 1}
        self.speed_mode = 3
        self.player_score = 0
        self.check_changes = False
        self.block_new_events = False
        self.player_time = time.time()
        self.create_start_blocks()

    def start_spaun(self):
        positions = [[i, j] for i in range(4) for j in range(4)]
        for i in range(2):
            chosen = positions.pop(random.randint(0, 15 - i))
            self.blocks[chosen[0]][chosen[1]].set_value(2, self.colors["2"])

    def create_start_blocks(self):
        for y in range(4):
            for x in range(4):
                self.blocks[y].append(CanvasBlock(self.canvas, 110 * x + 10, 110 * y + 10))
        self.start_spaun()

    def reset(self):
        self.player_score, self.check_changes, self.player_time, self.blocks = 0, 0, time.time(), [[] for _ in range(4)]
        self.create_start_blocks()

    def score(self):
        messagebox.showinfo("Score", "Your score : {}".format(str(self.player_score)))

    def time(self):
        messagebox.showinfo("Time", "Spent time : {} sec".format(str(int(time.time() - self.player_time))))

    def change_speed(self, value):
        self.speed_mode = value

    def get_color(self, value):
        if value > 512:
            return self.colors["512"]
        else:
            return self.colors[str(value)]

    def generate_new_value(self):
        chosen = random.choice([[i, j] for i in range(4) for j in range(4) if self.blocks[i][j].value == 0])
        if random.random() >= 0.9:
            self.blocks[chosen[0]][chosen[1]].set_value(4, self.colors["4"])
        else:
            self.blocks[chosen[0]][chosen[1]].set_value(2, self.colors["2"])

    def animation(self, array, button):
        for i in array:
            x, y = i[0].coordinates()
            color = self.get_color(i[2])
            i[0].set_value(0, self.get_color(0))
            self.canvas.create_rectangle(x, y, x + 110, y + 110, tags="move", fill=color[0], outline="")
            self.canvas.create_text(
                x + 50, y + 50, font=("arial", 25, "bold"), text=str(i[2]), fill=color[1], tags="move"
            )

        for _ in range(int(110 / self.speed_scale[self.speed_mode])):
            if button == "up":
                self.canvas.move("move", 0, -self.speed_scale[self.speed_mode])
            elif button == "down":
                self.canvas.move("move", 0, self.speed_scale[self.speed_mode])
            elif button == "left":
                self.canvas.move("move", -self.speed_scale[self.speed_mode], 0)
            else:
                self.canvas.move("move", self.speed_scale[self.speed_mode], 0)
            self.canvas.update()

        for i in array:
            i[1].set_value(i[2], self.get_color(i[2]))
        self.canvas.delete("move")

    def skip_zero_squares(self, button, replace_flag=True):
        while replace_flag:
            replace_flag, to_move = False, []
            for i in range(3):
                for pair in self.return_indexes(button, i):
                    first, second = self.blocks[pair[0][0]][pair[0][1]], self.blocks[pair[1][0]][pair[1][1]]
                    if second.value == 0 and first.value != 0:
                        to_move.append([first, second, first.value])
                        self.check_changes, replace_flag = True, True
            self.animation(to_move, button)

    def return_indexes(self, button, iteration, reverse=False):
        reverse_true = {
            "right": [([i, 3 - iteration], [i, 2 - iteration]) for i in range(4)],
            "left": [([i, iteration], [i, iteration + 1]) for i in range(4)],
            "up": [([iteration, i], [iteration + 1, i]) for i in range(4)],
            "down": [([3 - iteration, i], [2 - iteration, i]) for i in range(4)]
        }

        reverse_false = {
            "left": [([i, 3 - iteration], [i, 2 - iteration]) for i in range(4)],
            "right": [([i, iteration], [i, iteration + 1]) for i in range(4)],
            "down": [([iteration, i], [iteration + 1, i]) for i in range(4)],
            "up": [([3 - iteration, i], [2 - iteration, i]) for i in range(4)]
        }

        if reverse:
            return reverse_true[button]
        else:
            return reverse_false[button]

    def lose_condition(self):
        for i in range(3):
            vertical = self.return_indexes("up", i, reverse=True)
            horizontal = self.return_indexes("left", i, reverse=True)
            for j in range(4):
                first_v, second_v = (
                    self.blocks[vertical[j][0][0]][vertical[j][0][1]],
                    self.blocks[vertical[j][1][0]][vertical[j][1][1]]
                )
                first_h, second_h = (
                    self.blocks[horizontal[j][0][0]][horizontal[j][0][1]],
                    self.blocks[horizontal[j][1][0]][horizontal[j][1][1]]
                )
                if first_v.value == second_v.value and first_v.value != 0:
                    return False
                if first_h.value == second_h.value and first_h.value != 0:
                    return False
        return True

    def button_event(self, button):
        if not self.block_new_events:
            self.block_new_events, to_move, already_used = True, [], []
            self.skip_zero_squares(button)
            for i in range(3):
                for pair in self.return_indexes(button, i, reverse=True):
                    first, second = self.blocks[pair[0][0]][pair[0][1]], self.blocks[pair[1][0]][pair[1][1]]
                    if first.value == second.value and first.value != 0 and first not in already_used:
                        to_move.append([second, first, second.value * 2])
                        self.player_score += second.value * 2
                        self.check_changes = True
                        already_used.append(second)
                        if first.value == 2048:
                            messagebox.showinfo("Win", "You won!")
            self.animation(to_move, button)
            self.skip_zero_squares(button)

            if self.check_changes:
                self.generate_new_value()
                self.check_changes = False
            else:
                if len([[i, j] for i in range(4) for j in range(4) if self.blocks[i][j].value != 0]) == 16:
                    if self.lose_condition():
                        messagebox.showinfo("Defeat", "Game over!")
            self.block_new_events = False
