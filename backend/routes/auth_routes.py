"""
Auth / Profile Routes
Badge System:
  Bronze  → has LinkedIn or GitHub linked
  Iron    → 5+ tasks completed
  Silver  → 15+ tasks completed
  Gold    → 30+ tasks completed
  Diamond → 45+ tasks completed
  Platinum→ 55+ tasks completed

Quiz gives SKILL APPROVAL only (not a badge).
Badges are earned through completed tasks.
"""
from flask import Blueprint, request, jsonify
import json, os

auth_bp = Blueprint('auth', __name__)

PROFILES_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'profiles.json')


def compute_badge(task_count: int, linkedin: str, github: str) -> str | None:
    """Return badge tier name based on task count and social profiles."""
    if task_count >= 55: return 'Platinum'
    if task_count >= 45: return 'Diamond'
    if task_count >= 30: return 'Gold'
    if task_count >= 15: return 'Silver'
    if task_count >= 5:  return 'Iron'
    if linkedin or github: return 'Bronze'
    return None


def _load_profiles():
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, 'r') as f:
            return json.load(f)
    return {}


def _save_profiles(profiles):
    os.makedirs(os.path.dirname(PROFILES_FILE), exist_ok=True)
    with open(PROFILES_FILE, 'w') as f:
        json.dump(profiles, f, indent=2)


@auth_bp.route('/profile/<uid>', methods=['GET'])
def get_profile(uid):
    profiles = _load_profiles()
    profile = profiles.get(uid)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404
    return jsonify(profile)


@auth_bp.route('/profile', methods=['POST'])
def save_profile():
    data = request.get_json()
    if not data or 'uid' not in data:
        return jsonify({"error": "uid is required"}), 400

    profiles = _load_profiles()
    uid = data['uid']
    linkedin = data.get('linkedin', '')
    github = data.get('github', '')
    task_count = int(data.get('task_count', 0))

    profiles[uid] = {
        "uid": uid,
        "name": data.get('name', ''),
        "age": data.get('age', ''),
        "email": data.get('email', ''),
        "linkedin": linkedin,
        "github": github,
        "bio": data.get('bio', ''),
        "achievements": data.get('achievements', ''),
        "goal": data.get('goal', 'learn'),
        "skills": data.get('skills', []),
        "approved_skills": data.get('approved_skills', []),
        "task_count": task_count,
        "badge": compute_badge(task_count, linkedin, github),
        "onboarded": True
    }

    _save_profiles(profiles)
    return jsonify({"success": True, "profile": profiles[uid]}), 201


@auth_bp.route('/profile/<uid>/approve', methods=['POST'])
def approve_skill(uid):
    """Mark a skill as quiz-approved (NOT a badge – that's earned via tasks)."""
    data = request.get_json()
    skill = data.get('skill')
    score = data.get('score', 0)

    profiles = _load_profiles()
    if uid not in profiles:
        return jsonify({"error": "Profile not found"}), 404

    profile = profiles[uid]
    approved = profile.setdefault('approved_skills', [])
    if skill and skill not in approved:
        approved.append(skill)
    _save_profiles(profiles)
    return jsonify({"success": True, "approved_skills": approved,
                    "message": f"'{skill}' skill approved (score {score}%). Badge is earned via task completion."})


@auth_bp.route('/profile/<uid>/task-complete', methods=['POST'])
def complete_task(uid):
    """Increment task_count and recalculate badge tier."""
    profiles = _load_profiles()
    if uid not in profiles:
        return jsonify({"error": "Profile not found"}), 404

    profile = profiles[uid]
    profile['task_count'] = profile.get('task_count', 0) + 1
    tc = profile['task_count']
    profile['badge'] = compute_badge(tc, profile.get('linkedin', ''), profile.get('github', ''))
    _save_profiles(profiles)

    return jsonify({
        "success": True,
        "task_count": tc,
        "badge": profile['badge'],
        "message": f"Task #{tc} complete! Badge: {profile['badge'] or 'None yet'}"
    })
