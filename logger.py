import time
import sys

INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"


class Logger:

    SPACES = {INFO: 4, WARNING: 1, ERROR: 3}

    # NOTE: keep `to_console` false when running on Pi. When running on computer, manually pass `to_console=True`
    def __init__(self, filename):
        self.filename = filename
        self.console_available = self.check_console()
        self.file = open(self.filename, 'a+')  # Keep the file open

    def check_console(self):
        """ Checks whether standard output is an interactive file stream (terminal). """
        return sys.stdout.isatty()

    def _log(self, level: str, msg: str, to_file: bool = True, to_console: bool = False):

        # Get the local date and time and manually format it
        local_time = time.localtime()
        timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            local_time[0],  # year
            local_time[1],  # month
            local_time[2],  # day
            local_time[3],  # hour
            local_time[4],  # minute
            local_time[5]   # second
        )
        log_entry = f"{timestamp} [{level}]{self._spacing(level)}{msg}\n"

        # Write to file if required and flush
        if to_file is True:
            self.file.write(log_entry)
            self.file.flush()

        # Print to console if interactive file stream is available
        if to_console is True and self.console_available is True:
            print(log_entry, end='')

    def _spacing(self, level: str):
        return self.SPACES[level] * ' '

    def info(self, msg: str):
        """ Log the given info message to console if available. """
        self._log(INFO, msg, to_file=False, to_console=True)

    def warning(self, msg: str):
        """ Log the given warning message to file, and console if available. """
        self._log(WARNING, msg, to_file=True, to_console=True)

    def error(self, msg: str):
        """ Log the given error message to file, and console if available. """
        self._log(ERROR, msg, to_file=True, to_console=True)

    def close(self):
        # Ensure the file is properly closed
        if self.file:
            self.file.close()
