# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer
import joblib

# 1. Load dataset
data = pd.read_csv("data.csv")

# 2. Split data
X_train, X_test, y_train, y_test = train_test_split(data['message'], data['label'], test_size=0.2, random_state=42)

# 3. Load a small language model for embeddings
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
embedder = SentenceTransformer(model_name)

# 4. Convert text to embeddings
X_train_embeddings = embedder.encode(X_train.tolist(), convert_to_tensor=False)
X_test_embeddings = embedder.encode(X_test.tolist(), convert_to_tensor=False)

# 5. Train a simple classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_embeddings, y_train)

# 6. Evaluate the model
y_pred = clf.predict(X_test_embeddings)
print(classification_report(y_test, y_pred))

# 7. Save both model and classifier
joblib.dump(clf, "classifier.pkl")
embedder.save("text_encoder")

print("\n✅ Training complete! Model saved as classifier.pkl and text_encoder/")
