# class imports
import traceback
from turtle import width
from console_manager.console_manager import console_manager
from user_interface.help_tab.feedback_window.feedback import feedback
from user_interface.help_tab.report_window.report import report
from logging_manager.logging_manager import logging_manager

# module imports
from tkinter import messagebox
import traceback
from tkinter import *
import time
import logging
import json
import sys
from datetime import datetime
import platform
import os
import requests
import subprocess

from tkinter.filedialog import askopenfile, asksaveasfile
from PIL import ImageTk, Image


class user_interface():

    config = None
    my_feedback_window = None
    my_report_window = None
    is_feedback_open = False

    victim_name_cc = None
    victim_name = None
    dealy = None
    amount = None

    base_url = False

    root = None

    @classmethod
    def __init__(self, config) -> None:
        try:
            logging_manager(
                "Launching App...", logging.INFO, None, None)
            self.config = config
            root = Tk()
            root.configure(menu=self.build_menu(root=root))
            self.victim_name = StringVar()
            self.victim_name_cc = StringVar()
            self.dealy = StringVar()
            self.amount = StringVar()
            self.base_url = self.config.get("APP", "BASE_URL")

            logging_manager(
                "Launching Windows", logging.INFO, None, None)

            # feedback window
            self.my_feedback_window = feedback(self.config, root)
            self.my_report_window = report(self.config, root)

            logging_manager(
                "Windows Launched Successfully", logging.INFO, None, None)

            logging_manager(
                "Loading Hompage UI elements...", logging.INFO, None, None)

            # launch User Interface elements
            img = ImageTk.PhotoImage(Image.open(
                "user_interface/assets/rizwan.jpg"))
            my_home_image = Label(root, image=img, width=150, height=150)
            my_home_label = Label(
                root, text="FindMuck\nSMS Bomber", font=("Helvetica 20 bold"))

            title_det = Label(
                root, text="Victim Details", font=("Arial", 15))

            victim_label = Label(
                root, text="Phone (India Only) 10 digit")
            victim_Entry_cc = Entry(
                root, textvariable=self.victim_name_cc, width=5)
            victim_Entry = Entry(root, textvariable=self.victim_name)

            dealy = Label(
                root, text="Delay(3-15s)")
            delay_Entry = Entry(root, textvariable=self.dealy)

            amount = Label(
                root, text="Amount (1-200)")
            amount_Entry = Entry(root, textvariable=self.amount)

            submit_button = Button(root, text="Attack",
                                   command=self.initiate_attack)
            exit_button = Button(root, text="Exit", command=self.exitProgram)

            submit_button.grid(row=6, column=1, padx=10, pady=10)

            exit_button.grid(row=6, column=0, padx=10, pady=10)

            amount_Entry.grid(row=5, column=1, padx=10,)

            amount.grid(row=5, column=0, sticky="ew", padx=10)

            delay_Entry.grid(

                row=4,
                column=1,
                padx=10,
            )

            dealy.grid(
                row=4,
                column=0,
                sticky="ew",
                padx=10
            )

            title_det.grid(

                row=2,
                column=1,
                sticky="ew",
                padx=10,
                pady=20
            )

            victim_label.grid(
                row=3,
                column=0,
                sticky="ew",
                padx=10,
                pady=10,
            )

            # victim_Entry_cc.grid(
            #     row=3,
            #     column=1,
            #     sticky="ew",
            #     pady=10,
            #     padx=10,
            # )
            victim_Entry.grid(
                row=3,
                column=1,
                sticky="ew",
                padx=10,
                pady=10
            )

            my_home_image.grid(
                row=0,
                column=0,
                padx=10,
                pady=20
            )
            my_home_label.grid(
                row=0,
                column=1,
                padx=10,
                pady=20
            )

            logging_manager(
                "UI elements loaded.", logging.INFO, None, None)

            root.wm_title(
                f'{self.config.get("APP","APP_NAME")} {self.config.get("APP","VERSION")}')
            # root.geometry(self.config.get("APP","ROOT_FRAME"))

            logging_manager(
                "App launched successfully.", logging.INFO, None, None)

            ico = Image.open('user_interface/assets/rizwan.jpg')
            photo = ImageTk.PhotoImage(ico)
            root.wm_iconphoto(False, photo)
            self.root = root
            root.mainloop()

        except Exception as e:
            logging_manager(
                "Something went wrong while loaunching the app", logging.ERROR, e, traceback)

    @classmethod
    def open_log_dir(self):
        folder_ = self.config.get("LOGGER_CONFIGURATION", "LOG_DIRECTORY")
        path = f"./{folder_}"
        system = sys.platform
        if platform.system() == "Windows":
            os.startfile(f".\{folder_}")
        elif system == 'darwin':
            subprocess.check_call(['open', '--', path])
        elif system == 'linux2':
            subprocess.check_call(['xdg-open', '--', path])
        elif system == 'linux':
            subprocess.check_call(['xdg-open', path])
        elif system == 'win32':
            subprocess.check_call(['explorer', path])

    @classmethod
    def initiate_attack(self):
        try:
            logging_manager(
                "Attacking victim...", logging.INFO, None, None)
            phone_number = self.victim_name.get()
            sms_delay = self.dealy.get()
            sms_amount = self.amount.get()

            if (phone_number == "" or sms_amount == "" or sms_amount == ""):
                console_manager.make_console_log(
                    "[user_interface][feedback] Error : Fields were left blank.", logging.ERROR)
                self.show_dialog(
                    "ERROR", "Please fill all the details.", logging.ERROR)
                logging_manager(
                    "Incomplete details.", logging.WARN, None, None)
            else:
                self.root.config(cursor="watch")
                data_dictionary = {
                    "countryCode": int(self.config.get("APP", "COUNTRY_CODE")),
                    "phoneNumber": phone_number,
                    "delay": sms_delay,
                    "amount": sms_amount
                }

                my_feedback_route = self.config.get("ROUTES", "ATTACK_VICTIM")
                my_url = f"{self.base_url}{my_feedback_route}"

            try:

                response = requests.post(url=my_url, json=data_dictionary, headers={
                    'Content-Type': 'application/json'})

                response_dict = json.loads(response.text)

                if (response_dict['success'] == True):
                    self.root.config(cursor="arrow")
                    self.show_dialog(
                        "Success", f"{response_dict['status']}\nServer Time : {datetime.fromtimestamp(response_dict['timestamp']/1000)}", logging.INFO)
                else:
                    self.root.config(cursor="arrow")
                    try:
                        ERROR_LIST = response_dict['errors']
                    except Exception:
                        ERROR_LIST = None
                    errors_string = ""
                    index = 1
                    if (ERROR_LIST is not None):
                        for error in ERROR_LIST:
                            errors_string = errors_string + \
                                f"{index}. {error['msg']}\n"
                            index += 1
                    self.show_dialog(
                        f"ERROR", f"{response_dict['status']}\n\n{errors_string}\nServer Time : {datetime.fromtimestamp(response_dict['timestamp']/1000)}", logging.ERROR)

            except Exception as e:
                # self.my_pb.grid_remove()
                # self.my_text.grid_remove()
                self.show_dialog(
                    f"ERROR", f"Something went wrong.\nERROR : {e}", logging.ERROR)

            self.root.config(cursor="arrow")
        except Exception as e:
            logging_manager(
                "Something went wrong while initiating attacking victim.", logging.ERROR, e, traceback)

    @classmethod
    def load_configuration(self):
        logging_manager("Loading Configuration...", logging.INFO, None, None)
        try:
            files = [('JSON (Java Script Object Notation)', '*.json')]
            file = askopenfile(filetypes=files, defaultextension=".json")
            json_config = json.load(file)
            c_phone_number = json_config['phone_number']
            c_sms_delay = json_config['sms_delay']
            c_sms_amount = json_config['sms_amount']
            self.victim_name.set(c_phone_number)
            self.dealy.set(c_sms_delay)
            self.amount.set(c_sms_amount)
            logging_manager("Configuration loaded.", logging.INFO, None, None)

        except Exception as e:
            logging_manager(
                "Something went wrong while loading configuration.", logging.ERROR, e, traceback)

    @classmethod
    def save_configuration(self):
        try:
            logging_manager("Saving Configuration...",
                            logging.INFO, None, None)

            phone_number = self.victim_name.get()
            sms_dealy = self.dealy.get()
            sms_amount = self.amount.get()

            if (phone_number == "" or sms_amount == "" or sms_amount == ""):
                console_manager.make_console_log(
                    "[user_interface][feedback] Error : Fields were left blank.", logging.ERROR)
                self.show_dialog(
                    "ERROR", "Please fill all the details.", logging.ERROR)
            else:
                my_dict = {
                    "phone_number": phone_number,
                    "sms_delay": sms_dealy,
                    "sms_amount": sms_amount
                }
                files = [('JSON (Java Script Object Notation)', '*.json')]
                file = asksaveasfile(mode='w', filetypes=files, initialfile=f"config_{time.time()}.json",
                                     defaultextension=".json")
                configuration = str(json.dumps(my_dict))
                file.write(configuration)
                file.close()
            logging_manager("Configuration Saved",
                            logging.INFO, None, None)
        except Exception as e:
            logging_manager(
                "Something went wrong while saving configuration.", logging.ERROR, e, traceback)

    @classmethod
    def build_menu(self, root):

        try:
            logging_manager("Building menu...",
                            logging.INFO, None, None)
            my_menu = Menu(root, tearoff=False)
            fileMenu = Menu(my_menu, tearoff=False)
            fileMenu.add_command(label="Save Configuration",
                                 command=self.save_configuration)
            fileMenu.add_command(label="Load Configuration",
                                 command=self.load_configuration)
            fileMenu.add_command(label="Logs", command=self.open_log_dir)
            fileMenu.add_command(label="Exit", command=self.exitProgram)
            my_menu.add_cascade(label="File", menu=fileMenu)
            help_menu = Menu(my_menu, tearoff=False)
            help_menu.add_command(
                label="Feedback", command=lambda: self.my_feedback_window.get_new_window())
            help_menu.add_command(
                label="Report", command=lambda: self.my_report_window.get_new_window())
            my_menu.add_cascade(label="Help", menu=help_menu)
            my_menu.add_command(label="About", command=lambda: self.show_dialog(
                "About", "Hi,\nThank you for using FindMuck, I hope you liked it. Please use the tool with discretion.\n\n-Aapka Shub Chintak", logging.INFO))
            logging_manager("Menu has been built.",
                            logging.INFO, None, None)
            return my_menu

        except Exception as e:
            logging_manager(
                "Something went wrong while building menu", logging.ERROR, e, traceback)

    @classmethod
    def show_dialog(self, title: str, message: str, type: int):
        """This function is responsible for showing dialog information

        Args:
            title (str): title of dialog box
            message (str): message shown by dialog box
            type (int): type of dialog box
        """
        if (type == logging.INFO):
            messagebox.showinfo(title, message)
        elif (type == logging.WARN):
            messagebox.showwarning(title, message)
        elif (type == logging.ERROR):
            messagebox.showerror(title, message)
        else:
            console_manager.make_console_log(
                "Error : Message was not specified.", logging.ERROR)

    @classmethod
    def exitProgram(self):
        exit()
