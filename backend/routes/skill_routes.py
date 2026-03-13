"""
Skill Share, Borrow, and Courses Routes
"""
from flask import Blueprint, request, jsonify
import json, os, uuid
from datetime import datetime

skill_bp = Blueprint('skill', __name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def _load(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []


def _save(filename, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, filename), 'w') as f:
        json.dump(data, f, indent=2)


# ── SKILL SHARE (Free) ────────────────────────────────────────────────────────

@skill_bp.route('/skill-share', methods=['GET'])
def get_posts():
    posts = _load('posts.json')
    skill_filter = request.args.get('skill', '').lower()
    if skill_filter:
        posts = [p for p in posts if skill_filter in p.get('skill', '').lower()]
    return jsonify(sorted(posts, key=lambda x: x['created_at'], reverse=True))


@skill_bp.route('/skill-share', methods=['POST'])
def create_post():
    data = request.get_json()
    posts = _load('posts.json')
    post = {
        "id": str(uuid.uuid4()),
        "author": data.get('author', 'Anonymous'),
        "author_uid": data.get('uid', ''),
        "avatar": data.get('avatar', ''),
        "skill": data.get('skill', 'General'),
        "title": data.get('title', ''),
        "content": data.get('content', ''),
        "type": data.get('type', 'share'),  # 'share' | 'question' | 'tip'
        "tags": data.get('tags', []),
        "likes": 0,
        "replies": [],
        "created_at": datetime.utcnow().isoformat()
    }
    posts.append(post)
    _save('posts.json', posts)
    return jsonify(post), 201


@skill_bp.route('/skill-share/<post_id>/reply', methods=['POST'])
def add_reply(post_id):
    data = request.get_json()
    posts = _load('posts.json')
    for post in posts:
        if post['id'] == post_id:
            reply = {"author": data.get('author', 'Anonymous'),
                     "content": data.get('content', ''),
                     "created_at": datetime.utcnow().isoformat()}
            post['replies'].append(reply)
            _save('posts.json', posts)
            return jsonify(reply), 201
    return jsonify({"error": "Post not found"}), 404


# ── BORROW SKILL (Paid) ───────────────────────────────────────────────────────

@skill_bp.route('/borrow', methods=['GET'])
def get_projects():
    projects = _load('projects.json')
    return jsonify(sorted(projects, key=lambda x: x['created_at'], reverse=True))


@skill_bp.route('/borrow', methods=['POST'])
def post_project():
    data = request.get_json()
    projects = _load('projects.json')
    project = {
        "id": str(uuid.uuid4()),
        "client": data.get('client', 'Anonymous'),
        "client_uid": data.get('uid', ''),
        "title": data.get('title', ''),
        "description": data.get('description', ''),
        "skill_needed": data.get('skill_needed', ''),
        "budget": data.get('budget', ''),
        "duration": data.get('duration', ''),
        "status": "open",
        "bids": [],
        "created_at": datetime.utcnow().isoformat()
    }
    projects.append(project)
    _save('projects.json', projects)
    return jsonify(project), 201


@skill_bp.route('/borrow/<project_id>/bid', methods=['POST'])
def place_bid(project_id):
    data = request.get_json()
    projects = _load('projects.json')
    for project in projects:
        if project['id'] == project_id:
            bid = {"bidder": data.get('bidder', ''),
                   "bidder_uid": data.get('uid', ''),
                   "amount": data.get('amount', ''),
                   "message": data.get('message', ''),
                   "created_at": datetime.utcnow().isoformat()}
            project['bids'].append(bid)
            _save('projects.json', projects)
            return jsonify(bid), 201
    return jsonify({"error": "Project not found"}), 404


# ── COURSES / LEARN (Paid) ────────────────────────────────────────────────────

SEED_COURSES = [
    {"id": "c1", "title": "Python Mastery: Zero to Hero", "instructor": "Priya Sharma", "skill": "Python",
     "price": 1499, "rating": 4.8, "students": 1240, "duration": "24 hours", "level": "Beginner",
     "thumbnail": "🐍", "description": "Complete Python course covering basics to advanced OOP and projects."},
    {"id": "c2", "title": "JavaScript & React Complete Guide", "instructor": "Arjun Mehta", "skill": "JavaScript",
     "price": 1999, "rating": 4.7, "students": 980, "duration": "30 hours", "level": "Intermediate",
     "thumbnail": "⚛️", "description": "Build real-world apps with modern JS and React ecosystem."},
    {"id": "c3", "title": "UI/UX Design Fundamentals", "instructor": "Sneha Patel", "skill": "Design",
     "price": 1299, "rating": 4.9, "students": 760, "duration": "18 hours", "level": "Beginner",
     "thumbnail": "🎨", "description": "Learn Figma, design systems, user research and prototyping."},
    {"id": "c4", "title": "Machine Learning with Python", "instructor": "Rahul Verma", "skill": "Machine Learning",
     "price": 2499, "rating": 4.6, "students": 540, "duration": "36 hours", "level": "Advanced",
     "thumbnail": "🤖", "description": "Practical ML: regression, classification, neural networks, deployment."},
    {"id": "c5", "title": "Digital Marketing Mastery", "instructor": "Kavya Nair", "skill": "Marketing",
     "price": 999, "rating": 4.5, "students": 330, "duration": "15 hours", "level": "Beginner",
     "thumbnail": "📈", "description": "SEO, social media, content strategy and paid ads from scratch."},
    {"id": "c6", "title": "Java Backend Development", "instructor": "Vikram Singh", "skill": "Java",
     "price": 1799, "rating": 4.7, "students": 420, "duration": "28 hours", "level": "Intermediate",
     "thumbnail": "☕", "description": "Build REST APIs and enterprise apps with Java and Spring Boot."},
]


@skill_bp.route('/courses', methods=['GET'])
def get_courses():
    courses = _load('courses.json')
    if not courses:
        _save('courses.json', SEED_COURSES)
        courses = SEED_COURSES
    skill_filter = request.args.get('skill', '').lower()
    if skill_filter:
        courses = [c for c in courses if skill_filter in c.get('skill', '').lower()]
    return jsonify(courses)


@skill_bp.route('/courses/<course_id>/request_session', methods=['POST'])
def request_course_session(course_id):
    data = request.get_json()
    return jsonify({
        "success": True,
        "message": "✅ Session Access Granted! Your community post has been created for the session.",
        "course_id": course_id,
        "uid": data.get('uid', '')
    })
