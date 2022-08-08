from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.testing.schema import Table

Base = declarative_base()


skills_job_association = Table(
    "skills_job_association",
    Base.metadata,
    Column("skill", ForeignKey("skill.id"), nullable=False),
    Column("job", ForeignKey("job.id"), nullable=False),
    Column("created", DateTime, nullable=False, default=datetime.utcnow),
    Column("updated", DateTime, nullable=False, default=datetime.utcnow),
)


skills_candidate_association = Table(
    "skills_candidate_association",
    Base.metadata,
    Column("skill", ForeignKey("skill.id"), nullable=False),
    Column("candidate", ForeignKey("candidate.id"), nullable=False),
    Column("years_experience", type_=Integer),
    Column("created", DateTime, nullable=False, default=datetime.utcnow),
    Column("updated", DateTime, nullable=False, default=datetime.utcnow),
)


class Location(Base):
    __tablename__ = "location"
    __table_args__ = (
        UniqueConstraint("city", "country", name="city_country_constraint"),
    )

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.utcnow)

    city = Column(String, nullable=False)
    state = Column(String)
    country = Column(String, nullable=False)

    def __str__(self):
        return (
            f"<Location: id={self.id}, created={self.created}, updated={self.updated},"
            f"city={self.city}, state={self.state}, country={self.country}>"
        )


class Recruiter(Base):
    __tablename__ = "recruiter"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.utcnow)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    contact_number = Column(String)
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

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.utcnow)

    name = Column(String, nullable=False)

    jobs = relationship("Job", back_populates="hirer")

    def __str__(self):
        return (
            f"<Hirer: id={self.id}, created={self.created}, updated={self.updated},"
            f"name={self.name}, jobs={str(self.jobs)}>"
        )


class Skill(Base):
    __tablename__ = "skill"
    __table_args__ = (
        UniqueConstraint("name", name="skill_name_constraint"),
    )

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.utcnow)

    name = Column(String, nullable=False)

    def __str__(self):
        return (
            f"<Skill: id={self.id}, created={self.created}, updated={self.updated}, name=self.{self.name}>"
        )


class Currency(Base):
    __tablename__ = "currency"
    __table_args__ = (
        UniqueConstraint("name", "symbol", name="currency_name_symbol_constraint"),
    )

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.utcnow)

    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)

    def __str__(self):
        return (
            f"<Currency: id={self.id}, created={self.created}, updated={self.updated},"
            f"name={self.name}, symbol={self.symbol}>"
        )


class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.utcnow)

    hirer_id = Column(Integer, ForeignKey("hirer.id"), nullable=False)
    recruiter_id = Column(Integer, ForeignKey("recruiter.id"), nullable=False)

    title = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    rate_currency_id = Column(Integer, ForeignKey("currency.id"), nullable=False)
    rate_per_time_unit = Column(String, nullable=False)
    rate_annualized = Column(Float, nullable=False)

    learning_budget = Column(Float)
    learning_budget_currency_id = Column(Integer, ForeignKey("currency.id"))
    benefits = Column(String)

    contract_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_posted = Column(Date, nullable=False, default=lambda: datetime.utcnow().date())
    live_until = Column(DateTime, nullable=False)
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)

    applications = relationship("JobApplication", back_populates="job_listing")
    hirer = relationship("Hirer", back_populates="jobs")
    recruiter = relationship("Recruiter", foreign_keys=[recruiter_id])
    rate_currency = relationship("Currency", foreign_keys=[rate_currency_id])
    learning_budget_currency = relationship("Currency", foreign_keys=[learning_budget_currency_id])
    location = relationship("Location", foreign_keys=[location_id])
    skills = relationship("Skill", secondary=skills_job_association)

    def __str__(self):
        return (
            f"<Job: id={self.id}, created={self.created}, updated={self.updated},"
            f"hirer_id={self.hirer_id}, recruiter_id={self.recruiter_id}, title={self.title},"
            f"rate={self.rate}, rate_currency_id={self.rate_currency_id}, "
            f"rate_per_time_unit={self.rate_per_time_unit}, rate_annualized={self.rate_annualized},"
            f"learning_budget={self.learning_budget}, learning_budget_currency_id={self.learning_budget_currency_id},"
            f"benefits={self.benefits}, contract_type={self.contract_type}, description={self.description},"
            f"date_posted={self.date_posted}, live_until={self.live_until}, location_id={self.location_id}>"
        )


class Candidate(Base):
    __tablename__ = "candidate"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.utcnow)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    contact_number = Column(String)
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

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.utcnow)

    candidate_id = Column(Integer, ForeignKey("candidate.id"), nullable=False)
    job_listing_id = Column(Integer, ForeignKey("job.id"), nullable=False)

    job_listing = relationship("Job", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")

    def __str__(self):
        return (
            f"<JobApplication: id={self.id}, created={self.created}, updated={self.updated},"
            f"candidate_id={self.candidate_id}, job_listing_id={self.job_listing_id}>"
        )
