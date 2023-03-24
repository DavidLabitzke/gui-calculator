from tkinter import Tk, Canvas, Label, Button
import operator

# Global Variables
num1 = None
operation = None
num2 = None
num2_started = False

# Color Constants
BLUE = "#87CEEB"
RED = "#F47174"
GREY = "#d3d3d3"
LIME_GREEN = "#85FF00"
BLACK = "black"
ORANGE = "orange"

# Font Constants
DECIMAL_FONT = ("Helvetica", 24)
COMMON_BUTTON_FONT = ("Helvetica", 18)
BLACK_BUTTON_FONT = ("Helvetica", 14)
LARGE_BUTTON_FONT = ("Helvetica", 36)

# Creates window
window = Tk()
window.title("Calculator")
window.geometry("505x505")
window.resizable(width=False, height=False)


# Creates canvas where our calculator items will sit
canvas = Canvas(height=500, width=500, background=GREY, borderwidth=3, relief="solid")
canvas.place(relx=0.5, rely=0.5, anchor="center")


# Functions for erasing part of or all the number on screen
def clear_function():
    """Resets the number on screen to zero, and resets global variables back to None/False"""
    global num1, operation, num2, num2_started
    number_label['text'] = "0"
    num1 = None
    operation = None
    num2 = None
    num2_started = False


def back_function():
    """Erases the last number on screen. If it's a single digit number, it gets replaced with a 0"""
    new_number = number_label["text"][:-1]
    if new_number == "":
        new_number = "0"
    number_label["text"] = add_comma(new_number)


# Formats numbers with commas
def add_comma(number):
    """Formats numbers with commas in the correct places, accounting for decimal points"""
    number = number.replace(",", "")
    decimal_index = None
    for index, char in enumerate(number):
        if char == ".":
            decimal_index = index
    int_number = int(number[:decimal_index])
    number_with_commas = ('{:,}'.format(int_number))
    if decimal_index:
        final_result = f"{number_with_commas}{number[decimal_index:]}"
        return final_result
    else:
        return number_with_commas


# Functions affecting the displayed number
def number_to_put(string_number):
    """Adds the inputted string number on screen. If the number on screen is 0,
    it will be replaced by the inputted string number"""
    if number_label["text"] == "0":
        number_label["text"] = string_number
    elif number_label['text'] == "-0":
        number_label['text'] = f"-{string_number}"
    else:
        new_number = f"{number_label['text']}{string_number}"
        number_label["text"] = add_comma(new_number)


def put_decimal():
    """Places a decimal point if possible"""
    if "." in number_label["text"]:
        pass
    else:
        stripped_number = number_label["text"].replace(',', "")
        float_number = float(stripped_number)
        new_number = str(float_number)[:-1]
        number_label["text"] = add_comma(new_number)


def change_polarity():
    """Changes the number to either positive or negative"""
    if number_label["text"][0] == "-":
        number_label["text"] = number_label["text"][1:]
    else:
        number_label["text"] = f"-{number_label['text']}"


# Logic gates for number_to_put, put_decimal, and change_polarity
def perform_function(variable, action):
    """First checks if it is possible to add characters to the screen, then calls the appropriate function"""
    if len(number_label["text"]) >= 15:
        pass
    else:
        if action == number_to_put:
            action(variable)
        else:
            action()


def logic_gate(variable, action):
    """Logic gate for the number_to_put, put_decimal, and change_polarity functions"""
    global num1, operation, num2_started
    if num1 and operation:
        if not num2_started:
            number_label["text"] = variable
            num2_started = True
        else:
            perform_function(variable, action)
    else:
        perform_function(variable, action)


# Operations Functions
def operation_function(string_operator):
    """Stores the number on screen as num1, and the given operator as operation, given that these equal None"""
    global num1, operation
    if not num1:
        num1 = number_label["text"]
    if not operation:
        operation = string_operator


def equals_function():
    """First, saves the current number on screen as global num2. Then will perform an operation on
    num1 and num2, depending on what is stored in operation, and return the output.
    In the case of a ZeroDivisionError, the program will shut down"""
    global num1, operation, num2, num2_started
    if not num1 or not operation:
        pass
    else:
        num2 = number_label["text"]
        num1 = num1.replace(",", "")
        num2 = num2.replace(",", "")
        ops = {"+": operator.add, "-": operator.sub, "x": operator.mul, "/": operator.truediv}
        try:
            final_result = str(ops[operation](float(num1), float(num2)))
            if final_result[-2:] == ".0":
                final_result = final_result[:-2]
        except ZeroDivisionError:
            num1 = None
            final_result = None
            number_label["text"] = "0"
            window.destroy()
        try:
            check_number = final_result[:12]
            formatted_num1 = add_comma(check_number)
            num1 = formatted_num1
            number_label["text"] = formatted_num1
        except TypeError:
            pass
        finally:
            operation = None
            num2 = None
            num2_started = False


# Number Label on top
number_label = Label(bg="white", fg="black", text="0", font=LARGE_BUTTON_FONT, borderwidth=3, relief="solid",
                     anchor="e")
number_label.place(in_=canvas, width=430, height=80, relx=0.08, rely=0.09)

# Clear/Back Buttons
clear_button = Button(bg=BLACK, fg="white", text="Clear", font=BLACK_BUTTON_FONT, borderwidth=3, relief="solid",
                      command=clear_function)
clear_button.place(in_=canvas, width=60, height=60, relx=0.8, rely=0.35)

back_button = Button(bg=BLACK, fg="white", text="Back", font=BLACK_BUTTON_FONT, borderwidth=3, relief="solid",
                     command=back_function)
back_button.place(in_=canvas, width=60, height=60, relx=0.8, rely=0.5)

# Mathematical Symbols Buttons
pos_neg_button = Button(text="+/-", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=LIME_GREEN,
                        command=lambda variable="-0", action=change_polarity: logic_gate(variable, action))
pos_neg_button.place(in_=canvas, width=60, height=60, relx=.08, rely=.8)

decimal_button = Button(text=".", font=DECIMAL_FONT, borderwidth=3, relief="solid", bg=LIME_GREEN,
                        command=lambda variable="0.", action=put_decimal: logic_gate(variable, action))
decimal_button.place(in_=canvas, width=60, height=60, relx=0.42, rely=0.8)

# Operations Buttons
add_button = Button(text="+", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=RED,
                    command=lambda string_operator="+": operation_function(string_operator))
add_button.place(in_=canvas, width=60, height=60, relx=0.6, rely=0.8)

subtract_button = Button(text="-", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=RED,
                         command=lambda string_operator="-": operation_function(string_operator))
subtract_button.place(in_=canvas, width=60, height=60, relx=0.6, rely=0.65)

multiply_button = Button(text="x", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=RED,
                         command=lambda string_operator="x": operation_function(string_operator))
multiply_button.place(in_=canvas, width=60, height=60, relx=0.6, rely=0.5)

division_button = Button(text="/", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=RED,
                         command=lambda string_operator="/": operation_function(string_operator))
division_button.place(in_=canvas, width=60, height=60, relx=0.6, rely=0.35)

equals_button = Button(text="=", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=ORANGE,
                       command=equals_function)
equals_button.place(in_=canvas, width=60, height=140, relx=0.8, rely=0.65)

# Numbers Buttons
zero_button = Button(text="0", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=BLUE,
                     command=lambda variable="0", action=number_to_put: logic_gate(variable, action))
zero_button.place(in_=canvas, width=60, height=60, relx=0.25, rely=0.8)

one_button = Button(text="1", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=BLUE,
                    command=lambda variable="1", action=number_to_put: logic_gate(variable, action))
one_button.place(in_=canvas, width=60, height=60, relx=0.08, rely=0.65)

two_button = Button(text="2", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=BLUE,
                    command=lambda variable="2", action=number_to_put: logic_gate(variable, action))
two_button.place(in_=canvas, width=60, height=60, relx=0.25, rely=0.65)

three_button = Button(text="3", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=BLUE,
                      command=lambda variable="3", action=number_to_put: logic_gate(variable, action))
three_button.place(in_=canvas, width=60, height=60, relx=0.42, rely=0.65)

four_button = Button(text="4", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=BLUE,
                     command=lambda variable="4", action=number_to_put: logic_gate(variable, action))
four_button.place(in_=canvas, width=60, height=60, relx=0.08, rely=0.5)

five_button = Button(text="5", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=BLUE,
                     command=lambda variable="5", action=number_to_put: logic_gate(variable, action))
five_button.place(in_=canvas, width=60, height=60, relx=0.25, rely=0.5)

six_button = Button(text="6", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=BLUE,
                    command=lambda variable="6", action=number_to_put: logic_gate(variable, action))
six_button.place(in_=canvas, width=60, height=60, relx=0.42, rely=0.5)

seven_button = Button(text="7", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=BLUE,
                      command=lambda variable="7", action=number_to_put: logic_gate(variable, action))
seven_button.place(in_=canvas, width=60, height=60, relx=0.08, rely=0.35)

eight_button = Button(text="8", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=BLUE,
                      command=lambda variable="8", action=number_to_put: logic_gate(variable, action))
eight_button.place(in_=canvas, width=60, height=60, relx=0.25, rely=0.35)

nine_button = Button(text="9", font=COMMON_BUTTON_FONT, borderwidth=3, relief="solid", bg=BLUE,
                     command=lambda variable="9", action=number_to_put: logic_gate(variable, action))
nine_button.place(in_=canvas, width=60, height=60, relx=0.42, rely=0.35)

# Activates Window
window.mainloop()
