import os
import shutil


UPLOAD_FOLDER = "uploads"


def organize_file(filepath, department):

    # Clean department name
    department = department.strip()

    # If AI gives unknown department
    if department == "":
        department = "Other"


    # Create department folder

    department_folder = os.path.join(
        UPLOAD_FOLDER,
        department
    )


    os.makedirs(
        department_folder,
        exist_ok=True
    )


    # Get filename

    filename = os.path.basename(filepath)


    new_path = os.path.join(
        department_folder,
        filename
    )


    # Move file

    shutil.move(
        filepath,
        new_path
    )


    return new_path