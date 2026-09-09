from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.controllers.course_controller import router as course_router
from app.controllers.enrollment_controller import router as enrollment_router
from app.controllers.user_controller import router as user_router
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.responses import create_response
from app.infrastructure.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if not settings.DATABASE_URL.startswith("sqlite"):
        try:
            init_db()
            print(" Banco de dados inicializado com sucesso!")
        except Exception as e:
            print(f"⚠️ Atenção ao inicializar banco: {e}")
            print("💡 Dica: Verifique se o PostgreSQL está ativo e as credenciais no .env estão corretas.")
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API RESTful para gerenciamento de Usuários, Cursos e Matrículas desenvolvida com Clean Architecture e Clean Code.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=create_response(
            success=False,
            message=exc.message,
            data=None,
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    error_messages = []
    for error in exc.errors():
        field = error.get("loc", ["field"])[-1]
        msg = error.get("msg", "Invalid value")
        error_messages.append(f"{field}: {msg}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=create_response(
            success=False,
            message="Validation error: " + "; ".join(error_messages),
            data=None,
        ),
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=create_response(
            success=False,
            message=str(exc.detail),
            data=None,
        ),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_response(
            success=False,
            message="Internal server error",
            data=None,
        ),
    )


app.include_router(user_router)
app.include_router(course_router)
app.include_router(enrollment_router)


@app.get("/", summary="Health check e boas-vindas", tags=["Root"])
def root() -> dict:
    return create_response(
        success=True,
        message="StudyManager API está funcionando perfeitamente!",
        data={"docs_url": "/docs"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
    )
