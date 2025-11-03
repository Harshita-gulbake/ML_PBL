# IAgroscan - AI-Powered Plant Disease Detection

IAgroscan is an advanced machine learning application designed to detect and identify plant diseases in agricultural crops. Using computer vision and AI, it helps farmers and agricultural specialists quickly diagnose crop health issues.

## 🌱 Features

- **Single Image Detection**: Analyze individual plant images for disease identification
- **Batch Detection**: Process multiple images at once for large-scale assessment
- **Detailed Reports**: Generate comprehensive PDF reports with detection statistics
- **AI-Powered Recommendations**: Receive treatment and prevention advice for detected diseases
- **Data Visualization**: View detection statistics through intuitive charts and graphs
- **Detection History**: Access past detection records for tracking disease patterns

## 🔍 Supported Crops & Diseases

IAgroscan can detect various diseases across multiple crops:

- **Sugarcane**: Yellow Spot (Mycovellosiella koepkei), Red Rot
- **Corn**: Gray Leaf Spot, Rust, Leaf Blight
- **Banana**: Cordana, Pestalotiopsis, Sigatoka

## 💻 Technical Overview

IAgroscan is built with:
- **YOLO (You Only Look Once)**: For rapid, accurate object detection
- **CustomTkinter**: Modern UI framework for desktop application
- **OpenAI Integration**: For generating detailed disease management recommendations
- **Matplotlib**: For statistical visualization of detection results
- **PyMySQL**: For database management of detection records

## 📊 How It Works

1. **Select an image** or folder of images containing plant specimens
2. **AI model processes** the images to detect diseases
3. **Review results** displayed directly in the application
5. **Generate reports** with detection statistics and treatment recommendations
6. **Track disease patterns** over time with the built-in database

## 📷 Captures
<p align="center">
  <img src="https://github.com/user-attachments/assets/5106615b-66e7-44db-b802-c155a316b473" alt="GUI"/>
  <img src="https://github.com/user-attachments/assets/b0a3e4af-805a-42cc-809b-f8688f0e1e9b" alt="Multiple Detections 1"/>
  <img src="https://github.com/user-attachments/assets/7f34a6ee-778b-4202-9676-37f5f8244cd8" alt="Multiple Detections 2"/>
</p>

## 🙏 Acknowledgments

- The YOLO model was trained on a custom dataset of agricultural plant diseases
- Special thanks to agricultural specialists who provided expertise for the training data, all the links are shown below:
    - https://www.kaggle.com/datasets/shubham2703/five-crop-diseases-dataset
    - https://www.kaggle.com/datasets/kamal01/top-agriculture-crop-disease
    - https://www.kaggle.com/datasets/nirmalsankalana/sugarcane-leaf-disease-dataset
    - https://www.kaggle.com/datasets/kaiwenhuuu/sugarcane-leaf-disease-dataset
    - https://www.kaggle.com/datasets/roshitab/sugarcane-leaf-disease-dataset
