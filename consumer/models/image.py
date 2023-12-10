from datetime import datetime
from typing import Optional, Tuple, Callable, Generator, Any
from pydantic import BaseModel, Field, validator, errors
from hexbytes import HexBytes

import json


def hex_bytes_validator(val: Any, context: dict) -> bytes:
    if isinstance(val, bytes):
        return val
    elif isinstance(val, bytearray):
        return bytes(val)
    elif isinstance(val, str):
        return bytes.fromhex(val)
    raise errors.BytesError()


class HexBytes(bytes):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield hex_bytes_validator


class Image(BaseModel):
    id: int = Field(...)
    camera_id: int = Field(...)
    data: HexBytes
    gps_coordinates: Tuple[float, float]
    created_at: Optional[datetime] = Field(...)
    updated_at: Optional[datetime] = Field(...)
    is_active: bool = Field(...)
    is_deleted: bool = Field(...)

    class Config:
        json_encoders = {
            bytes: lambda bs: bs.hex()
        }

    def toJSON(self):
        result = json.dumps(self, default=str)
        # json.dumps(self, default=system_methods.json_datetime_default)
        return result


class PlantImage(Image):
    disease: Optional[str] = Field(...)
    percentage: Optional[float] = Field(...)


class ImageUpdate(BaseModel):
    id: int = Field(...)
    camera_id: Optional[int] = Field(...)
    gps_coordinates: Optional[tuple] = Field(...)
    is_active: Optional[bool] = Field(...)
    is_deleted: Optional[bool] = Field(...)


class PlantImageUpdate(ImageUpdate):
    disease: Optional[str] = Field(...)
    percentage: Optional[float] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "camera_id": 1,
                "gps_coordinates": [
                    48.476563,
                    16.585654
                ],
                "disease": "Healthy",
                "percentage": 0.995,
                "is_active": True,
                "is_deleted": False
            }
        }


class ImageCreate(BaseModel):
    camera_id: Optional[int] = Field(...)
    gps_coordinates: Optional[tuple] = Field(...)


class PlantImageCreate(ImageCreate):
    class Config:
        schema_extra = {
            "example": {
                "camera_id": 1,
                "gps_coordinates": [
                    48.476563,
                    16.585654
                ]
            }
        }
