# install.py
import launch

if not launch.is_installed("safetensors"):
    launch.run_pip("install safetensors", "requirements for TE Swap & Merge extension")

if not launch.is_installed("transformers"):
    launch.run_pip("install transformers", "requirements for TE Swap & Merge extension")
    
