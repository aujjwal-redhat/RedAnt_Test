import logging
import logging.handlers


logger = logging.getLogger(__name__)
class Logging:

    @staticmethod
    def set_logging_options(log_file_path="/tmp/redant.log", log_file_level="I"):
        """
        This function is for configuring the logger
        """
        global logger
        valid_log_level = ['I', 'D', 'W', 'E', 'C']
        log_level_dict = {'I':logging.INFO, 'D':logging.DEBUG, 'W':logging.WARNING,
                'E':logging.ERROR, 'C':logging.CRITICAL}
        log_format = logging.Formatter("[%(asctime)s] %(levelname)s "
                                    "[%(module)s - %(lineno)s:%(funcName)s] "
                                    "- %(message)s")
        if log_file_level not in valid_log_level:
            print("Invalid log level given, Taking Log Level as Info.")
            log_file_level = 'I'
        logger.setLevel(log_level_dict[log_file_level])
        log_file_handler = logging.handlers.WatchedFileHandler(log_file_path)
        log_file_handler.setFormatter(log_format)
        logger.addHandler(log_file_handler)
        return logger

    @staticmethod
    def get_logger_handle():
        return logger

