import os

from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import FastAPI, APIRouter, Depends, UploadFile  # type: ignore
from models import ResponseSignal
import re
import os

class DataController(BaseController):

    def __init__(self):
        super().__init__() #Calling the BaseController's __init__ method to initialize app_settings
        self.size_scale = 1048576 #convert bytes to MB since the FILE_MAX_SIZE is in MB & .size accesses the file size in bytes
    
    def validate_uploaded_file(self, file: UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED

        return True, ResponseSignal.FILE_VALIDATED_SUCCESS

    def generate_unique_filename(self, orig_file_name: str, project_id: str):

        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_file_name = self.get_clean_filename(
            orig_file_name=orig_file_name
        )

        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )
        return new_file_path
            
    def get_clean_filename(self, orig_file_name: str):

        #Remove any special character except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())
        #replace space with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name


        

