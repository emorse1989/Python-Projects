#importing chdir for try block and setting directory, and sleep for less spammy output
from os import chdir
from time import sleep

#list of unusable filename characters to prevent user from using them in filename
illegal_characters = ['\\', "/", '?', '%', '*', ':', '|', '"', '<', '>', '.', ',', ';', '=']

def try_chdir(target_dir):
    '''uses try to make sure directory name is valid'''
    try:
        chdir(target_dir)
    except FileNotFoundError:
        print("That directory does not exist. Please try again.")
        main()
    except OSError:
        print("Invalid syntax. Please try again.")
        main()

def confirm_dir(target_dir):
    '''checks if directory input is correct'''
    confirm = input(f'You have selected the following directory: {target_dir}. Is this correct? (y/n): ')
    return confirm

def select_dir():
    '''gets directory path from user'''
    target_dir = input("Please enter the path of the directory you wish to write to: ")
    return target_dir

def get_user_data():
    '''gets user info to be written to file'''
    retry = 'y'
    while retry == 'y':
        file_name = input("Please enter the name you wish to give to your file (a .txt file type will be adde automatically): ")
        for item in illegal_characters:
            if item in file_name:
                print("You have included an illegal character in your filename.")
                retry = 'y'
                break
            else:
                retry = 'n'
    user_name = input("Please enter your full name: ").title()
    street_address = input("Please enter your street address: ")
    city = input("Please enter your city: ")
    state = input("Please enter your state: ")
    zip_code = input("Please enter your ZIP code: ")
    phone_number = input("Please enter your phone number: ")
    return [file_name, user_name, street_address, city, state, zip_code, phone_number]

def write_file(user_data):
    '''writes user information to text file'''
    print(f"Now writing your information to {user_data[0]}.txt")
    with open(f'{user_data[0]}.txt', 'w') as w:
        w.write(f'Name: {user_data[1]}\nAddress: {user_data[2]} {user_data[3]}, {user_data[4]} {user_data[5]}'+
            f'\nPhone Number: {user_data[6]}')
    sleep(1)
    print("File creation was successful")

def read_file(file_name):
    '''reads back text file just created'''
    print("Confirming file text...")
    sleep(1)
    with open(file_name, 'r') as r:
        for line in r.readlines():
            print(line.strip())

def main():
    '''launches program and follows linear path to create user data file, then exits'''
    confirm = 'n'
    while confirm == 'n' or confirm == 'no':
        target_dir = select_dir()
        confirm = confirm_dir(target_dir)
    try_chdir(target_dir)
    chdir(target_dir)
    print(f'You have confirmed the following directory: {target_dir}')
    correct = 'n'
    while correct == 'n':
        user_data = get_user_data()
        print(user_data)
        correct = input(f'You have included the following information:\n\tFile Name: {user_data[0]}.txt\n\t'+
            f'Name: {user_data[1]}\n\tAddress: {user_data[2]} {user_data[3]}, {user_data[4]} {user_data[5]}'+
            f'\n\tPhone Number: {user_data[6]}\n\tIs this correct? (y/n): ')
    write_file(user_data)
    read_file(f'{user_data[0]}.txt')
    input("Thank you for using the user data input tool. Press enter to exit.")
    quit()

#simple greeting, then launches program    
print("Welcome. This is the user data input program.")
main()