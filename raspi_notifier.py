# Raspberry Pi
from gpiozero import LED
from time import sleep

DURATION = 0.7  # Duration for standard indicators and warnings

# TODO: add token freshing notifier, start blinking, and then turn it off once the refreshal ends

class RasPiNotifier:
    """ RasPi notifier class that allows the app to trigger LED responses on the Pi. """

    def __init__(self, gpio_pins: dict):
        # Set GPIO pin numbers
        self.success_led = LED(gpio_pins['led_success'])
        self.alert_led = LED(gpio_pins['led_alert'])
        self.error_led = LED(gpio_pins['led_error'])

    def clean_up_leds(self):
        """ Cleans up the LEDs by closing each one. """
        self.success_led.close()
        self.alert_led.close()
        self.error_led.close()

    def _flash_led(self, flashing_led: LED, duration: float):
        """ Flashes the given LED for the specified duration. """
        flashing_led.on()
        sleep(duration)
        flashing_led.off()

    def _flash_multiple_leds(self, flashing_leds: list[LED], duration: float):
        """ Flashes the multiple given LEDs simultaneously for the specified duration. """
        for flash_led in flashing_leds:
            flash_led.on()
        sleep(duration)
        for flash_led in flashing_leds:
            flash_led.off()

    def _quick_flash_led_repeatedly(self, flashing_led: LED, flash_count: int,
                                    flash_speed: float = 0.13, background: bool = False):
        """ Repeatedly flashes the given LED for the specified number of times. """
        flashing_led.blink(on_time=flash_speed, n=flash_count, background=background)

    def trigger_song_unlike_success(self, duration: float = DURATION):
        """ Flashes the success and alert LED simultaneously to indicate
            that the song was unliked after toggling. """
        self._flash_multiple_leds([self.success_led, self.alert_led], duration)

    def trigger_song_saved_success(self, duration: float = DURATION):
        """ Flashes the success LED to indicate that a song was saved. """
        self._flash_led(self.success_led, duration)

    def trigger_undo_save_success(self, duration: float = DURATION):
        """ Flashes the success and alert LED simultaneously
            to indicate that the last save was undid. """
        self._flash_multiple_leds([self.success_led, self.alert_led], duration)

    def trigger_duplicate_song_warning(self, duration: float = DURATION):
        """ Flashes the alert LED to warn that a duplicate song was attempted to be added. """
        self._flash_led(self.alert_led, duration)

    def trigger_max_undo_warning(self, duration: float = DURATION):
        """ Flashes the alert LED to warn that only one undo is allowed per save. """
        self._flash_led(self.alert_led, duration)

    def trigger_no_song_playing_warning(self):
        """ Flashes the alert LED repeatedly to warn that no song
            is currently playing, so no song can be saved. """
        self._quick_flash_led_repeatedly(self.alert_led, 3)

    def trigger_os_error(self):
        """ Flashes the error LED repeatedly to indicate an OS error was received. """
        self._quick_flash_led_repeatedly(self.error_led, 4)

    def trigger_unexpected_os_error(self, duration: float = DURATION):
        """ Flashes ____ to indicate an unexpected OS error was received. """
        # TODO:
        pass

    def trigger_critical_error(self):
        """ Triggers a sequence w/ all LEDs to indicate a critical error and program shutdown. """
        # TODO idea: do the same flash as file_not_found_error but with all the LEDs,
        # and then hold them on for half a sec or something.
        # most importantly flash them a few times and then hold them

        # Flash all the LEDs repeatedly for half the duration
        flash_speed, flash_count = 0.12, 3
        self.error_led.blink(on_time=flash_speed, n=flash_count)
        self.alert_led.blink(on_time=flash_speed, n=flash_count)
        self.success_led.blink(on_time=flash_speed, n=flash_count, background=False)

        # Hold all the LEDs on for half the duration
        self.error_led.on()
        self.alert_led.on()
        self.success_led.on()
        sleep(0.7)
        self.error_led.off()
        self.alert_led.off()
        self.success_led.off()

    def trigger_wifi_connecting_status(self, flash_speed: float = 0.09):
        """ Triggers a single wave animation w/ all LEDs (that can be called repeatedly)
            to indicate that the device is connecting to Wi-Fi. """
        self.success_led.on()
        sleep(flash_speed)
        self.alert_led.on()
        self.success_led.off()
        sleep(flash_speed)
        self.error_led.on()
        self.alert_led.off()
        sleep(flash_speed)
        self.error_led.off()

    def trigger_wifi_connection_failed(self):
        """ Flashes the error LED repeatedly to indicate the Wi-Fi failed to connect. """
        self._quick_flash_led_repeatedly(self.error_led, 3)

    def trigger_ready_lights(self, blink_count: int = 3, blink_time: float = 0.1):
        """ Triggers a sequence w/ all LEDs to indicate that the app is ready. """

        # Initiate blinking of the success and error LEDs
        self.success_led.blink(on_time=blink_time, n=blink_count)
        self.error_led.blink(on_time=blink_time, n=blink_count)

       # Wait for the LEDs to blink once, then start blinking the alert LED
        sleep(blink_time)
        self.alert_led.blink(on_time=blink_time, n=blink_count, background=False)

        # Turns off all the LEDs once the blink method finishes and unblocks
        self.success_led.off()
        self.error_led.off()
        self.alert_led.off()
