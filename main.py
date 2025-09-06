from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from exceptions.handlers import sqlalchemy_exception_handler, validation_exception_handler
from sqlalchemy.exc import IntegrityError
from settings.database import Base, engine
from router import product, brand, category

app = FastAPI(title='Products API')



# Register handler global
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, sqlalchemy_exception_handler)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)



# Router Register
app.include_router(product.router)
app.include_router(brand.router)
app.include_router(category.router)

@app.get('/')
def root():
    return {
        "message": "Products API running 🚀"
    }
