from lazyme import color_print

menu_options = {
    1: 'Login',
    2: 'Register'
}


# print login menu options
def print_login_menu():
    color_print("--------------------------", color='cyan')
    color_print("Welcome to Python Chatroom", color='green')
    color_print("--------------------------", color='cyan')
    for key in menu_options.keys():
        print(key, ': ', menu_options[key])


# handle login menu inputs
def handle_login_menu_input():
    while (True):
        print_login_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            color_print('Invalid option. Please enter 1 or 2.', color='red')
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
            color_print('Invalid option. Please enter 1 or 2.', color='red')
