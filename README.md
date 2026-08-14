# 🏙️ NYC House Type Classification

> **An end-to-end Machine Learning project inspired by a simple question: *How does Airbnb understand and categorize its listings?***

I wanted to understand what happens behind the scenes when a platform like Airbnb turns thousands of property attributes into meaningful categories for users.

So I built my own machine learning pipeline using **New York City housing/listing data** to classify different types of properties based on their available features.

This project started as curiosity about how Airbnb-like platforms work and evolved into a practical exploration of **data preprocessing, feature engineering, classification models, evaluation, and model-driven decision making**.

---

## 🎯 What I Built

A machine learning system that takes information about a New York City property and predicts its **house/property type**.

The goal is to transform raw listing information such as:

* Location
* Room characteristics
* Availability
* Reviews
* Pricing
* Host-related information
* Property attributes

into a predicted property category.

Conceptually:

```text
Raw Property Data
        ↓
Data Cleaning
        ↓
Exploratory Data Analysis
        ↓
Feature Engineering
        ↓
Feature Selection
        ↓
Machine Learning Model
        ↓
Property Type Prediction
```

---

## 💡 Why I Built This

This project began with curiosity rather than a predefined problem statement.

When using platforms such as Airbnb, users see a relatively simple interface:

> Location → Property → Price → Reviews → Booking

But underneath that interface is a large amount of structured and unstructured data.

I wanted to explore one small part of that problem:

**Can a machine learning model learn to identify what type of property a listing represents from the information associated with it?**

Rather than simply following a classification tutorial, I used the problem as an opportunity to understand how a real-world ML workflow is constructed from messy data.

---

## 🧠 Machine Learning Problem

### Problem Type

**Multiclass Classification**

### Input

A collection of numerical and categorical attributes describing a New York City property/listing.

### Output

The predicted **property/house type**.

```text
Property Features
       │
       ▼
 ┌───────────────┐
 │ ML Classifier │
 └───────────────┘
       │
       ▼
Predicted House Type
```

---

## 🔍 Dataset

The project uses New York City Airbnb-style listing data containing information about properties, hosts, locations, prices, reviews, availability, and other listing characteristics.

The dataset provides a realistic ML challenge because real-world datasets are rarely clean.

The workflow therefore focuses not only on training a model, but also on answering questions such as:

* Which features are actually useful?
* Which columns contain missing values?
* Are some categories heavily imbalanced?
* Which numerical variables contain outliers?
* Does location influence property type?
* Which features contribute most to classification?
* How well does the model generalize to unseen listings?

---

# 🛠️ Tech Stack

| Category         | Technologies                             |
| ---------------- | ---------------------------------------- |
| Language         | Python                                   |
| Data Processing  | Pandas, NumPy                            |
| Visualization    | Matplotlib, Seaborn                      |
| Machine Learning | Scikit-learn                             |
| Model Evaluation | Classification metrics, Confusion Matrix |
| Development      | Jupyter Notebook                         |

---

# 🔬 Project Workflow

## 1. Data Understanding

The first step was understanding the structure of the dataset rather than immediately training a model.

I examined:

* Dataset dimensions
* Data types
* Missing values
* Duplicate records
* Numerical distributions
* Categorical variables
* Target distribution

This helped identify the challenges that would need to be addressed before modelling.

---

## 2. Exploratory Data Analysis

I used exploratory analysis to understand relationships between property characteristics and the target variable.

Examples of questions explored:

```text
Does location correlate with property type?

Does price distribution differ between property categories?

How does availability vary across different property types?

Which neighbourhoods contain the highest concentration of listings?

Are reviews and ratings useful predictive signals?
```

Visualization was used not only for presentation, but also to guide feature selection and modelling decisions.

---

## 3. Data Preprocessing

Real-world datasets contain problems that can significantly affect model performance.

The preprocessing pipeline included:

* Handling missing values
* Removing/handling irrelevant columns
* Encoding categorical variables
* Processing numerical features
* Detecting potential outliers
* Preparing the target variable
* Splitting data into training and testing sets

The objective was to create a clean and reproducible dataset for model training.

---

## 4. Feature Engineering

One of the most important parts of the project was determining which information should actually be given to the model.

Instead of treating every column equally, I examined the available features and considered their relevance to the prediction problem.

The resulting feature set was designed to capture different dimensions of a listing:

```text
Location
   +
Property Characteristics
   +
Host Information
   +
Pricing
   +
Review Activity
   +
Availability
```

This provided the model with multiple signals from which to learn the underlying patterns.

---

# 🤖 Model Development

I experimented with machine learning classification techniques to determine which approach was most appropriate for the dataset.

The modelling process followed:

```text
Baseline Model
      ↓
Train / Validation
      ↓
Evaluate
      ↓
Analyze Errors
      ↓
Improve Features / Model
      ↓
Final Evaluation
```

Rather than focusing only on accuracy, I evaluated the model using multiple classification metrics.

---

# 📊 Model Evaluation

The model was evaluated using metrics such as:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

For a multiclass classification problem, the confusion matrix was particularly useful because it showed **which property types the model confused with each other**.

This helped move the project beyond:

> "The model achieved X% accuracy."

and toward:

> "Why is the model making these predictions?"

---

# 🔎 What I Learned

This project taught me that the difficult part of machine learning is often **not training the model**.

The more interesting challenges appeared earlier in the pipeline:

### Data quality matters

A model cannot compensate for poorly understood or incorrectly processed data.

### Feature engineering matters

The information given to the model strongly influences what patterns it can learn.

### Accuracy is not enough

A single metric can hide poor performance on minority classes.

### Real-world datasets are messy

Missing values, categorical variables, outliers, and class imbalance are normal parts of practical ML.

### ML is an iterative process

The workflow is not:

```text
Dataset → Model → Accuracy
```

It is closer to:

```text
Question
   ↓
Data
   ↓
Understanding
   ↓
Cleaning
   ↓
Features
   ↓
Baseline
   ↓
Evaluation
   ↓
Iteration
   ↓
Model
```

---

# 🚀 What I'd Build Next

This project started as an experiment to understand the machine learning side of an Airbnb-like platform.

The natural next step would be to turn the classifier into a small end-to-end application.

Possible extensions include:

### 🌐 Prediction API

Expose the trained model through a REST API using **FastAPI**.

```text
Frontend
   ↓
FastAPI
   ↓
ML Model
   ↓
House Type Prediction
```

### 🖥️ Interactive Web Application

Allow a user to enter property characteristics and receive a predicted property type.

### 📦 Model Deployment

Containerize the application using Docker and deploy it to a cloud environment.

### 📈 Better Modelling

Experiment with:

* Hyperparameter optimization
* Ensemble methods
* Feature importance
* Cross-validation
* Handling class imbalance
* More advanced classification algorithms

### 🔍 Explainability

Add model explainability so that users can understand:

> **Why did the model classify this property this way?**

This would make the system much closer to a real ML product rather than simply a trained notebook model.

---

# 📁 Project Structure

```text
NYC-House-Type-Classification/
│
├── data/
│   └── dataset.csv
│
├── notebooks/
│   └── house_type_classification.ipynb
│
├── src/
│   ├── preprocessing.py
│   ├── features.py
│   └── model.py
│
├── models/
│   └── model.pkl
│
├── requirements.txt
│
└── README.md
```
