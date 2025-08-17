import random
import tkinter as tk

root = tk.Tk()
root.title("Egg Catcher Game")

# Canvas
c = tk.Canvas(root, width=800, height=400, bg="skyblue")
c.pack()

# Ground
c.create_rectangle(-5, 390, 805, 405, fill="green", width=0)

# Basket
basket = c.create_rectangle(350, 370, 450, 390, fill="brown")

eggs = []
score = 0
lives_remaining = 3
egg_speed = 100  # lower = faster
game_over_flag = False

score_text = c.create_text(10, 10, anchor="nw", font=("Arial", 16, "bold"),
                           fill="darkblue", text="Score: " + str(score))
lives_text = c.create_text(10, 40, anchor="nw", font=("Arial", 16, "bold"),
                           fill="darkred", text="Lives: " + str(lives_remaining))

def create_egg():
    if not c.winfo_exists() or game_over_flag:
        return
    x = random.randrange(10, 740)
    egg = c.create_oval(x, 40, x+20, 60, fill="white", width=0)
    eggs.append(egg)
    root.after(3000, create_egg)

def move_eggs():
    if not c.winfo_exists() or game_over_flag:
        return
    for egg in eggs.copy():
        try:
            c.move(egg, 0, 10)
            (eggx, eggy, eggx2, eggy2) = c.coords(egg)
            if eggy2 >= 400:  # egg hit ground
                egg_dropped(egg)
        except tk.TclError:
            pass
    root.after(egg_speed, move_eggs)

def egg_dropped(egg):
    global lives_remaining
    if egg in eggs:
        eggs.remove(egg)
        c.delete(egg)
    lives_remaining -= 1
    c.itemconfigure(lives_text, text="Lives: " + str(lives_remaining))
    if lives_remaining == 0:
        game_over()

def check_catch():
    if not c.winfo_exists() or game_over_flag:
        return
    (basketx1, baskety1, basketx2, baskety2) = c.coords(basket)
    for egg in eggs.copy():
        (eggx1, eggy1, eggx2, eggy2) = c.coords(egg)
        if basketx1 < eggx1 and eggx2 < basketx2 and baskety1 < eggy2 < baskety2:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(10)
    root.after(100, check_catch)

def increase_score(points):
    global score
    score += points
    c.itemconfigure(score_text, text="Score: " + str(score))

def move_left(event):
    (x1, y1, x2, y2) = c.coords(basket)
    if x1 > 0:
        c.move(basket, -20, 0)

def move_right(event):
    (x1, y1, x2, y2) = c.coords(basket)
    if x2 < 800:
        c.move(basket, 20, 0)

def game_over():
    global game_over_flag
    game_over_flag = True
    c.create_text(400, 200, text=f"GAME OVER!\nFinal Score: {score}",
                  font=("Arial", 30, "bold"), fill="red")
    # Exit after 3 seconds
    root.after(3000, root.destroy)

# Controls
c.bind_all("<Left>", move_left)
c.bind_all("<Right>", move_right)

# Start game
create_egg()
move_eggs()
check_catch()

root.mainloop()
