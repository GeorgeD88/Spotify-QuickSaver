from spotify_client import SpotifyClient

# Constants
IS_DUPE = "IS_DUPLICATE"  # Status code for duplicate track
CONFIG = "config.json"


class QuickSaveController:
    """ Controller that handles the main quick saving functionality of the app (backend). """

    def __init__(self, notifier, logger, teardown_func):

        # Initialize the SpotifyClient
        self.client = SpotifyClient(notifier, logger, teardown_func)

        # Holds the last saved track and its playlist in a tuple (track_id, playlist_id)
        self.last_save = None

    def set_playlist_info(self, main_playlist_id: str, other_playlist_id: str,):
        """ Sets the playlists IDs and creates local records of the playlist contents (avoids adding duplicates). """
        self.main_playlist_id = main_playlist_id
        self.other_playlist_id = other_playlist_id
        self.main_plist_tracks = set(self.client.get_playlist_tracks(main_playlist_id))
        self.other_plist_tracks = set(self.client.get_playlist_tracks(other_playlist_id))

    def start_access_token_refresh_loop(self):
        self.client.start_access_token_refresh_loop()

    def validate_user_playlist(self, plist_id: str) -> bool:
        """ Validates that the given playlist ID exists on Spotify and is owned by the user. """
        plist_owner_id = self.client.get_playlist_owner_id(plist_id)

        # Playlist does not exist
        if plist_owner_id is None:
            return False

        # Playlist exists, return whether it's owned by the current user
        return plist_owner_id == self.client.user_id

    def create_sampler_playlist(self, plist_label: str) -> str:
        """ Creates a sampler playlist for the provided label and returns the new playlist ID. """
        plist_name = 'Sampler ' + plist_label.title()
        description = 'Playlist used by QuickSaver to save songs without distractions!'
        return self.client.create_new_playlist(plist_name, description)

    def toggle_like(self) -> tuple[str, bool]:
        """ Toggles currently playing track's library save (likes/unlikes track).

        Returns:
            tuple[str, bool]: Returns the ID of the currently playing track, and whether it's saved now.
        """

        track_id = self.client.currently_playing_track()

        # Terminate the function if no track is currently playing
        if track_id is None:
            return None

        # Check if the track is saved to the library
        is_saved = self.client.contains_saved_tracks(track_id)

        # Toggle the track's "liked" status
        if is_saved:
            self.client.remove_saved_tracks(track_id)
        else:
            self.client.add_saved_tracks(track_id)

        # Negate is_saved status from before toggling to the status after toggling
        return track_id, not is_saved

    def quick_save(self, playlist_id: str) -> tuple[str, str]:
        """ Quick saves currently playing track to given playlist and user library, and stores details in last save. """

        # Get the currently playing track
        track_id = self.client.currently_playing_track()

        # Terminate the function if no track is currently playing
        if track_id is None:
            return None

        # Record the saved track and its corresponding playlist in last_save
        self.last_save = (track_id, playlist_id)

        # Save the track to the library (likes song)
        self.client.add_saved_tracks(track_id)

        # Get the reference to the respective playlist's local track list
        playlist_tracks = self.get_local_track_list(playlist_id)

        # Terminate the function if the track is already in the playlist (duplicate track)
        if track_id in playlist_tracks:
            return track_id, IS_DUPE

        # Add the track to the Spotify playlist and the local track list
        self.client.add_track_to_playlist(track_id, playlist_id)
        playlist_tracks.add(track_id)

        return self.last_save

    def undo_last_save(self) -> tuple[str, str]:
        """ Undoes last quick save by removing the track from the playlist and user library. """

        # Check if the last save exists before attempting to undo it
        if self.last_save is None:
            return None

        # Get the last save details and update the last save to None
        (track_id, playlist_id), self.last_save = self.last_save, None

        # Remove the track from the user's library, the playlist, and the local track list
        self.client.remove_saved_tracks(track_id)
        self.client.remove_track_from_playlist(track_id, playlist_id)
        self.get_local_track_list(playlist_id).remove(track_id)

        return track_id, playlist_id

    def get_local_track_list(self, playlist_id: str) -> set[str]:
        """ Gets the corresponding local track list based on the given playlist ID. """
        return self.main_plist_tracks if playlist_id is self.main_playlist_id else self.other_plist_tracks
