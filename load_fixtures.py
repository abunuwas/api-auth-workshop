import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyjobs.models.models import Candidate, Hirer, Job, JobApplication, Recruiter, Location, Skill, Currency

fake = Faker()


def load_fixtures():
    session_maker = sessionmaker(bind=create_engine("sqlite:///database.db"))

    location = Location(city="London", country="UK")
    skills = [Skill(name=skill) for skill in ["FastAPI", "Python", "Docker"]]
    currency = Currency(name="US Dollar (USD)", symbol="$")
    hirer = Hirer(name="PyJobs.works")
    recruiter = Recruiter(first_name="Joe", last_name="Wow", email="joe@pyjobs.works")
    jobs = []
    for i in range(500):
        rate = fake.random_int()
        jobs.append(Job(
            title=fake.job(),
            rate=rate,
            rate_per_time_unit="hour",
            rate_annualized=rate * 8 * 255,
            contract_type=random.choice(["contract", "permanent"]),
            description="Being a cool Python tech lead",
            live_until=datetime.utcnow() + timedelta(days=30),
            skills=skills,
        ))
    candidate = Candidate(
        first_name="Wow",
        last_name="Whew",
        email="wow.whew@gmail.com",
        skills=skills,
    )

    with session_maker() as session:
        session.add(location)
        for skill in skills:
            session.add(skill)
        session.add(currency)
        session.add(hirer)

        recruiter.hirer = hirer
        session.add(recruiter)

        for job in jobs:
            job.rate_currency = currency
            job.location = location
            job.hirer = hirer
            job.recruiter = recruiter
            session.add(job)

        candidate.location = location
        session.add(candidate)

        for job in jobs:
            job_application = JobApplication()
            job_application.candidate = candidate
            job_application.job_listing = job
            session.add(job_application)

        session.commit()


load_fixtures()
