import json
import os


def read_json(filename: str) -> dict:
    """ Reads and returns the data stored in the given JSON file. """
    file_exists_error(filename)
    with open(filename, 'r') as json_infile:
        return json.load(json_infile)

def write_json(data: dict, filename: str, indent: int = None):
    """ Writes the given data to the given JSON file. """
    with open(filename, 'w+') as json_outfile:
        json.dump(data, json_outfile, indent=indent)

def format_json(data: dict, indent: int = None) -> str:
    """ Returns the given data as a JSON formatted string. """
    return json.dumps(data, indent=indent)

def file_exists(filename: str) -> bool:
    """ Returns whether the given file exists. """
    return filename in os.listdir()

def file_exists_error(filename: str) -> bool:
    """ Returns True if the given file exists, otherwise raises a FileNotFoundError. """
    if file_exists(filename) is False:
        raise FileNotFoundError(filename)
    return True

def spotify_id_from_link(spotify_link: str) -> str:
    """ Extracts and returns the Spotify ID from the given Spotify link. """
    return spotify_link.split('/')[-1].split('?')[0]
