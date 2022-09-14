import uuid
from datetime import datetime, date
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import conint
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from pyjobs.models.models import Job, Skill, Location, JobApplication
from pyjobs.web.api.schemas import GetJobSchema, ListJobsSchema, CreateJobSchema, ContractTypeEnum, SortByEnum, \
    SortByOrder, AmountPerTimeEnum, ListSkills, ListLocations, GetJobApplication, ListJobApplications, \
    CreateJobApplication

session_maker = sessionmaker(bind=create_engine("sqlite:///database.db"))

router = APIRouter()


@router.get("/skills", response_model=ListSkills)
async def get_skills(
        page: conint(ge=1) = 1,
        perPage: conint(ge=1, le=100) = 1,
        sortByOrder: SortByOrder = SortByOrder.ascending,
):
    with session_maker() as session:
        query = session.query(Skill)
        sorting_order = desc if sortByOrder.value == SortByOrder.descending.value else asc
        skills = query.order_by(sorting_order(Skill.name))
        offset = (page - 1) * perPage if page > 1 else None
    return {
        "skills": [skill.dict() for skill in skills.limit(perPage).offset(offset)],
        "pages": skills.count() / perPage,
    }


@router.get("/locations", response_model=ListLocations)
async def get_locations(
        page: conint(ge=1) = 1,
        perPage: conint(ge=1, le=100) = 1,
        sortByOrder: SortByOrder = SortByOrder.ascending,
):
    with session_maker() as session:
        query = session.query(Location)
        sorting_order = desc if sortByOrder.value == SortByOrder.descending.value else asc
        locations = query.order_by(sorting_order(Location.country)).order_by(sorting_order(Location.city))
        offset = (page - 1) * perPage if page > 1 else None
    return {
        "locations": [location.dict() for location in locations.limit(perPage).offset(offset)],
        "pages": locations.count() / perPage,
    }


@router.post("/applications", response_model=GetJobApplication)
async def apply_for_job(request: Request, job: CreateJobApplication):
    with session_maker() as session:
        application = JobApplication(
            candidate_id=request.state.user_id or 1,
            job_listing_id=job.job_id,
        )
        session.add(application)
        session.commit()
        return application.dict()


@router.get("/applications", response_model=ListJobApplications)
async def list_applications(
        page: conint(ge=1) = 1,
        perPage: conint(ge=1, le=100) = 1,
        sortByOrder: SortByOrder = SortByOrder.ascending,
):
    with session_maker() as session:
        query = session.query(JobApplication)
        sorting_order = desc if sortByOrder.value == SortByOrder.descending.value else asc
        applications = query.order_by(sorting_order(JobApplication.created))
        offset = (page - 1) * perPage if page > 1 else None
    return {
        "applications": [application.dict() for application in applications.limit(perPage).offset(offset)],
        "pages": applications.count() / perPage,
    }


@router.get("/applications/{application_id}", response_model=GetJobApplication)
async def get_application(application_id: int, request: Request):
    with session_maker() as session:
        application = session.query(JobApplication).filter(
            JobApplication.id == application_id,
            JobApplication.candidate_id == request.state.user_id
        ).first()
        if application is None:
            raise HTTPException(
                status_code=404,
                detail=f"Job application with ID {application_id} not Found",
            )
        return application.dict()


@router.post("/applications/{application_id}/cancel", response_model=GetJobApplication)
async def cancel_application(application_id: int, request: Request):
    with session_maker() as session:
        application = session.query(JobApplication).filter(
            JobApplication.id == application_id,
            JobApplication.candidate_id == request.state.user_id
        ).first()
        if application is None:
            raise HTTPException(
                status_code=404,
                detail=f"Job application with ID {application_id} not Found",
            )
        application.cancelled = True
        session.commit()
        return application.dict()


@router.get("/jobs", response_model=ListJobsSchema)
async def get_jobs(
        dateSincePosted: Optional[date] = None,
        contractType: Optional[ContractTypeEnum] = None,
        page: conint(ge=1) = 1,
        perPage: conint(ge=1, le=100) = 1,
        sortBy: SortByEnum = SortByEnum.datePosted,
        sortByOrder: SortByOrder = SortByOrder.descending,
):
    with session_maker() as session:
        query = session.query(Job)
        if dateSincePosted:
            query = query.filter(Job.date_posted >= dateSincePosted)
        if contractType:
            query = query.filter(Job.contract_type == contractType.value)
        sort_by_order = desc if sortByOrder.value == SortByOrder.descending.value else asc
        sort_by = getattr(Job, "date_posted") if sortBy == SortByEnum.datePosted else getattr(Job, "rate_annualized")
        jobs = query.order_by(sort_by_order(sort_by))
        offset = (page - 1) * perPage if page > 1 else None
    return {
        "jobs": [job.dict() for job in jobs.limit(perPage).offset(offset)],
        "pages": jobs.count() / perPage,
    }


def calculate_annualized_rate(rate, per_time):
    if per_time == AmountPerTimeEnum.hour.value:
        # assume 255 working days in a year
        return rate * 8 * 255
    elif per_time == AmountPerTimeEnum.month.value:
        # assume 11 working months
        return rate * 11
    elif per_time == AmountPerTimeEnum.year.value:
        return rate
    else:
        raise Exception("Invalid amount per time")


@router.post("/jobs", response_model=GetJobSchema, status_code=status.HTTP_201_CREATED)
async def create_job(job_details: CreateJobSchema):
    with session_maker() as session:
        job = Job(
            hirer_id=1,
            recruiter_id=1,
            title=job_details.title,
            rate=job_details.rate.amount,
            rate_per_time_unit=job_details.rate.amountPerTime,
            rate_annualized=calculate_annualized_rate(
                job_details.rate.amount, job_details.rate.amountPerTime
            ),
            benefits=job_details.benefits,
            contract_type=job_details.contractType,
            description=job_details.description,
            date_posted=datetime.today().date(),
            live_until=job_details.liveUntil,
            location_id=job_details.location,
            skills=session.query(Skill).filter(
                Skill.id.in_(job_details.skills)
            ).all()
        )
        session.commit()
        return job.dict()


@router.get("/jobs/{job_id}", response_model=GetJobSchema)
async def get_job(job_id: int):
    with session_maker() as session:
        job = session.query(Job).filter(Job.id == job_id).first()
        if job:
            return job.dict()
    raise HTTPException(
        status_code=404, detail=f"Job listing with ID {job_id} not found"
    )


@router.put("/jobs/{job_id}", response_model=GetJobSchema)
async def update_job(job_id: int, job_details: CreateJobSchema):
    with session_maker() as session:
        job = session.query(Job).filter(Job.id == job_id).first()
        if job is None:
            raise HTTPException(
                status_code=404, detail=f"Job listing with ID {job_id} not found"
            )
        job.title = job_details.title,
        job.contract_type = job_details.contractType
        job.rate = job_details.rate.amount,
        job.rate_per_time_unit = job_details.rate.amountPerTime,
        job.rate_annualized = calculate_annualized_rate(
            job_details.rate.amount, job_details.rate.amountPerTime
        )
        job.benefits = job_details.benefits,
        job.location_id = job_details.location,
        job.description = job_details.description,
        job.hirer_id = job_details.hirer,
        job.live_until = job_details.liveUntil
        job.skills = session.query(Skill).filter(
            Skill.id.in_(job_details.skills)
        ).all()
        session.commit()
        return job.dict()


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_job(job_id: uuid.UUID):
    with session_maker() as session:
        job = session.query(Job).filter(Job.id == job_id)
        if job is None:
            raise HTTPException(
                status_code=404, detail=f"Job listing with ID {job_id} not found"
            )
        session.delete(job)
        session.commit()
        return job.dict()


@router.post("/jobs/{job_id}/cancel", response_model=GetJobSchema, status_code=status.HTTP_201_CREATED)
async def cancel_job(job_id: uuid.UUID):
    with session_maker() as session:
        job = session.query(Job).filter(Job.id == job_id)
        if job is None:
            raise HTTPException(
                status_code=404, detail=f"Job listing with ID {job_id} not found"
            )
        job.visible = False
        session.commit()
        return job.dict()


@router.post("/jobs/{job_id}/reactivate", response_model=GetJobSchema, status_code=status.HTTP_201_CREATED)
async def reactivate_job(job_id: uuid.UUID):
    with session_maker() as session:
        job = session.query(Job).filter(Job.id == job_id)
        if job is None:
            raise HTTPException(
                status_code=404, detail=f"Job listing with ID {job_id} not found"
            )
        job.visible = True
        session.commit()
        return job.dict()


# job applications endpoints for recruiters
@router.get("/jobs/{job_id}/applications")
async def list_job_applications():
    pass
