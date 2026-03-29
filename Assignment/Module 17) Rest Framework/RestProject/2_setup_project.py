import os
import subprocess
import sys

def setup_django_project():
    """
    Module 17, Lab 2 & Practical 2:
    Write a requirements.txt file for a Django project and write a script to set up a Django project.
    
    Lab 9 & Practical 9:
    Create a new Django project and app for managing doctor profiles.
    """
    print("Setting up the Django Project and installing dependencies...")
    
    # 1. Install packages from requirements.txt
    if os.path.exists("requirements.txt"):
        print("Installing from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("requirements.txt not found. Exiting.")
        return

    # 2. Setup Django Project if it doesn't exist (assuming this script is run where you want the project)
    project_name = "RestProject"
    app_name = "doctor_finder"
    
    # Check if manage.py exists to see if the project is already created
    if not os.path.exists("manage.py"):
        print(f"Creating Django project '{project_name}'...")
        subprocess.check_call(["django-admin", "startproject", project_name, "."])
    else:
        print(f"Django project '{project_name}' already exists.")

    # 3. Create the app doctor_finder
    if not os.path.exists(app_name):
        print(f"Creating app '{app_name}'...")
        subprocess.check_call([sys.executable, "manage.py", "startapp", app_name])
    else:
        print(f"App '{app_name}' already exists.")

    print("\nProject setup complete!")
    print("Next steps:")
    print(f"1. Add '{app_name}' and other third-party apps to INSTALLED_APPS in {project_name}/settings.py")
    print("2. Run `python manage.py migrate` to apply database changes.")

if __name__ == "__main__":
    setup_django_project()
