# te_swap_merge.py
import gradio as gr
import torch
from transformers import CLIPTextModelWithProjection
from safetensors.torch import load_file, save_file

def load_model(model_path):
    model = CLIPTextModelWithProjection.from_pretrained(model_path)
    return model

def swap_text_encoder(fine_tuned_model_path, base_model_path, output_path):
    base_text_encoder_2 = load_model(base_model_path + "/text_encoder_2")
    fine_tuned_state_dict = load_file(fine_tuned_model_path)

    base_text_encoder_2_state_dict = base_text_encoder_2.state_dict()

    for key in base_text_encoder_2_state_dict.keys():
        fine_tuned_state_dict[f'text_encoder_2.{key}'] = base_text_encoder_2_state_dict[key]

    save_file(fine_tuned_state_dict, output_path)
    return "Swap completed and saved to " + output_path

def merge_text_encoder(fine_tuned_model_path, base_model_path, output_path, alpha=0.5):
    base_text_encoder_2 = load_model(base_model_path + "/text_encoder_2")
    fine_tuned_state_dict = load_file(fine_tuned_model_path)

    base_text_encoder_2_state_dict = base_text_encoder_2.state_dict()
    merged_state_dict = {}

    for key in base_text_encoder_2_state_dict.keys():
        fine_tuned_key = f'text_encoder_2.{key}'
        if fine_tuned_key in fine_tuned_state_dict:
            merged_state_dict[fine_tuned_key] = (
                alpha * base_text_encoder_2_state_dict[key] +
                (1 - alpha) * fine_tuned_state_dict[fine_tuned_key]
            )
        else:
            merged_state_dict[fine_tuned_key] = base_text_encoder_2_state_dict[key]

    fine_tuned_state_dict.update(merged_state_dict)
    save_file(fine_tuned_state_dict, output_path)
    return "Merge completed and saved to " + output_path

def on_ui_tabs():
    with gr.Blocks() as demo:
        with gr.Row():
            fine_tuned_model_path = gr.Textbox(label="Fine-Tuned Model Path")
            base_model_path = gr.Textbox(label="Base Model Path")
            output_path = gr.Textbox(label="Output Path")
            alpha = gr.Slider(label="Alpha for Merge", minimum=0.0, maximum=1.0, value=0.5)
        
        with gr.Row():
            swap_button = gr.Button("Swap Text Encoder")
            merge_button = gr.Button("Merge Text Encoder")

        swap_result = gr.Textbox(label="Swap Result")
        merge_result = gr.Textbox(label="Merge Result")

        swap_button.click(swap_text_encoder, inputs=[fine_tuned_model_path, base_model_path, output_path], outputs=[swap_result])
        merge_button.click(merge_text_encoder, inputs=[fine_tuned_model_path, base_model_path, output_path, alpha], outputs=[merge_result])

    return ("TE Swap & Merge", demo, "te_swap_merge")

if __name__ == "__main__":
    print("Launching TE Swap & Merge extension...")
    on_ui_tabs().launch()
