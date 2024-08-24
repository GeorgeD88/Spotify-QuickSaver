# 2024 George Doujaiji

import utils as utl

CONFIG_FILE = "config.json"
EMPTY_CONFIG = {
    "spotify": {
        "client_id": None,
        "client_secret": None,
        "redirect_uri": "http://localhost:8888/callback"
    },
    "playlists": {"main_playlist": None, "other_playlist": None},
    "log_filename": "quicksaver.log",
    "gpio_pins": {
        "led_save": 0,
        "led_alert": 0,
        "led_error": 0,
        "button_toggle_like": 0,
        "button_save_main": 0,
        "button_save_other": 0,
        "button_undo_save": 0
    }
}


def create_empty_config():
    """ Writes a template config to the config file. """
    utl.write_json(EMPTY_CONFIG, CONFIG_FILE)

def init_config():
    """ Creates an empty config file if it doesn't already exist
        and returns True if it was able to create it, otherwise False. """
    if utl.file_exists(CONFIG_FILE) is False:
        create_empty_config()
        return True
    return False

def set_config(config: dict):
    """ Writes the given configuration dict to the config file. """
    utl.write_json(config, CONFIG_FILE, indent=4)

def get_config() -> dict:
    """ Reads the config file and returns the configuration dict. """
    utl.file_exists_error(CONFIG_FILE)
    return utl.read_json(CONFIG_FILE)

def get_config_value(key: str, config: dict = None):# -> dict | list:
    """ Retrieves and returns the value associated with the given key from the config file,
        or retrieves the value from the already loaded config if provided. """
    if config is None:
        utl.file_exists_error(CONFIG_FILE)
        config = get_config()

    if key not in config:
        raise KeyError('Key not found in config: ' + key)

    return config[key]

def set_config_value(key: str, new_value):
    """ Stores or updates the given value for
        the specified key in the config file. """
    utl.file_exists_error(CONFIG_FILE)
    config = get_config()
    config[key] = new_value
    set_config(config)

def get_spotify_creds(loaded_config: dict = None) -> dict:
    """ Retrieves and returns the spotify creds. """
    return get_config_value('spotify', loaded_config)

def get_playlist_ids(loaded_config: dict = None) -> dict:
    """ Retrieves and returns the playlist IDs. """
    return get_config_value('playlists', loaded_config)

def get_log_filename(loaded_config: dict = None) -> str:
    """ Retrieves and returns the log filename. """
    return get_config_value('log_filename', loaded_config)

def get_gpio_pin_numbers(loaded_config: dict = None) -> dict:
    """ Retrieves and returns the GPIO pin numbers. """
    return get_config_value('gpio_pins', loaded_config)

def get_wlan_details(loaded_config: dict = None) -> dict:
    """ Retrieves and returns the wlan network details. """
    return get_config_value('wlan', loaded_config)

def set_playlist_id(plist: str, plist_id: str):
    """ Updates the specified playlist ID. """
    plist_ids = get_playlist_ids()
    plist_ids[plist] = plist_id
    set_config_value('playlists', plist_ids)
