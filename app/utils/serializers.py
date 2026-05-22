def serialize_enum(value):
    """Return enum value for JSON response."""
    return value.value if value else None


def serialize_date(value):
    """Return ISO formatted date/datetime for JSON response."""
    return value.isoformat() if value else None


def serialize_application(application):
    """Serialize JobApplication model into API-friendly dictionary."""
    return {
        "id": application.id,
        "company_name": application.company_name,
        "role_title": application.role_title,
        "job_url": application.job_url,
        "location": application.location,
        "work_mode": serialize_enum(application.work_mode),
        "employment_type": serialize_enum(application.employment_type),
        "salary_min": application.salary_min,
        "salary_max": application.salary_max,
        "source": application.source,
        "status": serialize_enum(application.status),
        "priority": serialize_enum(application.priority),
        "deadline": serialize_date(application.deadline),
        "date_saved": serialize_date(application.date_saved),
        "date_applied": serialize_date(application.date_applied),
        "job_description": application.job_descritpion,
        "resume_notes": application.resume_notes,
        "notes": application.notes,
        "created_at": serialize_date(application.created_at),
        "updated_at": serialize_date(application.updated_at),
    }