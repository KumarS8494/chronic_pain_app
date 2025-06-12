import gradio as gr
from fastapi import FastAPI
from app.UI.Screen import get_interface
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

interface = get_interface()
interface.queue()  

gradio_app = gr.mount_gradio_app(app, interface, path="/gradio")

@app.get("/")
def read_root():
    return {"message": "Visit /gradio to open the diagnosis UI"}
