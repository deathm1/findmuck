# class imports
from turtle import width
from console_manager.console_manager import console_manager

# module imports
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import time
import requests
import logging


class report():

    my_window = None
    root = None
    is_window_open = False

    my_name = None
    my_email = None
    my_options = None
    my_description = None

    my_pb = None
    my_text = None
    my_submit_btn = None
    my_exit_btn = None
    is_request_in_process = False

    @classmethod
    def __init__(self, config, root):
        self.config = config
        self.root = root
        self.my_name = StringVar()
        self.my_email = StringVar()
        self.my_options = StringVar()

    @classmethod
    def get_new_window(self):
        if (self.is_window_open == False):
            self.is_window_open = True
            report_window = Toplevel(self.root)
            report_window.title("Report")
            report_window.resizable(False, False)
            # report_window.geometry(self.config.get("APP","FEEDBACK_FRAME"))

            title = Label(
                report_window, text="Please report any issues or bugs you encounter.")
            loading_text = Label(
                report_window, text="Please wait...")

            L1 = Label(report_window, text="Name")
            E1 = Entry(report_window, textvariable=self.my_name, width=40)

            L2 = Label(report_window, text="Email")
            E2 = Entry(report_window, textvariable=self.my_email, width=40)

            OPTIONS = [
                "Bugs",
                "Improvements",
                "Code of Conduct"
            ]
            self.my_options.set("0")

            R1 = OptionMenu(
                report_window,
                self.my_options,
                "Select Report Type",
                * OPTIONS
            )
            LR1 = Label(report_window, text="Report Type")

            L3 = Label(report_window, text="Description")
            T1 = Text(report_window, width=30, height=10)

            pb = Progressbar(
                report_window,
                orient='horizontal',
                mode='indeterminate',
            )

            submit_button = Button(
                report_window, text="Submit", command=self.submit_button)
            exit_button = Button(report_window, text="Exit",
                                 command=lambda: self.on_x_pressed(report_window))

            title.grid(row=0, column=1, pady=10, padx=10)

            L1.grid(row=1, column=0, padx=10, sticky="ew")
            E1.grid(row=1, column=1, padx=10, sticky="ew")

            L2.grid(row=2, column=0, padx=10, sticky="ew")
            E2.grid(row=2, column=1, padx=10, sticky="ew")

            R1.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
            LR1.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

            L3.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
            T1.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

            self.my_description = T1

            submit_button.grid(row=5, column=1, pady=10)
            exit_button.grid(row=5, column=0, pady=10)

            #pb.grid(column=1, row=5, padx=10, pady=20)
            #loading_text.grid(column=0, row=5, padx=10, pady=20)

            self.my_pb = pb
            self.my_text = loading_text
            self.my_exit_btn = exit_button
            self.my_submit_btn = submit_button

            report_window.protocol(
                'WM_DELETE_WINDOW', lambda: self.on_x_pressed(report_window))

            return report_window

    @classmethod
    def on_x_pressed(self, my_window):
        if (self.is_request_in_process == False):
            self.is_window_open = False
            my_window.destroy()

    @classmethod
    def radio_selection(self):
        print(self.my_options.get())

    @classmethod
    def submit_button(self):
        name = self.my_name.get()
        email = self.my_email.get()
        description = self.my_description.get("1.0", "end-1c")
        report_type = self.my_options.get()

        if (name == "" or email == "" or description == "" or report_type == "0"):
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
                "userReportType": report_type,
                "userDescription": description
            }
            print(data_dictionary)

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
