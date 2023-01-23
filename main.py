import binascii

from app.note.domain import InputNote
from app.note.domain.exceptions import NoteNotFound, EmptyNote, ExceededMaxNoteLength
from app.note.application import NoteEncrypter
from app.note.infrastructure import NoteController, DummyNoteRepository, RedisNoteRepository

from app.url.domain import InputUrl
from app.url.domain.exceptions import UrlNotFound
from app.url.application import UrlEncoder
from app.url.infrastructure import RedisUrlRepository, UrlShorterController

from app.shared.application import Base64StrEncoder, AESEncrypter
from app.shared.domain import ExceptionResponse
from app.shared.domain.exceptions import DBConnectionError
from app.shared.constants import REDIS_URL, URL_SEPARATOR, USE_URL_SHORTER

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.config import get_settings


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

settings = get_settings()


# App Set Up
note_controller = NoteController(
    note_repository=RedisNoteRepository(url=REDIS_URL),
    note_encrypter=NoteEncrypter(encrypter=AESEncrypter())
)
str_encoder = Base64StrEncoder()
url_encoder = UrlEncoder(str_encoder=str_encoder)
url_shorter_controller = UrlShorterController(
    url_repository=RedisUrlRepository(url=REDIS_URL), str_encoder=str_encoder)


# Middlewares
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware('http')
async def connection_checker(request: Request, call_next):
    try:
        await note_controller.note_repository.check_connection()
        return await call_next(request)
    except DBConnectionError as e:
        return ExceptionResponse(exception=e, status_code=500, return_traceback=True)


# Routers
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.post("/api/create_note")
async def create_note(input_note: InputNote):
    try:
        key, tag, nonce, created_note = await note_controller.create_note(input_note)
        encoded_url = url_encoder.encode_many_to_url(
            [key, tag, nonce, created_note.id], separator=URL_SEPARATOR
        )
        if USE_URL_SHORTER:
            shorted_url = await url_shorter_controller.create_short_url(InputUrl(original_url=encoded_url, expires_in=input_note.expires_in))
            return {"url": shorted_url}
        else:
            return {"url": encoded_url}
    except (EmptyNote, ExceededMaxNoteLength) as e:
        return ExceptionResponse(exception=e, status_code=400)
    except Exception as e:
        return ExceptionResponse(exception=e, status_code=500, return_traceback=True)


@app.get("/api/note/{url}")
async def read_note_and_destroy(url: str):
    try:
        if USE_URL_SHORTER:
            encoded_url = await url_shorter_controller.get_original_url(url)
        else:
            encoded_url = url

        key, tag, nonce, id = url_encoder.decode_many_to_url(
            encoded_url, separator=URL_SEPARATOR, limit=4
        )
        return await note_controller.read_note_and_destroy(id, key, tag, nonce)
    except (NoteNotFound, UrlNotFound) as e:
        return ExceptionResponse(exception=e, status_code=404)
    except (UnicodeDecodeError, binascii.Error) as e:
        return ExceptionResponse(exception=e, status_code=400, return_traceback=True)
    except Exception as e:
        return ExceptionResponse(exception=e, status_code=500, return_traceback=True)
