# app/ui/gradio_ui.py

import gradio as gr
from app.utils.predict import predict_diagnosis
from app.utils.User_handler import save_to_mongo
from dotenv import load_dotenv
load_dotenv()

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
    
    print("🔍 Text to predict:\n", text)  

    try:
        prediction = predict_diagnosis(text)
        print("✅ Prediction Result:", prediction)
    except Exception as e:
        print("❌ Prediction Error:", e)
        return "Prediction failed. Please check the logs."

    data_to_save = {
        "age": age,
        "gender":gender,
        "weight": weight,
        "duration": duration,
        "pain_score": pain_score,
        "side_of_pain": side_of_pain,
        "pain_features": [pain1, pain2, pain3, pain4, pain5, pain6, pain7],
        "prediction_diagnosis": prediction,
        "confidence": prediction.split("Confidence: ")[-1] if "Confidence: " in prediction else "N/A",
    }
    try:
        mongo_id = save_to_mongo(data_to_save)
    except Exception as e:
        # print("MongoDB Save Error:", e)
        return f"Prediction: {prediction}\n Save Failed"
    return prediction

def get_interface():
    with gr.Blocks(css="""
    .gradio-container { background-color: #f9f9fc; }

    #logo-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 90px;
        padding: 10px 0;
        flex-wrap: wrap;
    }

    .logo-img img {
        max-height: 60px;
        width: auto;
        object-fit: contain;
    }

    /* Smaller logo for logo2 */
    #logo2 img {
        max-height: 50px;
    }

    /* Larger logo for logo3 */
    #logo3 img {
        max-height: 80px;
    }

    @media (max-width: 768px) {
        #logo-wrapper {
            flex-direction: column;
            gap: 40px;
        }

        .logo-img img {
            max-height: 40px;
        }

        #logo2 img {
            max-height: 35px;
        }

        #logo3 img {
            max-height: 55px;
        }
    }
    """) as demo:
        with gr.Row(elem_id="logo-row"):
            with gr.Row(elem_id="logo-wrapper"):
                gr.Image(value="app/ui/assets/logo1.png",show_label=False, show_download_button=False, show_fullscreen_button=False, elem_id="logo1", elem_classes=["logo-img"],container=False)
                gr.Image(value="app/ui/assets/logo2.png", show_label=False, show_download_button=False, show_fullscreen_button=False, elem_id="logo2", elem_classes=["logo-img"],container=False)
                gr.Image(value="app/ui/assets/logo3.png", show_label=False, show_download_button=False, show_fullscreen_button=False, elem_id="logo3", elem_classes=["logo-img"],container=False)
                gr.Image(value="app/ui/assets/logo4.png", show_label=False, show_download_button=False, show_fullscreen_button=False, elem_id="logo4", elem_classes=["logo-img"],container=False)

        gr.Markdown("# 🧠 Chronic Pain Diagnostic Tool")
        gr.Markdown("##### Fill out the patient info below and get a probable diagnosis using AI.")

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
    demo.launch(server_name="0.0.0.0", server_port=8000, share=True, debug=True)