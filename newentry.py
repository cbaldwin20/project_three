import datetime
import re
import os


def clear_screen():
    """clears the screen """
    os.system('cls' if os.name == 'nt' else 'clear')


class NewEntry:
    """creates a new entry """
    def make_new(self, dict_list):
        """walks through the process of creating a new entry"""
        self.dict_list = dict_list
        while True:
            clear_screen()
            self.task_name = input("What is the task name?: ").strip()
            print("")
            if self.task_name:
                break
            else:
                print("You did not enter a task name.")
                print("")
        while True:
            self.time_spent = input("How much time was spent on the task?"
                                    " (In minutes. Ex: 72): ").strip()
            print("")
            if re.search(r'\d+', self.time_spent):
                break
            else:
                print("{} is not an option.".format(self.time_spent))
                print("")
        while True:
            self.notes = input("What are your notes for this task?: ").strip()
            print("")
            if self.notes:
                break 
            else:
                print("You did not enter any notes.")
                print("")
        self.date = datetime.datetime.now().strftime('%m/%d/%Y %H:%M')  
        self.task_number = self.new_task_number()
        self.the_dict = {"task_name": self.task_name, 
                        "time_spent": self.time_spent, 
                        "notes": self.notes, "date": self.date, 
                        "task_number": self.task_number}
        self.dict_list.append(self.the_dict)
        self.print_result()
        return self.dict_list 

    def print_result(self):
        """prints the result of creating a new entry"""
        print("")
        print("")
        print("Date: {}".format(self.date))
        print("     Task name: {}".format(self.task_name))
        print("     Time spent: {}".format(self.time_spent))
        print("     Notes: {}".format(self.notes))
        print("     Task number: {}".format(self.task_number))
        print("")
        print("")

    def new_task_number(self):
        """finds the largest task number in our list, and +1 to it for a new 
        task number"""
        self.most = 0
        for i in self.dict_list:
            if int(i["task_number"]) > self.most:
                self.most = int(i["task_number"]) 
        self.most += 1
        return str(self.most) 
            