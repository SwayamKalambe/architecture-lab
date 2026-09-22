from fastapi import FastAPI
from monolith import (user_router,
                      products_router,
                      carts_router
                      )

app = FastAPI(title="Architecture Lab")

app.include_router(user_router)
app.include_router(products_router)
app.include_router(carts_router)


@app.get("/")
def cover_page():
    return "Welcome to Architecture Lab"