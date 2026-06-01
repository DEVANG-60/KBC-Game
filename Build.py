import tkinter as tk
from tkinter import messagebox
import random

questions = [
    ["What is another name for India", ["Bharat", "Pradesh", "Granto", "Rising sun"], "a"],
    ["What is (4*2)+12", ["93", "12", "20", "23"], "c"],
    ["Who is PM of India", ["Narendra Modi", "Rahul Gandhi", "Eknath Shinde", "Uddhav Thackeray"], "a"],
    ["Where is Maharashtra located on India map", ["East", "West", "North", "South"], "b"],
    ["National animal of India", ["Dog", "Horse", "Cheetah", "Tiger"], "d"],
    ["Most liked sport in India", ["Kabaddi", "Football", "Cricket", "KhoKho"], "c"],
    ["Which planet is known as the Red Planet", ["Earth", "Mars", "Jupiter", "Venus"], "b"],
    ["Which is the largest ocean", ["Atlantic", "Indian", "Pacific", "Arctic"], "c"],
    ["Who invented computer", ["Charles Babbage", "Einstein", "Newton", "Tesla"], "a"],
    ["Which gas do plants absorb", ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "b"],
    ["Capital of Japan", ["Seoul", "Beijing", "Tokyo", "Bangkok"], "c"],
    ["Fastest land animal", ["Lion", "Tiger", "Cheetah", "Horse"], "c"],
    ["Who wrote National Anthem of India", ["Tagore", "Gandhi", "Nehru", "Ambedkar"], "a"],
    ["Smallest prime number", ["0", "1", "2", "3"], "c"],
    ["Which organ pumps blood", ["Brain", "Lungs", "Heart", "Liver"], "c"]
]

# Prize Money
prizes = [
    1000, 2000, 3000, 6000, 12000,
    24000, 48000, 80000, 160000, 320000,
    640000, 1250000, 2500000, 5000000, 10000000
]
random.shuffle(questions)

current_q = 0
money = 0
time_left = 15
timer_id = None

lifelines = {
    "50-50": True,
    "audience": True,
    "phone": True
}

#Game Window
root = tk.Tk()
root.title("KBC Game")
root.geometry("750x520")
root.configure(bg="#02023a")

#options
money_label = tk.Label(root, text="Money: ₹0", fg="gold",
                       bg="#02023a", font=("Arial", 14, "bold"))
money_label.pack(pady=10)

timer_label = tk.Label(root, text="Time: 15", fg="white",
                       bg="#02023a", font=("Arial", 14, "bold"))
timer_label.pack()

question_label = tk.Label(root, text="", fg="white",
                          bg="#02023a", wraplength=650,
                          font=("Arial", 16, "bold"))
question_label.pack(pady=20)

#Clock
def start_timer():
    global time_left
    time_left = 15
    update_timer()

def update_timer():
    global time_left, timer_id

    timer_label.config(text=f"Time: {time_left}")

    if time_left > 0:
        time_left -= 1
        timer_id = root.after(1000, update_timer)
    else:
        messagebox.showerror("Time Up", f"You lost!\nMoney: ₹{money}")
        root.quit()

def load_question():
    q = questions[current_q]
    question_label.config(text=f"Q{current_q+1}: {q[0]}")

    for i in range(4):
        option_buttons[i].config(
            text=q[1][i],
            state="normal",
            bg="#1a1a6e"
        )

    start_timer()

def check_answer(option):
    global current_q, money

    root.after_cancel(timer_id)

    correct = questions[current_q][2]

    # highlight
    idx = ord(option) - 97
    option_buttons[idx].config(bg="orange")
    root.update()
    root.after(800)

    # highlight correct Answer
    correct_idx = ord(correct) - 97
    option_buttons[correct_idx].config(bg="green")
    root.update()
    root.after(800)

    if option == correct:
        money += prizes[current_q]
        money_label.config(text=f"Money: ₹{money}")

        current_q += 1
        if current_q < len(questions):
            load_question()
        else:
            messagebox.showinfo("Winner", f"You won ₹{money}")
            root.quit()
    else:
        messagebox.showerror("Wrong", f"You lost!\nMoney: ₹{money}")
        root.quit()

#LifeLines
def use_5050():
    if not lifelines["50-50"]:
        return

    lifelines["50-50"] = False

    correct = questions[current_q][2]
    correct_index = ord(correct) - 97

    options = [0,1,2,3]
    options.remove(correct_index)

    remove = random.sample(options, 2)

    for i in remove:
        option_buttons[i].config(state="disabled")

def audience_poll():
    if not lifelines["audience"]:
        messagebox.showinfo("Info", "Already used!")
        return

    lifelines["audience"] = False

    correct = questions[current_q][2]
    result = {}

    for opt in ["a","b","c","d"]:
        if opt == correct:
            result[opt] = random.randint(40,70)
        else:
            result[opt] = random.randint(5,20)

    text = "\n".join([f"{k.upper()}: {v}%" for k,v in result.items()])
    messagebox.showinfo("Audience Poll", text)

def phone_friend():
    if not lifelines["phone"]:
        messagebox.showinfo("Info", "Already used!")
        return

    lifelines["phone"] = False

    correct = questions[current_q][2]

    if random.random() < 0.8:
        ans = correct
    else:
        ans = random.choice(["a","b","c","d"])

    messagebox.showinfo("Phone Friend", f"I think answer is {ans.upper()}")

#Buttons Ui
frame = tk.Frame(root, bg="#02023a")
frame.pack()

option_buttons = []
for i in range(4):
    btn = tk.Button(frame, width=25, height=2,
                    bg="#1a1a6e", fg="white",
                    font=("Arial", 12, "bold"),
                    command=lambda i=i: check_answer(chr(97+i)))
    btn.grid(row=i//2, column=i%2, padx=10, pady=10)
    option_buttons.append(btn)

# Lifeline buttons
frame2 = tk.Frame(root, bg="#02023a")
frame2.pack(pady=15)

tk.Button(frame2, text="50-50", bg="gold", command=use_5050).grid(row=0, column=0, padx=10)
tk.Button(frame2, text="Audience Poll", bg="gold", command=audience_poll).grid(row=0, column=1, padx=10)
tk.Button(frame2, text="Phone", bg="gold", command=phone_friend).grid(row=0, column=2, padx=10)

load_question()
root.mainloop()
