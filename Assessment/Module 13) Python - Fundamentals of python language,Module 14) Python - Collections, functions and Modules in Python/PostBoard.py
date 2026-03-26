# ================================================================
# PostBoard — Terminal-Based Internal Community Board
# Company  : Tops Technologies
# Modules  : 13 (Python Fundamentals) + 14 (Collections,
#             Functions and Modules in Python)
#
# PDF Requirements covered — Page 1:
#   [1]  Login system with validation (login attempts)
#   [2]  Post Creation — Title, Description, Date, linked to user
#   [3]  Date — auto-generated OR manually entered
#   [4]  View All Posts — Author, Title, Date, Description
#   [5]  Search Posts by Username
#   [6]  Functions and modular code design
#   [7]  Lists and dictionaries
#   [8]  Looping (for / while)
#   [9]  Input/output formatting
#   [10] Basic validation — login attempts, blank fields
#
# PDF Requirements covered — Page 2:
#   [11] Temporary in-memory data (no database)
#   [12] Clean and organized function-based structure
#   [13] User-friendly prompts and formatted output
#   [14] Validate empty input or repeated usernames
# ================================================================

from datetime import date   # for auto-generated date

# ----------------------------------------------------------------
# SECTION 1 — IN-MEMORY DATA STORAGE
#   Requirement (Page 2): "Temporary in-memory data (no database)"
#   Requirement: "Lists and dictionaries"
# ----------------------------------------------------------------

# List of registered users — each user is a dictionary
# { "username": str, "password": str }
users = []          # list — stores all registered users

# List of posts — each post is a dictionary
# { "author": str, "title": str, "description": str, "date": str }
posts = []          # list — stores all created posts

# Tracks who is currently logged in (None if nobody)
current_user = None

# Maximum login attempts allowed before lockout
MAX_LOGIN_ATTEMPTS = 3


# ----------------------------------------------------------------
# SECTION 2 — UTILITY / HELPER FUNCTIONS
#   Requirement: "Functions and modular code design"
#   Requirement (Page 2): "Clean and organized function-based structure"
# ----------------------------------------------------------------

def print_divider(char="─", width=55):
    """Print a divider line for clean formatted output."""
    print(char * width)


def print_header(title):
    """Print a styled section header."""
    print_divider("═")
    print(f"  {title}")
    print_divider("═")


def print_post(post, index=None):
    """
    Print a single post in clean formatted output.
    Requirement: "Display all posts in a clean format showing:
                  Author, Title, Date, Description"
    """
    print_divider()
    if index is not None:
        print(f"  Post #{index}")
        print_divider("─")
    print(f"  Author      : {post['author']}")
    print(f"  Title       : {post['title']}")
    print(f"  Date        : {post['date']}")
    print(f"  Description : {post['description']}")


def get_non_empty_input(prompt):
    """
    Keep asking until user enters a non-blank value.
    Requirement: "Validate empty input"
    Requirement: "Basic validation (e.g., blank fields)"
    Uses a while loop — Requirement: "Looping (for/while)"
    """
    while True:                             # while loop
        value = input(prompt).strip()
        if value == "":
            print("  ⚠  This field cannot be empty. Please try again.")
        else:
            return value


def find_user(username):
    """
    Search the users list for a matching username.
    Returns the user dict if found, else None.
    Requirement: "Lists and dictionaries"
    """
    for user in users:                      # for loop
        if user["username"].lower() == username.lower():
            return user
    return None


# ----------------------------------------------------------------
# SECTION 3 — REGISTRATION FUNCTION
#   Requirement (Page 2): "Validate … repeated usernames"
# ----------------------------------------------------------------

def register():
    """
    Register a new user with a unique username and password.
    Validates:
      - Empty username or password
      - Repeated / duplicate username
    """
    print_header("REGISTER NEW ACCOUNT")

    # Validate empty username — while loop
    username = get_non_empty_input("  Enter new username : ")

    # Validate repeated usernames
    # Requirement (Page 2): "Validate empty input or repeated usernames"
    if find_user(username) is not None:
        print(f"\n  ⚠  Username '{username}' already exists. Please choose another.\n")
        return

    # Validate empty password — while loop
    password = get_non_empty_input("  Enter new password : ")

    # Store as dictionary inside the users list
    # Requirement: "Lists and dictionaries"
    new_user = {
        "username": username,
        "password": password
    }
    users.append(new_user)                  # append to list

    print(f"\n  ✔  Account created successfully! Welcome, {username}.\n")


# ----------------------------------------------------------------
# SECTION 4 — LOGIN FUNCTION
#   Requirement: "After login, a user can create a post"
#   Requirement: "Basic validation (e.g., login attempts)"
# ----------------------------------------------------------------

def login():
    """
    Log in an existing user.
    Allows MAX_LOGIN_ATTEMPTS tries before locking out.
    Requirement: "Basic validation (e.g., login attempts)"
    Uses a while loop — Requirement: "Looping (for/while)"
    """
    global current_user

    print_header("LOGIN")

    attempts = 0                            # track login attempts

    # while loop — Requirement: "Looping (for/while)"
    while attempts < MAX_LOGIN_ATTEMPTS:
        username = get_non_empty_input("  Username : ")
        password = get_non_empty_input("  Password : ")

        user = find_user(username)

        if user is not None and user["password"] == password:
            current_user = user["username"]
            print(f"\n  ✔  Login successful! Welcome back, {current_user}.\n")
            return True                     # login succeeded
        else:
            attempts += 1
            remaining = MAX_LOGIN_ATTEMPTS - attempts
            if remaining > 0:
                print(f"\n  ✘  Invalid credentials. {remaining} attempt(s) remaining.\n")
            else:
                print("\n  ✘  Too many failed attempts. Access locked.\n")

    return False                            # login failed after max attempts


def logout():
    """Log out the current user."""
    global current_user
    print(f"\n  ✔  Goodbye, {current_user}! You have been logged out.\n")
    current_user = None


# ----------------------------------------------------------------
# SECTION 5 — POST CREATION FUNCTION
#   Requirement: "After login, a user can create a post by providing:
#                 Title, Description, Date (auto-generated or manually entered)"
#   Requirement: "Each post is linked to the user who created it."
# ----------------------------------------------------------------

def create_post():
    """
    Create a new post linked to the logged-in user.
    Fields: Title, Description, Date (auto or manual).
    Validates all blank fields.
    """
    # Guard — must be logged in
    if current_user is None:
        print("\n  ⚠  You must be logged in to create a post.\n")
        return

    print_header("CREATE NEW POST")

    # --- Title (validated, non-empty) ---
    # Requirement: "Title"
    title = get_non_empty_input("  Post Title       : ")

    # --- Description (validated, non-empty) ---
    # Requirement: "Description"
    description = get_non_empty_input("  Post Description : ")

    # --- Date — auto-generated OR manually entered ---
    # Requirement: "Date (auto-generated or manually entered)"
    print("\n  Date Options:")
    print("    [1] Use today's date (auto-generated)")
    print("    [2] Enter date manually")

    date_choice = input("\n  Your choice (1 or 2) : ").strip()

    if date_choice == "2":
        # Manual date entry with basic format validation
        while True:                         # while loop for validation
            manual_date = input("  Enter date (DD-MM-YYYY) : ").strip()
            if manual_date == "":
                print("  ⚠  Date cannot be empty.")
            else:
                post_date = manual_date
                break
    else:
        # Auto-generate today's date
        # Requirement: "auto-generated"
        post_date = str(date.today().strftime("%d-%m-%Y"))
        print(f"  ✔  Date auto-set to: {post_date}")

    # --- Build post as dictionary, linked to current user ---
    # Requirement: "Each post is linked to the user who created it."
    # Requirement: "Lists and dictionaries"
    new_post = {
        "author"      : current_user,       # linked to logged-in user
        "title"       : title,
        "description" : description,
        "date"        : post_date
    }

    posts.append(new_post)                  # append to posts list

    print(f"\n  ✔  Post '{title}' created successfully!\n")


# ----------------------------------------------------------------
# SECTION 6 — VIEW ALL POSTS FUNCTION
#   Requirement: "Display all posts in a clean format showing:
#                 Author, Title, Date, Description"
# ----------------------------------------------------------------

def view_all_posts():
    """
    Display every post stored in the posts list.
    Shows: Author, Title, Date, Description — clean format.
    Requirement: "View All Posts"
    Uses a for loop — Requirement: "Looping (for/while)"
    """
    print_header("ALL POSTS")

    if len(posts) == 0:                     # check if list is empty
        print("  No posts available yet.\n")
        return

    # for loop — Requirement: "Looping (for/while)"
    for index, post in enumerate(posts, start=1):
        print_post(post, index=index)

    print_divider()
    print(f"  Total posts: {len(posts)}\n")


# ----------------------------------------------------------------
# SECTION 7 — SEARCH POSTS BY USERNAME FUNCTION
#   Requirement: "Search Posts by Username —
#                 Let staff search posts created by a specific user."
# ----------------------------------------------------------------

def search_posts_by_username():
    """
    Search and display all posts created by a given username.
    Requirement: "Search Posts by Username"
    Requirement: "Let staff search posts created by a specific user."
    Uses a for loop — Requirement: "Looping (for/while)"
    """
    print_header("SEARCH POSTS BY USERNAME")

    # Validate empty search input
    # Requirement: "Validate empty input"
    search_name = get_non_empty_input("  Enter username to search : ")

    # for loop — filter matching posts — Requirement: "Looping (for/while)"
    matched = [p for p in posts if p["author"].lower() == search_name.lower()]

    if len(matched) == 0:
        print(f"\n  No posts found for user '{search_name}'.\n")
        return

    print(f"\n  Found {len(matched)} post(s) by '{search_name}':\n")

    # for loop — display each matched post
    for index, post in enumerate(matched, start=1):
        print_post(post, index=index)

    print_divider()
    print()


# ----------------------------------------------------------------
# SECTION 8 — MENUS
#   Requirement: "User-friendly prompts and formatted output"
#   Requirement (Page 2): "User-friendly prompts and formatted output"
# ----------------------------------------------------------------

def show_main_menu():
    """Display the main menu options (before login)."""
    print_header("POSTBOARD — TOPS TECHNOLOGIES")
    print("  [1]  Register")
    print("  [2]  Login")
    print("  [3]  Exit")
    print_divider()


def show_user_menu():
    """Display the user menu options (after login)."""
    print_header(f"POSTBOARD — Logged in as: {current_user}")
    print("  [1]  Create Post")
    print("  [2]  View All Posts")
    print("  [3]  Search Posts by Username")
    print("  [4]  Logout")
    print_divider()


# ----------------------------------------------------------------
# SECTION 9 — USER SESSION LOOP
#   Runs after successful login.
#   Requirement: "Looping (for/while)"
# ----------------------------------------------------------------

def user_session():
    """
    Main interaction loop for a logged-in user.
    while loop — Requirement: "Looping (for/while)"
    """
    while current_user is not None:         # while loop
        show_user_menu()
        choice = input("  Select an option : ").strip()

        if choice == "1":
            create_post()
        elif choice == "2":
            view_all_posts()
        elif choice == "3":
            search_posts_by_username()
        elif choice == "4":
            logout()
        else:
            print("\n  ⚠  Invalid option. Please enter 1, 2, 3 or 4.\n")


# ----------------------------------------------------------------
# SECTION 10 — MAIN PROGRAM ENTRY POINT
#   Requirement: "Functions and modular code design"
#   Requirement (Page 2): "Clean and organized function-based structure"
# ----------------------------------------------------------------

def main():
    """
    Main entry point. Runs the top-level menu loop.
    while loop — Requirement: "Looping (for/while)"
    """
    print("\n")
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║       WELCOME TO POSTBOARD                      ║")
    print("  ║       Tops Technologies Internal Board          ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print()

    # while loop for main program — Requirement: "Looping (for/while)"
    while True:
        show_main_menu()
        choice = input("  Select an option : ").strip()

        if choice == "1":
            register()

        elif choice == "2":
            success = login()
            if success:
                user_session()          # enter user session loop

        elif choice == "3":
            print("\n  Thank you for using PostBoard. Goodbye!\n")
            break                       # exit the while loop

        else:
            print("\n  ⚠  Invalid option. Please enter 1, 2 or 3.\n")


# ----------------------------------------------------------------
# Run the program
# ----------------------------------------------------------------
if __name__ == "__main__":
    main()
