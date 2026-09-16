"""Seed core website data (services, packages, testimonials, team, FAQs) into PostgreSQL.

Blog content is not seeded here — it's scattered across several legacy
Mongo-only scripts (seed_blogs*.py) with overlapping/placeholder entries and
needs a separate cleanup pass before it can be migrated.

Run after `alembic upgrade head`:
    venv\\Scripts\\python.exe seed_postgres.py
"""
import asyncio

from sqlalchemy import delete

from database import AsyncSessionLocal
from models.orm import FAQ, Package, Service, TeamMember, Testimonial

services_data = [
    {
        "id": "1",
        "title": "Foundational Agreements",
        "subtitle": "Don't Just Plan a Wedding. Design Your Future.",
        "description": "Build a solid foundation with clear agreements on finances, roles, and responsibilities. Start your partnership with transparency and mutual understanding.",
        "icon": "Building2",
        "video_url": "https://videos.pexels.com/video-files/7233822/7233822-uhd_2560_1440_25fps.mp4",
        "full_description": "Our Foundational Agreements service helps couples establish clear expectations and understandings before marriage. Through structured sessions, we guide you in creating agreements around financial management, household responsibilities, career priorities, and life goals. This service ensures both partners enter marriage with aligned expectations and a shared vision for their future together.",
    },
    {
        "id": "2",
        "title": "Constructive Dialogue Toolkit",
        "subtitle": "Master the Language of a Lasting Partnership.",
        "description": "Learn proven communication strategies, conflict resolution techniques, and emotional intelligence tools to navigate challenges together with grace.",
        "icon": "MessagesSquare",
        "video_url": "https://videos.pexels.com/video-files/5533921/5533921-uhd_2560_1440_25fps.mp4",
        "full_description": "The Constructive Dialogue Toolkit equips couples with essential communication skills for a healthy relationship. Learn active listening techniques, non-violent communication strategies, and conflict de-escalation methods. We provide practical frameworks for expressing needs, handling disagreements, and maintaining emotional connection even during challenging times.",
    },
    {
        "id": "3",
        "title": "Family Integration Strategy",
        "subtitle": "Two Individuals. Two Families. One Harmonious Future.",
        "description": "Navigate the complexities of merging families with structured conversations about boundaries, traditions, and shared expectations.",
        "icon": "Users",
        "video_url": "https://videos.pexels.com/video-files/6893882/6893882-uhd_2560_1440_25fps.mp4",
        "full_description": "Family Integration Strategy addresses the often-challenging aspects of merging two families. We facilitate conversations about family boundaries, festival planning, living arrangements, and parental expectations. Learn how to honor both families while prioritizing your partnership and creating your own family traditions.",
    },
]

packages_data = [
    {
        "id": "1",
        "name": "Saamanjasya",
        "subtitle": "Foundational",
        "sessions": 3,
        "price": "₹15,000",
        "description": "Core clarity on money, roles, and communication; structured takeaways.",
        "ideal": "Ideal for couples seeking guided conversations on financial planning, conflict resolution, and family dynamics.",
        "features": [
            "3 Guided Sessions (90 mins each)",
            "Financial Planning Framework",
            "Communication Basics",
            "Conflict Resolution Starter Kit",
            "Digital Workbook",
        ],
        "popular": False,
    },
    {
        "id": "2",
        "name": "Sammati",
        "subtitle": "Consent & Clarity",
        "sessions": 5,
        "price": "₹28,000",
        "description": "Deeper alignment across finances, careers, family dynamics, intimacy & boundaries; draft Partnership Accord.",
        "ideal": "Insightful exploration of emotional expectations, conflict management, parenting perspectives, and shared responsibilities.",
        "features": [
            "5 Guided Sessions (90 mins each)",
            "Draft Partnership Accord",
            "Financial Strategy Deep Dive",
            "Intimacy & Boundaries Module",
            "Career Alignment Framework",
            "Family Dynamics Playbook",
        ],
        "popular": True,
    },
    {
        "id": "3",
        "name": "Sankalp",
        "subtitle": "Commitment & Alignment",
        "sessions": 8,
        "price": "₹45,000",
        "description": "Comprehensive partnership readiness and alignment journey integrating emotional intelligence, financial strategy, conflict resilience, and long-term planning.",
        "ideal": "Ideal for couples preparing for marriage, cohabitation, or long-term partnership who want to translate shared values into enduring practices.",
        "features": [
            "8 Comprehensive Sessions (90 mins each)",
            "Signed Partnership Accord",
            "Complete Financial Strategy",
            "Emotional Intelligence Training",
            "Conflict Resilience Toolkit",
            "Long-term Planning Framework",
            "3-Month Follow-up Session",
            "Lifetime Access to Resources",
        ],
        "popular": False,
    },
]

testimonials_data = [
    {
        "id": 1,
        "name": "Amrita & Rohan",
        "role": "Client",
        "content": "Kaushal helped us discuss topics we never even considered. We feel more confident stepping into marriage.",
        "rating": 5,
        "image": "https://images.pexels.com/photos/2788488/pexels-photo-2788488.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&fit=crop",
    },
    {
        "id": 2,
        "name": "Meera & Karan",
        "role": "Client",
        "content": "The pre-marital mediation sessions brought us closer. We now have a clear plan for finances and family planning.",
        "rating": 5,
        "image": "https://images.pexels.com/photos/1024311/pexels-photo-1024311.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&fit=crop",
    },
    {
        "id": 3,
        "name": "Aryan & Neha",
        "role": "Client",
        "content": "Kaushal taught us how to handle conflicts without letting them fester. It's been a game-changer for our relationship.",
        "rating": 5,
        "image": "https://images.pexels.com/photos/3585325/pexels-photo-3585325.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&fit=crop",
    },
    {
        "id": 4,
        "name": "Priya & Aditya",
        "role": "Client",
        "content": "The Partnership Accord has become our reference guide. It's helped us navigate the first year of marriage with confidence and clarity.",
        "rating": 5,
        "image": "https://images.pexels.com/photos/1415131/pexels-photo-1415131.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&fit=crop",
    },
]

team_data = [
    {
        "id": 1,
        "name": "Dr. Anjali Sharma",
        "role": "Lead Facilitator & Behavioral Expert",
        "description": "15+ years in relationship counseling and conflict resolution",
        "image": "https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&fit=crop",
    },
    {
        "id": 2,
        "name": "Rajiv Mehta",
        "role": "Financial Planning Specialist",
        "description": "Certified Financial Planner with expertise in couple's finances",
        "image": "https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&fit=crop",
    },
    {
        "id": 3,
        "name": "Priya Desai",
        "role": "Family Dynamics Mediator",
        "description": "Expert in intercultural relationships and family integration",
        "image": "https://images.pexels.com/photos/1181690/pexels-photo-1181690.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&fit=crop",
    },
    {
        "id": 4,
        "name": "Vikram Patel",
        "role": "Communication Coach",
        "description": "Specialized in emotional intelligence and effective dialogue",
        "image": "https://images.pexels.com/photos/1516680/pexels-photo-1516680.jpeg?auto=compress&cs=tinysrgb&w=400&h=400&fit=crop",
    },
]

faq_data = [
    {
        "id": 1,
        "question": "What does 'Kaushal - it's a skill' really mean?",
        "answer": "Kaushal translates to 'skill' — we believe partnership is not luck, but a practiced skill. Our sessions equip couples with emotional, financial, and relational tools to build sustainable harmony through conscious practice.",
    },
    {
        "id": 2,
        "question": "Is Kaushal therapy or counseling?",
        "answer": "Not exactly. Kaushal is a guided facilitation space, not a therapeutic or diagnostic one. Our facilitators combine behavioural frameworks, emotional intelligence tools, and structured discussions — so you learn to communicate, decide, and align better as partners.",
    },
    {
        "id": 3,
        "question": "How are the sessions structured?",
        "answer": "Each plan (3, 5, or 8 sessions) follows a guided conversation model with exercises, reflective prompts, and take-home frameworks. Every couple gets a dedicated facilitator who tracks their journey across sessions.",
    },
    {
        "id": 4,
        "question": "Are sessions confidential?",
        "answer": "Absolutely. All discussions and written materials remain private between the couple and facilitator. No recordings or data are shared externally.",
    },
    {
        "id": 5,
        "question": "Can we attend online?",
        "answer": "Yes, all sessions are offered virtually or in-person. Many couples prefer online for convenience.",
    },
    {
        "id": 6,
        "question": "What is a 'Partnership Accord'?",
        "answer": "It's a personalized document co-created through your sessions summarizing your agreements on communication, money, roles, conflict management, intimacy, and family boundaries. It's your shared blueprint for daily life.",
    },
    {
        "id": 7,
        "question": "What's the difference between the 3, 5, and 8-session plans?",
        "answer": "• Saamanjasya (3 sessions): builds foundational clarity. • Sammati (5 sessions): brings emotional and practical depth. • Sankalp (8 sessions): creates full readiness and a signed Partnership Accord with check-ins.",
    },
    {
        "id": 8,
        "question": "Who are these programs for?",
        "answer": "Couples at any stage - dating seriously, engaged, newly married, or cohabiting; who want to build clarity before commitment or reset and realign after.",
    },
    {
        "id": 9,
        "question": "What kind of results do couples see?",
        "answer": "Most couples report: • Fewer recurring arguments (within 4–6 weeks) • Better conversations around money and family • Greater emotional safety and mutual respect • A tangible sense of teamwork in daily life",
    },
    {
        "id": 10,
        "question": "Can we customize our plan?",
        "answer": "Yes, you can blend modules or extend to follow-up sessions depending on your readiness stage.",
    },
]


async def seed_all_data():
    async with AsyncSessionLocal() as db:
        print("Seeding core website data to PostgreSQL...")

        await db.execute(delete(Service))
        await db.execute(delete(Package))
        await db.execute(delete(Testimonial))
        await db.execute(delete(TeamMember))
        await db.execute(delete(FAQ))
        print("Cleared existing rows")

        db.add_all(Service(**row) for row in services_data)
        db.add_all(Package(**row) for row in packages_data)
        db.add_all(Testimonial(**row) for row in testimonials_data)
        db.add_all(TeamMember(**row) for row in team_data)
        db.add_all(FAQ(**row) for row in faq_data)

        await db.commit()

        print(f"  - Services: {len(services_data)}")
        print(f"  - Packages: {len(packages_data)}")
        print(f"  - Testimonials: {len(testimonials_data)}")
        print(f"  - Team Members: {len(team_data)}")
        print(f"  - FAQs: {len(faq_data)}")
        print("Done. (Blogs not seeded — see module docstring.)")


if __name__ == "__main__":
    asyncio.run(seed_all_data())
