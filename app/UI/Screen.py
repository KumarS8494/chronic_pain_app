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
"Pain over the buttock and posterior thigh",
"Midline and side of midline low back pain",
"Radiation of pain along thigh and leg",
"Pain increases with prolonged activity",
"Morning Stiffness",
"Tingling and pins or needle sensation along thigh and leg",
"Pain over the groin and lower abdomen",
"Pain increases after prolonged sitting",
"History of fall on the buttocks",
"Tenderness over the sacral sulcus",
"Pain along the outer aspect of thigh",
"Pain increases while raising leg on lying supine",
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
                Age = gr.Dropdown(age_values, value=None, label="Age",interactive=True, allow_custom_value=True)
                Gender = gr.Dropdown(gender_values, value=None ,label="Gender", interactive=True, allow_custom_value=True)
                Weight = gr.Dropdown(weight_values, value=None ,label="Weight (kg)", interactive=True, allow_custom_value=True)
                Duration = gr.Dropdown(duration_values,value=None, label="Duration (months)", interactive=True, allow_custom_value=True)
                PainScore = gr.Dropdown(pain_score_values, value=None ,label="Pain Score (out of 100)", interactive=True, allow_custom_value=True)
                Side_of_pain = gr.Dropdown(side_of_pain_values, value=None ,label="Side of Pain", interactive=True, allow_custom_value=True)

            with gr.Column():
                with gr.Accordion("🩻 Site and Features of Pain", open=True):
                    Pain1 = gr.Dropdown(pain_site_values, value= None, label="Site and Features of Pain 1 (Primary Pain Site)", interactive=True, allow_custom_value=True)
                    Pain2 = gr.Dropdown(pain_site_values, value= None, label="Site and Features of Pain 2(Secondary Pain Site)",   interactive=True, allow_custom_value=True)
                    Pain3 = gr.Dropdown(pain_site_values, value= None, label="Site and Features of Pain 3(Pain Extension or Specific Location)", interactive=True, allow_custom_value=True)
                    Pain4 = gr.Dropdown(pain_site_values, value= None, label="Site and Features of Pain 4 (Pain Triggers or Aggravating Factors)", interactive=True, allow_custom_value=True)
                    Pain5 = gr.Dropdown(pain_site_values, value= None, label="Site and Features of Pain 5 (Pain Relief Factors or Tenderness)",   interactive=True, allow_custom_value=True)
                    Pain6 = gr.Dropdown(pain_site_values, value= None, label="Site and Features of Pain 6(Movement or Functional Impact)", interactive=True, allow_custom_value=True)
                    Pain7 = gr.Dropdown(pain_site_values, value= None, label="Site and Features of Pain 7 (Additional Pain Characteristic)", interactive=True, allow_custom_value=True)

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