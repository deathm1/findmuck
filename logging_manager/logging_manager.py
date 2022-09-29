# class imports
from console_manager.console_manager import console_manager

# module imports
import logging
import configparser
import traceback
import os
import platform
from datetime import datetime
import json
from pathlib import Path


class logging_manager():
    """This class acts as an interface to manage logs.
    """
    my_console_manager = None

    @classmethod
    def __init__(self, message: str, level: int, exception: Exception, stack_trace: traceback):
        """Constructor

        Args:
            message (str): Log message string.
            level (int): Log level.
            exception (Exception): Whether there is an exception.
            stack_trace (traceback): Whether there is traceback.
        """
        single_line_message = str(message).replace("\n", " ")
        single_line_message = single_line_message.replace("'", "")
        single_line_message = single_line_message.replace('"', '')
        single_line_exception = "None"
        single_line_stack_trace = "None"
        if (exception == None):
            pass
        else:
            single_line_exception = str(exception).replace("\n", " ")
            single_line_exception = single_line_exception.replace("'", "")
            single_line_exception = single_line_exception.replace('"', '')
        if (stack_trace == None):
            pass
        else:
            single_line_stack_trace = str(
                stack_trace.format_exc()).replace("\n", " ")
            single_line_stack_trace = single_line_stack_trace.replace("'", "")
            single_line_stack_trace = single_line_stack_trace.replace('"', '')
        if (exception == None and stack_trace == None):
            message = f"{single_line_message}"
        elif (exception == None and stack_trace != None):
            message = f"{single_line_message} [Traceback] : {single_line_stack_trace}"
        elif (stack_trace == None and exception != None):
            message = f"{single_line_message} [Exception] : {single_line_exception}"
        else:
            message = f"{single_line_message} [Exception] : {single_line_exception} [Traceback] : {single_line_stack_trace}"

        self.my_console_manager = console_manager()
        try:
            config = configparser.ConfigParser()
            config.read("./config.ini")
        except Exception as e:
            self.my_console_manager.make_console_log(
                f"[logging_interface][__init__] Something went wrong while initializing logger. Error : {str(e)}",
                logging.ERROR
            )
        status_file = self.log_file(message, level, config)
        if (status_file):
            pass
        else:
            self.my_console_manager.make_console_log(
                f"[logging_interface][__init__] Something went wrong while pushing logs to log file.", logging.ERROR)

    @classmethod
    def log_file(self, message, level, config) -> bool:
        """Make logs in a file.

        Args:
            message (str): Log message.
            level (int): Integer level of log.
            config (configparser): Configuration file

        Returns:
            bool: Was log made ?
        """
        try:
            log_location = "./"
            log_directory_name = config.get(
                "LOGGER_CONFIGURATION", "LOG_DIRECTORY")
            current_log_directory = ""
            if (os.path.exists(log_location)):
                current_log_directory = os.path.join(
                    log_location, log_directory_name)
            else:
                current_log_directory = os.path.join(
                    os.getcwd(), log_directory_name)
                self.my_console_manager.make_console_log(
                    f"[logging_interface][log_file] Log location does not exist. Using root location. {str(current_log_directory)}",
                    logging.WARN
                )
            if (os.path.exists(current_log_directory)):
                pass
            else:
                os.mkdir(current_log_directory)
                self.my_console_manager.make_console_log(
                    f"[logging_interface][log_file] Created root log directory. {str(current_log_directory)}",
                    logging.INFO
                )
            current_dt = datetime.now()
            dt_string = current_dt.strftime("%d-%m-%Y")
            current_day_folder = os.path.join(
                current_log_directory, str(dt_string))
            if (os.path.exists(current_day_folder)):
                pass
            else:
                os.mkdir(current_day_folder)
                self.my_console_manager.make_console_log(
                    f"[logging_interface][log_file] Created day wise log directory. {str(current_day_folder)}",
                    logging.INFO
                )
            get_log_name = str(config.get(
                "LOGGER_CONFIGURATION", "LOG_FILENAME")).replace(" ", "_")
            my_log_filename = get_log_name+"_"+str(dt_string)+".log"
            full_filename = os.path.join(current_day_folder, my_log_filename)
            logger = logging.getLogger(config.get(
                "LOGGER_CONFIGURATION", "LOGGER_NAME"))
            logging.basicConfig(
                filename=full_filename, format="[%(asctime)s][%(name)s][%(levelname)s] : %(message)s", )
            logger.setLevel(level)
            if (level == logging.DEBUG):
                logger.debug(message)
            elif (level == logging.INFO):
                logger.info(message)
            elif (level == logging.WARNING):
                logger.warning(message)
            elif (level == logging.ERROR):
                logger.error(message)
            elif (level == logging.CRITICAL):
                logger.critical(message)
            elif (level == logging.NOTSET):
                logger.debug(message)
            else:
                logger.debug(message)
            self.log_file_split(full_filename, current_day_folder, config)
            return True
        except Exception as e:
            self.my_console_manager.make_console_log(
                f"[logging_interface][log_file] Something went wrong. Error : {str(e)}", logging.ERROR)
            return False

    @classmethod
    def log_file_split(self, file_path: str, log_directory: str, config: configparser):
        """This function is responsible for splitting files greater than the threshold.

        Args:
            file_path (str): log file path
            log_directory (str): log directory path
            config (configparser): configparser object
        """
        self.delete_existing_split_logs(file_path, log_directory)
        file_size_in_bytes = os.path.getsize(file_path)
        file_size_in_KB = file_size_in_bytes/1024.0
        file_size_in_MB = file_size_in_KB/1024.0
        threshold = int(config.get("LOGGER_CONFIGURATION", "THRESHOLD"))
        lines_per_log = int(config.get("LOGGER_CONFIGURATION", "SPLIT_LINES"))
        if (file_size_in_MB > threshold):
            lines_in_current_log_file = []
            with open(file_path) as file:
                for line in file:
                    lines_in_current_log_file.append(line)
            current_filename = Path(file_path).stem
            counter = 1
            start = 1
            end = lines_per_log
            part_counter = 1
            for line in lines_in_current_log_file:
                filename = str(current_filename)+"_p"+str(part_counter) + \
                    "_" + str(start)+"_"+str(end)+".log"
                my_filename = os.path.join(log_directory, filename)
                my_file = open(my_filename, "a")
                my_file.write(line)
                my_file.close()
                if (counter >= lines_per_log):
                    part_counter = part_counter + 1
                    start = counter
                    end = 2 * lines_per_log
                    lines_per_log = 2 * lines_per_log
                counter = counter + 1

    @classmethod
    def delete_existing_split_logs(self, file_path: str, log_directory: str):
        """This function delete existing split files in order to create fresh split files.

        Args:
            file_path (str): File path of current large log
            log_directory (str): This is the log directory of the log files.
        """
        list_directory = os.listdir(log_directory)
        if (len(list_directory) != 0):
            for file in list_directory:
                split_filename = str(Path(file).stem)
                if (split_filename != str(Path(file_path).stem)):
                    os.remove(os.path.join(log_directory, file))
