from huggingface_hub import upload_folder, login

import os
token = os.getenv("HUGGINGFACE_TOKEN")

upload_folder(
    repo_id="krsuman123/Chronic_Pain_classification",
    folder_path=r"D:\Amity\App\Chronic_Pain_App\app\ClinicalBert_Model",
    repo_type="model",
    path_in_repo="."  
)

print("✅ Model uploaded successfully!")
