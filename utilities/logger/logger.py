class Log:
    def __init__(
        self,
        log_console_debug=False,
        log_console_error=False,
        log_file_debug=False,
        log_file_error=False,
        log_file_name=0,
    ):
        self._console_debug_func = self._empty_func
        self._console_error_func = self._empty_func

        self._file_debug_func = self._empty_func
        self._file_error_func = self._empty_func

        self._console_log_init(log_console_debug, log_console_error)
        self._file_log_init(log_file_debug, log_file_error, log_file_name)

    def _empty_func(self, *args):
        pass

    def _error(self, message):
        return f'Error: {message}'

    def _debug(self, message):
        return f'Debug: {message}'

    def debug(self, message):
        self._console_debug_func(self._debug(message))
        self._file_debug_func(f'{self._debug(message)}\n')

    def console_debug(self, message):
        self._console_debug_func(self._debug(message))

    def file_debug(self, message):
        self._file_debug_func(f'{self._debug(message)}\n')

    def error(self, message):
        self._console_error_func(self._error(message))
        self._file_error_func(f'{self._error(message)}\n')

    def console_error(self, message):
        self._console_error_func(self._error(message))

    def file_error(self, message):
        self._file_error_func(f'{self._error(message)}\n')

    def _console_log_init(self, log_console_debug, log_console_error):
        if log_console_debug:
            self._console_debug_func = print

        if log_console_error:
            self._console_error_func = print

    def _file_log_init(self, log_file_debug, log_file_error, log_file_name):
        if not log_file_name:
            return

        try:
            self.log_file = open(log_file_name, 'a')
        except Exception as e:
            print(self._error(e))
            return

        if log_file_debug:
            self._file_debug_func = self.log_file.write

        if log_file_error:
            self._file_error_func = self.log_file.write
