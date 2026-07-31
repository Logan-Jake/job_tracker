from sqlalchemy import Column, BigInteger, Text, Numeric, Boolean, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class AdzunaJob(Base):
    __tablename__ = "adzuna_jobs"
    id                  = Column(BigInteger, primary_key=True)
    title               = Column(Text, nullable=False)
    description         = Column(Text)
    company_name        = Column(Text)
    salary_min          = Column(Numeric(10, 2))
    salary_max          = Column(Numeric(10, 2))
    salary_is_predicted = Column(Boolean)
    contract_type       = Column(Text)
    contract_time       = Column(Text)
    category_label      = Column(Text)
    latitude            = Column(Numeric(9, 6))
    longitude           = Column(Numeric(9, 6))
    location_display    = Column(Text)
    location_area       = Column(Text)
    redirect_url        = Column(Text)
    adref               = Column(Text)
    is_active           = Column(Boolean, server_default="true")
    created             = Column(TIMESTAMP(timezone=True))
    last_seen_at        = Column(TIMESTAMP(timezone=True), server_default=func.now())
    inserted_at         = Column(TIMESTAMP(timezone=True), server_default=func.now())