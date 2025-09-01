from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()


    # Si el body existe pero faltan campos específicos
    missing_fields = []
    for e in errors:
        if e["type"] == "missing" and len(e["loc"]) > 1:
            missing_fields.append(e["loc"][-1])

    if missing_fields:
        return JSONResponse(
            status_code=422,
            content={
                "error": "Missing required fields",
                "required_fields": missing_fields,
            },
        )

    # Caso genérico
    return JSONResponse(status_code=422, content={"detail": errors})

async def sqlalchemy_exception_handler(request: Request, exc: IntegrityError):
    if isinstance(exc.orig, UniqueViolation):
        return JSONResponse(
            status_code=400,
            content={
                "error": "Duplicate entry",
                "detail": str(exc.orig).strip(),
            },
        )

    return JSONResponse(
        status_code=400,
        content={
            "error": "Database integrity error",
            "detail": str(exc.orig).strip(),
        },
    )


