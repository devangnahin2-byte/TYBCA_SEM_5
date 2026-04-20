import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os

def train_and_save_model():
    np.random.seed(42)
    n_samples = 300
    
    study_hours = np.random.uniform(50, 200, n_samples)
    attendance = np.random.uniform(60, 100, n_samples)
    midterm_score = np.random.uniform(40, 95, n_samples)
    
    final_score = (study_hours * 0.1) + (attendance * 0.3) + (midterm_score * 0.5) + np.random.normal(0, 5, n_samples)
    final_score = np.clip(final_score, 0, 100)
    
    df = pd.DataFrame({
        'study_hours': study_hours,
        'attendance': attendance,
        'midterm_score': midterm_score
    })
    
    X = df
    y = final_score
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    score = model.score(X_test, y_test)
    print(f"Model R^2 Score: {score:.4f}")
    
    save_path = os.path.join(os.path.dirname(__file__), "student_marks_model.joblib")
    joblib.dump(model, save_path)
    joblib.dump(X.columns.tolist(), os.path.join(os.path.dirname(__file__), "student_features.joblib"))

if __name__ == "__main__":
    train_and_save_model()
