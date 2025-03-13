import time
import functions
import constants
import importlib

functions.generate_constants('../config/config.yaml')
time.sleep(1)
importlib.reload(constants)  # Reload in case it was just created

branches_objects={}

#initializing with smouha, the first branch
branch, obj = functions.create_branch(constants._FIRST_BRANCH)
branches_objects[branch]=obj

functions.welcome_message()
functions.main_login(obj)

