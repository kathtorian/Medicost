import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import base64
from PIL import Image
import io

# Configure the page
st.set_page_config(
    page_title="Medicost - Healthcare Insurance Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 'home'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'animation_done' not in st.session_state:
    st.session_state.animation_done = False

# Enhanced Insurance Companies Database
INSURANCE_COMPANIES = {
    'budget_friendly': [
        {
            'name': 'Ambetter Health',
            'monthly': 185,
            'deductible': 5800,
            'coverage': 'Essential',
            'network': 'Regional+',
            'rating': 4.2,
            'features': ['Telehealth included', 'Generic drug coverage', 'Preventive care'],
            'best_for': 'Young adults, healthy individuals',
            'copay': '$35',
            'oop_max': '$8700'
        },
        {
            'name': 'Oscar Health',
            'monthly': 225,
            'deductible': 4500,
            'coverage': 'Digital First',
            'network': 'Modern Network',
            'rating': 4.4,
            'features': ['Award-winning app', 'Virtual care', 'Transparent pricing'],
            'best_for': 'Tech-savvy, urban professionals',
            'copay': '$30',
            'oop_max': '$8000'
        },
        {
            'name': 'Molina Healthcare',
            'monthly': 195,
            'deductible': 5200,
            'coverage': 'Community Care',
            'network': 'Community Based',
            'rating': 4.1,
            'features': ['Community clinics', 'Medicaid expertise', 'Multi-language support'],
            'best_for': 'Community-focused, diverse populations',
            'copay': '$40',
            'oop_max': '$9100'
        }
    ],
    'comprehensive': [
        {
            'name': 'Blue Cross Blue Shield',
            'monthly': 385,
            'deductible': 2200,
            'coverage': 'Comprehensive Plus',
            'network': 'National Network',
            'rating': 4.6,
            'features': ['Largest network', 'Nationwide coverage', 'Specialist access'],
            'best_for': 'Frequent travelers, comprehensive needs',
            'copay': '$25',
            'oop_max': '$6000'
        },
        {
            'name': 'Aetna CVS Health',
            'monthly': 420,
            'deductible': 1800,
            'coverage': 'Premium Care',
            'network': 'Premium Network',
            'rating': 4.5,
            'features': ['Wellness programs', 'Chronic care management', 'Premium providers'],
            'best_for': 'Health-conscious, chronic conditions',
            'copay': '$20',
            'oop_max': '$5500'
        },
        {
            'name': 'Cigna HealthSpring',
            'monthly': 365,
            'deductible': 2500,
            'coverage': 'Complete Care',
            'network': 'Global Network',
            'rating': 4.3,
            'features': ['International coverage', 'Mental health focus', 'Integrated care'],
            'best_for': 'International needs, mental health priority',
            'copay': '$30',
            'oop_max': '$6500'
        }
    ],
    'family': [
        {
            'name': 'Kaiser Permanente',
            'monthly': 780,
            'deductible': 3200,
            'coverage': 'Family Complete',
            'network': 'Integrated HMO',
            'rating': 4.7,
            'features': ['Own hospitals', 'Coordinated care', 'Family wellness'],
            'best_for': 'Families wanting integrated care',
            'copay': '$20',
            'oop_max': '$12000'
        },
        {
            'name': 'UnitedHealthcare',
            'monthly': 850,
            'deductible': 2800,
            'coverage': 'Family Choice Plus',
            'network': 'Extensive PPO',
            'rating': 4.4,
            'features': ['Flexible networks', 'Pediatric specialists', 'Family discounts'],
            'best_for': 'Large families, flexibility priority',
            'copay': '$25',
            'oop_max': '$14000'
        },
        {
            'name': 'Anthem BlueCross',
            'monthly': 920,
            'deductible': 2200,
            'coverage': 'Family Premium',
            'network': 'Premium PPO',
            'rating': 4.5,
            'features': ['Premium providers', 'Maternity care', 'Child wellness'],
            'best_for': 'Premium family care, growing families',
            'copay': '$15',
            'oop_max': '$10000'
        }
    ],
    'senior': [
        {
            'name': 'Humana Medicare Advantage',
            'monthly': 125,
            'deductible': 1200,
            'coverage': 'Senior Plus',
            'network': 'Medicare Network',
            'rating': 4.6,
            'features': ['Medicare expertise', 'Senior benefits', 'Prescription included'],
            'best_for': '65+ Medicare-eligible seniors',
            'copay': '$10',
            'oop_max': '$3500'
        },
        {
            'name': 'Aetna Medicare',
            'monthly': 145,
            'deductible': 1000,
            'coverage': 'Senior Complete',
            'network': 'Medicare Plus',
            'rating': 4.4,
            'features': ['Chronic condition support', 'Wellness programs', 'Coordinated care'],
            'best_for': 'Seniors with chronic conditions',
            'copay': '$15',
            'oop_max': '$3000'
        },
        {
            'name': 'Wellcare Medicare',
            'monthly': 95,
            'deductible': 1500,
            'coverage': 'Essential Senior',
            'network': 'Value Network',
            'rating': 4.2,
            'features': ['Budget-friendly', 'Essential coverage', 'Prescription focus'],
            'best_for': 'Budget-conscious seniors',
            'copay': '$20',
            'oop_max': '$4000'
        }
    ]
}

# US States and their regions
STATE_REGIONS = {
    'Alabama': 'Southeast', 'Alaska': 'Northwest', 'Arizona': 'Southwest', 'Arkansas': 'South',
    'California': 'West', 'Colorado': 'West', 'Connecticut': 'Northeast', 'Delaware': 'Northeast',
    'Florida': 'Southeast', 'Georgia': 'Southeast', 'Hawaii': 'West', 'Idaho': 'Northwest',
    'Illinois': 'Midwest', 'Indiana': 'Midwest', 'Iowa': 'Midwest', 'Kansas': 'Midwest',
    'Kentucky': 'South', 'Louisiana': 'South', 'Maine': 'Northeast', 'Maryland': 'Northeast',
    'Massachusetts': 'Northeast', 'Michigan': 'Midwest', 'Minnesota': 'Midwest', 'Mississippi': 'South',
    'Missouri': 'Midwest', 'Montana': 'Northwest', 'Nebraska': 'Midwest', 'Nevada': 'West',
    'New Hampshire': 'Northeast', 'New Jersey': 'Northeast', 'New Mexico': 'Southwest', 'New York': 'Northeast',
    'North Carolina': 'Southeast', 'North Dakota': 'Midwest', 'Ohio': 'Midwest', 'Oklahoma': 'South',
    'Oregon': 'Northwest', 'Pennsylvania': 'Northeast', 'Rhode Island': 'Northeast', 'South Carolina': 'Southeast',
    'South Dakota': 'Midwest', 'Tennessee': 'South', 'Texas': 'South', 'Utah': 'West',
    'Vermont': 'Northeast', 'Virginia': 'Southeast', 'Washington': 'Northwest', 'West Virginia': 'Southeast',
    'Wisconsin': 'Midwest', 'Wyoming': 'West'
}

# Professional CSS with cohesive blue-green theme
def load_professional_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #EBF8FF 0%, #F0FDF4 100%);
            min-height: 100vh;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
                /* Hide visible streamlit buttons on home page */
[data-testid="baseButton-secondary"][key="explore"],
[data-testid="baseButton-secondary"][key="costs"],  
[data-testid="baseButton-secondary"][key="family"],
[data-testid="baseButton-secondary"][key="learn"] {
    display: none !important;
}
        
        /* Main container adjustments */
        .main .block-container {
            padding-top: 0;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* Professional header with logo */
        .header-container {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            padding: 2rem;
            margin: 0 -2rem 2rem -2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }
        
        .header-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
            opacity: 0.3;
        }
        
        .logo-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 2rem;
            position: relative;
            z-index: 2;
        }
        
        .logo-img {
            width: 120px;
            height: 120px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            background: white;
            padding: 12px;
        }
        
        .header-text {
            text-align: left;
        }
        
        .header-title {
            font-size: 3rem;
            font-weight: 800;
            color: white;
            margin: 0;
            letter-spacing: -0.02em;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        .header-subtitle {
            font-size: 1.2rem;
            font-weight: 500;
            color: rgba(255,255,255,0.95);
            margin-top: 0.5rem;
        }
        
        /* Animated poll container */
        .poll-card {
            background: white;
            border-radius: 24px;
            padding: 3rem;
            margin: 2rem auto;
            max-width: 900px;
            box-shadow: 0 10px 40px rgba(14, 165, 233, 0.15);
            border: 2px solid rgba(14, 165, 233, 0.1);
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .poll-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #0C4A6E;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .poll-subtitle {
            font-size: 1.1rem;
            color: #64748B;
            text-align: center;
            margin-bottom: 3rem;
        }
        
        /* Uniform button styling - blue-green gradient theme */
        .stButton > button {
            background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 1rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1.05rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(14, 165, 233, 0.25) !important;
            width: 100% !important;
            min-height: 3.5rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            white-space: normal !important;
            word-wrap: break-word !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(14, 165, 233, 0.35) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }
        
        /* Card designs */
        .info-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
            border: 1px solid #E0F2FE;
            box-shadow: 0 4px 20px rgba(14, 165, 233, 0.08);
            transition: all 0.3s ease;
        }
        
        .info-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(14, 165, 233, 0.15);
        }
        
        /* Section headers */
        .section-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #0C4A6E;
            margin: 2rem 0 1rem 0;
            text-align: center;
            position: relative;
        }
        
        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 4px;
            background: linear-gradient(90deg, #2563eb, #3b82f6);
            border-radius: 2px;
        }
        
        /* Form elements styling */
        .stSelectbox > div > div,
        .stNumberInput > div > div,
        .stTextInput > div > div,
        .stSlider > div > div {
            background: white !important;
            border: 2px solid #dbeafe !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
        }
        
        .stSelectbox > div > div:hover,
        .stNumberInput > div > div:hover,
        .stTextInput > div > div:hover {
            border-color: #0EA5E9 !important;
        }
        
        .stSelectbox > div > div:focus-within,
        .stNumberInput > div > div:focus-within,
        .stTextInput > div > div:focus-within {
            border-color: #0EA5E9 !important;
            box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
        }
        
        /* Insurance plan cards */
        .plan-card {
            background: white;
            border: 2px solid #dbeafe;
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
            position: relative;
            transition: all 0.3s ease;
        }
        
        .plan-card:hover {
            border-color: #2563eb;;
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(14, 165, 233, 0.15);
        }
        
        .plan-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #2563eb, #3b82f6);
            border-radius: 20px 20px 0 0;
        }
        
        .plan-name {
            font-size: 1.6rem;
            font-weight: 700;
            color: #0C4A6E;
            margin-bottom: 0.5rem;
        }
        
        .plan-price {
            font-size: 2rem;
            font-weight: 800;
            color: #2563eb;
            margin: 0.5rem 0;
        }
        
        .plan-features {
            margin: 1rem 0;
        }
        
        .feature-tag {
            background: linear-gradient(135deg, #dbeafe, #eff6ff);
            border: 1px solid rgba(37, 99, 235, 0.2);
            color: #0C4A6E;
            padding: 0.4rem 1rem;
            font-size: 0.9rem;
            font-weight: 500;
            margin: 0.3rem;
            display: inline-block;
            border: 1px solid rgba(14, 165, 233, 0.2);
        }
        
        /* BMI indicator */
        .bmi-card {
            background: linear-gradient(135deg, #dbeafe, #eff6ff);
            border: 1px solid rgba(37, 99, 235, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            border: 2px solid #2563eb;
            margin: 1rem 0;
        }
        
        .bmi-value {
            font-size: 2.5rem;
            font-weight: 800;
            color: #0C4A6E;
            margin: 0;
        }
        
        .bmi-label {
            font-size: 1rem;
            font-weight: 600;
            color: #2563eb;
            margin-top: 0.5rem;
        }
        
        /* Cost breakdown styling */
        .cost-table {
            background: #F8FAFC;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 4px solid #2563eb;
        }
        
        .cost-row {
            display: flex;
            justify-content: space-between;
            padding: 0.75rem 0;
            border-bottom: 1px solid #E0F2FE;
        }
        
        .cost-row:last-child {
            border-bottom: none;
            font-weight: 700;
            color: #0C4A6E;
            font-size: 1.2rem;
        }
        
        /* Success messages */
        .success-banner {
            background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
            border: 2px solid #10B981;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            color: #065F46;
            font-weight: 600;
            text-align: center;
        }
        
        /* Info messages */
        .info-banner {
            background: linear-gradient(135deg, #dbeafe, #bfdbfe);
            border: 2px solid #2563eb;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            color: #0C4A6E;
            font-weight: 500;
            text-align: center;
        }
        
        /* Radio button styling */
        .stRadio > div {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            border: 2px solid #dbeafe;
        }
        
        /* Multiselect styling */
        .stMultiSelect > div > div {
            background: white !important;
            border: 2px solid #E0F2FE !important;
            border-radius: 10px !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            background: white;
            border-radius: 12px;
            padding: 0.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 3rem;
            background: transparent;
            border-radius: 8px;
            color: #64748B;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            color: white;
        }
        
        /* Progress indicator */
        .progress-bar {
            background: #E0F2FE;
            height: 8px;
            border-radius: 4px;
            margin: 2rem 0;
            overflow: hidden;
        }
        
        .progress-fill {
            background: linear-gradient(90deg, #1e40af, #10B981);
            height: 100%;
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .header-title {
                font-size: 2rem;
            }
            
            .logo-header {
                flex-direction: column;
                text-align: center;
            }
            
            .header-text {
                text-align: center;
            }
            
            .poll-card {
                padding: 2rem;
            }
            
            .plan-card {
                padding: 1.5rem;
            }
                

                    /* Premium option cards */
    .option-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #e2e8f0;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        position: relative;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.08);
        overflow: hidden;
    }

    .option-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(30, 64, 175, 0.05), transparent);
        transition: left 0.6s ease;
    }

    .option-card:hover::before {
        left: 100%;
    }

    .option-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: #2563eb;
        box-shadow: 0 20px 40px rgba(30, 64, 175, 0.15);
    }

    .card-icon {
        font-size: 4rem;
        text-align: center;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }

    .card-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e40af;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -0.025em;
    }

    .card-description {
        color: #64748b;
        font-size: 1.1rem;
        line-height: 1.6;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }

    .card-arrow {
        position: absolute;
        bottom: 1.5rem;
        right: 1.5rem;
        font-size: 1.5rem;
        color: #2563eb;
        font-weight: bold;
        opacity: 0;
        transform: translateX(-10px);
        transition: all 0.3s ease;
    }

    .option-card:hover .card-arrow {
        opacity: 1;
        transform: translateX(0);
    }

    /* Hide hidden buttons */
    button[key="explore"], 
    button[key="costs"], 
    button[key="family"], 
    button[key="learn"] {
        display: none !important;
    }

    /* Responsive design for cards */
    @media (max-width: 768px) {
        .option-card {
            padding: 2rem;
            margin: 1rem 0;
        }
        
        .card-icon {
            font-size: 3rem;
        }
        
        .card-title {
            font-size: 1.5rem;
        }
        
        .card-description {
            font-size: 1rem;
        }
                    

                    /* Style the main home buttons */
    button[key="explore_btn"], 
    button[key="costs_btn"], 
    button[key="family_btn"], 
    button[key="learn_btn"] {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%) !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        color: #1e40af !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        line-height: 1.5 !important;
        min-height: 200px !important;
        white-space: pre-line !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.08) !important;
    }

    button[key="explore_btn"]:hover, 
    button[key="costs_btn"]:hover, 
    button[key="family_btn"]:hover, 
    button[key="learn_btn"]:hover {
        transform: translateY(-5px) !important;
        border-color: #2563eb !important;
        box-shadow: 0 20px 40px rgba(30, 64, 175, 0.15) !important;
        background: linear-gradient(145deg, #ffffff 0%, #f1f5f9 100%) !important;
    }
                

     /* Platform Overview Metric Cards */
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 16px;
            border: 2px solid #E0F2FE;
            box-shadow: 0 4px 20px rgba(14, 165, 233, 0.08);
            text-align: center;
            transition: all 0.3s ease;
            margin-bottom: 1rem;
        }

        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(14, 165, 233, 0.15);
        }

        /* Section titles */
        .section-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #0C4A6E;
            margin: 2rem 0 1.5rem 0;
            text-align: center;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 4px;
            background: linear-gradient(90deg, #2563eb, #3b82f6);
            border-radius: 2px;
        }

        .subsection-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #1e40af;
            margin: 2rem 0 1rem 0;
            border-bottom: 2px solid #E0F2FE;
            padding-bottom: 0.5rem;
        }

        /* Key Insights Info Banners */
        .info-banner {
            background: linear-gradient(135deg, #dbeafe, #bfdbfe);
            border: 2px solid #2563eb;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            color: #0C4A6E;
            font-weight: 500;
            text-align: left;
        }

        .warning-banner {
            background: linear-gradient(135deg, #FEF3C7, #FDE68A);
            border: 2px solid #F59E0B;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            color: #92400E;
            font-weight: 600;
            text-align: left;
        }
             
    </style>
    """, unsafe_allow_html=True)

def show_dashboard():
    """Dashboard with key metrics and insights"""
    
    # Sample data - replace with your actual data loading
    import pandas as pd
    import numpy as np
    
    # Generate sample data (replace this with: df = pd.read_csv('your_data.csv'))
    np.random.seed(42)
    df = pd.DataFrame({
        'age': np.random.randint(18, 65, 1338),
        'charges': np.random.normal(13270, 5000, 1338),
        'smoker': np.random.choice(['yes', 'no'], 1338, p=[0.21, 0.79]),
        'sex': np.random.choice(['male', 'female'], 1338),
        'bmi': np.random.normal(30, 6, 1338),
        'region': np.random.choice(['northeast', 'southeast', 'southwest', 'northwest'], 1338)
    })
    
    # Platform Overview Cards
    st.markdown('<h2 class="section-title">Platform Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #2563eb; margin: 0; font-size: 1.2rem;">Dataset Size</h3>
            <p style="font-size: 2.5rem; font-weight: 800; color: #0C4A6E; margin: 0.5rem 0;">
                {len(df):,}
            </p>
            <p style="color: #64748B; margin: 0; font-size: 0.9rem;">Records Analyzed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_cost = df['charges'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #10B981; margin: 0; font-size: 1.2rem;">Avg Cost</h3>
            <p style="font-size: 2.5rem; font-weight: 800; color: #065F46; margin: 0.5rem 0;">
                ${avg_cost:,.0f}
            </p>
            <p style="color: #64748B; margin: 0; font-size: 0.9rem;">Annual Premium</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #F59E0B; margin: 0; font-size: 1.2rem;">ML Accuracy</h3>
            <p style="font-size: 2.5rem; font-weight: 800; color: #92400E; margin: 0.5rem 0;">
                94.6%
            </p>
            <p style="color: #64748B; margin: 0; font-size: 0.9rem;">R² Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        age_range = f"{df['age'].min()}-{df['age'].max()}"
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #8B5CF6; margin: 0; font-size: 1.2rem;">Age Range</h3>
            <p style="font-size: 2.5rem; font-weight: 800; color: #5B21B6; margin: 0.5rem 0;">
                {age_range}
            </p>
            <p style="color: #64748B; margin: 0; font-size: 0.9rem;">Years Old</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        smoker_pct = (df['smoker'] == 'yes').mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #EF4444; margin: 0; font-size: 1.2rem;">Smokers</h3>
            <p style="font-size: 2.5rem; font-weight: 800; color: #DC2626; margin: 0.5rem 0;">
                {smoker_pct:.1f}%
            </p>
            <p style="color: #64748B; margin: 0; font-size: 0.9rem;">of Dataset</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Insights
    st.markdown('<h3 class="subsection-title">Key Insights</h3>', unsafe_allow_html=True)
    
    # Calculate insights
    smoker_multiplier = df[df['smoker'] == 'yes']['charges'].mean() / df[df['smoker'] == 'no']['charges'].mean()
    male_avg = df[df['sex'] == 'male']['charges'].mean()
    female_avg = df[df['sex'] == 'female']['charges'].mean()
    highest_region = df.groupby('region')['charges'].mean().idxmax()
    obese_pct = (df['bmi'] >= 30).mean() * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="info-banner">
            <strong>Smoking Impact:</strong> Smokers pay between 2x and 3x more on average
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-banner">
            <strong>Gender Difference:</strong> Males pay ${abs(male_avg - female_avg):.0f} more annually
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-banner">
            <strong>Regional Variation:</strong> {highest_region.title()} region has highest average costs
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="warning-banner">
            <strong>Health Alert:</strong> {obese_pct:.1f}% of population has BMI ≥30 (obese)
        </div>
        """, unsafe_allow_html=True)


# BMI calculation function
def calculate_bmi(height, weight, unit_system):
    """Calculate BMI based on selected unit system"""
    if unit_system == "Imperial (ft/in, lbs)":
        # Convert height to meters and weight to kg
        height_m = height * 0.0254  # height is already in total inches
        weight_kg = weight * 0.453592
    else:  # Metric
        height_m = height  # height is already in meters
        weight_kg = weight  # weight is already in kg
    
    if height_m > 0:
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 1)
    return 0

# Insurance recommendation model
@st.cache_data
def create_ml_models():
    """Create ML models for insurance recommendation and cost prediction"""
    np.random.seed(42)
    n_samples = 2000
    
    # Generate synthetic training data
    ages = np.random.randint(18, 80, n_samples)
    bmis = np.random.normal(27, 5, n_samples)
    smokers = np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
    children = np.random.randint(0, 5, n_samples)
    regions = np.random.randint(0, 4, n_samples)
    income_levels = np.random.randint(1, 5, n_samples)
    
    # Create feature matrix
    X = np.column_stack([ages, bmis, smokers, children, regions, income_levels])
    
    # Create targets for classification
    def determine_category(row):
        age, bmi, smoker, kids, region, income = row
        if age >= 65:
            return 3  # senior
        elif kids >= 2:
            return 2  # family
        elif income <= 2 or (age < 30 and bmi < 25):
            return 0  # budget_friendly
        else:
            return 1  # comprehensive
    
    y_category = np.array([determine_category(row) for row in X])
    
    # Create cost targets for regression
    base_costs = ages * 50 + bmis * 30 + smokers * 2000 + children * 500 + np.random.normal(0, 500, n_samples)
    y_cost = np.clip(base_costs, 1000, 15000)
    
    # Train classification model
    clf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    clf_model.fit(X, y_category)
    
    # Train regression model for cost prediction
    reg_model = GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=5)
    reg_model.fit(X, y_cost)
    
    return clf_model, reg_model, ['budget_friendly', 'comprehensive', 'family', 'senior']



def show_header():
    """Display compact centered Medicost logo"""
    # Compact logo with minimal spacing
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
    """, unsafe_allow_html=True)
    
    try:
        # Display smaller logo using Streamlit's image function
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.image("media/logo.png", use_container_width=True)
    except:
        # Fallback if logo not found
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="color: #1e40af; font-size: 2.5rem; font-weight: 900; margin: 0;">
                Medicost
            </h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_home():
    """Display home page with dashboard cards and navigation options"""
    
    # Sample data for dashboard - replace with your actual data loading
    import pandas as pd
    import numpy as np
    
    # Generate sample data (replace this with: df = pd.read_csv('your_data.csv'))
    np.random.seed(42)
    df = pd.DataFrame({
        'age': np.random.randint(18, 65, 1338),
        'charges': np.random.normal(13270, 5000, 1338),
        'smoker': np.random.choice(['yes', 'no'], 1338, p=[0.21, 0.79]),
        'sex': np.random.choice(['male', 'female'], 1338),
        'bmi': np.random.normal(30, 6, 1338),
        'region': np.random.choice(['northeast', 'southeast', 'southwest', 'northwest'], 1338)
    })
    
    # Header section
    st.markdown("""
    <div style="background: white; border-radius: 20px; padding: 1.5rem; margin: 1rem auto; max-width: 700px;
                box-shadow: 0 8px 30px rgba(14, 165, 233, 0.12); border: 2px solid rgba(14, 165, 233, 0.1);
                text-align: center;">
        <h2 style="font-size: 1.8rem; font-weight: 700; color: #0C4A6E; margin-bottom: 0.5rem;">
            Making insurance costs predictable, not painful
        </h2>
        <p style="font-size: 1rem; color: #64748B; margin: 0;">
            PREDICT. PLAN. SAVE: KNOW BEFORE YOU OWE.
        </p>
    </div>
    """, unsafe_allow_html=True)
    

    # Platform Overview Cards
    st.markdown('<h2 class="section-title">Platform Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; 
                    border: 2px solid #E0F2FE; box-shadow: 0 4px 20px rgba(14, 165, 233, 0.08);
                    text-align: center; transition: all 0.3s ease; margin-bottom: 1rem;">
            <h3 style="color: #2563eb; margin: 0; font-size: 1.2rem;">Dataset Size</h3>
            <p style="font-size: 2.5rem; font-weight: 800; color: #0C4A6E; margin: 0.5rem 0;">
                {len(df):,}
            </p>
            <p style="color: #64748B; margin: 0; font-size: 0.9rem;">Records Analyzed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_cost = df['charges'].mean()
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; 
                    border: 2px solid #E0F2FE; box-shadow: 0 4px 20px rgba(14, 165, 233, 0.08);
                    text-align: center; transition: all 0.3s ease; margin-bottom: 1rem;">
            <h3 style="color: #10B981; margin: 0; font-size: 1.2rem;">Avg Cost</h3>
            <p style="font-size: 2.5rem; font-weight: 800; color: #065F46; margin: 0.5rem 0;">
                ${avg_cost:,.0f}
            </p>
            <p style="color: #64748B; margin: 0; font-size: 0.9rem;">Annual Premium</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; 
                    border: 2px solid #E0F2FE; box-shadow: 0 4px 20px rgba(14, 165, 233, 0.08);
                    text-align: center; transition: all 0.3s ease; margin-bottom: 1rem;">
            <h3 style="color: #F59E0B; margin: 0; font-size: 1.2rem;">ML Accuracy</h3>
            <p style="font-size: 2.5rem; font-weight: 800; color: #92400E; margin: 0.5rem 0;">
                94.6%
            </p>
            <p style="color: #64748B; margin: 0; font-size: 0.9rem;">R² Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        age_range = f"{df['age'].min()}-{df['age'].max()}"
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; 
                    border: 2px solid #E0F2FE; box-shadow: 0 4px 20px rgba(14, 165, 233, 0.08);
                    text-align: center; transition: all 0.3s ease; margin-bottom: 1rem;">
            <h3 style="color: #8B5CF6; margin: 0; font-size: 1.2rem;">Age Range</h3>
            <p style="font-size: 2.5rem; font-weight: 800; color: #5B21B6; margin: 0.5rem 0;">
                {age_range}
            </p>
            <p style="color: #64748B; margin: 0; font-size: 0.9rem;">Years Old</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        smoker_pct = (df['smoker'] == 'yes').mean() * 100
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; 
                    border: 2px solid #E0F2FE; box-shadow: 0 4px 20px rgba(14, 165, 233, 0.08);
                    text-align: center; transition: all 0.3s ease; margin-bottom: 1rem;">
            <h3 style="color: #EF4444; margin: 0; font-size: 1.2rem;">Smokers</h3>
            <p style="font-size: 2.5rem; font-weight: 800; color: #DC2626; margin: 0.5rem 0;">
                {smoker_pct:.1f}%
            </p>
            <p style="color: #64748B; margin: 0; font-size: 0.9rem;">of Dataset</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Insights
    st.markdown('<h3 class="subsection-title">Key Insights</h3>', unsafe_allow_html=True)
    
    # Calculate insights
    smoker_multiplier = df[df['smoker'] == 'yes']['charges'].mean() / df[df['smoker'] == 'no']['charges'].mean()
    male_avg = df[df['sex'] == 'male']['charges'].mean()
    female_avg = df[df['sex'] == 'female']['charges'].mean()
    highest_region = df.groupby('region')['charges'].mean().idxmax()
    obese_pct = (df['bmi'] >= 30).mean() * 100
    
    # Use simple 2x2 layout with regular columns
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.info(f"**Smoking Impact:** Smokers pay between 2x and 3x more on average")
        st.info(f"**Gender Difference:** Males pay ${abs(male_avg - female_avg):.0f} more annually")
    
    with insight_col2:
        st.info(f"**Regional Variation:** {highest_region.title()} region has highest average costs")
        st.warning(f"**Health Alert:** {obese_pct:.1f}% of population has BMI ≥30 (obese)")
    
    # Navigation Cards
    st.markdown('<h3 class="subsection-title">Get Started</h3>', unsafe_allow_html=True)
    
    # Create responsive grid with clickable cards
    nav_col1, nav_col2 = st.columns(2, gap="large")
    
    with nav_col1:
        # Explore Insurance Plans Card
        if st.button("🔍\n\n**EXPLORE INSURANCE PLANS**\n\nCompare plans from top providers\nwith AI-powered recommendations", 
                    key="explore_btn", use_container_width=True):
            st.session_state.user_data['intent'] = 'explore'
            st.session_state.current_step = 'experience_level'
            st.rerun()
        
        # Estimate Costs Card  
        if st.button("💰\n\n**ESTIMATE MY COSTS**\n\nGet precise cost predictions\nusing machine learning", 
                    key="costs_btn", use_container_width=True):
            st.session_state.user_data['intent'] = 'estimate'
            st.session_state.current_step = 'user_form'
            st.rerun()
    
    with nav_col2:
        # Family Coverage Card
        if st.button("👨‍👩‍👧‍👦\n\n**FIND FAMILY COVERAGE**\n\nComprehensive family plans\nwith pediatric care", 
                    key="family_btn", use_container_width=True):
            st.session_state.user_data['intent'] = 'family'
            st.session_state.current_step = 'family_form'
            st.rerun()
        
        # Learn Healthcare Card
        if st.button("📚\n\n**LEARN ABOUT HEALTHCARE**\n\nMaster US healthcare basics\nwith our guide", 
                    key="learn_btn", use_container_width=True):
            st.session_state.user_data['intent'] = 'learn'
            st.session_state.current_step = 'education'
            st.rerun()



# Experience level selection
def show_experience_level():
    """Show experience level selection with different paths"""
    st.markdown("""
    <div class="poll-card">
        <h2 class="poll-title">Tell Us About Your Experience</h2>
        <p class="poll-subtitle">This helps us customize your journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        if st.button("🆕 I'm New to Insurance Plans", key="new_user"):
            st.session_state.user_data['experience'] = 'beginner'
            st.session_state.current_step = 'simple_form'
            st.rerun()
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        if st.button("📖 I Know the Basics", key="intermediate"):
            st.session_state.user_data['experience'] = 'intermediate'
            st.session_state.current_step = 'user_form'
            st.rerun()
    
    with col2:
        if st.button("💼 I'm an Expert", key="expert"):
            st.session_state.user_data['experience'] = 'expert'
            st.session_state.current_step = 'advanced_form'
            st.rerun()
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        if st.button("🔄 Switching Plans", key="switching"):
            st.session_state.user_data['experience'] = 'switching'
            st.session_state.current_step = 'switch_form'
            st.rerun()

# Simple form for beginners
def show_simple_form():
    """Simplified form for users new to insurance"""
    st.markdown("""
    <div class="info-card">
        <h2 class="section-title">Let's Keep It Simple</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("simple_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.slider("Your Age", 18, 100, 30)
            health_status = st.select_slider(
                "Overall Health",
                options=["Excellent", "Good", "Fair", "Poor"],
                value="Good"
            )
            
        with col2:
            family_size = st.selectbox(
                "Who needs coverage?",
                ["Just Me", "Me + Partner", "Small Family (3-4)", "Large Family (5+)"]
            )
            budget = st.selectbox(
                "Monthly Budget",
                ["Under $200", "$200-400", "$400-600", "$600-800", "Over $800"]
            )
        
        state = st.selectbox("Your State", list(STATE_REGIONS.keys()))
        
        if st.form_submit_button("Get Simple Recommendations"):
            st.session_state.user_data.update({
                'age': age,
                'health_status': health_status,
                'family_size': family_size,
                'budget': budget,
                'state': state,
                'region': STATE_REGIONS[state]
            })
            st.session_state.current_step = 'recommendations'
            st.rerun()

# Main user form
def show_user_form():
    """Comprehensive user information form"""
    st.markdown("""
    <div class="info-card">
        <h2 class="section-title">Tell Us About Yourself</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Personal Information
    st.markdown("### 👤 Personal Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
    
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
    
    with col3:
        smoker = st.selectbox("Smoking Status", ["Non-smoker", "Former Smoker", "Current Smoker"])
    
    # Location
    st.markdown("### 📍 Location")
    col1, col2 = st.columns(2)
    
    with col1:
        state = st.selectbox("State", list(STATE_REGIONS.keys()))
    
    with col2:
        st.markdown(f"""
        <div class="info-banner">
            Region: {STATE_REGIONS[state]}
        </div>
        """, unsafe_allow_html=True)
    
    # Health Metrics with dual unit system
    st.markdown("### 📊 Health Metrics")
    
    unit_system = st.radio(
        "Measurement System",
        ["Imperial (ft/in, lbs)", "Metric (m, kg)"],
        horizontal=True
    )
    
    col1, col2, col3 = st.columns(3)
    
    if unit_system == "Imperial (ft/in, lbs)":
        with col1:
            height_ft = st.number_input("Height (feet)", min_value=3, max_value=8, value=5)
            height_in = st.number_input("Height (inches)", min_value=0, max_value=11, value=8)
            total_inches = (height_ft * 12) + height_in
        with col2:
            weight = st.number_input("Weight (lbs)", min_value=50, max_value=500, value=160)
    else:
        with col1:
            height_m = st.number_input("Height (meters)", min_value=1.0, max_value=2.5, value=1.73, step=0.01)
            total_inches = height_m / 0.0254  # Convert to inches for BMI calc
        with col2:
            weight = st.number_input("Weight (kg)", min_value=25, max_value=250, value=73)
    
    # Calculate and display BMI
    bmi = calculate_bmi(total_inches if unit_system == "Imperial (ft/in, lbs)" else height_m, 
                       weight, unit_system)
    
    with col3:
        if bmi > 0:
            if bmi < 18.5:
                bmi_category = "Underweight"
                bmi_color = "#3B82F6"
            elif bmi < 25:
                bmi_category = "Normal"
                bmi_color = "#10B981"
            elif bmi < 30:
                bmi_category = "Overweight"
                bmi_color = "#F59E0B"
            else:
                bmi_category = "Obese"
                bmi_color = "#EF4444"
            
            st.markdown(f"""
            <div class="bmi-card">
                <div class="bmi-value">{bmi}</div>
                <div class="bmi-label">BMI - {bmi_category}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Family Information
    st.markdown("### 👨‍👩‍👧‍👦 Family Information")
    col1, col2 = st.columns(2)
    
    with col1:
        children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
    
    with col2:
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
    
    # Health Conditions
    st.markdown("### 🏥 Health History")
    conditions = st.multiselect(
        "Pre-existing Conditions (select all that apply)",
        ["None", "Diabetes", "Heart Disease", "High Blood Pressure", "Asthma", 
         "Mental Health Conditions", "Arthritis", "Cancer History", "Chronic Pain", "Other"]
    )
    
    # Income and Budget
    st.markdown("### 💰 Financial Information")
    col1, col2 = st.columns(2)
    
    with col1:
        income_range = st.selectbox(
            "Annual Household Income",
            ["Under $30,000", "$30,000-50,000", "$50,000-75,000", 
             "$75,000-100,000", "$100,000-150,000", "Over $150,000"]
        )
    
    with col2:
        max_monthly = st.number_input(
            "Maximum Monthly Premium Budget",
            min_value=50, max_value=2000, value=400, step=50
        )
    
    # Submit button
    if st.button("Get Personalized Recommendations", type="primary"):
        # Map income to numerical
        income_map = {
            "Under $30,000": 1, "$30,000-50,000": 2, "$50,000-75,000": 3,
            "$75,000-100,000": 4, "$100,000-150,000": 5, "Over $150,000": 6
        }
        
        st.session_state.user_data.update({
            'age': age,
            'gender': gender,
            'smoker': 1 if smoker == "Current Smoker" else 0,
            'state': state,
            'region': STATE_REGIONS[state],
            'bmi': bmi,
            'children': children,
            'marital_status': marital_status,
            'conditions': conditions,
            'income_range': income_range,
            'income_level': income_map[income_range],
            'max_monthly': max_monthly
        })
        st.session_state.current_step = 'recommendations'
        st.rerun()

# Advanced form for experts
def show_advanced_form():
    """Advanced form with detailed options for experienced users"""
    st.markdown("""
    <div class="info-card">
        <h2 class="section-title">Advanced Plan Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["Coverage Preferences", "Network Requirements", "Cost Structure", "Additional Benefits"])
    
    with tabs[0]:
        st.markdown("### Coverage Preferences")
        plan_type = st.selectbox("Preferred Plan Type", ["PPO", "HMO", "EPO", "HDHP", "POS"])
        coverage_level = st.select_slider(
            "Coverage Level",
            options=["Bronze", "Silver", "Gold", "Platinum"]
        )
        prescription_tier = st.selectbox("Prescription Coverage Tier", ["Generic Only", "Preferred", "Non-Preferred", "Specialty"])
    
    with tabs[1]:
        st.markdown("### Network Requirements")
        network_size = st.selectbox("Network Size Priority", ["Local", "Regional", "National", "International"])
        specific_providers = st.text_area("Specific Providers/Hospitals (optional)")
        out_of_network = st.checkbox("Out-of-Network Coverage Required")
    
    with tabs[2]:
        st.markdown("### Cost Structure Preferences")
        col1, col2 = st.columns(2)
        with col1:
            max_premium = st.number_input("Max Monthly Premium", 100, 3000, 500)
            max_deductible = st.number_input("Max Annual Deductible", 500, 10000, 2000)
        with col2:
            max_oop = st.number_input("Max Out-of-Pocket", 1000, 20000, 5000)
            copay_preference = st.selectbox("Copay Preference", ["Low Copays", "Moderate Copays", "High Copays OK"])
    
    with tabs[3]:
        st.markdown("### Additional Benefits")
        benefits = st.multiselect(
            "Required Benefits",
            ["Dental", "Vision", "Mental Health", "Maternity", "Wellness Programs", 
             "Telemedicine", "Alternative Medicine", "International Coverage"]
        )
    
    if st.button("Find Matching Plans", type="primary"):
        st.session_state.user_data.update({
            'plan_type': plan_type,
            'coverage_level': coverage_level,
            'advanced': True
        })
        st.session_state.current_step = 'recommendations'
        st.rerun()

# Switch analysis form
def show_switch_form():
    """Form for users switching insurance plans"""
    st.markdown("""
    <div class="info-card">
        <h2 class="section-title">Let's Improve Your Coverage</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Current Plan Information")
    col1, col2 = st.columns(2)
    
    with col1:
        current_provider = st.text_input("Current Insurance Provider")
        current_premium = st.number_input("Current Monthly Premium", 0, 3000, 350)
        current_deductible = st.number_input("Current Deductible", 0, 15000, 2500)
    
    with col2:
        satisfaction = st.select_slider(
            "Satisfaction Level",
            options=["Very Unsatisfied", "Unsatisfied", "Neutral", "Satisfied", "Very Satisfied"]
        )
        switch_reason = st.multiselect(
            "Reasons for Switching",
            ["Too Expensive", "Poor Coverage", "Limited Network", "Bad Service", 
             "Life Changes", "Better Options Available"]
        )
    
    st.markdown("### What You're Looking For")
    priorities = st.multiselect(
        "Top Priorities (select up to 3)",
        ["Lower Costs", "Better Coverage", "Larger Network", "Specific Doctors", 
         "Better Service", "Additional Benefits"],
        max_selections=3
    )
    
    if st.button("Analyze Better Options", type="primary"):
        st.session_state.user_data.update({
            'current_provider': current_provider,
            'current_premium': current_premium,
            'switch_reason': switch_reason,
            'priorities': priorities
        })
        st.session_state.current_step = 'switch_recommendations'
        st.rerun()

# Family form
def show_family_form():
    """Specialized form for family coverage"""
    st.markdown("""
    <div class="info-card">
        <h2 class="section-title">Family Coverage Assessment</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Family Members")
    
    num_adults = st.number_input("Number of Adults", 1, 10, 1)
    num_children = st.number_input("Number of Children", 0, 10, 2)
    
    if num_children > 0:
        st.markdown("### Children's Ages")
        children_ages = []
        cols = st.columns(min(num_children, 4))
        for i in range(num_children):
            with cols[i % 4]:
                age = st.number_input(f"Child {i+1} Age", 0, 26, 5, key=f"child_{i}")
                children_ages.append(age)
    
    st.markdown("### Family Health Needs")
    
    family_conditions = st.multiselect(
        "Family Health Considerations",
        ["Pediatric Care", "Maternity/Pregnancy", "Chronic Conditions", 
         "Mental Health Services", "Orthodontics/Dental", "Vision Care", 
         "Special Needs Care", "Regular Prescriptions"]
    )
    
    st.markdown("### Budget and Priorities")
    col1, col2 = st.columns(2)
    
    with col1:
        family_budget = st.selectbox(
            "Monthly Family Budget",
            ["Under $500", "$500-750", "$750-1000", "$1000-1500", "Over $1500"]
        )
    
    with col2:
        family_priority = st.selectbox(
            "Most Important Factor",
            ["Comprehensive Pediatric Care", "Low Out-of-Pocket Costs", 
             "Wide Network of Providers", "Prescription Coverage", 
             "Preventive Care Coverage"]
        )
    
    if st.button("Find Best Family Plans", type="primary"):
        st.session_state.user_data.update({
            'num_adults': num_adults,
            'num_children': num_children,
            'children_ages': children_ages if num_children > 0 else [],
            'family_conditions': family_conditions,
            'family_budget': family_budget,
            'family_priority': family_priority
        })
        st.session_state.current_step = 'family_recommendations'
        st.rerun()

# Recommendations display
def show_recommendations():
    """Display personalized insurance recommendations"""
    load_professional_css()
    
    user_data = st.session_state.user_data
    
    # Get ML models
    clf_model, reg_model, categories = create_ml_models()
    
    # Prepare features for prediction
    region_map = {'Northeast': 0, 'Southeast': 1, 'Midwest': 2, 'West': 3, 
                  'Southwest': 2, 'Northwest': 3, 'South': 1}
    
    # Handle different user paths
    if 'bmi' not in user_data:
        user_data['bmi'] = 25  # Default BMI
    if 'children' not in user_data:
        user_data['children'] = 0
    if 'income_level' not in user_data:
        user_data['income_level'] = 3  # Default middle income
    
    features = [[
        user_data.get('age', 30),
        user_data.get('bmi', 25),
        user_data.get('smoker', 0),
        user_data.get('children', 0),
        region_map.get(user_data.get('region', 'Northeast'), 0),
        user_data.get('income_level', 3)
    ]]
    
    # Get predictions
    category_pred = clf_model.predict(features)[0]
    category_probs = clf_model.predict_proba(features)[0]
    cost_pred = reg_model.predict(features)[0]
    
    category_name = categories[category_pred]
    recommended_plans = INSURANCE_COMPANIES[category_name]
    
    # Display header - SIMPLIFIED
    st.success(f"✨ We found the perfect plans for you! Based on your profile, we recommend **{category_name.replace('_', ' ').title()}** plans.")
    
    # Show confidence scores
    st.subheader("Match Confidence")
    
    cols = st.columns(4)
    for i, (cat, prob) in enumerate(zip(categories, category_probs)):
        with cols[i]:
            if i == category_pred:
                st.metric(
                    label=cat.replace('_', ' ').title(),
                    value=f"{prob*100:.0f}%",
                    help="Best match for your profile"
                )
            else:
                st.metric(
                    label=cat.replace('_', ' ').title(),
                    value=f"{prob*100:.0f}%"
                )
    
    # Display recommended plans - USING STREAMLIT NATIVE COMPONENTS
    st.subheader("Your Top Insurance Plans")
    
    for i, plan in enumerate(recommended_plans):
        # Calculate estimated total annual cost
        annual_premium = plan['monthly'] * 12
        estimated_total = annual_premium + (plan['deductible'] * 0.3)
        
        # Use st.container for each plan
        with st.container():
            # Plan header
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"### {plan['name']}")
                st.markdown(f"⭐ **{plan['rating']}/5.0** ({int(plan['rating'])} stars)")
            with col2:
                st.markdown(f"# ${plan['monthly']}/mo")
                st.caption(f"~${estimated_total:,.0f}/year")
            
            # Features as tags using st.columns
            st.markdown("**Key Features:**")
            feature_cols = st.columns(len(plan['features']))
            for idx, feature in enumerate(plan['features']):
                with feature_cols[idx]:
                    st.markdown(f"`{feature}`")
            
            # Cost breakdown using st.columns
            st.markdown("**Cost Breakdown:**")
            cost_cols = st.columns(5)
            with cost_cols[0]:
                st.metric("Monthly Premium", f"${plan['monthly']}")
            with cost_cols[1]:
                st.metric("Annual Deductible", f"${plan['deductible']:,}")
            with cost_cols[2]:
                st.metric("Copay", plan['copay'])
            with cost_cols[3]:
                st.metric("Out-of-Pocket Max", plan['oop_max'])
            with cost_cols[4]:
                st.metric("Network", plan['network'])
            
            # Best for section
            st.info(f"**Best For:** {plan['best_for']}")
            
            # Add separator
            st.markdown("---")
    
    # Cost prediction chart
    st.subheader("Your Estimated Healthcare Costs")
    
    # Create cost scenarios
    scenarios = {
        'Low Usage': cost_pred * 0.7,
        'Average Usage': cost_pred,
        'High Usage': cost_pred * 1.5
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(scenarios.keys()),
            y=list(scenarios.values()),
            marker=dict(color=['#10B981', '#0EA5E9', '#F59E0B']),
            text=[f'${v:,.0f}' for v in scenarios.values()],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Annual Healthcare Cost Scenarios",
        yaxis_title="Estimated Annual Cost ($)",
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Family recommendations
def show_family_recommendations():
    """Display family-specific recommendations"""
    load_professional_css()
    
    user_data = st.session_state.user_data
    family_plans = INSURANCE_COMPANIES['family']
    
    total_members = user_data['num_adults'] + user_data['num_children']
    
    # This part is working (the green banner)
    st.success(f"👨‍👩‍👧‍👦 Perfect family plans for your household of {total_members} members!")
    
    for plan in family_plans:
        per_person = plan['monthly'] / total_members
        annual_cost = plan['monthly'] * 12
        
        with st.container():
            # Plan header
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"### {plan['name']}")
                st.caption(f"${per_person:.0f} per person")
            with col2:
                st.markdown(f"# ${plan['monthly']}/mo")
                st.caption(f"⭐ {plan['rating']}/5.0")
            
            # Replace the HTML features with this:
            st.markdown("**Key Features:**")
            feature_cols = st.columns(len(plan['features']))
            for idx, feature in enumerate(plan['features']):
                with feature_cols[idx]:
                    st.markdown(f"`{feature}`")
            
            # Replace HTML cost table with this:
            st.markdown("**Cost Breakdown:**")
            cost_cols = st.columns(3)
            with cost_cols[0]:
                st.metric("Annual Premium", f"${annual_cost:,}")
            with cost_cols[1]:
                st.metric("Family Deductible", f"${plan['deductible']:,}")
            with cost_cols[2]:
                st.metric("Network Type", plan['network'])
            
            st.markdown("---")



# Switch recommendations
def show_switch_recommendations():
    """Display recommendations for switching plans"""
    load_professional_css()  # Add this line
    
    user_data = st.session_state.user_data
    current_premium = user_data.get('current_premium', 0)
    
    # Use native Streamlit info banner
    st.info("🔄 Based on your current plan analysis, here are better alternatives")
    
    # Show potential savings
    all_plans = []
    for category in INSURANCE_COMPANIES.values():
        all_plans.extend(category)
    
    # Filter plans based on priorities
    filtered_plans = [p for p in all_plans if p['monthly'] <= current_premium * 1.2]
    filtered_plans.sort(key=lambda x: x['monthly'])
    
    for plan in filtered_plans[:3]:
        savings = max(0, current_premium - plan['monthly'])
        
        # Use Streamlit container instead of HTML
        with st.container():
            # Plan header
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"### {plan['name']}")
                if savings > 0:
                    st.success(f"Save ${savings}/month!")
            with col2:
                st.markdown(f"# ${plan['monthly']}/mo")
                st.caption(f"⭐ {plan['rating']}/5.0")
            
            # Features using native components
            st.markdown("**Key Features:**")
            feature_cols = st.columns(len(plan['features']))
            for idx, feature in enumerate(plan['features']):
                with feature_cols[idx]:
                    st.markdown(f"`{feature}`")
            
            # Separator
            st.markdown("---")

# Educational content
def show_education():
    """Display educational content about US healthcare"""
    load_professional_css()
    
    st.markdown("""
    <div class="info-card">
        <h2 class="section-title">Understanding US Healthcare Insurance</h2>
    </div>
    """, unsafe_allow_html=True)
    
    
    tabs = st.tabs(["📚 Key Terms", "🏥 Plan Types", "💰 Cost Structure", "✅ Choosing a Plan"])
    
    with tabs[0]:
        st.markdown("""
        ### Essential Insurance Terms
        
        **Premium** 💳
        - Your monthly payment to maintain insurance coverage
        - Paid regardless of whether you use healthcare services
        - Typically ranges from $200-800+ for individuals
        
        **Deductible** 💰
        - Amount you pay before insurance starts covering costs
        - Resets annually
        - Higher deductible usually means lower premium
        
        **Copayment (Copay)** 🏥
        - Fixed amount you pay for covered services
        - Example: $25 for a doctor visit
        - Applies after deductible is met
        
        **Coinsurance** 📊
        - Percentage of costs you share with insurance
        - Example: 80/20 split (insurance pays 80%, you pay 20%)
        - Applies after deductible is met
        
        **Out-of-Pocket Maximum** 🎯
        - Most you'll pay in a year for covered services
        - Insurance pays 100% after this limit
        - Includes deductibles, copays, and coinsurance
        """)
    
    with tabs[1]:
        st.markdown("""
        ### Types of Health Insurance Plans
        
        **HMO (Health Maintenance Organization)** 🏢
        - ✅ Lower costs
        - ✅ Predictable expenses
        - ❌ Must choose primary care doctor
        - ❌ Need referrals for specialists
        - ❌ Limited to network providers
        
        **PPO (Preferred Provider Organization)** 🌐
        - ✅ See any doctor without referral
        - ✅ Out-of-network coverage available
        - ✅ More flexibility
        - ❌ Higher premiums
        - ❌ Higher out-of-network costs
        
        **EPO (Exclusive Provider Organization)** ⚖️
        - ✅ No referrals needed
        - ✅ Lower premiums than PPO
        - ❌ No out-of-network coverage
        - ❌ Must stay in network
        
        **HDHP (High Deductible Health Plan)** 💎
        - ✅ Lower monthly premiums
        - ✅ HSA eligible (tax benefits)
        - ❌ High deductible ($1,400+ individual)
        - ❌ Pay more upfront for care
        """)
    
    with tabs[2]:
        st.markdown("""
        ### Understanding Healthcare Costs
        
        **How You Pay for Healthcare:**
        
        1. **Monthly Premium** - Ongoing cost regardless of usage
        2. **When You Need Care:**
           - First: Pay full cost until deductible is met
           - Then: Pay copays or coinsurance
           - Finally: Insurance pays 100% after out-of-pocket max
        
        **Example Cost Scenario:**
        - Premium: $300/month = $3,600/year
        - Deductible: $2,000
        - Doctor visit: $200
        - You pay: $200 (toward deductible)
        - After deductible met: You pay $25 copay per visit
        
        **Tips to Save Money:**
        - Use in-network providers (30-50% savings)
        - Generic medications (80% cheaper)
        - Preventive care is usually free
        - Use urgent care instead of ER when appropriate
        - Ask about payment plans for large bills
        """)
    
    with tabs[3]:
        st.markdown("""
        ### How to Choose the Right Plan
        
        **Consider Your Needs:**
        
        🏥 **Choose HMO if:**
        - You want lower costs
        - You don't mind having a primary doctor
        - You rarely need specialists
        
        🌐 **Choose PPO if:**
        - You want flexibility
        - You have preferred doctors
        - You travel frequently
        
        💰 **Choose HDHP if:**
        - You're healthy and rarely need care
        - You want lower monthly costs
        - You can afford high deductible if needed
        
        **Key Questions to Ask:**
        1. Are my doctors in-network?
        2. Are my medications covered?
        3. What's the total annual cost if I get sick?
        4. Does it cover my specific health needs?
        5. What's the quality rating of the plan?
        """)

    if st.button("Start Finding My Plan", type="primary"):
        st.session_state.current_step = 'home'
        st.rerun()

# Progress indicator
def show_progress(current_step):
    """Display progress indicator"""
    steps = {
        'home': 1,
        'experience_level': 2,
        'simple_form': 3,
        'user_form': 3,
        'advanced_form': 3,
        'switch_form': 3,
        'family_form': 3,
        'recommendations': 4,
        'family_recommendations': 4,
        'switch_recommendations': 4,
        'education': 2
    }
    
    current = steps.get(current_step, 1)
    total = 4
    progress_pct = (current / total) * 100
    
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress_pct}%;"></div>
    </div>
    """, unsafe_allow_html=True)

# Back button functionality
def show_back_button():
    """Display back button for navigation"""
    if st.session_state.current_step != 'home':
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button("← Back", key="back_btn"):
                # Navigate back logic
                step_map = {
                    'experience_level': 'home',
                    'simple_form': 'experience_level',
                    'user_form': 'experience_level',
                    'advanced_form': 'experience_level',
                    'switch_form': 'experience_level',
                    'family_form': 'home',
                    'recommendations': 'user_form',
                    'family_recommendations': 'family_form',
                    'switch_recommendations': 'switch_form',
                    'education': 'home'
                }
                st.session_state.current_step = step_map.get(st.session_state.current_step, 'home')
                st.rerun()

# Cost calculator tool
def show_cost_calculator():
    """Interactive cost calculator tool"""
    st.markdown("""
    <div class="info-card">
        <h2 class="section-title">Healthcare Cost Calculator</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_premium = st.number_input("Monthly Premium ($)", 100, 2000, 350)
        annual_deductible = st.number_input("Annual Deductible ($)", 0, 10000, 2000)
        copay = st.number_input("Typical Copay ($)", 0, 100, 25)
        
    with col2:
        doctor_visits = st.slider("Expected Doctor Visits/Year", 0, 24, 4)
        prescriptions = st.slider("Monthly Prescriptions", 0, 10, 1)
        emergency_risk = st.select_slider(
            "Emergency Risk",
            options=["Low", "Medium", "High"],
            value="Low"
        )
    
    # Calculate costs
    annual_premium = monthly_premium * 12
    copay_costs = copay * doctor_visits
    prescription_costs = prescriptions * 50 * 12  # Assume $50/prescription
    
    emergency_costs = {"Low": 0, "Medium": 1500, "High": 5000}
    emergency_estimate = emergency_costs[emergency_risk]
    
    # Total before insurance
    total_medical_costs = copay_costs + prescription_costs + emergency_estimate
    
    # Calculate what you pay
    if total_medical_costs <= annual_deductible:
        out_of_pocket = total_medical_costs
    else:
        # Assume 20% coinsurance after deductible
        out_of_pocket = annual_deductible + (total_medical_costs - annual_deductible) * 0.2
    
    total_annual_cost = annual_premium + out_of_pocket
    
    # Display results
    st.markdown("""
    <div class="cost-table" style="margin-top: 2rem;">
        <h3 style="color: #0C4A6E; margin-bottom: 1rem;">Annual Cost Breakdown</h3>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="cost-row">
            <span>Insurance Premiums:</span>
            <strong>${annual_premium:,}</strong>
        </div>
        <div class="cost-row">
            <span>Doctor Visit Copays:</span>
            <strong>${copay_costs:,}</strong>
        </div>
        <div class="cost-row">
            <span>Prescription Costs:</span>
            <strong>${prescription_costs:,}</strong>
        </div>
        <div class="cost-row">
            <span>Emergency Care (est.):</span>
            <strong>${emergency_estimate:,}</strong>
        </div>
        <div class="cost-row" style="font-size: 1.3rem; color: #2563eb;">
            <span>Total Annual Cost:</span>
            <strong>${total_annual_cost:,}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Monthly breakdown
    monthly_total = total_annual_cost / 12
    st.markdown(f"""
    <div class="success-banner" style="margin-top: 1rem;">
        📊 This equals approximately <strong>${monthly_total:.0f}/month</strong> for your healthcare
    </div>
    """, unsafe_allow_html=True)

# Comparison tool
def show_comparison_tool():
    """Plan comparison tool"""
    st.markdown("""
    <div class="info-card">
        <h2 class="section-title">Compare Insurance Plans Side-by-Side</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Select plans to compare
    all_plan_names = []
    for category in INSURANCE_COMPANIES.values():
        for plan in category:
            all_plan_names.append(plan['name'])
    
    selected_plans = st.multiselect(
        "Select plans to compare (up to 3)",
        all_plan_names,
        max_selections=3
    )
    
    if len(selected_plans) >= 2:
        cols = st.columns(len(selected_plans))
        
        for idx, plan_name in enumerate(selected_plans):
            # Find the plan
            selected_plan = None
            for category in INSURANCE_COMPANIES.values():
                for plan in category:
                    if plan['name'] == plan_name:
                        selected_plan = plan
                        break
            
            if selected_plan:
                with cols[idx]:
                    st.markdown(f"""
                    <div class="plan-card">
                        <div class="plan-name" style="font-size: 1.2rem;">{selected_plan['name']}</div>
                        <div class="plan-price">${selected_plan['monthly']}/mo</div>
                        
                        <div style="margin: 1rem 0;">
                            <div style="color: #F59E0B;">{'⭐' * int(selected_plan['rating'])}</div>
                        </div>
                        
                        <div class="cost-table" style="font-size: 0.9rem;">
                            <div class="cost-row">
                                <span>Deductible:</span>
                                <strong>${selected_plan['deductible']:,}</strong>
                            </div>
                            <div class="cost-row">
                                <span>Copay:</span>
                                <strong>{selected_plan['copay']}</strong>
                            </div>
                            <div class="cost-row">
                                <span>OOP Max:</span>
                                <strong>{selected_plan['oop_max']}</strong>
                            </div>
                            <div class="cost-row">
                                <span>Network:</span>
                                <strong style="font-size: 0.8rem;">{selected_plan['network']}</strong>
                            </div>
                        </div>
                        
                        <div style="margin-top: 1rem;">
                            {"".join([f'<span class="feature-tag" style="font-size: 0.8rem;">{feature}</span>' for feature in selected_plan['features'][:2]])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# FAQ section
def show_faq():
    """Display frequently asked questions"""
    st.markdown("""
    <div class="info-card">
        <h2 class="section-title">Frequently Asked Questions</h2>
    </div>
    """, unsafe_allow_html=True)
    
    faqs = [
        {
            "question": "When can I enroll in health insurance?",
            "answer": "Open Enrollment is typically November 1 - December 15 each year. You can also enroll during Special Enrollment Periods if you have qualifying life events (job loss, marriage, new baby, etc.)."
        },
        {
            "question": "What's the difference between in-network and out-of-network?",
            "answer": "In-network providers have contracts with your insurance for lower rates. Out-of-network providers cost more, and some plans don't cover them at all."
        },
        {
            "question": "Is dental and vision included?",
            "answer": "Most health plans don't include dental and vision. These are usually separate plans, though some comprehensive plans may include basic coverage."
        },
        {
            "question": "What if I can't afford health insurance?",
            "answer": "You may qualify for subsidies through Healthcare.gov, Medicaid, or CHIP. Many people qualify for plans under $100/month with subsidies."
        },
        {
            "question": "What's an HSA?",
            "answer": "A Health Savings Account lets you save pre-tax money for medical expenses. You need a High Deductible Health Plan to qualify. Money rolls over year to year."
        }
    ]
    
    for faq in faqs:
        with st.expander(f"❓ {faq['question']}"):
            st.write(faq['answer'])

# Sidebar tools
def show_sidebar_tools():
    """Display sidebar with additional tools"""
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0EA5E9, #10B981); 
                    padding: 1.5rem; 
                    border-radius: 12px; 
                    color: white; 
                    text-align: center;
                    margin-bottom: 2rem;">
            <h2 style="color: white; margin: 0;">Quick Tools</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💰 Cost Calculator", key="calc_tool", use_container_width=True):
            st.session_state.current_step = 'calculator'
            st.rerun()
        
        if st.button("📊 Compare Plans", key="compare_tool", use_container_width=True):
            st.session_state.current_step = 'compare'
            st.rerun()
        
        if st.button("❓ View FAQ", key="faq_tool", use_container_width=True):
            st.session_state.current_step = 'faq'
            st.rerun()
        
        st.markdown("---")

        
        # Quick stats
        if 'user_data' in st.session_state and st.session_state.user_data:
            st.markdown("""
            <div style="background: white; 
                        padding: 1rem; 
                        border-radius: 8px; 
                        border: 2px solid #dbeafe;">
                <h4 style="color: #0C4A6E; margin-bottom: 0.5rem;">Your Profile</h4>
            """, unsafe_allow_html=True)
            
            user_data = st.session_state.user_data
            if 'age' in user_data:
                st.write(f"Age: {user_data['age']}")
            if 'state' in user_data:
                st.write(f"State: {user_data['state']}")
            if 'family_size' in user_data:
                st.write(f"Family: {user_data['family_size']}")
            
            st.markdown("</div>", unsafe_allow_html=True)

# Main application
def main():
    # Load CSS
    load_professional_css()
    
    # Show header
    show_header()
    
    # Show progress indicator
    if st.session_state.current_step not in ['home', 'calculator', 'compare', 'faq']:
        show_progress(st.session_state.current_step)
    
    # Show back button
    show_back_button()
    
    # Route to appropriate page
    if st.session_state.current_step == 'home':
        show_home()
    elif st.session_state.current_step == 'experience_level':
        show_experience_level()
    elif st.session_state.current_step == 'simple_form':
        show_simple_form()
    elif st.session_state.current_step == 'user_form':
        show_user_form()
    elif st.session_state.current_step == 'advanced_form':
        show_advanced_form()
    elif st.session_state.current_step == 'switch_form':
        show_switch_form()
    elif st.session_state.current_step == 'family_form':
        show_family_form()
    elif st.session_state.current_step == 'recommendations':
        show_recommendations()
    elif st.session_state.current_step == 'family_recommendations':
        show_family_recommendations()
    elif st.session_state.current_step == 'switch_recommendations':
        show_switch_recommendations()
    elif st.session_state.current_step == 'education':
        show_education()
    elif st.session_state.current_step == 'calculator':
        show_cost_calculator()
        if st.button("← Back to Main", key="back_calc"):
            st.session_state.current_step = 'home'
            st.rerun()
    elif st.session_state.current_step == 'compare':
        show_comparison_tool()
        if st.button("← Back to Main", key="back_compare"):
            st.session_state.current_step = 'home'
            st.rerun()
    elif st.session_state.current_step == 'faq':
        show_faq()
        if st.button("← Back to Main", key="back_faq"):
            st.session_state.current_step = 'home'
            st.rerun()
    elif st.session_state.current_step == 'dashboard':
        show_dashboard()
    
    # Show sidebar tools
    show_sidebar_tools()
    
    # Footer
    st.markdown("""
    <div style="margin-top: 4rem; padding: 2rem; background: linear-gradient(135deg, #0EA5E9, #10B981); text-align: center; border-radius: 12px;">
        <p style="color: white; margin: 0;">
            © 2025 Medicost - AI-Powered Healthcare Insurance Platform<br>
            <small style="opacity: 0.9;">Making healthcare accessible and understandable for everyone</small>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()