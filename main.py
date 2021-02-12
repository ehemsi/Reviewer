import speech_recognition as sr
import csv
import os  # For opening and closing files

r = sr.Recognizer() 

# Global Variables
username = ""
user_path = ""
user_question_sets_path = ""
program_path = os.getcwd()
question_sets_path = program_path + "\\question_sets"
question_sets = os.listdir(question_sets_path)
question_sets.sort()

def get_input():
    return input("> ")

def user_login():
    while(True):
        print("\nEnter username:")
        global username
        username = get_input()
        if (os.path.isdir("users\\" + username)):
            print("Successfully loaded information.")
            global user_path 
            user_path = program_path + "\\users\\" + username
            global user_question_sets_path
            user_question_sets_path = user_path + "\\question_sets"
            return True
        else:
            print("Username not found. Would you like to try again?")
            print("1: YES")
            print("2: NO (Returns to previous options)")
            user_input = get_input()
            if(user_input == "1"):
                continue
            else:
                return False

def create_user():
    while(True):
        print("\nEnter username:")
        global username
        username = get_input()
        try:
            os.mkdir("users\\" + username)
            global user_path 
            user_path = program_path + "\\users\\" + username
            print("User successfully created.")
            return True
        except FileExistsError:
            print("Username already exists. Would you like to try again?")
            print("1: YES")
            print("2: NO (Returns to previous options)")
            user_input = get_input()
            if(user_input == "1"):
                continue
            else:
                return False
        except:
            print("Invalid username. Would you like to try again?")
            print("1: YES")
            print("2: NO (Returns to previous options)")
            user_input = get_input()
            if(user_input == "1"):
                continue
            else:
                return False
 
def menu_1():
    while(True):
        print("\nWelcome! What would you like to do?")
        print("1: Login")
        print("2: Create New Account")
        print ("0: Exit")
        user_input = get_input()
        if (user_input == "1"):
            if(user_login()):
                return True
            else:
                continue
        elif (user_input == "2"):
            if(create_user()):
                return True
            else:
                continue
        elif (user_input == "0"):
            print("Closing program.")
            return False
        else:
            print("Unknown command. Please enter again.")
            continue

def menu_2():
    while(True):
        print("\n" + username + "'s data loaded. What would you like to do?")
        print("1: Take quiz")
        print("2: Show data")
        print("0: Logout.")
        user_input = get_input()
        if(user_input == "1"):
            return 1
        elif(user_input == "2"):
            return 2
        elif(user_input == "0"):
            return 0
        else:
            print("Unknown command. Please enter again.")
            continue

def select_exam():
    while(True):
        print("\nWhat quiz would you like to take?")
        question_count = 1
        for question_set in question_sets:
            print(f"{question_count}: {question_set}")
            question_count+=1
        print(f"{question_count}: ***Questions with most mistakes")
        try:
            user_input = int(get_input())
        except:
            print("Not a number. Please try again.")
            continue
        if(user_input == question_count):
            return 0
        elif(user_input > 0 and user_input < question_count):
            return user_input
        else:
            print("Unknown command. Please try again.")
            continue

def find_equivalent_answer_in_database(user_answer, user_voice_recognition_data):
    for key in user_voice_recognition_data:
        if(user_answer == key[0]):
            return key[1]

def take_exam(question_set_no):
    with open(f"voice_recognition_data.csv", newline='') as voice_file:
        reader = csv.reader(voice_file)
        user_voice_recognition_data = list(reader)
    voice_file.close()
    with open(f"{question_sets_path}\\{question_sets[question_set_no]}", newline='') as question_set_file:
        reader = csv.reader(question_set_file)
        current_question_set_data = list(reader)
    question_set_file.close()
    current_question_set_user_correct_column = 0
    header_row = current_question_set_data[0]
    for count, header in enumerate(header_row):
        if(header == f"{username} Correct Count"):
            current_question_set_user_correct_column = count
    if (current_question_set_user_correct_column == 0):    # First time user answers this question set
        current_question_set_user_correct_column = len(header_row)
        header_row.append(f"{username} Correct Count")
        header_row.append(f"{username} Incorrect Count")
        for i in range(1, len(current_question_set_data)):
            current_question_set_data[i].append(0)      # Appending two zero columns to be able to access and add to them
            current_question_set_data[i].append(0)
    iteration_no = 1
    print(f"\n------  Iteration no. {iteration_no}  ------")
    current_correct_no = 0
    incorrect_question_rows = []
    current_question_no = 1
    while(current_question_no < len(current_question_set_data)):
        print(f"\nQuestion number {current_question_no} of {len(current_question_set_data) - 1}:")     # -1 is to remove header
        print(current_question_set_data[current_question_no][0])
        print("Choices:")
        print("A." + current_question_set_data[current_question_no][1])
        print("B." + current_question_set_data[current_question_no][2])
        print("C." + current_question_set_data[current_question_no][3])
        print("D." + current_question_set_data[current_question_no][4])
        user_answer = input("Answer: ").upper()
        user_equivalent_answer = find_equivalent_answer_in_database(user_answer, user_voice_recognition_data)
        correct_answer = current_question_set_data[current_question_no][5]
        if(user_equivalent_answer == correct_answer):
            print("CORRECT!")
            current_question_set_data[current_question_no][current_question_set_user_correct_column] = int(current_question_set_data[current_question_no][current_question_set_user_correct_column]) + 1
            current_correct_no += 1
        elif(user_equivalent_answer):   # Answer is wrong but exists in database
            print(f"INCORRECT. Correct answer is {correct_answer}. ", end = "")
            if(correct_answer == "A"):
                print(current_question_set_data[current_question_no][1])
            elif(correct_answer == "B"):
                print(current_question_set_data[current_question_no][2])
            elif(correct_answer == "C"):
                print(current_question_set_data[current_question_no][3])
            else:
                print(current_question_set_data[current_question_no][4])
            current_question_set_data[current_question_no][current_question_set_user_correct_column + 1] = int(current_question_set_data[current_question_no][current_question_set_user_correct_column + 1]) + 1
            incorrect_question_rows.append(current_question_no)
        else:   # User answer is not found in database
            while(True):
                print(f"Unknown answer. You have entered: {user_answer}")
                print("Please enter a valid answer:")
                user_input = get_input().upper()
                user_equivalent_answer = find_equivalent_answer_in_database(user_input, user_voice_recognition_data)
                if(user_equivalent_answer):     # New input found in database
                    if(user_equivalent_answer == correct_answer):
                        print("CORRECT!")
                        current_question_set_data[current_question_no][current_question_set_user_correct_column] = int(current_question_set_data[current_question_no][current_question_set_user_correct_column]) + 1
                        current_correct_no += 1
                    elif(user_equivalent_answer): 
                        print(f"INCORRECT. Correct answer is {correct_answer}. ", end = "")
                        if(correct_answer == "A"):
                            print(current_question_set_data[current_question_no][1])
                        elif(correct_answer == "B"):
                            print(current_question_set_data[current_question_no][2])
                        elif(correct_answer == "C"):
                            print(current_question_set_data[current_question_no][3])
                        else:
                            print(current_question_set_data[current_question_no][4])
                        current_question_set_data[current_question_no][current_question_set_user_correct_column + 1] = int(current_question_set_data[current_question_no][current_question_set_user_correct_column + 1]) + 1
                        incorrect_question_rows.append(current_question_no)
                    print(f"Would you like to save {user_answer} as {user_equivalent_answer}? [Y/N]")
                    user_input = get_input().upper()
                    if(user_input == "Y" or "YES"):
                        user_voice_recognition_data.append([user_answer, "A"])
                    break
                else:   # New input not found in database
                    print("Answer not found in database. Please try again.")
        current_question_no += 1
    print(f"You got {current_correct_no} out of {len(current_question_set_data) - 1}")

    # Continue iterating until the user can answer everything correctly
    while(incorrect_question_rows):
        iteration_no += 1
        print(f"\n------  Iteration no. {iteration_no}  ------")
        new_incorrect_question_rows = []
        current_correct_no = 0
        incorrect_question_no = 0
        while(incorrect_question_no < len(incorrect_question_rows)):
            print(f"\nQuestion number {incorrect_question_no + 1} of {len(incorrect_question_rows)}:")
            print(current_question_set_data[incorrect_question_rows[incorrect_question_no]][0])
            print("Choices:")
            print("A." + current_question_set_data[incorrect_question_rows[incorrect_question_no]][1])
            print("B." + current_question_set_data[incorrect_question_rows[incorrect_question_no]][2])
            print("C." + current_question_set_data[incorrect_question_rows[incorrect_question_no]][3])
            print("D." + current_question_set_data[incorrect_question_rows[incorrect_question_no]][4])
            user_answer = input("Answer: ").upper()
            user_equivalent_answer = find_equivalent_answer_in_database(user_answer, user_voice_recognition_data)
            correct_answer = current_question_set_data[incorrect_question_rows[incorrect_question_no]][5]
            if(user_equivalent_answer == correct_answer):
                print("CORRECT!")
                current_question_set_data[incorrect_question_rows[incorrect_question_no]][current_question_set_user_correct_column] = int(current_question_set_data[incorrect_question_rows[incorrect_question_no]][current_question_set_user_correct_column]) + 1
                current_correct_no += 1
            elif(user_equivalent_answer):   # Answer is wrong but exists in database
                print(f"INCORRECT. Correct answer is {correct_answer}. ", end = "")
                if(correct_answer == "A"):
                    print(current_question_set_data[incorrect_question_rows[incorrect_question_no]][1])
                elif(correct_answer == "B"):
                    print(current_question_set_data[incorrect_question_rows[incorrect_question_no]][2])
                elif(correct_answer == "C"):
                    print(current_question_set_data[incorrect_question_rows[incorrect_question_no]][3])
                else:
                    print(current_question_set_data[incorrect_question_rows[incorrect_question_no]][4])
                current_question_set_data[incorrect_question_rows[incorrect_question_no]][current_question_set_user_correct_column + 1] = int(current_question_set_data[incorrect_question_rows[incorrect_question_no]][current_question_set_user_correct_column + 1]) + 1
                new_incorrect_question_rows.append(incorrect_question_rows[incorrect_question_no])
            else:   # User answer is not found in database
                while(True):
                    print(f"Unknown answer. You have entered: {user_answer}")
                    print("Please enter a valid answer:")
                    user_input = get_input().upper()
                    user_equivalent_answer = find_equivalent_answer_in_database(user_input, user_voice_recognition_data)
                    if(user_equivalent_answer):     # New input found in database
                        if(user_equivalent_answer == correct_answer):
                            print("CORRECT!")
                            current_question_set_data[incorrect_question_rows[incorrect_question_no]][current_question_set_user_correct_column] = int(current_question_set_data[incorrect_question_rows[incorrect_question_no]][current_question_set_user_correct_column]) + 1
                            current_correct_no += 1
                        elif(user_equivalent_answer): 
                            print(f"INCORRECT. Correct answer is {correct_answer}. ", end = "")
                            if(correct_answer == "A"):
                                print(current_question_set_data[incorrect_question_rows[incorrect_question_no]][1])
                            elif(correct_answer == "B"):
                                print(current_question_set_data[incorrect_question_rows[incorrect_question_no]][2])
                            elif(correct_answer == "C"):
                                print(current_question_set_data[incorrect_question_rows[incorrect_question_no]][3])
                            else:
                                print(current_question_set_data[incorrect_question_rows[incorrect_question_no]][4])
                            current_question_set_data[incorrect_question_rows[incorrect_question_no]][current_question_set_user_correct_column + 1] = int(current_question_set_data[current_question_no][current_question_set_user_correct_column + 1]) + 1
                            new_incorrect_question_rows.append(incorrect_question_rows[incorrect_question_no])
                        print(f"Would you like to save {user_answer} as {user_equivalent_answer}? [Y/N]")
                        user_input = get_input().upper()
                        if(user_input == "Y" or "YES"):
                            user_voice_recognition_data.append([user_answer, "A"])
                        break
                    else:   # New input not found in database
                        print("Answer not found in database. Please try again.")
            incorrect_question_no += 1
        print(f"You got {current_correct_no} of {len(incorrect_question_rows)}")
        incorrect_question_rows = new_incorrect_question_rows
    
    # Save session data to disk
    with open('voice_recognition_data.csv', 'w', newline= "") as voice_file:
        writer = csv.writer(voice_file)
        writer.writerows(user_voice_recognition_data)
    voice_file.close()
    with open(f"{question_sets_path}\\{question_sets[question_set_no]}", 'w', newline= "") as question_set_file:
        writer = csv.writer(question_set_file)
        writer.writerows(current_question_set_data)
    question_set_file.close()

def menu_21():
    while(True):
        print("What would you like to do next?")
        print("1: Retake exam.")
        print("2: Take next exam in list.")
        print("0: Go back to previous options.")
        user_input = get_input()
        if(user_input == "1"):
            return 1
        elif(user_input == "2"):
            return 2
        elif(user_input == "0"):
            return 0
        else:
            print("Unknown command. Please try again.")
            continue

def menu_22():
    user_data = []
    # user_data.append("Correct", "Wrong", "%Correct","Question", "Question Set", "Answer")
    print("What data would you like to get?")
    print("1: Lifetime %Correct.")
    print("2: Top X question sets with the least %Correct.")
    print("3: Top x questions with the least %Correct.")
    print("0: Return to previous menu.")
    user_input = get_input()
    question_set_no = 0
    while(question_set_no < len(question_sets)):
        with open(f"{question_sets_path}\\{question_sets[question_set_no]}", newline='') as question_set_file:
            reader = csv.reader(question_set_file)
            current_question_set_data = list(reader)
        question_set_file.close()
        current_question_set_user_correct_column = 0
        header_row = current_question_set_data[0]
        for count, header in enumerate(header_row):
            if(header == f"{username} Correct Count"):
                current_question_set_user_correct_column = count
        if (current_question_set_user_correct_column == 0):    # Skip since the user never answered it
            question_set_no += 1
            continue     # Skip
        else:
            current_question_no = 1
            while(current_question_no < len(current_question_set_data)):
                correct_answer = current_question_set_data[current_question_no][5]
                if(correct_answer == "A"):
                    correct_answer_text = current_question_set_data[current_question_no][1]
                elif(correct_answer == "B"):
                    correct_answer_text = current_question_set_data[current_question_no][2]
                elif(correct_answer == "C"):
                    correct_answer_text = current_question_set_data[current_question_no][3]
                else:
                    correct_answer_text = current_question_set_data[current_question_no][4]
                # user_data Header : ["Correct", "Wrong", "%Correct","Question", "Question Set", "Answer"]
                try:
                    user_data.append([
                                    int(current_question_set_data[current_question_no][current_question_set_user_correct_column]), 
                                    int(current_question_set_data[current_question_no][current_question_set_user_correct_column + 1]),
                                    (int(current_question_set_data[current_question_no][current_question_set_user_correct_column]) / int(current_question_set_data[current_question_no][current_question_set_user_correct_column + 1])) * 100,
                                    current_question_set_data[current_question_no][0],
                                    question_sets[question_set_no],
                                    correct_answer_text
                                    ])
                except ZeroDivisionError:
                    user_data.append([
                                    int(current_question_set_data[current_question_no][current_question_set_user_correct_column]), 
                                    int(current_question_set_data[current_question_no][current_question_set_user_correct_column + 1]),
                                    100,
                                    current_question_set_data[current_question_no][0],
                                    question_sets[question_set_no],
                                    correct_answer_text
                                    ])
                current_question_no += 1
        question_set_no += 1
        
    if(user_input == "1"):
        total_correct_no = 0
        total_wrong_no = 0
        for question in user_data:
            total_correct_no += question[0]
            total_wrong_no += question[1]
        total_correct_percentage = total_correct_no / (total_wrong_no + total_correct_no)
        print(f"Total %Correct = {total_correct_percentage}")

    if(user_input == "2"):
        question_set_correct_percentage = []     # [[Correct],[Wrong],[Percentage],[Question Set]]
        first_time_check = 0
        for question_row in user_data:
            if(first_time_check == 0):
                question_set_correct_percentage.append([0,0,0,question_row[4]])
                first_time_check = 1
            print("Im here two")
            for question_row_percentage in question_set_correct_percentage:
                print("Im here one")
                if(question_row[4] in question_row_percentage):
                    question_row_percentage[0] += question_row[0]
                    question_row_percentage[1] += question_row[1]
                    print("Im here three")
                else:
                    question_set_correct_percentage.append([0,0,0,question_row[4]])
                    print("Im here")
        print("[Percentage] [Question Set]")
        for question_row_percentage in question_set_correct_percentage:
            try:
                question_row_percentage[2] = (question_row_percentage[0] / (question_row_percentage[0] + question_row_percentage[1])) * 100
            except ZeroDivisionError:
                question_row_percentage[2] = 100
        print(question_set_correct_percentage)
        user_input = get_input()
        question_set_correct_percentage.sort(key = lambda x:x[3])
        for question_row_percentage in question_set_correct_percentage:
            print(f"{question_row_percentage[2]}  {question_row_percentage[3]}")

         



####### MAIN PROGRAM ########
while(True):
    if(menu_1()):
        while(True):
            user_input = menu_2()
            if(user_input == 1):
                selected_exam = select_exam()
                print(f"Question chosen: {question_sets[selected_exam - 1]}")
                take_exam(selected_exam - 1)
                while(True):
                    user_input = menu_21()
                    if(user_input == 1):
                        take_exam(selected_exam - 1)
                    elif(user_input == 2):
                        selected_exam += 1
                        if(selected_exam >= len(question_sets)):
                            print("No more exams. Returning to past menu.")
                            break
                        take_exam(selected_exam - 1)
                    else:
                        break
            elif(user_input == 2):
                print("Show data")
                menu_22()
            else:
                print("\nLogging out.")
                break
    else:
        print("End of program.")
        break



    


    

