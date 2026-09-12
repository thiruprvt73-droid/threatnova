from fastapi import APIRouter
from pydantic import BaseModel
from typing import List


router = APIRouter(
    prefix="/gamification",
    tags=["Gamification"]
)


# -----------------------------
# Data Models
# -----------------------------

class Scenario(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    points: int


class Achievement(BaseModel):
    id: int
    name: str
    description: str
    points: int


class EducationalContent(BaseModel):
    id: int
    title: str
    category: str
    description: str


# -----------------------------
# Sample Learning Scenarios
# -----------------------------

scenarios = [
    {
        "id": 1,
        "title": "Phishing Email Challenge",
        "description": "Identify whether a suspicious email is a phishing attempt.",
        "difficulty": "Beginner",
        "points": 100
    },
    {
        "id": 2,
        "title": "Malware Detection",
        "description": "Analyze system behavior and identify possible malware activity.",
        "difficulty": "Intermediate",
        "points": 200
    },
    {
        "id": 3,
        "title": "Network Intrusion",
        "description": "Analyze suspicious network traffic and identify an intrusion.",
        "difficulty": "Advanced",
        "points": 300
    }
]


# -----------------------------
# Achievements
# -----------------------------

achievements = [
    {
        "id": 1,
        "name": "First Challenge",
        "description": "Complete your first security challenge.",
        "points": 100
    },
    {
        "id": 2,
        "name": "Cyber Defender",
        "description": "Complete 5 security challenges.",
        "points": 500
    },
    {
        "id": 3,
        "name": "Threat Hunter",
        "description": "Complete an advanced threat simulation.",
        "points": 1000
    }
]


# -----------------------------
# Educational Content
# -----------------------------

educational_content = [
    {
        "id": 1,
        "title": "Phishing Attacks",
        "category": "Threat Encyclopedia",
        "description": "Learn how phishing attacks work and how to identify them."
    },
    {
        "id": 2,
        "title": "Password Security",
        "category": "Best Practices",
        "description": "Learn best practices for creating and protecting passwords."
    },
    {
        "id": 3,
        "title": "Ransomware Case Study",
        "category": "Real-World Case Study",
        "description": "Study how ransomware attacks affect organizations."
    },
    {
        "id": 4,
        "title": "Cybersecurity Fundamentals",
        "category": "Certification Pathway",
        "description": "Begin your cybersecurity learning pathway."
    }
]


# -----------------------------
# API Endpoints
# -----------------------------

@router.get("/scenarios")
async def get_scenarios():
    return {
        "total": len(scenarios),
        "scenarios": scenarios
    }


@router.get("/scenarios/{scenario_id}")
async def get_scenario(scenario_id: int):
    for scenario in scenarios:
        if scenario["id"] == scenario_id:
            return scenario

    return {
        "error": "Scenario not found"
    }


@router.get("/achievements")
async def get_achievements():
    return {
        "total": len(achievements),
        "achievements": achievements
    }


@router.get("/leaderboard")
async def get_leaderboard():
    return {
        "leaderboard": [
            {
                "rank": 1,
                "username": "CyberMaster",
                "points": 2500
            },
            {
                "rank": 2,
                "username": "ThreatHunter",
                "points": 2100
            },
            {
                "rank": 3,
                "username": "CyberDefender",
                "points": 1800
            }
        ]
    }


@router.get("/education")
async def get_educational_content():
    return {
        "total": len(educational_content),
        "content": educational_content
    }


@router.get("/education/{content_id}")
async def get_educational_item(content_id: int):
    for item in educational_content:
        if item["id"] == content_id:
            return item

    return {
        "error": "Educational content not found"
    }