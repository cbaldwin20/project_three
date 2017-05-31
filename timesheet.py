from newentry import NewEntry
from lookupentry import LookupEntry
import csv
import os
#turns my csv file into a list with dictionaries inside.
f = 'timesheet_csv.csv'
with open(f, 'r') as fin:
    if os.stat(f).st_size == 0:
        example_dict_list = []
    else:
        reader = csv.reader(fin, delimiter = '\t')
        headers = next(reader)
        dict_list = []
        for line in reader:
            dict_list.append(dict(zip(headers, line)))
        example_dict_list = [i for i in dict_list if i]


def clear_screen():
    """clears the screen """
    os.system('cls' if os.name == 'nt' else 'clear')


class Start:
    """Starts off the program, giving options, then finishes the program
    by writing the results to the csv file"""
    def return_dict(self, dict_list=None):
        """opening menu to add, edit, or quit"""
        self.dict_list = dict_list 
        while True:
            clear_screen()
            self.choice = input("Press 1 to add a new entry.\n"
                            "Press 2 to lookup and/or edit previous entries.\n"
                            "Press 3 to quit.\n"
                            ": ").upper()
            self.choice = self.choice.strip()
            if self.choice.upper() in ["1", "ONE", "NEW ENTRY", "NEW"]:
                self.dict_list = NewEntry().make_new(self.dict_list)
                return self.dict_list
            elif self.choice.upper() in ["2", "TWO", "LOOKUP", "EDIT"]:
                self.dict_list = LookupEntry().lookup_begin(self.dict_list)
            elif self.choice == "3":
                print("")
                print("Goodbye.")
                if self.dict_list:
                    self.write_to_csv()
                else:
                    with open('timesheet_csv.csv', 'w') as f:
                        f.write("")    
                exit()
            else:
                print("")
                print("{} is not an option.".format(self.choice))
                print("")
            
    def run(self, example_dict_list):
        """After completing a task, asks if wants to do more,
        if no, then writes to the csv file the results """
        self.example_dict_list = example_dict_list
        while True:
            self.example_dict_list = self.return_dict(self.example_dict_list)
            if_continue = input("Do you want to do some more? Enter N for no,"
                                " or Y for yes: ").upper()
            if_continue = if_continue.strip()
            if if_continue.upper() in ["N", "NO", "QUIT", "Q", "EXIT"]:
                print("Goodbye.")
                #if theres nothing in the list, then it will write nothing.
                if self.dict_list:
                    self.write_to_csv() 
                else:
                    with open('timesheet_csv.csv', 'w') as f:
                        f.write("") 
                break 

    def write_to_csv(self):
        """writes to the csv file """
        with open('timesheet_csv.csv', 'w') as csvfile:
            fieldnames = ['task_name', 'time_spent'] 
            fieldnames.extend(['notes', 'date', 'task_number'])
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, 
                    delimiter='\t')
            writer.writeheader()
            for d in self.dict_list:
                writer.writerow(d)


Start().run(example_dict_list)

