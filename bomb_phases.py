##################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: Daniel Jaffe and Jordano Liberato
#################################
# import the configs

from bomb_configs import *
# other imports
from tkinter import *
import tkinter
from threading import Thread
from time import sleep
import os
import sys
from random import *
#########
# classes
#########
# the LCD display GUI
class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window, bg="black")
        # make the GUI fullscreen
        window.attributes("-fullscreen", False)
        # we need to know about the timer (7-segment display) to be able to pause/unpause it
        self._timer = None
        # we need to know about the pushbutton to turn off its LED when the program exits
        self._button = None
        # setup the initial "boot" GUI
        self.setupBoot()
    # sets up the LCD "boot" GUI
    def setupBoot(self):
        # set column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        # the scrolling informative "boot" text
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 14), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)
        self.pack(fill=BOTH, expand=True)
    # sets up the LCD GUI
    def setup(self):
        # the timer
        self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
        self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        # the toggle switches status
        self._ltoggles = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Toggles phase: ")
        #row span was made bigger to allow for question and choices
        self._ltoggles.grid(row=2, column=0, columnspan=3, rowspan = 5, sticky=NW)

        self._ltoggles2 = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18))
        #row span was made bigger to allow for question and choices
        self._ltoggles2.grid(row=3, column=0, columnspan=3, sticky=W)

        self._ltoggles3 = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18))
        # row span was made bigger to allow for question and choices
        self._ltoggles3.grid(row=4, column=1, sticky=W)

        self._ltoggles4 = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18))
        # row span was made bigger to allow for question and choices
        self._ltoggles4.grid(row=5, column=1, sticky=W)

        self._ltoggles5 = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18))
        # row span was made bigger to allow for question and choices
        self._ltoggles5.grid(row=6, column=1, sticky=W)

        # the keypad passphrase
        self._lkeypad = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Keypad phase: ")

        self._lkeypad.grid(row=7, column=0, columnspan=3, sticky=W)
        # the jumper wires status
        self._lwires = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Wires phase: ")
        self._lwires.grid(row=8, column=0, columnspan=3, sticky=W)
        # the pushbutton status
        self._lbutton = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Button phase: ")
        self._lbutton.grid(row=9, column=0, columnspan=3, sticky=W)

        # the strikes left
        self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
        self._lstrikes.grid(row=10, column=0, sticky=W)
        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._bpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Pause",
                                          anchor=CENTER, command=self.pause)
            self._bpause.grid(row=6, column=0, pady=40)
            # the quit button
            self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit",
                                         anchor=CENTER, command=self.quit)
            self._bquit.grid(row=6, column=2, pady=40)
            
            self._hex_entry = Entry(self, bg="black", fg="#00ff00", font=("Courier New", 18))
            self._hex_entry.grid(row=11, column=1, sticky=W)
            self._bsubmit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Submit", anchor=CENTER, command=self.submit_hex)
            self._bsubmit.grid(row=11, column=1, pady=40, padx=10)
    '''        
    def submit_hex(self):
        hex_input = self._hex_entry.get().replace(' ', '').upper()
        # Check if any input was entered
        if hex_input:  # This will be False if the input is empty
            if hex_input == hex(keypad._target)[2:].upper():
                keypad._defused = True
                print("Correct input! Bomb defused.")
            else:
                keypad._failed = True
                print("Incorrect input! Try again.")
        else:
            # Handle the scenario where no keypad was touched
            print("No input detected. Please enter a valid hexadecimal code.")
        self._hex_entry.delete(0, END)  # Clear the input field after submission.

'''
    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer
    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button
    # pauses the timer
    def pause(self):
        if (RPi):
            self._timer.pause()
    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, success=False):
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._lstrikes.destroy()
        self._ltoggles2.destroy()
        self._ltoggles3.destroy()
        self._ltoggles4.destroy()
        self._ltoggles5.destroy()

        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bquit.destroy()
        # reconfigure the GUI
        # the retry button
        self._bretry = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Retry", anchor=CENTER,
                                      command=self.retry)
        self._bretry.grid(row=1, column=0, pady=40)
        # the quit button
        self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER,
                                     command=self.quit)
        self._bquit.grid(row=1, column=2, pady=40)
    # re-attempts the bomb (after an explosion or a successful defusion)
    def retry(self):
        # re-launch the program (and exit this one)
        os.execv(sys.executable, ["python3"] + [sys.argv[0]])
        exit(0)
    # quits the GUI, resetting some components
    def quit(self):
        if (RPi):
            # turn off the 7-segment display
            self._timer._running = False
            self._timer._component.blink_rate = 0
            self._timer._component.fill(0)
            # turn off the pushbutton's LED
            for pin in self._button._rgb:
                pin.value = True
        # exit the application
        exit(0)
# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        # phases have an electronic component (which usually represents the GPIO pins)
        self._component = component
        # phases have a target value (e.g., a specific combination on the keypad, the proper jumper wires to "cut", etc)
        self._target = target
        # phases can be successfully defused
        self._defused = False
        # phases can be failed (which result in a strike)
        self._failed = False
        # phases have a value (e.g., a pushbutton can be True/Pressed or False/Released, several jumper wires can be "cut"/False, etc)
        self._value = None
        # phase threads are either running or not
        self._running = False
# the timer phase
class Timer(PhaseThread):
    def __init__(self, component, initial_value, name="Timer"):
        super().__init__(name, component)
        # the default value is the specified initial value
        self._value = initial_value
        # is the timer paused?
        self._paused = False
        # initialize the timer's minutes/seconds representation
        self._min = ""
        self._sec = ""
        # by default, each tick is 1 second
        self._interval = 1
    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            if (not self._paused):
                # update the timer and display its value on the 7-segment display
                self._update()
                self._component.print(str(self))
                # wait 1s (default) and continue
                sleep(self._interval)
                # the timer has expired -> phase failed (explode)
                if (self._value == 0):
                    self._running = False
                self._value -= 1
            else:
                sleep(0.1)
    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)
    # pauses and unpauses the timer
    def pause(self):
        # toggle the paused state
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._component.blink_rate = (2 if self._paused else 0)
    # returns the timer as a string (mm:ss)
    def __str__(self):
        return f"{self._min}:{self._sec}"

class Keypad(PhaseThread):
    def __init__(self, component, name="Keypad"):
        super().__init__(name, component, target)
        '''
        target = randint(0, 2**8 - 1)  # Generate a random 8-bit binary number
        self._display_hexadecimal = ""
    def run(self):
        self._running = True
        while self._running:
            # Display the target in hexadecimal
            self._display_hexadecimal = f"Target: {hex(self._target)[2:].upper()}"
            # Get user input
            user_input = input("Enter the hexadecimal equivalent of the binary number: ")
            # Check if the user input is correct
            if user_input.upper() == hex(self._target)[2:].upper():
                self._defused = True
            else:
                self._failed = True
                self._strikes += 1
            sleep(1)
    def __str__(self):
        if self._defused:
            return "DEFUSED"
        elif self._failed:
            return f"STRIKES: {self._strikes}"
        else:
            return self._display_hexadecimal
        '''
# Wires phase class
class Wires(PhaseThread):
    def __init__(self, component, target, name="Wires"):
        super().__init__(name, component, target)
        self._display_binary_numbers = ""
    def run(self):
        self._running = True
        while self._running:
            self.wire_state = 0
            # Compute the wire state based on the value of the pins
            for i, pin in enumerate(self._component):
                if pin.value:  # Assuming pin.value is True if the wire corresponding to the pin is pulled
                    self.wire_state |= (1 << (len(self._component) - 1 - i))
            # Debugging output
            print(f"Current wire state: {bin(self.wire_state)}")
            print(f"Target state: {bin(self._target)}")
            # Check if the current wire state matches the target
            if self.wire_state == self._target:
                self._defused = True
                self._running = False  # Optionally stop checking once defused
                print("Bomb defused!")
            else:
                self._failed = True  # Consider what should trigger a failure
            sleep(1)  # Sleep to prevent too rapid checking
    def __str__(self):
        if self._defused:
            return "DEFUSED"
        elif self._failed:
            return "STRIKE"
        else:
            return f"Current State: {bin(self.wire_state)[2:].zfill(5)}"
# Further class definitions (e.g., Keypad, Button, etc.) would follow here
# This is an example instantiation, which you would normally place in the part of your code
# that sets up and starts thread objects:
# component_wires = [YourWireComponentSetupHere]  # Setup your wire component list
# target_wires = 0b11000  # Example target
# wires = Wires(component_wires, target_wires)
# wires.start()  # Starting the Wires thread
# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, target, color, timer, name="Button"):
        super().__init__(name, component_state, target)
        # the default value is False/Released
        self._value = False
        # has the pushbutton been pressed?
        self._pressed = False
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        # the pushbutton's randomly selected LED color
        self._color = color
        # we need to know about the timer (7-segment display) to be able to determine correct pushbutton releases in some cases
        self._timer = timer
        # The amount of time the superpower freezes the timer
        self._time_frozen = 0
    # This will give the user a chance to get a 5 minute freeze in time with a 5 percent chance of getting it
    def chance(self):
        random = randint(1, 50)
        if random == 50:
            return 300
        else:
            return False
    # runs the thread
    def run(self):
        self._running = True
        # set the RGB LED color
        self._rgb[0].value = False if self._color == "R" else True
        self._rgb[1].value = False if self._color == "G" else True
        self._rgb[2].value = False if self._color == "B" else True
        while (self._running):
            # While chance is not false return the ablity to have the chance to get a super freeze
            if self.chance() == 300:
                # Time frozen for a random amout of time either 10 20 or 30 seconds
                self._time_frozen = self.chance()
            else:
                # No ability to get the superfreeze
                self._time_frozen = choice([10, 20, 30])
            # get the pushbutton's state
            self._value = self._component.value
            # Color starts on green
            self._rgb[0].value = True
            self._rgb[1].value = False
            self._rgb[2].value = True
            if (self._value):
                # note it
                self._pressed = True
                # it is released
            else:
                # was it previously pressed?
                if (self._pressed):
                    # Once the button is push a blue color shows up and a 10 second timer extension start
                    self._rgb[0].value = True
                    self._rgb[1].value = True
                    self._rgb[2].value = False
                    # Freezes time for 10 seconds
                    self._timer.pause()
                    sleep(self._time_frozen)
                    # resumes the timer
                    self._timer.pause()
                    # Timer button is under cooldown for 60 seconds and color changes to red
                    self._rgb[0].value = False
                    self._rgb[1].value = True
                    self._rgb[2].value = True
                    sleep(60)
                    self._pressed = False
    # returns the pushbutton's state as a string
    def __str__(self):
        if (not self._rgb[0].value):
            return ("You are now on cooldown!")
        elif (not self._rgb[2].value):
            return (f"Time freeze is now active for {self._time_frozen} seconds!")
        elif (not self._rgb[1].value):
            return "Your time freeze now usable!"

# the toggle switches phase
class Toggles(PhaseThread):
    def __init__(self, component, target, name="Toggles"):
        super().__init__(name, component, target)
    #Give the incorrect possible answer
    #Incorrect answers are chosen at random but are close to the real answer
    def incorrect_answers(self,decimal):
        incorrect_list =[]
        for i in range(0,3):
            incorrect_list.append(bin(decimal + randint(5000,1000000)))
        return incorrect_list


    def run(self):
        self._running = True
        while self._running:
            # Give a random decimal number
            self._decimal = randint(20000000, 5000000000)
            # Taking the random decimal number and move it into binary
            self._correct_answer = bin(self._decimal)
            # All answers
            self._all_answers = self.incorrect_answers(self._decimal)
            self._all_answers.append(self._correct_answer)
            # Mixing up the answers so they are not in the same spot everytime
            shuffle(self._all_answers)
            # List of questions with their options and correct answers
            self._question = f"Convert the decimal {self._decimal} to binary!"
            self._options = [self._all_answers[0], self._all_answers[1], self._all_answers[2], self._all_answers[3]]
            # Display text
            self._display_text_toggle = f"{self._question} \nA) {self._options[0]} \nB) {self._options[1]} \nC) {self._options[2]} \nD) {self._options[3]}"
            # Display the question and options together
            #Get the answer the user selected
            answer_selected = self.get_selected_answer()
            # Check if the selected answer is correct
            # If answer is correct you have won the game
            if str("answer_selected") == str("self._correct_answer"):
                self._defused = True
            #If all the toggles are off then the toggles should continue to run
            elif answer_selected == "All False":
                self._running = True
            # If answer is incorrect you have lost the game you are only given one chance since you have 1 strikes on self.failed
            else:
                self._failed = True
    def get_selected_answer(self):
        # Put the toggles in a list
        toggle_list = []
        for toggle in self._component:
            toggle_list.append(toggle.value)

        # Checks which toggles are True and then outputs the letter that corresponds with each toggle
        if toggle_list == [True, False, False, False]:
            return self._all_answers[0]
        elif toggle_list == [False, True, False, False]:
            return self._all_answers[1]
        elif toggle_list == [False, False, True, False]:
            return self._all_answers[2]
        elif toggle_list == [False, False, False, True]:
            return self._all_answers[3]
        elif toggle_list == [False, False, False, False]:
            return "All False"
        else:
            # Return F for failed if more than one toggle is on
            return "F"
        pass
    #returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        elif self._failed:
            return "failed"
        else:
            return self._display_text_toggle
