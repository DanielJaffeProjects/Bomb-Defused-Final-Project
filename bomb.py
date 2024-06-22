#################################
# CSC 102 Defuse the Bomb Project
# Main program
# Team: Daniel Jaffe and Jordano Liberato
#################################

# import the configs
from bomb_configs import *
# import the phases
from bomb_phases import *

###########
# functions
###########
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
    pass
    '''
    global timer, keypad, wires, button, toggles
    
    # setup the timer thread
    timer = Timer(component_7seg, COUNTDOWN)
    # bind the 7-segment display to the LCD GUI so that it can be paused/unpaused from the GUI
    gui.setTimer(timer)
    # setup the keypad thread
    keypad = Keypad(component_keypad, keypad_target, gui)
    # setup the jumper wires thread
    wires = Wires(component_wires, wires_target, gui)
    # setup the pushbutton thread
    button = Button(component_button_state, component_button_RGB, button_target, button_color, timer)
    # bind the pushbutton to the LCD GUI so that its LED can be turned off when we quit
    gui.setButton(button)
    # setup the toggle switches thread
    toggles = Toggles(component_toggles, toggles_target, gui)

    # start the phase threads
    timer.start()
    keypad.start()
    wires.start()
    button.start()
    toggles.start()
    '''

# checks the phase threads
def check_phases():
    global gui
    global active_phases
    if gui.timer._running:
        gui._ltimer["text"] = f"Time left: {gui.timer}"
    else:
        # the countdown has expired -> explode!
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(100, gui.conclusion, False)
        # don't check any more phases
        return
    # check the keypad
    if gui.keypad._running:
        # update the GUI
        gui._lkeypad["text"] = f"Combination: {gui.keypad}"
        # the phase is defused -> stop the thread
        if gui.keypad._defused:
            keypad._running = False
            active_phases -= 1
        # the phase has failed -> strike
        elif gui.keypad._failed:
            turn_off()
            gui.after(100, gui.conclusion, False)
            return
    # check the wires
    if gui.wires._running:
        # update the GUI
        gui._lwires["text"] = f"Wires: {gui.wires}"
        # the phase is defused -> stop the thread
        if gui.wires._defused:
            gui.wires._running = False
            active_phases -= 1
        # the phase has failed -> strike
        elif gui.wires._failed:
            turn_off()
            gui.after(100, gui.conclusion, False)
            return
    # check the button
    if gui.button._running:
        # update the GUI
        gui._lbutton["text"] = f"Button: {gui.button}"
        # the phase is defused -> stop the thread
        if gui.button._defused:
            gui.button._running = False
            active_phases -= 1
        # the phase has failed -> strike
        elif gui.button._failed:
            strike()
            # reset the button
            gui.button._failed = False
    # check the toggles
    if gui.toggles._running:
        # update the GUI
        gui._ltoggles["text"] = f"Toggles: {gui.toggles}"
        # the phase is defused -> stop the thread
        if gui.toggles._defused:
            gui.toggles._running = False
            active_phases -= 1
        # the phase has failed -> strike
        elif (toggles._failed):
            strike()
            '''
            strike()
            strike()
            '''
            # reset the toggles
            gui.toggles._failed = False

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
    gui.timer._running = False
    gui.keypad._running = False
    gui.wires._running = False
    gui.button._running = False
    gui.toggles._running = False

    # turn off the 7-segment display
    component_7seg.blink_rate = 0
    component_7seg.fill(0)
    # turn off the pushbutton's LED
    for pin in gui.button._rgb:
        pin.value = True

######
# MAIN
######

# initialize the LCD GUI
window = Tk()
global gui
gui = Lcd(window)

# initialize the bomb strikes and active phases (i.e., not yet defused)
strikes_left = NUM_STRIKES
active_phases = NUM_PHASES

# "boot" the bomb
gui.after(1000, bootup)

# display the LCD GUI
window.mainloop()
