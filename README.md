# Bangkit Academy 2024 - Product-Based Capstone Team - C242-PS027

## 📖 Peduli Bumil - Cloud Computing
Peduli Bumil is a health application designed to help pregnant women monitor and maintain their health during pregnancy. This application offers key features such as gestational age tracker, pregnancy risk detection based on health parameters (height, weight, body temperature, blood pressure, blood sugar, age, and heart rate), as well as risk classification into High, Medium, Risk categories. or Low. In addition, Peduli Bumil provides informative articles, interactive chatbots to answer questions about pregnancy, and personal reminders regarding health. With this technology, the application supports pregnant women, especially in remote areas, to prevent complications, increase health understanding, and contribute to the Indonesian government's efforts to reduce maternal mortality.

### Role of Cloud Computing in Peduli Bumil
The Cloud Computing team leverages the power of Google Cloud Platform (GCP) to build a robust, secure, and scalable backend infrastructure for the application. The following services and technologies are integrated into the application:

#### Cloud Run
The backend API, developed using Python Flask, runs on Cloud Run to ensure a fully managed and scalable serverless architecture.
This API processes health data submitted by users and integrates with the TensorFlow Lite (TFLite) model, developed by the Machine Learning team, to deliver real-time pregnancy risk predictions.

#### Firestore 
Acts as the primary database for securely storing user information, including pregnancy risk predictions and historical data.
Firebase Authentication

#### Firebase Authentication
Provides a secure and user-friendly login system, including support for email-based login and Google Sign-In integration.

#### Cloud Storage
Enables an intelligent chatbot that interacts with users, answers queries, and provides personalized health recommendations during pregnancy.
Trained on curated health-related content stored in Cloud Storage, ensuring accuracy and reliability.

#### Vertex AI
Enables an chatbot that interacts with users, answers queries, and provides personalized health recommendations during pregnancy.

#### Google Cloud Monitoring and Logging
Provides end-to-end visibility into application performance with real-time metrics and log analysis.
Assists in proactive troubleshooting and ensuring smooth operation of the application.

## API Backend
[api Backend](https://backend-api-511713702149.asia-southeast2.run.app)

## Installation Instructions API Backend

1. **Clone the repository:**
   ```bash
   https://github.com/BangkitPeduliBumil/cloud-computing
   ```

2. **Create a service account, assign the roles `Cloud Datastore User`, `Cloud Run Invoker`, and `Storage Object Admin`, download the `key.json`, and place it into the folder**

3. Enable API & SERVICES
   ```bash
    gcloud services enable run.googleapis.com
    gcloud services enable containerregistry.googleapis.com
    gcloud services enable cloudbuild.googleapis.com
   ```

4. **Container image and uploads it to Google Container Registry with the tag:**
   ```bash
      gcloud builds submit --tag gcr.io/[PROJECT_ID]/[containername]
   ```

4. **Deploy to Cloud Run**
   ```bash
     gcloud run deploy [containername]\
    --image gcr.io/[PROJECT_ID]/ [containername]\
    --platform managed \
    --region [REGION] \
    --allow-unauthenticated
    --memory 1Gi [OPSIONAL]
   ```

## Testing the API

```bash
https://documenter.getpostman.com/view/39629700/2sAYBd7oEU
```

### Example Endpoints

- **Predict Pregnancy Risk**
  - `POST /predict`
  - Input: Age, Body, Systolic Blood Pressure, Diastolic Blood Pressure, BMI, Blood Glucose.


## Chatbot
[Chatbot](pedulibumil-2792a.et.r.appspot.com)

## 🏛️ Build Architecture 
![](https://github.com/BangkitPeduliBumil/asset/blob/227452df435927ac67084e737a7fbe4140a2b851/architecture.png)


## 🧑‍🤝‍🧑 Cloud Computing Team

|  No. | Member                          | Student ID   | Learning Path        | GitHub            |
|------|---------------------------------|--------------|----------------------|-------------------|
|   1  | Sarhan Pratama                  | C265B4KY4071 | :cloud: Cloud Computing      | [![GitHub](https://img.shields.io/badge/-GitHub-brightgreen?logo=github&logoColor=white)](https://github.com/SarhanPratama) |
|   2  | Muhammad Fadhil                 | C308B4KY2797 | :cloud: Cloud Computing      | [![GitHub](https://img.shields.io/badge/-GitHub-brightgreen?logo=github&logoColor=white)](https://github.com/Dedeuuw) |
