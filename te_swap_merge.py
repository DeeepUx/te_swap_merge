import gradio as gr

def on_ui_tabs():
    print("Setting up the UI tab for TE Swap & Merge...")
    with gr.Blocks() as demo:
        gr.Markdown("# TE Swap & Merge Extension")
    print("UI setup complete.")
    return ("TE Swap & Merge", demo, "te_swap_merge")

if __name__ == "__main__":
    print("Launching TE Swap & Merge extension...")
    demo = on_ui_tabs()
    demo[1].launch()
