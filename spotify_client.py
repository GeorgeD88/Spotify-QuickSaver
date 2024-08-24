import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import config_handler as config
import time

SCOPES = [
    "user-read-playback-state",     # Get current playback
    "user-read-currently-playing",  # Get current user playing track
    "user-library-read",            # Check user's saved tracks (user library)
    "user-library-modify",          # Add/remove saved tracks (user library)
    "playlist-read-private",        # Read user's private playlists
    "playlist-modify-public",       # Add/remove user playlist tracks
    "playlist-modify-private"       # Add/remove user playlist tracks
]


class SpotifyClient:
    """ Wrapper for the Spotipy library that simplifies interaction with the Spotify API. """

    def __init__(self, notifier, logger, teardown_func):
        self.notifier = notifier
        self.logger = logger
        self.teardown = teardown_func  # Teardown function from QuickSaver

        # Initialize the Spotify auth manager and create the Spotify API client
        self._load_api_creds()
        self.auth_manager = self._init_spotify_auth_manager()
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def _load_api_creds(self):
        """ Loads the Spotify API credentials from the config file and defines them. """
        config_file = config.get_spotify_creds()#self._except_os_error(config.get_spotify_creds)
        self.client_id = config_file['client_id']
        self.client_secret = config_file['client_secret']
        self.redirect_uri = config_file['redirect_uri']

    def _init_spotify_auth_manager(self):
        """ Initializes Spotify's OAuth authorization manager. """
        return SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=SCOPES
        )

    # !!! ===v TODO: v=== !!!
    # def _except_error(self, try_func):
    #     """ Tries to run the given the function while catching errors. """
    #     try:
    #         return try_func()
    #     # TODO: see what needs to be changed for regular python
    #     # only thing to consider would be FileNotFoundError
    #     except OSError as e:
    #         self.logger.error(f'error received [{errno.errorcode[e.errno]}] handling accordingly...')
    #         self._handle_os_error(e)

    # def _handle_error(self, e: OSError):
    #     """ Handles errors that were safely caught. """

    #     # Build log string and get notifier method (handle unexpected errors differently)
    #     errorcode = errno.errorcode[e.errno] if e.errno in errno.errorcode else e.errno
    #     log_string = f'received [{errorcode}]'
    #     notify_error = self.notifier.trigger_os_error

    #     # Unexpected error
    #     if e.errno not in [errno.ENOENT, errno.ENOMEM]:
    #         notify_error = self.notifier.trigger_unexpected_os_error
    #         log_string += ' <unexpected>'

    #         # Add args to output if they exist
    #         if len(e.args) > 1:
    #             log_string += ' args: ' + ', '.join(e.args[1:])

    #     # File not found error
    #     elif e.errno == errno.ENOENT:
    #         log_string += f' {e.args[1]} {e.args[2]}'
    #     # Cannot allocate memory
    #     elif e.errno == errno.ENOMEM:
    #         log_string += ' <Cannot allocate memory> args: ' + ', '.join(e.args[1:])

    #     # Log and notify error, then teardown and exit program
    #     self.logger.error(log_string)
    #     notify_error()
    #     self.teardown()  # Cleans up LEDs, closes the logger, and exits the program

    # !! REFRESH LOOP !!
    # def start_access_token_refresh_loop(self):
    #     # TODO: look into how spotipy handles refreshing
    #     # je pense qu'il rafraîchit si tu fais une requête mais les jetons ont expiré
    #     # TODO: still have a refresh loop that will refresh every 20 minutes so that the tokens are always fresh.
    #     # Something we can also do is make the refresh directly after a user's input (wait 5 secs, incase e.g. they need to undo),
    #     # this makes sure we do it at a time when they won't likely need the device
    #     """ Starts a loop that refreshes the Spotify access tokens
    #         every 20 minutes and retries upon failures. """

    #     last_refresh_time = time.time()

    #     while True:
    #         # Deal with memory (code from vergogh)
    #         # gc.collect()
    #         # gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

    #         curr_time = time.time()

    #         # Refresh tokens every 20 minutes
    #         if curr_time - last_refresh_time >= REFRESH_INTERVAL:
    #             # Retry every 10 minutes if the access tokens fails to refresh
    #             if self._refresh_access_token() is False:
    #                 curr_time = self.start_retry_token_refresh_loop(curr_time)
    #             last_refresh_time = curr_time

    #         # Sleep to reduce CPU usage
    #         time.sleep(60)

    # def start_retry_token_refresh_loop(self, failed_refresh_time: int) -> int:
    #     """ Starts a loop that retries to refresh the Spotify access tokens every 10 minutes
    #         until it is successful, and returns the time of the successful refresh. """
    #     last_refresh_time = failed_refresh_time

    #     while True:
    #         curr_time = time.time()

    #         # Retry to refresh tokens every 10 minutes
    #         if curr_time - last_refresh_time >= RETRY_INTERVAL:
    #             # Return the time of the token refresh if it's successful
    #             if self._refresh_access_token() is True:
    #                 return curr_time
    #             last_refresh_time = curr_time

    #         # Sleep to reduce CPU usage
    #         time.sleep(60)
    # !!! ===^ TODO: ^=== !!!

    def current_user_id(self) -> str:
        """ Gets the current user's ID. """
        return self.sp.me()['id']

    def current_playback(self) -> bool:
        """ Gets information about the user's current playback. """
        return self.sp.current_playback()

    def is_playback_active(self) -> bool:
        """ Checks whether the user has an active playback session.  """
        return self.current_playback() is not None

    def currently_playing_track(self) -> str:
        """ Gets the currently playing track ID (None if there's no active playback session). """
        response = self.sp.current_user_playing_track()
        return response['item']['id'] if response is not None else None

    def add_saved_tracks(self, track_id: str):
        """ Adds the given track to the user's Spotify library (saved tracks). """
        self.sp.current_user_saved_tracks_add([track_id])

    def remove_saved_tracks(self, track_id: str):
        """ Removes the given track from the user's Spotify library (saved tracks). """
        self.sp.current_user_saved_tracks_delete([track_id])

    def contains_saved_tracks(self, track_id: str) -> bool:
        """ Checks whether the given track is saved in the user's Spotify library (saved tracks). """
        return self.sp.current_user_saved_tracks_contains([track_id])[0]

    def get_playlist_owner_id(self, playlist_id: str) -> str:
        """ Gets the owner ID of the given playlist. """
        try:
            # Get playlist info of specified playlist ID
            return self.sp.playlist(playlist_id, fields='owner(id)')['owner']['id']

        except SpotifyException as sp_err:
            # Received 404 error, assumed to be due to non-existent playlist
            if sp_err.http_status == 404:
                return None
            # Received unexpected error but not 404 HTTP status
            else:
                self.logger.error('Unexpected SpotifyException in client.get_playlist_owner_id: ' + sp_err.__str__())
                return None

    def add_track_to_playlist(self, track_id: str, playlist_id: str):
        """ Adds the given track to the specified playlist. """
        self.sp.playlist_add_items(playlist_id, [track_id])

    def remove_track_from_playlist(self, track_id: str, playlist_id: str):
        """ Removes the given track from the specified playlist. """
        self.sp.playlist_remove_all_occurrences_of_items(playlist_id, [track_id])

    def create_new_playlist(self, plist_name: str, description: str = None) -> str:
        """ Creates a new Spotify playlist using the provided details. """
        return self.sp.user_playlist_create(self.current_user_id(), plist_name, description=description)['id']

    def get_playlist_tracks(self, playlist_id: str) -> list[str]:
        """ Gets all the tracks in the given playlist. """

        # Make initial call to API
        results = self.sp.playlist_tracks(playlist_id)
        playlist_tracks = []

        # Helper function to extract all track IDs from the current page of results
        def nested():
            for track in results['items']:
                if track['track']['id'] is not None:  # Avoid null IDs (usually local files)
                    playlist_tracks.append(track['track']['id'])

        # Continuously page the API response and extract the track IDs
        nested()
        while results['next']:
            results = self.sp.next(results)
            nested()

        return playlist_tracks
