import os
import shutil

from huggingface_hub import login, upload_file

embedding_name = "openai"
DATABASE_DIR = f"data/manifestos/chroma/{embedding_name}/"

def push_to_huggingface():
    """Creates a zip file of the database folder and pushes it to the Hugging Face dataset.
        NOTE: Make sure to set the HUGGINGFACE_TOKEN environment variable.
    """

    login(token=os.getenv("HUGGINGFACE_TOKEN")) 
    # Create zip file of the database folder
    shutil.make_archive(
        base_name = DATABASE_DIR.rstrip("/"), 
        format = 'zip', 
        root_dir = DATABASE_DIR
    )
    upload_file(
        path_or_fileobj=f"{DATABASE_DIR.rstrip('/')}.zip",
        repo_id="cliedl/electify",
        repo_type="dataset",
        path_in_repo=f"{os.path.basename(DATABASE_DIR.rstrip('/'))}.zip"
    )

if __name__ == "__main__":

    push_to_huggingface()