# class imports
from console_manager.console_manager import console_manager
from user_interface.user_interface import user_interface


# module imports
import logging
import configparser

def driver():
    console_manager.make_console_log("Lauching system...", logging.INFO)
    config = configparser.ConfigParser()
    config.read("./config.ini")
    my_user_interface = user_interface(config=config)

    
    

if (__name__ == "__main__"):
    driver()