.\.venv\Scripts\Activate.ps1 

python -m pip install -r requirements.txt


** uninstall this, because normally install torch, it will not match the CUDA
python -m pip uninstall torch torchvision torchaudio


** make sure you install CUDA for windows (my OS) and have gpu from nvidia
** use this to match the CUDA for torch
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

stabilityai/sd-turbo (done and ok with animal and things, not with human)
stabilityai/sdxl-turbo (better and larger)

Heartsync/NSFW-Uncensored (trying and okay with uncensored but only anime theme)
UnfilteredAI/NSFW-gen-v2.1 (still too large)
