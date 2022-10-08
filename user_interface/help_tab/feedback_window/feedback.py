# class imports
from console_manager.console_manager import console_manager

# module imports
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import time
from datetime import datetime
import json
import requests
import logging


class feedback():

    my_window = None
    root = None
    is_window_open = False

    my_name = None
    my_email = None
    my_description = None
    my_pb = None
    my_text = None
    my_submit_btn = None
    my_exit_btn = None
    is_request_in_process = False

    base_url = False

    @classmethod
    def __init__(self, config, root):
        self.config = config
        self.root = root
        self.my_name = StringVar()
        self.my_email = StringVar()
        self.base_url = self.config.get("APP", "BASE_URL")

    @classmethod
    def get_new_window(self):
        if (self.is_window_open == False):
            self.is_window_open = True
            feedback_window = Toplevel(self.root)
            feedback_window.title("Feedback")
            feedback_window.resizable(False, False)
            # feedback_window.geometry(self.config.get("APP","FEEDBACK_FRAME"))

            title = Label(
                feedback_window, text="Please let us know how you feel about this app.")
            loading_text = Label(
                feedback_window, text="Please wait...")

            L1 = Label(feedback_window, text="Name")
            E1 = Entry(feedback_window, textvariable=self.my_name, width=40)

            L2 = Label(feedback_window, text="Email")
            E2 = Entry(feedback_window, textvariable=self.my_email, width=40)

            L3 = Label(feedback_window, text="Description")
            T1 = Text(feedback_window, width=30, height=10)

            pb = Progressbar(
                feedback_window,
                orient='horizontal',
                mode='indeterminate',
            )

            submit_button = Button(
                feedback_window, text="Submit", command=self.submit_button)
            exit_button = Button(feedback_window, text="Exit",
                                 command=lambda: self.on_x_pressed(feedback_window))

            title.grid(row=0, column=1, pady=10, padx=10)

            L1.grid(row=1, column=0, padx=10, sticky="ew")
            E1.grid(row=1, column=1, padx=10, sticky="ew")

            L2.grid(row=2, column=0, padx=10, sticky="ew")
            E2.grid(row=2, column=1, padx=10, sticky="ew")

            L3.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
            T1.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

            self.my_description = T1

            submit_button.grid(row=4, column=1, pady=10)
            exit_button.grid(row=4, column=0, pady=10)

            #pb.grid(column=1, row=5, padx=10, pady=20)
            #loading_text.grid(column=0, row=5, padx=10, pady=20)

            self.my_pb = pb
            self.my_text = loading_text
            self.my_exit_btn = exit_button
            self.my_submit_btn = submit_button

            feedback_window.protocol(
                'WM_DELETE_WINDOW', lambda: self.on_x_pressed(feedback_window))

            return feedback_window

    @classmethod
    def on_x_pressed(self, my_window):
        if (self.is_request_in_process == False):
            self.is_window_open = False
            my_window.destroy()

    @classmethod
    def submit_button(self):
        name = self.my_name.get()
        email = self.my_email.get()
        description = self.my_description.get("1.0", "end-1c")
        if (name == "" or email == "" or description == ""):
            console_manager.make_console_log(
                "[user_interface][feedback] Error : Fields were left blank.", logging.ERROR)
            self.show_dialog(
                "ERROR", "Please fill all the details.", logging.ERROR)
        else:
            self.is_request_in_process = True
            self.my_pb.grid(column=1, row=6, padx=2, pady=10, sticky="ew")
            self.my_pb.start()
            self.my_text.grid(column=0, row=6, padx=2, pady=10, sticky="ew")

            data_dictionary = {
                "userFullName": name,
                "userEmail": email,
                "userDescription": description
            }
            my_feedback_route = self.config.get("ROUTES", "SEND_FEEDBACK")
            my_url = f"{self.base_url}{my_feedback_route}"

            try:

                response = requests.post(url=my_url, json=data_dictionary, headers={
                                        'Content-Type': 'application/json'})

                response_dict = json.loads(response.text)

                if (response_dict['success'] == True):
                    self.my_pb.grid_remove()
                    self.my_text.grid_remove()
                    self.show_dialog(
                        "Success", f"{response_dict['status']}\nServer Time : {datetime.fromtimestamp(response_dict['timestamp']/1000)}", logging.INFO)
                else:
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
                    self.my_pb.grid_remove()
                    self.my_text.grid_remove()
                    self.show_dialog(
                        f"ERROR", f"{response_dict['status']}\n\n{errors_string}\nServer Time : {datetime.fromtimestamp(response_dict['timestamp']/1000)}", logging.ERROR)

            except Exception as e:
                self.my_pb.grid_remove()
                self.my_text.grid_remove()
                self.show_dialog(
                        f"ERROR", f"Something went wrong.\nERROR : {e}", logging.ERROR)

        self.is_request_in_process = False

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
