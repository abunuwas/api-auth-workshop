from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime, Float, UniqueConstraint, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.testing.schema import Table


class Base:
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.utcnow)


Base = declarative_base(cls=Base)


skills_job_association = Table(
    "skills_job_association",
    Base.metadata,
    Column("skill", ForeignKey("skill.id"), nullable=False),
    Column("job", ForeignKey("job.id"), nullable=False),
)


skills_candidate_association = Table(
    "skills_candidate_association",
    Base.metadata,
    Column("skill", ForeignKey("skill.id"), nullable=False),
    Column("candidate", ForeignKey("candidate.id"), nullable=False),
    Column("years_experience", type_=Integer),
)


class Location(Base):
    __tablename__ = "location"
    __table_args__ = (
        UniqueConstraint("city", "country", name="city_country_constraint"),
    )

    city = Column(String, nullable=False)
    state = Column(String)
    country = Column(String, nullable=False)

    def dict(self):
        return {
            "id": self.id,
            "city": self.city,
            "state": self.state,
            "country": self.country,
        }

    def __str__(self):
        return (
            f"<Location: id={self.id}, created={self.created}, updated={self.updated},"
            f"city={self.city}, state={self.state}, country={self.country}>"
        )


class Skill(Base):
    __tablename__ = "skill"
    __table_args__ = (
        UniqueConstraint("name", name="skill_name_constraint"),
    )

    name = Column(String, nullable=False)

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def __str__(self):
        return (
            f"<Skill: id={self.id}, created={self.created}, updated={self.updated}, name=self.{self.name}>"
        )


class Recruiter(Base):
    __tablename__ = "recruiter"

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hirer_id = Column(Integer, ForeignKey("hirer.id"), nullable=False)

    hirer = relationship("Hirer", foreign_keys=[hirer_id])

    def __str__(self):
        return (
            f"<Recruiter: id={self.id}, created={self.created}, updated={self.updated},"
            f"first_name={self.first_name}, last_name={self.last_name}, email={self.email},"
            f"contact_number={self.contact_number}, hirer_id={self.hirer_id}>"
        )


class Hirer(Base):
    __tablename__ = "hirer"

    name = Column(String, nullable=False)
    jobs = relationship("Job", back_populates="hirer")

    def __str__(self):
        return (
            f"<Hirer: id={self.id}, created={self.created}, updated={self.updated},"
            f"name={self.name}, jobs={str(self.jobs)}>"
        )


class Job(Base):
    __tablename__ = "job"

    hirer_id = Column(Integer, ForeignKey("hirer.id"), nullable=False)
    recruiter_id = Column(Integer, ForeignKey("recruiter.id"), nullable=False)

    title = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    rate_per_time_unit = Column(String, nullable=False)
    rate_annualized = Column(Float, nullable=False)
    benefits = Column(String)
    contract_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_posted = Column(Date, nullable=False, default=lambda: datetime.utcnow().date())
    live_until = Column(DateTime, nullable=False)
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    visible = Column(Boolean, nullable=False, default=True)

    applications = relationship("JobApplication", back_populates="job_listing")
    hirer = relationship("Hirer", back_populates="jobs")
    recruiter = relationship("Recruiter", foreign_keys=[recruiter_id])
    location = relationship("Location", foreign_keys=[location_id])
    skills = relationship("Skill", secondary=skills_job_association)

    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "rate": {
                "amount": self.rate,
                "amountPerTime": self.rate_per_time_unit,
            },
            "benefits": self.benefits or "",
            "contractType": self.contract_type,
            "description": self.description,
            "dateListed": self.date_posted,
            "liveUntil": self.live_until,
            "location": {
                "city": self.location.city,
                "state": self.location.state,
                "country": self.location.country,
            },
            "hirer": self.hirer.name,
            "recruiter": {
                "name": self.recruiter.name,
                "email": self.recruiter.email,
            },
            "skills": [skill.name for skill in self.skills]
        }

    def __str__(self):
        return (
            f"<Job: id={self.id}, created={self.created}, updated={self.updated},"
            f"hirer_id={self.hirer_id}, recruiter_id={self.recruiter_id}, title={self.title},"
            f"rate={self.rate}, rate_per_time_unit={self.rate_per_time_unit}, rate_annualized={self.rate_annualized},"
            f"benefits={self.benefits}, contract_type={self.contract_type}, description={self.description}, "
            f"date_posted={self.date_posted}, live_until={self.live_until}, location_id={self.location_id}>"
        )


class Candidate(Base):
    __tablename__ = "candidate"

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    cv = Column(String)
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)

    applications = relationship("JobApplication", back_populates="candidate")
    location = relationship("Location", foreign_keys=[location_id])
    skills = relationship("Skill", secondary=skills_candidate_association)

    def __str__(self):
        return (
            f"<Candidate: id={self.id}, created={self.created}, updated={self.updated},"
            f"first_name={self.first_name}, last_name={self.last_name}, email={self.email},"
            f"contact_number={self.contact_number}, cv={self.cv}, location_id={self.location_id}>"
        )


class JobApplication(Base):
    __tablename__ = "job_application"

    candidate_id = Column(Integer, ForeignKey("candidate.id"), nullable=False)
    job_listing_id = Column(Integer, ForeignKey("job.id"), nullable=False)
    cancelled = Column(Boolean, nullable=False, default=False)

    job_listing = relationship("Job", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")

    def dict(self):
        return {
            "id": self.id,
            "applied": self.created,
            "cancelled": self.cancelled,
            "job": self.job_listing.dict()
        }

    def __str__(self):
        return (
            f"<JobApplication: id={self.id}, created={self.created}, updated={self.updated},"
            f"candidate_id={self.candidate_id}, job_listing_id={self.job_listing_id}>"
        )
