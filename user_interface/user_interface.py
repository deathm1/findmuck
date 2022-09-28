# class imports
from tkinter import ttk
from console_manager.console_manager import console_manager
from user_interface.help_tab.feedback_window.feedback import feedback

# module imports
from tkinter import messagebox
from tkinter import * 
import logging
import os



class user_interface():

    config = None
    my_feedback_window = None
    is_feedback_open = False

    @classmethod
    def __init__(self, config) -> None:
        self.config=config

        root = Tk()
        root.config(menu=self.build_menu(root=root))

        # feedback window
        self.my_feedback_window = feedback(self.config, root)
        

        # launch User Interface elements
        root.wm_title(f'{self.config.get("APP","APP_NAME")} {self.config.get("APP","VERSION")}')
        #root.geometry(self.config.get("APP","ROOT_FRAME"))


        root.mainloop()


    
    
    @classmethod
    def build_menu(self, root):
        my_menu = Menu(root, tearoff=False)
        fileMenu = Menu(my_menu,tearoff=False)
        fileMenu.add_command(label="Save Configuration")
        fileMenu.add_command(label="Load Configuration")
        fileMenu.add_command(label="Logs")
        fileMenu.add_command(label="Exit", command=self.exitProgram)

        my_menu.add_cascade(label="File", menu=fileMenu)

        # editMenu = Menu(my_menu,tearoff=False)
        # editMenu.add_command(label="Undo")
        # editMenu.add_command(label="Redo")

        # my_menu.add_cascade(label="Edit", menu=editMenu)

        # tools_menu = Menu(my_menu, tearoff=False)
        # tools_menu.add_command(label="Undo")
        # tools_menu.add_command(label="Redo")
        
        # my_menu.add_cascade(label="Tools", menu=tools_menu)

        help_menu = Menu(my_menu, tearoff=False)
        help_menu.add_command(label="Feedback", command=lambda:self.my_feedback_window.get_new_window())
        help_menu.add_command(label="Report")
        
        my_menu.add_cascade(label="Help", menu=help_menu)
        
        my_menu.add_command(label="About", command=lambda:self.show_dialog("About", "About message", logging.INFO))

        return my_menu

    


    @classmethod
    def show_dialog(self, title:str, message:str, type:int):
        """This function is responsible for showing dialog information

        Args:
            title (str): title of dialog box
            message (str): message shown by dialog box
            type (int): type of dialog box
        """
        if(type == logging.INFO):
            messagebox.showinfo(title, message)
        elif(type == logging.WARN):
            messagebox.showwarning(title, message)
        elif(type == logging.ERROR):
            messagebox.showerror(title, message)
        else:
            console_manager.make_console_log("Error : Message was not specified.", logging.ERROR)
    
    @classmethod
    def exitProgram(self):
        exit()
