"""
Skill Test Routes - Skill Verification Quiz
"""
from flask import Blueprint, request, jsonify
import random
import os
import requests
import json
import re

test_bp = Blueprint('test', __name__)
import os

# Load static fallback questions from data file
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')

def load_local_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, 'r') as f:
            return json.load(f)
    return {}

QUESTIONS = load_local_questions()

# Map aliases/display names to question keys
SKILL_MAP = {
    "python": "python", "javascript": "javascript", "js": "javascript",
    "react": "react", "reactjs": "react",
    "design": "design", "ui/ux": "design", "ui": "design",
    "data science": "data_science", "data_science": "data_science",
    "machine learning": "machine_learning", "ml": "machine_learning", "ai": "machine_learning",
    "web development": "web_development", "html/css": "web_development", "web dev": "web_development",
    "java": "java", "marketing": "marketing",
}


@test_bp.route('/test/<skill>', methods=['GET'])
def get_test(skill):
    key = SKILL_MAP.get(skill.lower(), skill.lower().replace(' ', '_'))
    questions = QUESTIONS.get(key)
    
    # If not hardcoded, use Hugging Face AI to generate a quiz
    if not questions:
        hf_token = os.environ.get("HF_TOKEN")
        if not hf_token:
            available = list(set(QUESTIONS.keys()))
            return jsonify({"error": f"No hardcoded questions for '{skill}' and HF_TOKEN not set.", "available_skills": available}), 404
            
        print(f"Generating quiz for {skill} using Hugging Face...")
        try:
            # We use a fast, free instruction-tuned model from HF
            API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
            headers = {"Authorization": f"Bearer {hf_token}"}
            
            prompt = f"[INST] You are an expert technical interviewer. Generate a 10-question multiple-choice quiz about '{skill}'.\n" \
                     f"Return ONLY a raw JSON array of objects. Do not wrap it in ```json or any other text.\n" \
                     f"Each object must have exactly:\n" \
                     f" - 'q': a string containing the question\n" \
                     f" - 'options': an array of exactly 4 string options\n" \
                     f" - 'answer': an integer 0, 1, 2, or 3 representing the index of the correct option\n" \
                     f"ONLY output the raw valid JSON array list: [/INST]"
                     
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 2048,
                    "temperature": 0.2,
                    "return_full_text": False
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            if response.status_code != 200:
                print(f"HF API Error {response.status_code}: {response.text}")
                return jsonify({"error": "Failed to generate AI quiz (API Error)."}), 500
                
            result_text = response.json()[0]['generated_text']
            
            # Clean possible markdown formatting
            result_text = result_text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
                
            # Attempt to parse
            try:
                questions = json.loads(result_text)
                if len(questions) < 5:
                    raise ValueError("Not enough questions generated.")
            except json.JSONDecodeError:
                # Fallback regex extraction if model hallucinated extra text
                match = re.search(r'\[.*\]', result_text, re.DOTALL)
                if match:
                    questions = json.loads(match.group(0))
                else:
                    print("Failed to parse JSON generator output")
                    raise
                    
            print(f"✅ AI Quiz generated successfully. ({len(questions)} questions)")        
            
        except Exception as e:
            print(f"❌ Error generating quiz: {e}")
            available = list(set(QUESTIONS.keys()))
            return jsonify({"error": f"Failed to generate AI quiz for '{skill}'. Please try a built-in skill.", "available_skills": available}), 404

    sample = random.sample(questions, min(10, len(questions)))
    # Remove answer before sending to client
    clean = [{"id": i, "q": q["q"], "options": q["options"]} for i, q in enumerate(sample)]
    return jsonify({"skill": skill, "total": len(clean), "questions": clean,
                    "_answers": [q["answer"] for q in sample]})  # NOTE: remove _answers in production!


@test_bp.route('/test/submit', methods=['POST'])
def submit_test():
    data = request.get_json()
    skill = data.get('skill', '')
    user_answers = data.get('answers', [])
    correct_answers = data.get('correct_answers', [])

    if not user_answers or not correct_answers:
        return jsonify({"error": "answers and correct_answers required"}), 400

    correct_count = sum(1 for u, c in zip(user_answers, correct_answers) if u == c)
    total = len(correct_answers)
    score = round((correct_count / total) * 100) if total > 0 else 0

    passed = score >= 70
    level = "Expert" if score >= 90 else "Intermediate" if score >= 70 else "Beginner"

    return jsonify({
        "skill": skill,
        "score": score,
        "correct": correct_count,
        "total": total,
        "passed": passed,
        "level": level,
        "badge": f"{skill.title()} {level}" if passed else None,
        "message": f"🎉 Congratulations! You earned the '{skill.title()} {level}' badge!" if passed
                   else f"You scored {score}%. Score 70%+ to earn your verified badge."
    })
