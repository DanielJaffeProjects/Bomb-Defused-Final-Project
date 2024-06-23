#################################
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
        # the keypad passphrase
        self._lkeypad = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Keypad phase: ")
        self._lkeypad.grid(row=2, column=0, columnspan=3, sticky=W)
        # the jumper wires status
        self._lwires = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Wires phase: ")
        self._lwires.grid(row=3, column=0, columnspan=3, sticky=W)
        # the pushbutton status
        self._lbutton = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Button phase: ")
        self._lbutton.grid(row=4, column=0, columnspan=3, sticky=W)
        # the toggle switches status
        self._ltoggles = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Toggles phase: ")
        self._ltoggles.grid(row=5, column=0, columnspan=2, sticky=W)
        # the strikes left
        self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
        self._lstrikes.grid(row=5, column=2, sticky=W)
        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._bpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Pause",
                                          anchor=CENTER, command=self.pause)
            self._bpause.grid(row=6, column=0, pady=40)
            # the quit button
            self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit",
                                         anchor=CENTER, command=self.quit)
            self._bquit.grid(row=6, column=2, pady=40)
    # Add entry widget for hexadecimal input
        self._hex_entry = Entry(self, bg="black", fg="#00ff00", font=("Courier New", 18))
        self._hex_entry.grid(row=6, column=1, sticky=W)
        # Add submit button for hexadecimal input
        self._bsubmit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Submit", anchor=CENTER, command=self.submit_hex)
        self._bsubmit.grid(row=6, column=1, pady=40, padx=10)
    def submit_hex(self):
        hex_input = self._hex_entry.get().replace(' ', '').upper()
        if hex_input == ''.join(keypad._hex_values):
            keypad._defused = True
        else:
            keypad._failed = True
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
        # Add callback for GUI updates update starts here
        self._update_callback = None
    def set_update_callback(self, callback):
        """Set the callback function for GUI updates."""
        self._update_callback = callback

    def update_gui(self, data):
        """Call the update callback if set."""
        if self._update_callback:
            self._update_callback(data)
            # update ends here
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
# the keypad phase
class Keypad(PhaseThread):
    def __init__(self, component, target, name="Keypad"):
        super().__init__(name, component, target)
        self._value = ""
        self._binary_numbers = self.generate_binary_numbers()
        self._hex_values =[self.binary_to_hex(b) for b in self._binary_numbers]
    def generate_binary_numbers(self):
        return [format(randint(0, 15), '04b') for _ in range(8)]
    def binary_to_hex(self, binary_str):
        return format(int(binary_str, 2), 'X')
    def run(self):
        self._running = True
        while self._running:
            display_text = f"Binary numbers: {' '.join(self._binary_numbers)}"
            self.update_gui(display_text)  # Use the update_gui method

            # Simulate user input for testing
            user_input = input("Enter the hexadecimal values: ")
            if user_input.replace(' ', '').upper() == ''.join(self._hex_values):
                self._defused = True
            else:
                self._failed = True
            sleep(1)
    def __str__(self):
        if self._defused:
            return "DEFUSED"
        else:
            return self._value
# the jumper wires phase
class Wires(PhaseThread):
    def __init__(self, component, target, name="Wires"):
        super().__init__(name, component, target)
    def run(self):
        self._running = True
        while self._running:
            # Check the state of each wire and form a binary number
            wire_state = 0
            for i, pin in enumerate(self._component):
                if pin.value:
                    wire_state |= (1 << (4 - i))  # Convert pin states to a binary number
            # Compare the binary number to the target
            if wire_state == self._target:
                self._defused = True
            else:
                self._failed = True
            # Update the GUI with the current wire state (binary number)
            self.update_gui(f"Wires: {bin(wire_state)[2:].zfill(5)}")
            sleep(1)
    def __str__(self):
        if self._defused:
            return "DEFUSED"
        else:
            wire_state = 0
            for i, pin in enumerate(self._component):
                if pin.value:
                    wire_state |= (1 << (4 - i))
            return bin(wire_state)[2:].zfill(5)
# Example target value for the puzzle (24 in binary is 11000)
wires_target = 24  # This would be set in bomb_configs or dynamically generated
# In bomb_configs or the main script, ensure the wires target is correctly assigned
component_wires = [DigitalInOut(board.D14), DigitalInOut(board.D15), DigitalInOut(board.D18), DigitalInOut(board.D23), DigitalInOut(board.D24)]
for pin in component_wires:
    pin.direction = Direction.INPUT
    pin.pull = Pull.DOWN
# Assign the wires phase with the correct target
wires = Wires(component_wires, 24)
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
        random = randint(1, 500)
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
        # List of questions with their options and correct answers
        self._questions = [
            ("Convert the binary number 11010101101010100101011010101010 to decimal.",
             {"A": "65536", "B": "3584710314", "C": "3560384384", "D": "43887402"}, "C"),("Convert the hexadecimal number AB23FE97 to decimal",
     {"A": "2871262871", "B": "2871263271", "C": "2823262871", "D": "2871262886"}, "A"),
    ("Convert the hexadecimal number 0x1A2F4C7E to binary.",
     {"A": "00011010001011110100110001111110", "B": "10101111010000100101001110111110",
      "C": "00011010001011110010110000011110", "D": "00011010001011110100110000111110"}, "B")
        ]
        # Choose a random question
        self._current_question = choice(self._questions)
        self._question = self._current_question[0]
        self._options = self._current_question[1]
        self._correct_answer = self._current_question[2]
        self._display_text_toggle = ""
    def run(self):
        self._running = True
        while self._running:
            # Display the question and options together
            #Got from ChatGPT
            '''
            self._display_text_toggle = "{}\n{}".format(self._question, "\n".join(self._options))
            #Get the answer the user selected
            '''
            display_text = "{}\n{}".format(self._question, "\n".join([f"{k}: {v}" for k, v in self._options.items()]))
            self.update_gui(display_text)  # Use the update_gui method
            answer_selected = self.get_selected_answer()
            # Check if the selected answer is correct
            # If answer is correct you have won the game
            if answer_selected == self._correct_answer:
                self._defused = True
            #If all the toggles are off then the toggles should continue to run
            elif answer_selected == "All False":
                self._running = True
            # If answer is incorrect you have lost the game you are only given one chance since you have 3 strikes on self.failed
            else:
                self._failed = True
    def get_selected_answer(self):
        # Put the toggles in a list
        toggle_list = []
        print(toggle_list)
        for toggle in self._component:
            toggle_list.append(toggle.value)
            '''
        print(toggle_list)
            '''
        # Checks which toggles are True and then outputs the letter that corresponds with each toggle
        if toggle_list == [True, False, False, False]:
            return "A"
        elif toggle_list == [False, True, False, False]:
            return "B"
        elif toggle_list == [False, False, True, False]:
            return "C"
        elif toggle_list == [False, False, False, True]:
            return "D"
        elif toggle_list == [False, False, False, False]:
            return "All False"
        else:
            # Return F for failed if more than one toggle is on
            return "F"
        pass
    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        elif self._failed:
            return "failed"
        else:
            return self._display_text_toggle
