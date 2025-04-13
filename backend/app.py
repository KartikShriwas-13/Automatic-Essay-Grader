
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pandas as pd
# import os
# import joblib
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
# import language_tool_python

# app = Flask(__name__)
# CORS(app)

# # Initialize grammar checker
# tool = language_tool_python.LanguageTool('en-US')

# # Load and prepare dataset (only 5000 rows for speed)
# df = pd.read_csv("data/essay_llama3_8B_groq.csv").sample(n=5000, random_state=42)

# # Load model/vectorizer if exist, otherwise train and save them
# if os.path.exists("model.pkl") and os.path.exists("vectorizer.pkl"):
#     model = joblib.load("model.pkl")
#     vectorizer = joblib.load("vectorizer.pkl")
# else:
#     vectorizer = TfidfVectorizer()
#     X = vectorizer.fit_transform(df["cleaned_text"])
#     y = df["score"]

#     model = RandomForestRegressor(n_estimators=100, random_state=42)
#     model.fit(X, y)

#     joblib.dump(model, "model.pkl")
#     joblib.dump(vectorizer, "vectorizer.pkl")

# @app.route("/grade", methods=["POST"])
# def grade_essay():
#     data = request.get_json()
#     prompt = data.get("prompt", "")
#     essay = data.get("essay", "")

#     if not essay:
#         return jsonify({"error": "No essay provided"}), 400

#     # Predict score
#     essay_vec = vectorizer.transform([essay])
#     predicted_score = model.predict(essay_vec)[0]

#     # Analysis
#     words = essay.split()
#     word_count = len(words)
#     sentence_count = essay.count('.') + essay.count('!') + essay.count('?')
#     grammar_matches = tool.check(essay)
#     grammar_issues = len(grammar_matches)
    
#     grammar_suggestions = [
#         f"{match.context.strip()}: {match.message}" for match in grammar_matches[:5]
#     ]

#     # Improved Prompt Match - Partial Keyword Match
#     prompt_words = [word for word in prompt.lower().split() if word not in ENGLISH_STOP_WORDS]
#     essay_words = essay.lower().split()
#     common_words = set(prompt_words).intersection(essay_words)
#     prompt_matched = len(common_words) > 0

#     return jsonify({
#         "score": round(predicted_score, 2),
#         "analysis": {
#             "word_count": word_count,
#             "sentence_count": sentence_count,
#             "grammar_issues": grammar_issues,
#             "grammar_suggestions": grammar_suggestions,
#             "contains_prompt": prompt_matched
#         }
#     })

# if __name__ == "__main__":
#     app.run(debug=True)


#change 1

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import joblib
# import pandas as pd
# from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
# import language_tool_python
# import os

# from flask import send_from_directory

# app = Flask(__name__)
# CORS(app)

# # Initialize grammar checker
# tool = language_tool_python.LanguageTool('en-US')

# # Load model and vectorizer
# model = joblib.load("model.pkl")
# vectorizer = joblib.load("vectorizer.pkl")

# # @app.route("/")
# # def home():
# #     return "🚀 Essay Grading API is running! Use /grade endpoint to POST essays."
# @app.route("/")
# def serve_react():
#     return send_from_directory("build", "index.html")

# @app.route('/<path:path>')
# def static_proxy(path):
#     return send_from_directory("build", path)

# @app.route("/grade", methods=["POST"])
# def grade_essay():
#     data = request.get_json()
#     prompt = data.get("prompt", "")
#     essay = data.get("essay", "")

#     if not essay:
#         return jsonify({"error": "No essay provided"}), 400

#     essay_vec = vectorizer.transform([essay])
#     predicted_score = model.predict(essay_vec)[0]

#     words = essay.split()
#     word_count = len(words)
#     sentence_count = essay.count('.') + essay.count('!') + essay.count('?')
#     grammar_matches = tool.check(essay)
#     grammar_issues = len(grammar_matches)

#     grammar_suggestions = [
#         f"{match.context.strip()}: {match.message}" for match in grammar_matches[:5]
#     ]

#     prompt_words = [word for word in prompt.lower().split() if word not in ENGLISH_STOP_WORDS]
#     essay_words = essay.lower().split()
#     common_words = set(prompt_words).intersection(essay_words)
#     prompt_matched = len(common_words) > 0

#     return jsonify({
#         "score": round(predicted_score, 2),
#         "analysis": {
#             "word_count": word_count,
#             "sentence_count": sentence_count,
#             "grammar_issues": grammar_issues,
#             "grammar_suggestions": grammar_suggestions,
#             "contains_prompt": prompt_matched
#         }
#     })

# if __name__ == "__main__":
#     app.run(debug=True)


#change 2
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import language_tool_python
import os

app = Flask(__name__, static_folder='build', static_url_path='/')  # Set static folder
CORS(app)

# Initialize grammar checker
tool = language_tool_python.LanguageTool('en-US')

# Load model and vectorizer
try:
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    print("✅ Model and vectorizer loaded successfully")
except Exception as e:
    print(f"❌ Error loading model/vectorizer: {e}")
    model = None
    vectorizer = None
    # IMPORTANT:  Handle this error.  The app may not function correctly!
    # You might want to raise an exception or exit if the model fails to load.


@app.route("/")
def serve_react():
    """Serves the main React page (index.html)."""
    return send_from_directory(app.static_folder, "index.html")


@app.route('/<path:path>')
def static_proxy(path):
    """Serves static files from the React build directory."""
    # This should be more general
    return send_from_directory(app.static_folder, path)



@app.route("/grade", methods=["POST"])
def grade_essay():
    """Grades an essay and returns the score and analysis."""
    data = request.get_json()
    prompt = data.get("prompt", "")
    essay = data.get("essay", "")

    if not essay:
        return jsonify({"error": "No essay provided"}), 400

    if model is None or vectorizer is None:
        return jsonify({"error": "Model or vectorizer is not loaded"}), 500

    try:
        essay_vec = vectorizer.transform([essay])
        predicted_score = model.predict(essay_vec)[0]
    except Exception as e:
        print(f"Error in /grade: {e}")
        return jsonify({"error": "Error processing essay"}), 500

    words = essay.split()
    word_count = len(words)
    sentence_count = essay.count('.') + essay.count('!') + essay.count('?')
    try:
        grammar_matches = tool.check(essay)
        grammar_issues = len(grammar_matches)
        grammar_suggestions = [
            f"{match.context.strip()}: {match.message}" for match in grammar_matches[:5]
        ]
    except ImportError:
        grammar_issues = 0
        grammar_suggestions = ["Grammar check is unavailable. Install language_tool_python."]

    prompt_words = [word for word in prompt.lower().split() if word not in ENGLISH_STOP_WORDS]
    essay_words = essay.lower().split()
    common_words = set(prompt_words).intersection(essay_words)
    prompt_matched = len(common_words) > 0

    return jsonify({
        "score": round(predicted_score, 2),
        "analysis": {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "grammar_issues": grammar_issues,
            "grammar_suggestions": grammar_suggestions,
            "contains_prompt": prompt_matched,
        },
    })


if __name__ == "__main__":
    app.run(debug=True)
