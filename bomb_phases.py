##################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: Daniel Jaffe and Jordano Liberato
#################################
# import the configs

import os
import sys
import tkinter
from threading import Thread
from time import sleep
from tkinter import *
import pygame
from bomb_configs import *

# got import chatgpt
#########
# classes
#########
# the LCD display GUI
# Initializing pygame
pygame.init()

def music():
    # added music
    pygame.mixer.music.load("unstoppable.mp3")
    pygame.mixer.music.set_volume(.5)
    pygame.mixer.music.play(1)

# Added voice over
pygame.mixer.music.load("start of game voice.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(1)
sleep(50)


class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window, bg="black")
        # make the GUI fullscreen
        window.attributes("-fullscreen", True)
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
        self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 16), text="Time left: ")
        self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        # the toggle switches status
        self._ltoggles = Label(self, bg="black", fg="#00ff00", font=("Courier New", 16), text="Toggles phase: ")
        # row span was made bigger to allow for question and choices
        self._ltoggles.grid(row=2, column=0, columnspan=3, rowspan=5, sticky=NW)

        self._lkeypad_binary = Label(self, bg="black", fg="#00ff00", font=("Courier New", 12),
                                     text="Keypad Binary code: ")
        self._lkeypad_binary.grid(row=7, column=0, columnspan=3, sticky=W)
        self._lkeypad_entry = Label(self, bg="black", fg="#00ff00", font=("Courier New", 12), text="Keypad Entry: ")
        self._lkeypad_entry.grid(row=8, column=0, columnspan=3, sticky=W)

        # the jumper wires status
        self._lwires = Label(self, bg="black", fg="#00ff00", font=("Courier New", 16), text="Wires phase: ")
        self._lwires.grid(row=9, column=0, columnspan=3, sticky=W)

        # the pushbutton status
        self._lbutton = Label(self, bg="black", fg="#00ff00", font=("Courier New", 16), text="Button phase: ")
        self._lbutton.grid(row=10, column=0, columnspan=3, sticky=W)
        # the strikes left
        self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 16), text="Strikes left: ")
        self._lstrikes.grid(row=11, column=0, sticky=W)
        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._bpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 16), text="Pause",
                                          anchor=CENTER, command=self.pause)
            self._bpause.grid(row=6, column=0, pady=40)
            # the quit button
            self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 16), text="Quit",
                                         anchor=CENTER, command=self.quit)
            self._bquit.grid(row=6, column=2, pady=40)

    # This code updates the display for keypad phase with the current binary code and the user entry
    def update_keypad_display(self, binary_value, entry_value):
        self._lkeypad_binary.config(text=f"Keypad Binary code: {binary_value}")
        self._lkeypad_entry.config(text=f"Keypad Entry: {entry_value}")

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
    def conclusion(self, strikes_left, active_phases):
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lkeypad_binary.destroy()
        self._lkeypad_entry.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._lstrikes.destroy()


        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bquit.destroy()
        # reconfigure the GUI
        # the retry button
        self._bretry = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 16), text="Retry", anchor=CENTER,
                                      command=self.retry)
        self._bretry.grid(row=1, column=0, pady=40)
        # the quit button
        self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 16), text="Quit", anchor=CENTER,
                                     command=self.quit)
        self._bquit.grid(row=1, column=2, pady=40)

        # Used chatgpt to help me addwith creating a image and resizing it
        # Displaying the image if you lose
        if strikes_left <= 0 or str(self._timer) == ('00:00'):
            losing_image = "losing image.gif"  # Replace with your image path
            img1 = PhotoImage(file=losing_image)
            self.image1 = Label(self, bg="black", image=img1)
            self.image1.image = img1  # Keep a reference to the image to prevent garbage collection
            self.image1.grid(row=2, column=1, columnspan=3, sticky=W)
            # added voice over
            pygame.mixer.music.load("mission failed.mp3")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(1)

        # Displaying the image if you win
        if active_phases == 0:
            winning_image = "winning image.gif"  # Replace with your image path
            img1 = PhotoImage(file=winning_image)
            self.image1 = Label(self, bg="black", image=img1)
            self.image1.image = img1  # Keep a reference to the image to prevent garbage collection
            self.image1.grid(row=2, column=1, columnspan=3, sticky=W)
            # added voice over
            sleep(1)
            pygame.mixer.music.load("Bomb defuse sound.mp3")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(1)

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
        # added music
        music()
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
# Used chatGPT to generate the binary code and binary-to-hex-code
class Keypad(PhaseThread):
    def __init__(self, keypad, target, name="Keypad"):
        super().__init__(name, keypad, target)
        self._value = ""
        # the keypad pins
        self._keypad = keypad 
        # this is the variable to generate binary code
        self._binary_code = self.generate_binary_code()
        # this is the variable to converts the binary to hexadecimal
        self._hex_target = self.binary_to_hex(self._binary_code)  

    # this function generates a six 4-digit random binary number
    def generate_binary_code(self):
        binary_code = [format(randint(0, 9), '04b') for _ in range(6)]
        return " ".join(binary_code)

    # this funtion converts binary code to hexadecimal
    def binary_to_hex(self, binary_code):
        binary_code = binary_code.replace(" ", "")
        hex_code = ""
        for i in range(0, len(binary_code), 4):
            hex_digit = binary_code[i:i + 4]
            hex_code += format(int(hex_digit, 2), 'X')
        return hex_code

    # this function is used to map keypad input to hexadecimal characters
    def map_key_to_hex(self, key):
        key_to_hex_map = {
            0: '0', 1: '1', 2: '2', 3: '3',
            4: '4', 5: '5', 6: '6', 7: '7',
            8: '8', 9: '9', '*': '*', '#': '#'
        }
        return key_to_hex_map.get(key, "")

    # runs the thread
    def run(self):
        self._running = True
        self._value = ""
        while self._running:
            # Displays the initial target binary code
            self._update_callback(self._binary_code, self._value)  
            # process keys when keypad key(s) are pressed
            # this will handle when the first key is presed, also handles case when no key is pressed
            if self._keypad.pressed_keys:
                # debounce
                while self._keypad.pressed_keys:
                    try:
                        key = self._keypad.pressed_keys[0]
                    except IndexError:
                        key = ""
                    sleep(0.1)
                # if the STAR key is pressed, then it will clear the input
                if key == "*" and STAR_CLEARS_PASS:
                    self._value = ""
                else:
                    hex_char = self.map_key_to_hex(key)
                    if len(self._value) < MAX_PASS_LEN and hex_char != "":
                        self._value += hex_char
                # Here we check if the input matches the target hexadecilas code
                if self._value.upper() == self._hex_target:
                    self._update_callback(self._binary_code, "Defused")
                    self._defused = True
                    sleep(4)
                    self._update_callback(self._binary_code, "Defused")
                    self._running = False
                elif len(self._value) == MAX_PASS_LEN and self._value.upper() != self._hex_target:
                    self._failed = True
                    self._update_callback(self._binary_code, "One strike added")
                else:
                    self._update_callback(self._binary_code, self._value)
            sleep(0.1)
        self._running = False

    # Returns proper string if defused, failed to defuse, or neither 
    def __str__(self):
        if self._defused:
            return "Defused"
        elif self._failed:
            return "strike added"
        else:
            return (f"Current input value: {self._value}")

    # Setter for update callback (updates the display)
    def set_update_callback(self, callback):
        self._update_callback = callback


# Wires phase class
class Wires(PhaseThread):
    def __init__(self, component, target, letter, name="Wires"):
        super().__init__(name, component, target)
        self._display_binary_numbers = ""
        # This tracks the state of the previous wires
        self.previous_state = None
        # Tracks the number of strikes
        self._strikes = 0  
        # This stores the letters that match the corresponding target 
        self._letter = letter  

    def run(self):
        self._running = True
        while self._running:
            self.wire_state = 0
            # Compute the wire state based on the value of the pins
            for i, pin in enumerate(self._component):
                if pin.value:  # Assuming pin.value is True if the wire corresponding to the pin is pulled
                    self.wire_state |= (1 << (len(self._component) - 1 - i))
            # Check if the current wire state matches the target
            if self.wire_state == self._target:
                self._defused = True
            else:
                 # Ensure this isn't the first check
                if self.previous_state is not None:  
                    if not self._check_wire_removal_correctness(self.previous_state, self.wire_state):
                        self._failed = True

            self.previous_state = self.wire_state  # Update the previous state after processing
            sleep(1)  # Sleep to prevent too rapid checking

    def _check_wire_removal_correctness(self, old_state, new_state):
        # Check if removing a wire was correct (only one wire should be considered at a time for simplicity)
        # Incorrect removal if new_state has a 0 where target has a 1 at the same position
        return (old_state & ~new_state) & self._target == 0
    
    def __str__(self):
        if self._defused:
            return "DEFUSED"
        elif self._strikes > 0:
            return "Strike added! Incorrect wire removed."
        else:
            return f"Letter: {self._letter} | Current State: {bin(self.wire_state)[2:].zfill(5)}"


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
                    # added music with 5 different tracks
                    button_voice_choice = randint(1, 5)
                    # Once the button is push a blue color shows up and a 10 second timer extension start
                    self._rgb[0].value = True
                    self._rgb[1].value = True
                    self._rgb[2].value = False
                    # Freezes time for 10 seconds
                    self._timer.pause()
                    if button_voice_choice == 1:
                        # added voice over
                        pygame.mixer.music.load("button sound 1.mp3")
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play(1)
                        sleep(self._time_frozen)
                        music()
                    elif button_voice_choice == 2:
                        # added voice over
                        pygame.mixer.music.load("button sound 2.mp3")
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play(1)
                        sleep(self._time_frozen)
                        music()
                    elif button_voice_choice == 3:
                        # added voice over
                        pygame.mixer.music.load("button sound 3.mp3")
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play(1)
                        sleep(self._time_frozen)
                        music()
                    elif button_voice_choice == 4:
                        # added voice over
                        pygame.mixer.music.load("button sound 4.mp3")
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play(1)
                        sleep(self._time_frozen)
                        music()
                    elif button_voice_choice == 5:
                        # added voice over
                        pygame.mixer.music.load("button sound 5.mp3")
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play(1)
                        sleep(self._time_frozen)
                        music()
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
    def __init__(self, component, target, timer, name="Toggles"):
        super().__init__(name, component, target)
        self._timer = timer

    # Give the incorrect possible answer
    # Incorrect answers are chosen at random but are close to the real answer
    def incorrect_answers(self, decimal):
        incorrect_list = []
        for i in range(0, 3):
            incorrect_list.append(bin(decimal + 2 ** (randint(10, 20)))[2:])
        return incorrect_list

    def update_question(self):
        # Give a random decimal number
        self._decimal = randint(20000000, 500000000)
        # Taking the random decimal number and move it into binary
        self._correct_answer = bin(self._decimal)[2:]  # Remove the 0b prefix
        # All answers
        self._all_answers = self.incorrect_answers(self._decimal)
        self._all_answers.append(self._correct_answer)
        # Mixing up the answers so they are not in the same spot everytime
        shuffle(self._all_answers)
        # List of questions with their options and correct answers
        self._question = f"Convert the decimal {self._decimal} to binary!"
        self._options = [self._all_answers[0], self._all_answers[1], self._all_answers[2], self._all_answers[3]]
        # Display text
        self._display_text_toggle = (f"{self._question} \n" +
                                     f"A) {self._options[0]} \n" +
                                     f"B) {self._options[1]} \n" +
                                     f"C) {self._options[2]} \n" +
                                     f"D) {self._options[3]} ")

        # Display the question and options together
        return self._display_text_toggle, self._correct_answer

    def run(self):
        self._running = True
        self.update_question()
        while self._running:
            # Answer the user selected
            self.answer_selected = self.get_selected_answer()
            # Check if the selected answer is correct
            # If answer is correct you have won the game
            # Get the answer the user selected
            if str(self.answer_selected) == str(self._correct_answer):
                self._defused = True
            # If all the toggles are off then the toggles should continue to run
            elif self.answer_selected == "All False":
                self._running = True
            # If answer is incorrect you have lost the game you are only given one chance since you have 1 strikes on self.failed
            else:
                self._failed = True
            sleep(1)

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

    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        elif self._failed:
            return "You have failed!"
        else:
            return self._display_text_toggle
