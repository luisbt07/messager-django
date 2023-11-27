### Setup a Django Project
Let’s start by creating and activating a new virtual environment with the venv module.
    
    mkdir django_project
    cd django_project

    # To install specific python version on venv
    sudo apt-get install python3.11-venv
    python3.11 -m venv my_env
    source my_env/bin/activate
    # Create requirements.txt file
    pip freeze > requirements.txt


Now that you have your virtual environment created, you can install Django with pip.