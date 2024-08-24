# Raspberry Pi
from gpiozero import Button

# constants
from actions import TOGGLE_LIKE, SAVE_MAIN, SAVE_OTHER, UNDO_SAVE, QUIT_APP


class RasPiListener:

    def __init__(self, button_callback, gpio_pins: dict):
        self.callback = button_callback

        # Initialize buttons
        self.toggle_like_button = Button(gpio_pins['button_toggle_like'])
        self.save_main_button = Button(gpio_pins['button_save_main'])
        self.save_other_button = Button(gpio_pins['button_save_other'])
        self.undo_save_button = Button(gpio_pins['button_undo_save'])

        # Map actions to buttons
        self.toggle_like_button.when_pressed = self.toggle_like
        self.save_main_button.when_pressed = self.save_main
        self.save_other_button.when_pressed = self.save_other
        self.undo_save_button.when_pressed = self.undo_save

    def toggle_like(self):
        self.callback(TOGGLE_LIKE)

    def save_main(self):
        self.callback(SAVE_MAIN)

    def save_other(self):
        self.callback(SAVE_OTHER)

    def undo_save(self):
        self.callback(UNDO_SAVE)
