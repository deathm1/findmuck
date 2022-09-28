# class imports
from datetime import datetime

# moduel imports
import logging

class console_manager():
    """This class is responsible for generating parsed console output.

    Returns:
        str: Parsed console output.
    """

    @classmethod
    def make_console_log(self, message : str, level : int) -> str:
        """This function is responsible for generating parsed console output.

        Args:
            message (str): Message to be printed on console.
            level (int): logging module level integer, 0, 10, 20...

        Returns:
            str: Returns the parsed message string.
        """
        make_console_log_string = ""
        if(level == logging.DEBUG):
            make_console_log_string = f"[console_output][DEBUG][{str(datetime.now())}] : {message}"
            print(make_console_log_string)
        elif(level == logging.INFO):
            make_console_log_string = f"[console_output][INFO][{str(datetime.now())}] : {message}"
            print(make_console_log_string)
        elif(level == logging.WARNING):
            make_console_log_string = f"[console_output][WARNING][{str(datetime.now())}] : {message}"
            print(make_console_log_string) 
        elif(level == logging.ERROR):
            make_console_log_string = f"[console_output][ERROR][{str(datetime.now())}] : {message}"
            print(make_console_log_string)    
        elif(level == logging.CRITICAL):
            make_console_log_string = f"[console_output][CRITICAL][{str(datetime.now())}] : {message}"
            print(make_console_log_string)  
        elif(level == logging.NOTSET):
            make_console_log_string = f"[console_output][NOTSET][{str(datetime.now())}] : {message}"
            print(make_console_log_string)
        else:
            make_console_log_string = f"[console_output][UNDEFINED][{str(datetime.now())}] : {message}"
            print(make_console_log_string)
        return make_console_log_string