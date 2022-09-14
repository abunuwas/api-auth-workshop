from datetime import datetime, date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, confloat, conlist, conint, Extra, create_model


class AmountPerTimeEnum(Enum):
    hour = "hour"
    day = "day"
    month = "month"
    year = "year"


class Rate(BaseModel):
    amount: confloat(ge=1)
    amountPerTime: AmountPerTimeEnum


class Location(BaseModel):
    city: str
    state: Optional[str]
    country: str

    def dict(
        self,
        *args,
        **kwargs
    ) -> 'DictStrAny':
        kwargs["exclude_none"] = True
        return super().dict(*args, **kwargs)


class ContractTypeEnum(Enum):
    contract = "contract"
    permanent = "permanent"


class GetJobSchema(BaseModel):
    id: int
    title: str
    dateListed: date
    rate: Rate
    benefits: str
    location: Location
    hirer: str
    recruiter: create_model(
        "Recruiter", name=(str, ...), email=(str, ...)
    )
    contractType: ContractTypeEnum
    skills: conlist(str, min_items=1)
    liveUntil: datetime


class ListJobsSchema(BaseModel):
    jobs: list[GetJobSchema]
    pages: conint(ge=1)


class CreateJobSchema(BaseModel):
    title: str
    rate: Rate
    benefits: str
    location: int
    hirer: int
    contractType: ContractTypeEnum
    description: str
    skills: conlist(str, min_items=1)
    liveUntil: datetime


class SortByEnum(Enum):
    datePosted = "datePosted"
    rate = "rate"


class SortByOrder(Enum):
    ascending = "ascending"
    descending = "descending"


class GetSkill(BaseModel):
    id: int
    name: str


class ListSkills(BaseModel):
    skills: list[GetSkill]
    pages: int


class GetLocation(BaseModel):
    id: int
    city: str
    state: Optional[str]
    country: str

    def dict(
        self,
        *args,
        **kwargs
    ) -> 'DictStrAny':
        kwargs["exclude_none"] = True
        return super().dict(*args, **kwargs)


class ListLocations(BaseModel):
    locations: list[GetLocation]
    pages: int


class CreateJobApplication(BaseModel):
    job_id: int


class Candidate(BaseModel):
    id: int


class GetJobApplication(BaseModel):
    id: int
    job: GetJobSchema
    applied: date
    cancelled: bool


class ListJobApplications(BaseModel):
    applications: list[GetJobApplication]
    pages: int
