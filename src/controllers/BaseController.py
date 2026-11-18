from helpers.config import get_settings, Settings
import os
import random
import string

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__)) #Get the BaseController's directory path which is the controllers directory which is the file named src
        self.files_dir = os.path.join(
            self.base_dir, 
            "assets/files"
        ) #You know the place where you will store your files

    def generate_random_string(self, length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))