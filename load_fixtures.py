import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyjobs.models.models import Candidate, Hirer, Job, Recruiter, Location, Skill

fake = Faker()


def load_skills(session):
    skills = [
        "Python",
        "JavaScript",
        "Node.js",
        "Vue.js",
        "Java",
        "Erlang",
        "Docker",
        "PostgreSQL",
        "MongoDB",
        "AWS",
        "Azure",
        "GCP",
        "Django",
        "Flask",
        "FastAPI",
        "SQLAlchemy",
    ]
    skills = [Skill(name=skill) for skill in skills]

    for skill in skills:
        session.add(skill)

    return skills


def load_jobs(skills, session):
    for _ in range(500):
        rate = random.randint(500, 5000)
        job = Job(
            title=fake.job(),
            rate=rate,
            rate_per_time_unit="hour",
            rate_annualized=rate * 8 * 255,
            contract_type=random.choice(["contract", "permanent"]),
            location_id=1,
            hirer_id=1,
            recruiter_id=1,
            description="Being a cool Python tech lead",
            live_until=datetime.utcnow() + timedelta(days=random.randint(10, 60)),
            skills=[skills[random.randint(0, 15)] for _ in range(5)],
        )

        session.add(job)


def load_candidates(skills, session):
    candidate1 = Candidate(
        name="Wow Whew",
        email="wow.whew@gmail.com",
        location_id=1,
        skills=[skills[random.randint(0, 15)] for _ in range(5)],
    )
    candidate2 = Candidate(
        name="Joe Whey",
        email="joe.whew@gmail.com",
        location_id=1,
        skills=[skills[random.randint(0, 15)] for _ in range(5)],
    )

    session.add(candidate1)
    session.add(candidate2)


def load_fixtures():
    session_maker = sessionmaker(bind=create_engine("sqlite:///database.db"))
    location = Location(city="London", country="UK")
    hirer = Hirer(name="PyJobs.works")
    recruiter = Recruiter(name="Joe Wow", email="joe@pyjobs.works")

    with session_maker(expire_on_commit=False) as session:
        skills = load_skills(session)

        session.add(location)
        session.add(hirer)

        recruiter.hirer = hirer
        session.add(recruiter)

        session.commit()

        load_candidates(skills, session)
        load_jobs(skills, session)

        session.commit()


load_fixtures()
