import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
import os

print("Training the Student Admissions Predictor...")

data = {
    "Math_Score": [90, 45, 60, 85, 30, 95, 70, 50],
    "Science_Score": [85, 50, 65, 80, 40, 90, 75, 55],
    "Admitted": [1, 0, 0, 1, 0, 1, 1, 0] # 1 means Admitted
}
df = pd.DataFrame(data)

X = df[["Math_Score", "Science_Score"]]
y = df["Admitted"]

model = LogisticRegression()
model.fit(X, y)

model_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "student_model.joblib")
joblib.dump(model, model_filename)

print(f"Success! Model trained and saved as '{model_filename}'")
print("You can now run 'flask_api.py'.")
