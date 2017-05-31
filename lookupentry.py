import re
import datetime
import os


def clear_screen():
    """clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


class LookupEntry:
    """Gives option to lookup entry to edit or delete it"""
    def lookup_begin(self, dict_list):
        """asks which option to look up an entry"""
        self.dict_list = dict_list 
        while True:
            print("")
            print("Enter 1 to find by date.")
            print("Enter 2 to find by time spent.")
            print("Enter 3 to find by exact match.")
            print("Enter 4 to find by pattern.")
            print("Enter 5 if you know the task number and want to delete/edit.")
            print("Enter 6 if you want to quit to the main screen.")
            self.which_option = input(": ").strip().upper()

            if self.which_option in ["1", "ONE", "DATE", "D"]:
                self.find_by_date()
                return self.dict_list
            elif self.which_option in ["2", "TWO", "TIME", "TIME SPENT"]:
                self.find_by_time_spent()
                return self.dict_list
            elif self.which_option in ["3", "THREE", "EXACT", "EXACT MATCH", 
                                        "MATCH", "E"]:
                self.find_by_exact_match()
                return self.dict_list
            elif self.which_option in ["4", "FOUR", "PATTERN", "P"]:
                self.find_by_pattern()
                return self.dict_list
            elif self.which_option in ["5", "FIVE"]:
                self.del_or_edit()
                return self.dict_list
            elif self.which_option in ["6", "SIX"]:
                x = self.dict_list
                return self.dict_list
            else:
                print("{} was not an option.".format(self.which_option))
                print("")

    def find_by_date(self):
        """can find an entry with a single date, or range of dates"""
        clear_screen()
        while True:
            self.date = input("Which date would you like to look at, ex: MM/DD/"
                "YYYY? Or you can find all dates including and between two "
                "dates, ex: MM/DD/YYYY - MM/DD/YYYY. Or Q to quit to the main "
                "screen.: ")
            if self.date.strip().upper() in ["Q", "QUIT", "EXIT"]:
                break
                #if the user put a range of dates it will go into this option.
            elif re.search(r'[0-1][0-9]/[0-3][0-9]/[1-2][0-9]{3}\s?[-]\s?[0-1]'
                            '[0-9]/[0-3][0-9]/[1-2][0-9]{3}',self.date):
                self.date_one = re.search(r'([0-1][0-9]/[0-3][0-9]/[1-2]'
                                           '[0-9]{3})\s?[-]\s?',self.date)
                self.date_two = re.search(r'\s?[-]\s?([0-1][0-9]/[0-3][0-9]/'
                                           '[1-2][0-9]{3})', self.date)
                clear_screen() 
                self.dates_to_print = "Results for dates including and between "
                "{} - {}.".format(self.date_one.group(1), self.date_two.group(1))
                self.date_one = datetime.datetime.strptime(self.date_one.group(1),
                                                                     '%m/%d/%Y')
                self.date_two = datetime.datetime.strptime(self.date_two.group(1),
                                                                     '%m/%d/%Y')
                self.find_by_date_list = []
                a = 0
                #finds the dates that are in between the two entered dates.
                for i in self.dict_list:
                    self.this_date = datetime.datetime.strptime(i["date"], 
                                                            '%m/%d/%Y %H:%M')
                    if self.date_one <= self.this_date <= self.date_two:
                        self.find_by_date_list.append(i) 
                        a += 1
                if a == 0:
                    print("{} was not listed.".format(self.date))
                    continue 
                else:
                    self.display_style(self.find_by_date_list, 
                                    dates=self.dates_to_print)
                    self.del_or_edit()
                    break
            #if user entered a single date, this option will be triggered
            elif re.search(r'[0-1][0-9]/[0-3][0-9]/[1-2][0-9]{3}',self.date):
                print("Results for the date {}.".format(self.date))
                self.find_by_date_list = []
                a = 0
                for i in self.dict_list:
                    if re.search(self.date, i["date"]):
                        self.find_by_date_list.append(i)
                        a += 1
                if a == 0:
                    print("{} was not listed.".format(self.date))
                    continue 
                else:
                    self.display_style(self.find_by_date_list)
                    self.del_or_edit()
                    break
            else:
                print("{} is not an acceptable date.".format(self.date))
                print("")
        
    def find_by_time_spent(self):
        """can find an entry by the time spent"""
        while True:
            self.time_spent = input("Roughly what length of time did the task "
                "you are looking for take in minutes? Ex: 25. Or Q to quit to "
                "the main screen.: ")
            if self.time_spent.upper() in ["Q", "EXIT", "QUIT"]:
                break 
            if re.search(r'\d+', self.time_spent):
                self.find_by_time_spent_list = []
                a = 0
                for i in self.dict_list:
                    try:
                        if (int(self.time_spent) - 10) <= int(i["time_"
                                "spent"]) <= (int(self.time_spent) +10): 
                            self.find_by_time_spent_list.append(i)
                            a+=1
                    except ValueError:
                        break 
                if a == 0:
                    print("")
                    print("{} was not listed.".format(self.time_spent))
                    continue 
                else:
                    self.display_style(self.find_by_time_spent_list)
                    self.del_or_edit()
                    break
            else:
                print("{} is not an acceptable time "
                    "response.".format(self.time_spent)) 
                 
        
    def find_by_exact_match(self):
        """can enter a search keyword to find an entry"""
        while True:    
            self.task_name_search = input("What is the keyword/s you are looking"
                " for? Press Q to quit to the main screen: ").strip()
            if self.task_name_search.upper() in ["Q", "QUIT", "EXIT"]:
                x = self.dict_list
                return x
            self.find_by_exact_match_list = []
            count = 0
            for i in self.dict_list:
                for key, value in i.items():
                    if re.search(self.task_name_search, value):
                        self.find_by_exact_match_list.append(i)
                        count+=1
                        break
            if count == 0:
                print("There were no matches.")
            else:
                self.display_style(self.find_by_exact_match_list)
                break
        self.del_or_edit()
               

    def find_by_pattern(self):
        """can enter a regular expression to find an entry"""
        while True:    
            word = input("Enter a regular expression ex: \d\d\w+. Press Q to "
                        "quit to the main screen: ")
            if word.upper() in ["Q", "QUIT", "EXIT"]:
                return self.dict_list
            self.find_by_pattern_list = []
            count = 0
            for i in self.dict_list:
                for key, value in i.items():
                    if re.search(word, value):
                        self.find_by_pattern_list.append(i)
                        count+=1
                        break
            if count == 0:
                print("There were no matches.")
            else:
                self.display_style(self.find_by_pattern_list)
                break
        self.del_or_edit()
        
    
    def del_or_edit(self):
        """gives the option to either delete or edit an entry"""
        while True:    
            print("")
            #asking the user explicitly for the task number of desired entry to 
            #edit or delete, then seeing if it exists in our list.
            self.current_task_num = input("Type in the task number of the entry"
                " if you want to edit or delete the entry. Or press Q to quit "
                "to main screen.: ")
            if self.current_task_num.upper() in ["Q", "QUIT"]:
                x = self.dict_list
                return x
            else:
                a = 0
                for i in self.dict_list:
                    if i["task_number"] == self.current_task_num:
                        self.task_name = i["task_name"]
                        self.time_spent = i["time_spent"]
                        self.notes = i["notes"]
                        self.date = i["date"]
                        self.task_number = i["task_number"]
                        a += 1
                if a == 0:
                    print("{} task number had no "
                        "matches.".format(self.current_task_num))
                else:
                    self.display_simple() 
                    self.is_correct = input("Is this the correct entry you were"
                        " looking for? Y for yes, N for no.: ").strip().upper()
                    if self.is_correct in ["NO", "N"]:
                        continue 
                    else:
                        break 
        while True:
            #User has enterd the task they want to edit/delete by this point,
            #and it has been confirmed the entry exists.
            print("")
            self.modify = input("Press E to edit entry, press D to delete entry,"
                                " or press Q to quit to main screen: ")
            print("")
            self.modify =self.modify.strip().upper()
            if self.modify in ["Q", "QUIT"]:
                break 
            elif self.modify not in ["D", "DELETE", "E", "EDIT"]:
                print("{} was not an option.".format(self.modify))
                continue  
            #user has chosen the delete option.
            elif self.modify in ["D", "DELETE"]:
                b = 0
                for i in self.dict_list:
                    if i["task_number"] == self.current_task_num:
                        a = self.dict_list.index(i)
                        del self.dict_list[a]
                        print("")
                        print("You have deleted the entry with the task number "
                            "{}.".format(self.current_task_num))
                        input("Press enter to continue.")
                        b += 1
                        return self.dict_list 
            #user has chosen the edit option
            elif self.modify in ["E", "EDIT"]:
                self.how_to_edit = input("Press 1 to edit the date, press 2 to "
                    "edit the task name, press 3 to edit the time spent, press "
                    "4 to edit the notes: ").strip().upper()
                #user has chosen to edit the date
                if self.how_to_edit in ["1", "ONE", "D", "DATE"]:
                    while True:   
                        print("The date currently reported is {}. What would you"
                            " like to change it to? (Must be in "
                            "MM/DD/YYYY HH:MM)".format(self.date))
                        self.changed_date = input(": ")
                        self.date = self.changed_date 
                        if re.search(r'[0-1][0-9]/[0-3][0-9]/[1-2][0-9][0-9]'
                            '[0-9]\s[0-2][0-9]:[0-5][0-9]',self.changed_date):
                            break 
                        else:
                            print("{} is not an acceptable "
                                  "input.".format(self.changed_date))
                    self.get_index("date", self.changed_date)
                    
                    for i in self.dict_list:
                        i["date"] = datetime.datetime.strptime(i["date"],
                                                             '%m/%d/%Y %H:%M')
                    #putting the dates in order
                    self.dict_list = sorted(self.dict_list, 
                                            key=lambda k: k['date'])
                    #now converting the datetimes back to strings
                    for i in self.dict_list:
                        i["date"] = i["date"].strftime('%m/%d/%Y %H:%M')
                    print("")
                    self.display_simple()
                    input("This is the final result. Press enter to continue.")
                    return self.dict_list
                #user has chosen to edit the task name
                elif self.how_to_edit in ["2", "TWO", "TASK NAME", "TASK"]:
                    print("The task name currently reported is {}. What would "
                          "you like to change it to?".format(self.task_name))
                    changed_task = input(": ")
                    self.task_name = changed_task
                    self.get_index("task_name", changed_task)
                    print("")
                    self.display_simple()
                    input("This is the final result. Press enter to continue.")
                    return self.dict_list
                #user has chosen to edit the time spent
                elif self.how_to_edit in ["3", "THREE", "TIME SPENT"]:
                    while True:
                        print("The time spent currently reported is {}. What "
                              "would you like to change it "
                              "to?".format(self.time_spent))
                        self.changed_time_spent = input(": ")
                        self.time_spent = self.changed_time_spent
                        try:
                            float(self.changed_time_spent)
                        except ValueError:
                            print("{} is not a "
                                "number.".format(self.changed_time_spent))
                        else:
                            break 
                    self.get_index("time_spent", self.changed_time_spent)
                    self.display_simple()
                    input("This is the final result. Press enter to continue.")
                    return self.dict_list
                #user has chosen to edit the notes
                elif self.how_to_edit in ["4", "FOUR", "N", "NOTES"]:
                    print("The note currently reported is {}. What would you "
                        "like to change it to?".format(self.notes))
                    changed_notes = input(": ")
                    self.notes = changed_notes
                    self.get_index("notes", changed_notes)
                    self.display_simple()
                    input("This is the final result. Press enter to continue.")
                    return self.dict_list
                #user did not give a valid option, and will go back over the
                #loop from the beginning
                else:
                    print("{} is not an acceptable "
                        "answer.".format(self.how_to_edit))
                    continue 
             
    def display_simple(self):
        """displays the outcome of an edited entry"""
        print("") 
        print("Date: {}".format(self.date))
        print("     Task name: {}".format(self.task_name))
        print("     Time spent: {} minutes".format(self.time_spent))
        print("     Notes: {}".format(self.notes))
        print("     Task number: {}".format(self.task_number))
        print("")

    def display_style(self, list, dates=None): 
        """takes in a list of matching entries, and displays them"""
        self.list = list
        self.num = 0
        while True:
            i = self.list[self.num]
            clear_screen()
            if dates:
                print(dates)
            print("")
            print("Display match {}/{}".format(self.num + 1, len(self.list)))
            print("") 
            print("Date: {}".format(i["date"]))
            print("     Task name: {}".format(i["task_name"]))
            print("     Time spent: {} minutes".format(i["time_spent"]))
            print("     Notes: {}".format(i["notes"]))
            print("     Task number: {}".format(i["task_number"]))
            print("")
            #works out the 'next, previous' portion to let the
            #user shuffle through matching entries one at a time.
            while True:
                if len(self.list) == 1:
                    print("")
                    input("Press any button to continue.: ").strip().upper()
                    return self.dict_list
                elif self.num + 1 == len(self.list):
                    print("")
                    self.what_choice = input("Press P for previous match, or Q"
                                            " to quit to the main screen or edit"
                                            " an entry.: ").strip().upper()
                    if self.what_choice in ["P", "PREVIOUS"]:
                        self.num -= 1
                        break 
                    elif self.what_choice in ["Q", "QUIT"]:
                        return self.dict_list
                    else:
                        print("{} was not an option.".format(self.what_choice))
                        continue 
                elif self.num == 0:
                    print("")
                    self.what_choice = input("Press N for next match, or Q to"
                                             " quit to the main screen or edit"
                                             " an entry.: ").strip().upper()
                    if self.what_choice in ["N", "NEXT"]:
                        self.num += 1
                        break 
                    elif self.what_choice in ["Q", "QUIT"]:
                        return self.dict_list
                    else:
                        print("{} was not an option.".format(self.what_choice))
                        continue 
                else:
                    print("")
                    self.what_choice = input("Press N for next match, P for"
                        " previous match, or Q to quit to the main screen or"
                        " edit an entry.: ").strip().upper()
                    if self.what_choice in ["N", "NEXT"]:
                        self.num += 1
                        break 
                    elif self.what_choice in ["P", "PREVIOUS"]:
                        self.num -= 1
                        break 
                    elif self.what_choice in ["Q", "QUIT"]:
                        return self.dict_list
                    else:
                        print("{} was not an option.".format(self.what_choice))
                        continue 
    #gets the task number and finds the correct dictionary, 
    #then changes whatever attributes value you passed through the argument.
    def get_index(self, attribute, value):
        """changes the value of a keyword in a dictionary in the list."""
        for i in self.dict_list:
            if i["task_number"] == self.current_task_num:
                a = self.dict_list.index(i)
                self.dict_list[a][attribute] = value 
         