import pandas as pd
import coremltools as ct
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# === Load CSVs ===
users_df = pd.read_csv("exercise.csv")       # contains Gender, Age, etc.
calories_df = pd.read_csv("calories.csv") # contains Calories

# === Merge on User_ID ===
df = pd.merge(users_df, calories_df, on="User_ID")

# === Encode Gender ===
df["Gender"] = LabelEncoder().fit_transform(df["Gender"])  # male=1, female=0

# === Prepare features and target ===
X = df[["Gender", "Age", "Height", "Weight", "Duration", "Heart_Rate", "Body_Temp"]]
y = df["Calories"]

# === Fit the model ===
model = LinearRegression()
model.fit(X, y)

# === (Optional) test prediction ===
sample = pd.DataFrame([{
    'Gender': 1,
    'Age': 26,
    'Height': 187,
    'Weight': 91,
    'Duration': 15,
    'Heart_Rate': 160,
    'Body_Temp': 37
}])
print("Prediction:", model.predict(sample))

# === Export to Core ML ===
mlmodel = ct.converters.sklearn.convert(
    model,
    input_features=["Gender", "Age", "Height", "Weight", "Duration", "Heart_Rate", "Body_Temp"],
    output_feature_names="Calories"
)

mlmodel.save("CaloriesPredictorFromCSV.mlmodel")
print("✅ Model saved.")
