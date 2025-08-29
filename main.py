from fastapi import FastAPI
from settings.database import Base, engine
from router import product, brand, category

app = FastAPI(title='Products API')


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
