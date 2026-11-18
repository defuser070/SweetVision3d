# 🍬 SweetVision 3D

### AI-Powered Indian Sweets Recognition & 3D Visualization

**SweetVision 3D** is an AI-powered web application that identifies Indian sweets from uploaded images or camera input and generates interactive 3D visualizations. It combines computer vision, deep learning, and data visualization to make food recognition more interactive and informative.

< p></p>
## 🚀 Live Demo

**[🌐 Try SweetVision 3D](https://sweetvision3d.streamlit.app/)**

## ✨ Features

- **AI-Based Sweet Recognition:** Identifies different Indian sweets using a CLIP-based image classification model.
- **Image Upload:** Upload an image of a sweet for analysis.
- **Camera Input:** Capture images directly using your device camera.
- **3D Visualization:** Generates interactive 3D visualizations of detected sweets.
- **Image Segmentation:** Uses OpenCV-based image processing to isolate the food region.
- **Nutrition Estimation:** Provides indicative portion, mass, volume, and sugar estimates.
- **Analysis History:** Keeps analysis results within the current session.
- **CSV Export:** Export available analysis history for further use.
- **Responsive Interface:** Designed to work across desktop and mobile devices.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| PyTorch | Deep learning framework |
| Hugging Face Transformers | CLIP model integration |
| OpenCV | Image processing and segmentation |
| NumPy | Numerical operations |
| Pandas | Data handling |
| Plotly | Interactive 3D visualization |
| Pillow | Image processing |

## 🧠 How It Works

1. Upload an image or capture a photo using the camera.
2. The image is processed and prepared for AI analysis.
3. The CLIP model compares the image against supported sweet categories.
4. The application displays the predicted sweet and similarity score.
5. OpenCV processes the image for approximate segmentation.
6. Plotly generates an interactive 3D visualization.
7. Indicative portion and nutrition estimates are displayed.

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/SweetVision3D.git
```

### 2. Navigate to the project folder

```bash
cd SweetVision3D
```

### 3. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## 📁 Project Structure

```text
SweetVision3D/
│
├── app.py
├── requirements.txt
└── README.md
```

## ⚠️ Important Notes & Limitations

- AI predictions are based on image similarity scores and may not always be accurate.
- Similar-looking sweets may sometimes be misclassified.
- 3D visualization is an approximate representation generated through image processing, not a physical 3D scan.
- Nutrition and portion values are indicative estimates, not laboratory measurements.
- Camera access requires browser permission and a secure connection (HTTPS).
- Analysis history is session-based and is not permanently stored in a database.

## 🔮 Future Improvements

- Improve recognition accuracy with a dedicated Indian sweets dataset.
- Integrate more advanced object detection and segmentation models.
- Improve 3D reconstruction and depth estimation.
- Provide more accurate nutritional information.
- Add user accounts and permanent analysis history.
- Expand support for regional Indian sweets.

## 👨‍💻 Author

**Anurag Sharma**

B.Tech Computer Science & Engineering

GitHub: [Xharma-Anurag](https://github.com/Xharma-Anurag)

LinkedIn: [Anurag Sharma](https://www.linkedin.com/in/anurag-sharma-284715296)

---

⭐ If you find SweetVision 3D interesting, consider giving this repository a star!

**Built with ❤️ using Python, AI, Computer Vision, and Streamlit.**
