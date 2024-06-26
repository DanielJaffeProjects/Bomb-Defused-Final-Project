# CSC 102 Defuse the Bomb Project
# Main program
# Team: Daniel Jaffe and Jordano Liberato
#################################

import pygame

# import the configs
# import the phases
from bomb_phases import *

###########
# functions
###########
pygame.init()

# generates the bootup sequence on the LCD
def bootup(n=0):
    # if we're not animating (or we're at the end of the bootup text)
    if (not ANIMATE or n == len(boot_text)):
        # if we're not animating, render the entire text at once (and don't process \x00)
        if (not ANIMATE):
            gui._lscroll["text"] = boot_text.replace("\x00", "")
        # configure the remaining GUI widgets
        gui.setup()
        # setup the phase threads, execute them, and check their statuses
        if (RPi):
            setup_phases()
            check_phases()
    # if we're animating
    else:
        # add the next character (but don't render \x00 since it specifies a longer pause)
        if (boot_text[n] != "\x00"):
            gui._lscroll["text"] += boot_text[n]
        # scroll the next character after a slight delay (\x00 is a longer delay)
        gui.after(25 if boot_text[n] != "\x00" else 750, bootup, n + 1)


# sets up the phase threads
def setup_phases():
    global timer, keypad_phase, wires, button, toggles
    # setup the timer thread
    timer = Timer(component_7seg, COUNTDOWN)
    # bind the 7-segment display to the LCD GUI so that it can be paused/unpaused from the GUI
    gui.setTimer(timer)

    # setup the keypad thread
    keypad_phase = Keypad(component_keypad, int(keypad_target))
    keypad_phase.set_update_callback(gui.update_keypad_display)

    # setup the jumper wires thread
    wires = Wires(component_wires, wires_target)
    # setup the pushbutton thread
    button = Button(component_button_state, component_button_RGB, button_target, button_color, timer)
    # bind the pushbutton to the LCD GUI so that its LED can be turned off when we quit
    gui.setButton(button)
    # setup the toggle switches thread
    toggles = Toggles(component_toggles, toggles_target, timer)
    # start the phase threads
    timer.start()
    keypad_phase.start()
    wires.start()
    button.start()
    toggles.start()


# checks the phase threads
def check_phases():
    global active_phases
    def music():
        #added music
        pygame.mixer.music.load("unstoppable.mp3")
        pygame.mixer.music.set_volume(.5)
        pygame.mixer.music.play(1)

    # check the timer
    if (timer._running):
        # update the GUI
        gui._ltimer["text"] = f"Time left: {timer}"
    else:
        # the countdown has expired -> explode!
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(100, gui.conclusion, False)
        # don't check any more phases
        return
    # check the keypad
    if keypad_phase._running:
        gui.update_keypad_display(keypad_phase._binary_code, keypad_phase._value)
        if keypad_phase._defused:
            keypad_phase._running = False
            active_phases -= 1
            #added voice over
            pygame.mixer.music.load("Keypad defuse sound.mp3")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(1)
            sleep(3)
            music()
        elif keypad_phase._failed:
            strike()
            keypad_phase._failed = False
    if (wires._running):
        # update the GUI
        gui._lwires["text"] = f"Wires: {wires}"
        # the phase is defused -> stop the thread
        if (wires._defused):
            wires._running = False
            active_phases -= 1
            # added voice over
            pygame.mixer.music.load("wires defused sound.mp3")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(1)
            sleep(3)
            music()
        # the phase has failed -> strike
        elif (wires._failed):
            strike()
            # reset the wire
            wires._failed = False
    # check the button
    if (button._running):
        # update the GUI
        gui._lbutton["text"] = f"Button: {button}"
        # the phase is defused -> stop the thread
        if (button._defused):
            button._running = False
            active_phases -= 1
            button_voice_choice = randint(1,3)
            if button_voice_choice == 1:
                # added voice over
                pygame.mixer.music.load("button 1 sound.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(1)
                sleep(3)
                music()
            elif button_voice_choice == 2:
                # TODO
                pass
            elif button_voice_choice == 3:
                #TODO
                pass
        # the phase has failed -> strike
        elif (button._failed):
            strike()
            # reset the button
            button._failed = False
    # check the toggles
    if (toggles._running):
        # update the GUI
        gui._ltoggles["text"] = f"Toggles: {toggles}"
        # the phase is defused -> stop the thread
        if (toggles._defused):
            toggles._running = False
            active_phases -= 1
            # added voice over
            pygame.mixer.music.load("toggles defused sound.mp3")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(1)
            sleep(3)
            music()
        # the phase has failed -> strike
        elif (toggles._failed):
            strike()
            strike()
            # reset the toggles
            toggles._failed = False
    # note the strikes on the GUI
    gui._lstrikes["text"] = f"Strikes left: {strikes_left}"
    # too many strikes -> explode!
    if (strikes_left == 0):
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(1000, gui.conclusion, False)
        # stop checking phases
        return
    # the bomb has been successfully defused!
    if (active_phases == 0):
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(100, gui.conclusion, True)
        # stop checking phases
        return
    # check the phases again after a slight delay
    gui.after(100, check_phases)


# handles a strike
def strike():
    global strikes_left

    # note the strike
    strikes_left -= 1


# turns off the bomb
def turn_off():
    # stop all threads
    timer._running = False
    keypad_phase._running = False
    wires._running = False
    button._running = False
    toggles._running = False
    # turn off the 7-segment display
    component_7seg.blink_rate = 0
    component_7seg.fill(0)
    # turn off the pushbutton's LED
    for pin in button._rgb:
        pin.value = True


######
# MAIN
######
# initialize the LCD GUI
window = Tk()
gui = Lcd(window)

# initialize the bomb strikes and active phases (i.e., not yet defused)
strikes_left = NUM_STRIKES
active_phases = NUM_PHASES
# "boot" the bomb
gui.after(1000, bootup)
# display the LCD GUI
window.mainloop()
