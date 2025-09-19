# MediCost – Advanced Medical Insurance Cost Prediction System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Table of Contents
- [Project Overview](#-project-overview)
- [The Challenge](#-the-challenge)
- [The Vision](#-the-vision)
- [The Data](#-the-data)
- [Machine Learning Models](#-machine-learning-models)
- [Tools & Libraries](#️-tools--libraries)
- [Key Insights](#-key-insights)
- [Repository Structure](#-repository-structure)
- [Usage Example](#-usage-example)
- [Personal Challenges](#-personal-challenges)
- [The Future](#-the-future)
- [Author](#-author)

---

## Project Overview
**Bringing Transparency and Smarter Pricing to Healthcare**

Every year, millions of Americans face unexpected medical bills and rising insurance costs. Healthcare costs rise 3-5% annually, with 1 in 4 Americans experiencing surprise medical expenses. Insurance premiums have jumped 60% in the last decade, while the $2.1T healthcare market loses billions from poor cost prediction.

This project develops **MediCost**, an intelligent machine learning system that predicts medical insurance costs with 89.6% accuracy, providing transparency and fair pricing for healthcare consumers.

**Mission**: *"Predict. Plan. Save: Know Before You Owe."*

---

## The Challenge
The current healthcare system faces critical issues:

- Healthcare costs rise 3–5% every year in the US
- 1 in 4 Americans faces unexpected medical bills
- Insurance premiums have jumped 60% in the last decade
- $2.1T market loses billions from poor cost prediction
- Traditional models misprice premiums for millions

**So, how do we fix a broken system...?**
This is where MediCost comes in!

---

## The Vision
**PERSONALIZED, FAIR HEALTHCARE COSTS**  
No more one-size-fits-all premiums.

**SMARTER INSURANCE SYSTEMS**  
Reducing billion-dollar losses from mispricing.

**GREATER TRANSPARENCY**  
Patients know what to expect before the bill arrives.

**SCALABLE AI SOLUTION**  
A foundation for future healthcare innovations (risk prevention, resource planning).

---

## The Data
**CLEAN DATASET**
- 1,338 insurance records, zero missing values, no duplicates
- Right-skewed target: charges range $1K-$64K (mean $13K)

**KEY FINDINGS**
- Smokers show strongest correlation with high insurance costs
- BMI and age demonstrate moderate positive correlations with charges

**FEATURE ENGINEERING**
- Created 10+ new features: age groups, BMI categories, risk scores
- Built interaction features (smoker×age, age×BMI) for better predictions

**PREPROCESSING COMPLETE**
- Applied outlier detection (kept valid medical outliers)
- Encoded all categorical variables, final dataset ready for modeling

---

## Machine Learning Models
**DATA PREPROCESSING**
- Encoded categorical variables (sex, smoker, region) using label encoding
- Created engineered features: BMI categories and age groups
- Prepared clean dataset for machine learning models

**MODEL SELECTION**
- Trained 3 algorithms: Linear Regression, Random Forest, Gradient Boosting
- Used 80/20 train-test split with standardized features
- Applied hyperparameter tuning (n_estimators=100, optimized depth/learning rates)

**PERFORMANCE COMPARISON**
- Evaluated using R², RMSE, and MAE metrics
- Random Forest achieved highest accuracy: 89.6% R² score
- Controlled overfitting through validation and regularization

**FEATURE IMPORTANCE**
- Identified top predictors driving insurance costs
- Smoker status likely emerged as strongest predictor
- Age, BMI, and engineered features showed significant impact

**DEPLOYMENT READY**
- Built prediction function for new customer quotes
- Model validates with mean error of $383.40 on test data
- Ready for real-world insurance cost estimation!

---

## Tools & Libraries
- **Python** (Jupyter Notebook environment)
- `pandas`, `numpy` → data manipulation and analysis
- `matplotlib`, `seaborn` → static visualizations
- `plotly` → interactive charts and correlation matrices
- `scikit-learn` → machine learning algorithms and preprocessing
- `scipy` → statistical analysis and distributions
- `xgboost`, `lightgbm` → advanced gradient boosting models

---

## Key Insights
**Top Risk Factors Identified:**
- **Smoking Status** → Increases costs by ~250% (strongest predictor)
- **Age** → Linear correlation with charges
- **BMI** → Obesity significantly impacts costs
- **Region** → Geographic cost variations
- **Children** → Family size effect on premiums

**Cost Distribution Analysis:**
- Mean Cost: $13,270
- Median Cost: $9,382
- Standard Deviation: $12,110
- Skewness: 1.51 (right-skewed distribution)

**Model Performance:**
- Best Model: Random Forest with 89.6% accuracy
- RMSE: $4,891 (average prediction error)
- MAE: $2,647 (mean absolute error)

---

## Repository Structure
```bash
medicost/
│
├── data/
│   ├── insurance.csv              # Raw dataset
│   └── processed/
│       ├── insurance_processed.csv # Cleaned data
│       └── feature_info.json      # Feature metadata
│
├── models/
│   ├── insurance_model.pkl        # Trained model
│   ├── scaler.pkl                # Feature scaler
│   └── encoders.pkl              # Label encoders
│
├── notebooks/
│   ├── data_exploration.py        # EDA & preprocessing
│   └── ml_models.py              # Model training & evaluation
│
├── requirements.txt               # Project dependencies
├── LICENSE                       # Project license
└── README.md                     # Project documentation
```

---

## Usage Example
```python
# Load the trained model
from medicost import predict_insurance_cost

# Predict for a new customer
cost = predict_insurance_cost(
    age=35,
    sex='female',
    bmi=25.0,
    children=1,
    smoker='no',
    region='northwest'
)

print(f"Predicted insurance cost: ${cost:.2f}")
# Output: Predicted insurance cost: $8,947.23
```

**Example Predictions:**

| Profile | Age | BMI | Smoker | Predicted Cost |
|---------|-----|-----|--------|----------------|
| Young Non-Smoker | 25 | 22.0 | No | $3,247 |
| Middle-aged Smoker | 45 | 30.0 | Yes | $28,456 |
| Average Case | 35 | 25.0 | No | $8,947 |

---

## Personal Challenges
**EDA Complexity**  
Handling mixed data types in correlation analysis - solved with proper categorical encoding

**Model Selection & Tuning**  
Comparing 3 algorithms with hyperparameter optimization - used systematic metrics for selection

**LLM Integration Failure**  
API configuration errors prevented recommendation chatbot - documented approach for future work

**Time Management**  
Balancing thorough EDA, model training, and LLM integration in limited time - prioritized core pipeline

---

## The Future
**LLM-POWERED RECOMMENDATION ENGINE**
- Natural language insurance advisor chatbot
- Automated policy comparison with plain-English explanations
- Real-time integration with insurance company APIs

**ADVANCED FEATURES**
- Interactive risk profiling dashboard
- Geographic cost analysis and heatmaps
- Mobile app with document scanning
- Voice interface for hands-free input

**BUSINESS APPLICATIONS**
- Insurance company pricing optimization tools
- Broker decision support system
- Claims prediction modeling
- Regulatory compliance monitoring

**TECHNICAL IMPROVEMENTS**
- Real-time model updates with new data
- Multi-modal data integration (wearables, medical records)
- Enterprise API for scalable deployment
- Alternative data sources (lifestyle, environmental factors)

---

## Author

**Katherine Torian**  
*Advanced Medical Insurance Cost Prediction System*

**Find me online:**
- [LinkedIn](https://www.linkedin.com/in/katherine-torian)
- [GitHub](https://www.github.com/kathtorian)

---

*Making insurance costs predictable, not painful*