# Spotify QuickSave :zap: :notes:
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-orange.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&style=flat)](https://www.python.org/)
[![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi&style=flat)](https://www.raspberrypi.com/)
[![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white&style=flat)](https://developer.spotify.com/dashboard)

Welcome to **Spotify QuickSave**! The Raspberry Pi-powered Python app designed to enhance your music listening experience. It enables quick and effortless song saving with a quick button press, minimizing interruptions to your workflow.

I found that when I was doing work while listening to a new playlist, I would keep finding new songs I loved and wanted to save to my library. The problem is switching to the Spotify app every few minutes to add songs to my library was very disruptive to my workflow. This drove me to create **Spotify QuickSave**. With QuickSave all it takes is a quick press of a button and the currently playing song gets quickly saved to your library and a previously specified playlist. If you for some reason change your mind about saving that song, you can easily undo the last save with the push of another button.

This allows you to effortlessly save songs while you're browsing the web, doing homework, working on a project, etc. I actually found myself constantly needing QuickSave **_while_ I was developing it,** and I'm even using it as I write this README.

Ready to give it a try? Download the repo and follow the instructions below to get started!

## License :penguin:
**Spotify QuickSave** is released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html). See the [LICENSE](LICENSE) file for more details.

## What I Learned :books:
- Programming self-sustaining embedded systems.
- Working with Raspberry Pis and designing circuits.
- Designing very robust system architecture and learning modular software design patterns.
- Automated system startup and operation using `systemd` for seamless, headless execution.
- Implemented robust mechanisms for autonomous error handling and logging.

## Getting Started :rocket:

### Prerequisites :package:
Before you can run the project, make sure you have the following dependencies installed:
- Python 3
- [Spotipy](https://pypi.org/project/spotipy/) | Spotify API wrapper | `pip install spotipy`
- [GPIO Zero](https://pypi.org/project/gpiozero/) | Raspberry Pi | `pip install gpiozero`

If you're still having trouble running QuickSaver, your Python version might be too old to use the required packages. Either install older versions of the packages that work with your version of Python, or upgrade your Python version.

### Setup :hammer_and_wrench:
To begin, you will need a Raspberry Pi capable of running an Operating System; any RasPi except for the RasPi Pico. It is recommended to install a light, headless OS on the RasPi you're using, such as **Raspberry Pi OS Lite**. You can find numerous tutorials online for setting up your RasPi and installing an OS.

Once you have a RasPi with a working OS, you'll need to download this repository. If you installed a headless OS as recommended, you'll need to SSH into your Pi to access it; which means opening a terminal session on the Pi, through your local network. You can use the [following guide](https://www.raspberrypi.com/documentation/computers/remote-access.html) from the official RaspberryPi site to get started. SSH into your Pi and use `git` to clone this repository to your RasPi.

Direct your attention to the `empty_config.json` file. You're going to be filling in this configuration file with information about your Spotify and Raspberry Pi setup as you go through the rest of the README. Start by renaming the file to `config.json`.

### Spotify API Setup :notes:
**Spotify QuickSave** uses the Spotify API, so you'll be required to create your own API keys on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard); don't worry, it' pretty simple!

Follow these steps if you need help:
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in with your Spotify account.
2. Click on the _"Create an App"_ button and fill out the required fields.
3. After creating the app, open the _"Settings"_ tab to view your client ID and secret, you'll need them in the next step.
4. Go to the *Redirect URIs* field and add the following `http://localhost:8888/callback`

Once you have your client ID and secret, open the `config.json` file in the project directory and paste your client ID and secret in the appropriate spots. It looks like this:

```json
{
    "spotify": {
        "client_id": "CLIENT ID HERE",
        "client_secret": "CLIENT SECRET HERE",
        "redirect_uri": "http://localhost:8888/callback"  # <- DO NOT CHANGE THIS
    },
    ...
```

### Raspberry Pi Setup
The Raspberry Pi setup will require you to wire 4 buttons and 3 LEDs:
- **4 Buttons:**
  1. Toggle Like
  2. Save to main playlist
  3. Save to other playlist
  4. Undo last save
- **3 LEDs:**
  1. Green (for success signals)
  2. Yellow (for warnings)
  3. Red (for errors)

You can wire the circuit however you like, as long as you include the components listed above, with each one starting from a GPIO pin, and ending at a ground pin; note what GPIO pins you use, as they will need to be added to the `config.json` file.

Below is a schematic of how I wired the circuit (the resisters are 100Ω) as an example that you can copy. Whether you copy my circuit or wire it your own way, **DO SO AT YOUR OWN RISK**, because electronics can be dangerous and you may damage your hardware if you're not sure what you're doing. It's not that difficult but it's important to do the proper research and exercise caution.

![Raspberry Pi QuickSave Schmeatic](Spotify-QuickSave_Schematic.png)

Compare your circuit to a [GPIO pinout diagram](https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png?hash=df7d7847c57a1ca6d5b2617695de6d46) to figure out the GPIO pin numbers you used, then fill them in in `config.json`. It looks like this:

```json
    ...
    "gpio_pins": {
        "led_success": 0, # Green LED
        "led_alert": 0,   # Yellow LED
        "led_error": 0,   # Red LED
        "button_toggle_like": 0,
        "button_save_main": 0,
        "button_save_other": 0,
        "button_undo_save": 0
    }
}
```

### Spotify Playlist IDs (optional)
You might have noticed the following section in `config.json`:

```json
    ...
    "playlists": {
         "main_playlist": "LEAVE UNTOUCHED TO ALLOW QS TO AUTO CREATE",
         "other_playlist": "LEAVE UNTOUCHED TO ALLOW QS TO AUTO CREATE"
     },
    ...
```

**Spotify QuickSave** gives you the option to pick between 2 different playlists to save to. When you run the app, QuickSaver will grab the playlist IDs of these 2 playlist options from `config.json` and use them whenever you save a song. If the playlist configuration in `config.json` is left untouched, QuickSaver will automatically create new playlists on the first run of the app and update `config.json` with the new playlist IDs. Once created, you can edit the names, descriptions, and images of these playlists if desired; make sure to differentiate between the main playlist and the other playlist.

## Usage :technologist:
The purpose of **Spotify QuickSave** is to be able to easily and quickly save the *currently playing song* to your playlist and library with the press of a button, I like to call this a *"Quicksave"*. When a Quicksave is triggered, the currently playing song is liked (saved to your Spotify library) and added to the playlist specified in the config file.

Below are all the functions of QuickSaver:
1. **Toggle Like:** Likes/unlikes the currently playing song. In Spotify, this means saving/unsaving it to your library.
2. **Save to Main:** Saves the currently playing song to the "main" playlist.
3. **Save to Other:** Saves the currently playing song to the "other" playlist.
4. **Undo Last Save:** Undoes the last save by unliking the song and removing it from the playlist it was saved to (main or other); this can not be performed more than once at a time, you will need to save another song before being able to undo.

QuickSave allows you to save to 2 different playlists because sometimes you might want to differentiate between your regular saves and another category of saves. A common usage would be listening to a radio of mostly one genre, like pop, so you would likely want the songs you quicksave to be added to your pop playlist. Oftentimes, you might come across one or two songs that are not pop songs (do not match the main genre). When this happens, you can instead quicksave the song to the ***other playlist*** while keeping the ***main playlist*** strictly for pop songs. Later when you're less busy, you can add the entire ***main playlist*** to your pop playlist, and sort the few songs in the ***other playlist*** to their respective playlists.

Another common usage would be to use the ***main playlist*** for songs you 100% would like to save, while using the ***other playlist*** for songs you might save. Once you're done with your focused session, you can come back to Spotify and give the other songs a second look. The ideas are endless, it's up to you to decide how you want to use the 2 playlists.

If you change your mind about the song you just quicksaved, you can ***undo save*** to unlike it and remove it from the playlist it was saved to. **Note** that you can only undo one time after saving a song, meaning you won't be able to undo again until you quicksave another song.

In addition to quicksaving, you can simply ***toggle like*** to save (or unsave) the currently playing song to your Spotify library.
 
<!-- # TODO: continue writing. -->

set up service and wifi and stuff