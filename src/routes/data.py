from fastapi import FastAPI, APIRouter, Depends, UploadFile, status  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController #Imported from the __int__.py file in the controllers directory
import aiofiles # type: ignore
from models import ResponseSignal
import logging


logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):

    # Validate the file properties
    data_controller = DataController()

    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id) #get_project_path is returned on the one in the ProjectController.py file
    file_path = data_controller.generate_unique_filename(
        orig_file_name=file.filename,
        project_id=project_id
    )


#The following code is used to save the uploaded file to the specified file path asynchronously using aiofiles. It opens the file in write-binary mode ("wb") and writes the contents of the uploaded file to it.
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:

        logger.error(f"Error while uploading file: {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED
            }
        )            

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS
        }
    )