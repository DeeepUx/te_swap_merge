from modules import script_callbacks

def on_ui_tabs():
    from .te_swap_merge import on_ui_tabs as te_on_ui_tabs
    print("Registering TE Swap & Merge tab...")
    return [te_on_ui_tabs()]

print("Initializing TE Swap & Merge extension...")
script_callbacks.on_ui_tabs(on_ui_tabs)
