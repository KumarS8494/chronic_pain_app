# app/ui/gradio_ui.py

import gradio as gr
from app.utils.predict import predict_diagnosis

age_values = ['25', '30', '35', '40', '45']
gender_values = ['Male', 'Female']
weight_values = ['24','40','50', '60', '70', '80']
duration_values = ['8', '12', '18', '24']
pain_score_values = ['30-50', '20-40', '30-50', '40-60', '50-80', '60-90']
side_of_pain_values = ['Left', 'Right', 'Both']
pain_site_values = [
    "Low back pain",
        "Pain over side of low back midline",
        "Midline low back pain",
        "Midline and side of midline low back pain",
        "Pain over the flank and side of low back midline",
        "History of fall on the buttocks",
        "Pain over the buttock",
        "Pain over the buttock and posterior thigh",
        "Pain over the buttock and back side of thigh",
        "Pain over the buttocks",
        "Low back pain with pain over the buttock and thigh",
        "Low back pain over the side above buttock",
        "Low back and leg pain",
        "Pain over midline low back and over the side",
        "Pain over the side of low back and buttock",
        "Pain over the side of low back midline",
        "Pain over the lower part of low back",
        "Pain over the buttock",
        "Pain over the buttock and thigh",
        "Pain over the posterolateral thigh",
        "Pain over the flank and hip",
        "Morning Stiffness",
        "Pain increases with prolonged activity",
        "Pain over the outer and back side of thigh",
        "Pain over the buttock and posterior thigh",
        "History of fall on the buttocks",
        "Pain over the back side of thigh",
        "Pain over the buttock and outer thigh",
        "Pain over outer thigh",
        "Occasionally the pain occurs below knee",
        "Pain over the back of thigh",
        "Pain over the outer side of thigh",
        "Radiation of pain along thigh and leg",
        "Radiation of pain along thigh",
        "Severe pain may travel from low back to thigh and leg",
        "Pain over the thigh, leg and foot",
        "Pain travels from low back to thigh and legs",
        "Stiffness in low back",
        "Pain over the side of thigh and leg",
        "band like sensation ove the low back",
        "Sharp, burning along the buttock, thigh and leg",
        "Pain occurs in a line along posterior thigh and leg",
        "Pain along the outer aspect of thigh",
        "Burning and tingling sensation along posterior thigh and leg",
        "Pain along the outer and front aspect of leg",
        "When pain increases in low back, pain travels along the outer aspect of thigh",
        "Severe pain along the outer aspect of thigh",
        "Pain along the back of leg and heel",
        "Pain along the side of leg and foot",
        "Pain over the side of low back midline is more than pain in the midline",
        "Pain over the upper lateral thigh",
        "Pain is present over the side of low back midline",
        "Morning Stiffness",
        "Pain over the posterolateral thigh",
        "Pain over the outer aspect of leg",
        "Pain increases with prolonged activity",
        "tenderness over side of low back midline",
        "Paraspinal tenderness is present",
        "Pain over the back of thigh",
        "Occasionally the pain occurs below knee",
        "Pain over the groin",
        "Tenderness over the sacral sulcus",
        "Pain increases after prolonged sitting",
        "History of fall on the buttocks",
        "Pain over the groin and lower abdomen",
        "Pain over the back side of thigh",
        "Tenderness over the posterior superior iliac spine",
        "Pain over outer thigh",
        "Pain over the back and outer side of thigh",
        "Pain over the thigh",
        "Tingling and pins or needle sensation along thigh and leg",
        "Pain is aching and cramping in character",
        "Tingling sensation in the thigh",
        "Nodules or areas of taught muscle bands in the low back muscles",
        "Pain increases while curling on bed",
        "Tingling, pins and needle sensation along the thigh or leg",
        "Pain and stiffness after period of inactivity",
        "Pain is along the outer aspect of thigh and leg",
        "Pain increases with walking and standing",
        "Tingling on the outer aspect of thigh",
        "Pain increases while raising leg on lying supine",
        "Pain increasses after walking for 10 to 15 minutes",
        "Pain increases with walking and forward bending activities",
        "Pines and needle sensation along the back of leg",
        "Tingling on the outer aspect of foot"
] 

def predict_wrapper(age, gender, weight, duration, pain_score, side_of_pain,
                    pain1, pain2, pain3, pain4, pain5, pain6, pain7):
    features = ', '.join(filter(None, [pain1, pain2, pain3, pain4, pain5, pain6, pain7]))
    text = (
        f"Age: {age}\n"
        f"Gender: {gender}\n"
        f"Weight: {weight} kg\n"
        f"Duration of Pain: {duration} months\n"
        f"Pain Score: {pain_score}/5\n"
        f"Side of Pain: {side_of_pain}\n"
        f"Features of Pain: {features}"
    )
    return predict_diagnosis(text)

def get_interface():
    with gr.Blocks(css=".gradio-container { background-color: #f9f9fc; }") as demo:
        gr.Markdown("## 🧠 Chronic Pain Diagnostic Tool")
        gr.Markdown("Fill out the patient info below and get a probable diagnosis using ClinicalBERT.")

        with gr.Row():
            with gr.Column():
                Age = gr.Dropdown(age_values, label="Age",interactive=True, allow_custom_value=True)
                Gender = gr.Dropdown(gender_values, label="Gender", interactive=True, allow_custom_value=True)
                Weight = gr.Dropdown(weight_values, label="Weight (kg)", interactive=True, allow_custom_value=True)
                Duration = gr.Dropdown(duration_values, label="Duration (months)", interactive=True, allow_custom_value=True)
                PainScore = gr.Dropdown(pain_score_values, label="Pain Score (1–5)", interactive=True, allow_custom_value=True)
                Side_of_pain = gr.Dropdown(side_of_pain_values, label="Side of Pain", interactive=True, allow_custom_value=True)

            with gr.Column():
                with gr.Accordion("🩻 Site and Features of Pain", open=True):
                    Pain1 = gr.Dropdown(pain_site_values, label="Pain Feature 1", interactive=True, allow_custom_value=True)
                    Pain2 = gr.Dropdown(pain_site_values, label="Pain Feature 2",   interactive=True, allow_custom_value=True)
                    Pain3 = gr.Dropdown(pain_site_values, label="Pain Feature 3", interactive=True, allow_custom_value=True)
                    Pain4 = gr.Dropdown(pain_site_values, label="Pain Feature 4", interactive=True, allow_custom_value=True)
                    Pain5 = gr.Dropdown(pain_site_values, label="Pain Feature 5",   interactive=True, allow_custom_value=True)
                    Pain6 = gr.Dropdown(pain_site_values, label="Pain Feature 6", interactive=True, allow_custom_value=True)
                    Pain7 = gr.Dropdown(pain_site_values, label="Pain Feature 7", interactive=True, allow_custom_value=True)

        with gr.Row():
            predict_btn = gr.Button("🧠 Predict Diagnosis", variant="primary")
            clear_btn = gr.Button("🧹 Clear Inputs")

        output = gr.Text(label="Predicted Diagnosis")

        predict_btn.click(
            fn=predict_wrapper,
            inputs=[Age, Gender, Weight, Duration, PainScore, Side_of_pain, Pain1, Pain2, Pain3, Pain4, Pain5, Pain6, Pain7],
            outputs=output
        )

        clear_btn.click(
        lambda *args: [""] * 13,
        inputs=[Age, Gender, Weight, Duration, PainScore, Side_of_pain, Pain1, Pain2, Pain3, Pain4, Pain5, Pain6, Pain7],
        outputs=[Age, Gender, Weight, Duration, PainScore, Side_of_pain, Pain1, Pain2, Pain3, Pain4, Pain5, Pain6, Pain7]
        )


    return demo

if __name__ == "__main__":
    demo = get_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)