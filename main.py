from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"
back_card = None
current_card = {}

window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# Generate Cards
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")

if len(data) == 0:
    data = pd.read_csv("data/french_words.csv")
data_dict = data.to_dict(orient="records")

def generate_back_card():
    global current_card
    card_front.itemconfig(canvas_image, image=card_back_image)
    card_front.itemconfig(title_text, text="English", fill="white")
    card_front.itemconfig(word_text, text=f"{current_card['English']}", fill="white")

def ok_action():
    global back_card, current_card, data, data_dict
    window.after_cancel(back_card)
    data_dict.remove(current_card)
    if len(data_dict) == 0:
        data = pd.read_csv("data/french_words.csv")
        data_dict = data.to_dict(orient="records")
    else:
        words_to_learn = pd.DataFrame(data_dict)
        words_to_learn.to_csv('data/words_to_learn.csv',index=False)
    generate_card()

def cross_action():
    global back_card
    window.after_cancel(back_card)
    generate_card()

def generate_card():
    global back_card, current_card
    card_front.itemconfig(canvas_image, image=card_front_image)
    current_card = random.choice(data_dict)
    card_front.itemconfig(title_text, text="French", fill="black")
    card_front.itemconfig(word_text, text=f"{current_card['French']}", fill="black")

    back_card = window.after(3000, generate_back_card)



## UI Interface

#Card image
card_front = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
canvas_image = card_front.create_image(400, 263, image=card_front_image)
title_text = card_front.create_text(400, 150, text="Title", font = (FONT_NAME, 35, "italic"))
word_text = card_front.create_text(400, 263, text="Word", font = (FONT_NAME, 55, "bold"))
card_front.grid(column=0, row=0, columnspan=2)

#Buttons
right_button_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_image, highlightthickness=0, command=ok_action)
right_button.grid(row=1, column=1)

wrong_button_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=cross_action)
wrong_button.grid(row=1, column=0)

generate_card()

window.mainloop()



