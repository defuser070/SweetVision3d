# SweetVision 3D — Enhanced UI

## What's improved
- Responsive pink/white/berry UI with animated cards and transitions.
- Working Home → Analyze Food navigation using Streamlit callbacks.
- First-visit dessert splash screen and animated sweet-themed loading panel during recognition.
- Sweet emoji cursor selected randomly for each new app session.
- Camera and image-upload tabs. Streamlit's camera input requests browser permission when the user captures a photo.
- Result tabs for overview, visual studio, and nutrition explorer.
- Interactive Plotly similarity chart, 3D-style surface, and nutrition composition chart.
- Session history and CSV export.
- Lazy PyTorch/Transformers imports so the dashboard can still open if the model runtime has an installation problem.

## Run on Windows
Open CMD in this project folder, then:

```cmd
py -3.11 -m venv venv311
venv311\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If you already have `venv311`, activate it instead of recreating it.

## First run
The first recognition may download the `openai/clip-vit-base-patch32` model from Hugging Face. Keep the internet connection on. The model is cached for later runs.

## Camera permissions
- Camera permission is requested by the browser when the camera capture widget is used.
- Camera access generally requires `localhost` or HTTPS.
- If permission was previously denied, change the browser's site settings to Allow for Camera, then reload.
- Image upload remains available if camera access is unavailable.

## Notes about estimates
The CLIP score is image-text similarity, not a calibrated probability. GrabCut is approximate foreground extraction. The depth-style visualization is generated from mask shape and is not physical depth reconstruction. Mass, density and sugar references are class-level estimates, not lab-verified nutrition values.

## Files
- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies
