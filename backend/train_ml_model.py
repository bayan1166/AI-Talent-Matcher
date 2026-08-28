import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print(" Starting ML Model Training Pipeline...")

np.random.seed(42)
n_samples = 1000

data = {
    'skill_match': np.random.randint(40, 100, n_samples),
    'experience_years': np.random.randint(0, 15, n_samples), 
    'project_relevance': np.random.randint(20, 100, n_samples),
    'availability_score': np.random.randint(0, 100, n_samples),
    'education_score': np.random.randint(50, 100, n_samples)
}

df = pd.DataFrame(data)

df['experience_normalized'] = (df['experience_years'] / 15) * 100 

df['weighted_score'] = (
    (df['skill_match'] * 0.40) +
    (df['experience_normalized'] * 0.25) +
    (df['project_relevance'] * 0.15) +
    (df['availability_score'] * 0.10) +
    (df['education_score'] * 0.10)
)

noise = np.random.normal(0, 5, n_samples) 
df['is_successful'] = ((df['weighted_score'] + noise) > 70).astype(int)

X = df[['skill_match', 'experience_years', 'project_relevance', 'availability_score', 'education_score']]
y = df['is_successful']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(class_weight='balanced')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("-" * 40)
print(f" Model Training Completed!")
print(f" Model Accuracy: {accuracy * 100:.2f}%")
print("-" * 40)
print("Classification Report:")
print(classification_report(y_test, y_pred))

model_path = os.path.join(os.path.dirname(__file__), "candidate_scorer_model.pkl")
joblib.dump(model, model_path)
print(f" Model saved successfully at: {model_path}")
