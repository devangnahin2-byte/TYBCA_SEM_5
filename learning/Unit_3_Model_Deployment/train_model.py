import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def main():
    print("Loading Dataset...")
    data = load_iris()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Model...")
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"Model trained with accuracy: {accuracy:.4f}")

    import os
    model_filename = os.path.join(os.path.dirname(__file__), "iris_model.joblib")
    joblib.dump(model, model_filename)
    print(f"Model saved successfully to {model_filename}")

    joblib.dump(data.target_names, os.path.join(os.path.dirname(__file__), "target_names.joblib"))

if __name__ == "__main__":
    main()
