import database_handler

menu_options = {
    1: 'Login',
    2: 'Register'
}

# login menu
def print_login_menu():
    for key in menu_options.keys():
        print(key, ': ', menu_options[key])


def handle_login_menu_input():
    while (True):
        print_login_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        # Check what choice was entered and act accordingly
        if option == 1:
            username = input("Input username: ")
            password = input("Input password: ")
            return [username, password, "1"]
        elif option == 2:
            username = input("Pick new username: ")
            password = input("Pick new password: ")
            return [username, password, "2"]
        else:
            print('Invalid option. Please enter 1 or 2.')