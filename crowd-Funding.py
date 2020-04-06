#!/usr/bin/python3
import json, re, datetime

def get_users():
    users = {}
    with open('users.json', 'r') as f:
        users = json.load(f)
    return users

def get_last_id(users):
    return list(users.keys())[-1]

def get_next_id(id):
    return str(int(id)+1)

def validate_email(email):
    valid = re.search("^[a-zA-Z]+[a-zA-Z0-9]*@[a-z]+.[a-z]+", email)
    if not valid:
        print("please enter a valid email")
        return False
    else:
        users = get_users()
        for user in users.values():
            if email in user["email"]:
                print("Email already exists")
                return False
    return True

def validate_phone(phone):
    valid = re.search("(201)[0-9]{9}", phone)
    if not valid:
        print("please enter a valid phone number")
        return False
    return True

def validate_password(password):
    if len(password) < 6 or len(password) > 20:
        print("Password must be at least 6 characters to 20 characters")
        return False
    return True

def login_check(email, password):
    users = get_users()
    for id, user in users.items():
        if email == user['email'] and password == user['password']:
            return {id:user}
    return False

def login():
    email = input("please enter your email: ")
    password = input("Password: ")
    user = login_check(email, password)
    if user:
        return user
    else:
        print("Invaild email or password")

def register():
    fname = input("Please enter your frist name: ")
    lname = input("Please enter your last name: ")
    email = input("Please enter your email: ")
    if not validate_email(email):
        return False
    password = input("please enter your password: ")
    confirm = input("please re-enter your password: ")
    if not(password == confirm):
        return False
    mobile = input("please enter your mobile number: ")
    if not validate_phone(mobile):
        return False
    users = get_users()
    user = {}
    
    if validate_email(email) and validate_password(password) and password == confirm and validate_phone(mobile):
        user["fname"] = fname
        user["lname"] = lname
        user["email"] = email
        user["password"] = password
        user["mobile"] = mobile
        users = get_users()
        id = 1
        if users:
            id = get_next_id(get_last_id(users))
        users[id] = user
        with open('users.json', 'w') as users_file:
            json.dump(users, users_file, sort_keys=True, indent=4)
        print("Registration compeleted")
        return True
    print("Registarion went wrong!")
    return False

def get_user_details(user):
    return list(user.values())[0]


def get_projects():
    projects = {}
    with open('projects.json', 'r') as f:
        projects = json.load(f)
    return projects

def display_projects(projects):
    print("\ncurrent projects: ")
    for users_projects in projects.values():
        for project in users_projects.values():
            print(f"project-title: {project['title']}")
            print(f"project-details: {project['details']}")
            print(f"project-target: {project['target']}")
            print(f"project-start-date: {project['start']}")
            print(f"project-end-date: {project['end']}\n")

def list_projects():
    projects = get_projects()
    if not projects:
        print("No projects added yet\n")
    else:
        display_projects(projects)

def validate_date(date):
    try:
        day,month,year = date.split('/')
        isValidDate = True
        datetime.datetime(int(year),int(month),int(day))
    except ValueError :
        isValidDate = False
    return isValidDate

def get_last_project_id(projects, email):
    return list(projects[email].keys())[-1]

def create_project(email):
    projects = get_projects()
    project_id = 1
    if email not in projects.keys():
        projects[email] = {}
    if projects[email]:
        project_id = get_next_id(get_last_project_id(projects, email))

    title = input("please enter title of the fund: ")
    details = input("please enter details of the fund: ")
    target = input("please enter target of the fund: $")
    start = input("please enter the start date: ")
    if not validate_date(start):
        print("wrong date format day/month/year")
        return False
    end = input("please enter the end date: ")
    if not validate_date(end):
        print("wrong date format day/month/year")
        return False
    project = {}
    project["title"] = title
    project["details"] = details
    project["target"] = target
    project["start"] = start
    project["end"] = end
    projects[email][project_id] = project
    with open('projects.json', 'w') as projects_file:
        json.dump(projects, projects_file, sort_keys=True, indent=4)
    print("Project added\n")


def edit_project(email):
    id = input("please enter project id: ")
    projects = get_projects()
    if email not in projects.keys():
        print("No project exist\n")
    else:
        if id in projects[email][id]:
            project = projects[email][id]
            while True:
                title = input("please enter new title: ")
                details = input("please enter new details: ")
                target = input("please enter new target: ")
                start = input("please enter new start date: ")
                if not validate_date(start):
                    print("wrong date format\n")
                    return
                end = input("please enter new end date: ")
                if not validate_date(end):
                    print("wrong date format\n")
                    return
                if title:
                    project["title"] = title
                if target:
                    project["target"] = target
                if details:
                    project["details"] = details
                if start:
                    project["start"] = start
                if end:
                    project["end"] = end
                projects[email][id] = project
                with open('projects.json', 'w') as projects_file:
                    json.dump(projects, projects_file, indent=4)
                print("Editted successfully\n")

        else:
            print(f"No project with id {id}\n")

def delete_project(email):
    id = input("please enter project id: ")
    projects = get_projects()
    if email not in projects.keys():
        print("No project exist\n")
    else:
        if id in projects[email][id]:
            del projects[email][id]
            with open('projects.json', 'w') as projects_file:
                json.dump(projects, projects_file, sort_keys=True, indent=4)
            print("deleted successfully\n")

        else:
            print(f"No project with id {id}\n")

def show_searched_projects(search_result):
    print("\nsearched results: ")
    for project in search_result:
            print(f"project-title: {project['title']}")
            print(f"project-details: {project['details']}")
            print(f"project-target: {project['target']}")
            print(f"project-start-date: {project['start']}")
            print(f"project-end-date: {project['end']}\n")

def search_project():
    search_date = input("please enter a valid date to search for(start of the project): ")
    if not validate_date(search_date):
        print("wrong date format\n")
        return
    search_result = []
    projects = get_projects()
    for users_projects in projects.values():
        for project in users_projects.values():
            if search_date in project["start"]:
                search_result.append(project)
    if search_result:
        show_searched_projects(search_result)
    else:
        print("No projects with the chosen start date\n")


current_logged_in = {}
user_details = {}
registered_actions = ["create", "edit", "list", "delete", "search", "logout","exit"]
exit_flag = False


print("Welcome to crowd Funding app")
while not exit_flag:
    if current_logged_in:
        user_details = get_user_details(current_logged_in)
        while not exit_flag:
            action = input("please enter your action:\n(create, edit, list, delete, search, logout, exit): ").lower()
            if action not in registered_actions:
                print("Wrong choice")
            elif action == 'create':
                create_project(user_details["email"])
            elif action == 'edit':
                edit_project(user_details["email"])
            elif action == 'list':
                list_projects()
            elif action == "delete":
                delete_project(user_details["email"])
            elif action == "search":
                search_project()
            elif action == "logout":
                current_logged_in = {}
                break
            else:
                exit_flag = True

    else:
        print("\nYou need to log in in order to use the app")
        while not exit_flag and not current_logged_in:
            action = input("please enter your action(login, register, exit): ")
            if action.lower() == "exit":
                exit_flag = True
            elif action.lower() == "login":
                current_logged_in = login()
            elif action.lower() == "register":
                register()
            else :
                print("wrong choice")

print("Thank you for using our application")

