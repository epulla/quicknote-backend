from pydantic import BaseModel


class InputNote(BaseModel):
    content: str
    expires_in: int  # expiration time in seconds
    max_views: int  # max number of views of the note before it gets destroyed

    class Config:
        schema_extra = {
            "example": {
                "content": "This is a secret that will expire in 5 minutes",
                "expires_in": 300,
                "max_views": 1
            }
        }
