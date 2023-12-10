from models.image import *
from fastapi import APIRouter, Body, HTTPException, Response, Request, status
from confluent_kafka import Consumer
from datetime import datetime
from fastapi.responses import JSONResponse
import random


router = APIRouter(
    prefix="/image-plant",
    tags=['plants']
)


@router.get("/potato/total/")
def get_total_images_potato(request: Request):
    total_images = request.app.col_name_plant_potato.count_documents({})

    if total_images is not None:
        result = {
            "total_images": total_images
        }
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Images not found")


@router.get("/tomato/total/")
def get_total_images_tomato(request: Request):
    total_images = request.app.col_name_plant_tomato.count_documents({})

    if total_images is not None:
        result = {
            "total_images": total_images
        }
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Images not found")


@router.get("/pepper/total/")
def get_total_images_pepper(request: Request):
    total_images = request.app.col_name_plant_pepper.count_documents({})

    if total_images is not None:
        result = {
            "total_images": total_images
        }
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Images not found")


@router.get("/potato/{image_id}", response_model=PlantImage)
def get_potato_image(image_id: int, request: Request):
    result = request.app.col_name_plant_potato.find_one({"id": image_id})

    if (result is not None):
        result["_id"] = str(result["_id"])
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Image with id {image_id} not found")


@router.get("/tomato/{image_id}", response_model=PlantImage)
def get_tomato_image(image_id: int, request: Request):
    result = request.app.col_name_plant_tomato.find_one({"id": image_id})

    if (result is not None):
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Image with id {image_id} not found")


@router.get("/pepper/{image_id}", response_model=PlantImage)
def get_pepper_image(image_id: int, request: Request):
    result = request.app.col_name_plant_pepper.find_one({"id": image_id})

    if (result is not None):
        return result

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Image with id {image_id} not found")


@router.post("/potato/", response_model=PlantImage)
def update_image_potato(request: Request, image_request: PlantImageUpdate):
    filter = {"id": image_request.id}
    image_db = request.app.col_name_plant_potato.find_one(filter)
    if (image_request is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Image with {id} not found")
    new_values = {
        "$set":  {
            "camera_id": image_request.camera_id if image_request.camera_id is not None else image_db["camera_id"],
            "gps_coordinates": image_request.gps_coordinates if image_request.gps_coordinates is not None else image_db["gps_coordinates"],
            "disease": image_request.disease if image_request.disease is not None else image_db["disease"],
            "percentage": image_request.percentage if image_request.percentage is not None else image_db["percentage"],
            "updated_at": datetime.now(),
            "is_active": image_request.is_active if image_request.is_active is not None else image_db["is_active"],
            "is_deleted": image_request.is_deleted if image_request.is_deleted is not None else image_db["is_deleted"],
        }
    }

    result = request.app.col_name_plant_potato.update_one(filter, new_values)
    if (result.modified_count > 0):
       # image_metrics.add_metrics('potato', updated_image)
        return image_db

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Image with id {image_request.id} not found")


@router.post("/tomato/", response_model=PlantImage)
def update_image_tomato(request: Request, image_request: PlantImageUpdate):
    filter = {"id": image_request.id}
    image_db = request.app.col_name_plant_tomato.find_one(filter)

    if (image_request is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Image with id not found")

    new_values = {
        "$set":  {
            "camera_id": image_request.camera_id if image_request.camera_id is not None else image_db["camera_id"],
            "gps_coordinates": image_request.gps_coordinates if image_request.gps_coordinates is not None else image_db["gps_coordinates"],
            "disease": image_request.disease if image_request.disease is not None else image_db["disease"],
            "percentage": image_request.percentage if image_request.percentage is not None else image_db["percentage"],
            "updated_at": datetime.now(),
            "is_active": image_request.is_active if image_request.is_active is not None else image_db["is_active"],
            "is_deleted": image_request.is_deleted if image_request.is_deleted is not None else image_db["is_deleted"],
        }
    }

    result = request.app.col_name_plant_tomato.update_one(filter, new_values)

    if (result.modified_count > 0):
        # image_metrics.add_metrics('tomato', updated_image)
        return image_db

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Image with id {image_request.id} not found")


@router.post("/pepper/", response_model=PlantImage)
def update_image_pepper(request: Request, image_request: PlantImageUpdate):
    filter = {"id": image_request.id}
    image_db = request.app.col_name_plant_pepper.find_one(filter)

    if (image_request is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Image with id not found")

    new_values = {
        "$set":  {
            "camera_id": image_request.camera_id if image_request.camera_id is not None else image_db["camera_id"],
            "gps_coordinates": image_request.gps_coordinates if image_request.gps_coordinates is not None else image_db["gps_coordinates"],
            "disease": image_request.disease if image_request.disease is not None else image_db["disease"],
            "percentage": image_request.percentage if image_request.percentage is not None else image_db["percentage"],
            "updated_at": datetime.now(),
            "is_active": image_request.is_active if image_request.is_active is not None else image_db["is_active"],
            "is_deleted": image_request.is_deleted if image_request.is_deleted is not None else image_db["is_deleted"],
        }
    }

    result = request.app.col_name_plant_pepper.update_one(filter, new_values)

    if (result.modified_count > 0):
        # image_metrics.add_metrics('pepper', updated_image)
        return image_db

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Image with id {image_request.id} not found")


@router.put("/potato/", response_model=PlantImage,)
def create_image_potato(request: Request, image_create: PlantImageCreate):
    last_image_query = request.app.col_name_plant_potato.find().sort(
        "id", -1).limit(1)
    last_image_json = list(last_image_query)[0]
    last_image = PlantImage(**last_image_json)

    last_image.id += 1
    last_image.camera_id = image_create.camera_id

    image_query = request.app.col_name_plant_potato.find({}, {"id": 1})
    image_list = list(image_query)

    if (len(image_list) == 0):
        content = {"description": "There are no images with the specified filter"}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    random_image_id = random.choice(image_list)['id']
    random_image = request.app.col_name_plant_potato.find_one(
        {"id": random_image_id})

    last_image.data = random_image['data']
    last_image.gps_coordinates = image_create.gps_coordinates
    last_image.created_at = datetime.now()
    last_image.updated_at = datetime.now()
    last_image.is_active = False
    last_image.is_deleted = False

    result = request.app.col_name_plant_potato.insert_one(last_image.dict())

    # if (result.inserted_id is not None):
    #     # filter = {"id": last_image.id}
    #     # created_image_db = request.app.col_name_plant_potato.find_one(filter)
    #     # created_image = PlantImage(**created_image_db)
    #     # #image_metrics.add_metrics('potato', created_image)

    return last_image


@router.put("/tomato/", response_model=PlantImage,)
def create_image_potato(request: Request, image_create: PlantImageCreate):
    last_image_query = request.app.col_name_plant_tomato.find().sort(
        "id", -1).limit(1)
    last_image_json = list(last_image_query)[0]

    last_image = PlantImage(**last_image_json)

    last_image.id += 1
    last_image.camera_id = image_create.camera_id

    image_query = request.app.col_name_plant_tomato.find({}, {"id": 1})
    image_list = list(image_query)

    if (len(image_list) == 0):
        content = {"description": "There are no images with the specified filter"}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    random_image_id = random.choice(image_list)['id']

    random_image = request.app.col_name_plant_tomato.find_one(
        {"id": random_image_id})

    last_image.data = random_image['data']
    last_image.gps_coordinates = image_create.gps_coordinates
    last_image.created_at = datetime.now()
    last_image.updated_at = datetime.now()
    last_image.is_active = False
    last_image.is_deleted = False

    result = request.app.col_name_plant_tomato.insert_one(last_image.dict())

    # if (result.inserted_id is not None):
    #     filter = {"id": last_image.id}
    #     created_image_db = request.app.col_name_plant_tomato.find_one(filter)
    #     created_image = PlantImage(**created_image_db)
    #     image_metrics.add_metrics('tomato', created_image)

    return last_image


@router.put("/pepper/", response_model=PlantImage,)
def create_image_potato(request: Request, image_create: PlantImageCreate):
    last_image_query = request.app.col_name_plant_pepper.find().sort(
        "id", -1).limit(1)
    last_image_json = list(last_image_query)[0]

    last_image = PlantImage(**last_image_json)

    last_image.id += 1
    last_image.camera_id = image_create.camera_id

    image_query = request.app.col_name_plant_pepper.find({}, {"id": 1})
    image_list = list(image_query)

    if (len(image_list) == 0):
        content = {"description": "There are no images with the specified filter"}
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    random_image_id = random.choice(image_list)['id']

    random_image = request.app.col_name_plant_pepper.find_one(
        {"id": random_image_id})

    last_image.data = random_image['data']
    last_image.gps_coordinates = image_create.gps_coordinates
    last_image.created_at = datetime.now()
    last_image.updated_at = datetime.now()
    last_image.is_active = False
    last_image.is_deleted = False

    result = request.app.col_name_plant_pepper.insert_one(last_image.dict())

    # if (result.inserted_id is not None):
    #     filter = {"id": last_image.id}
    #     created_image_db = request.app.col_name_plant_pepper.find_one(filter)
    #     created_image = PlantImage(**created_image_db)
    #     image_metrics.add_metrics('pepper', created_image)

    return last_image


@router.delete("/potato/{image_id}")
def delete_image_potato(image_id: int, request: Request):

    filter = {"id": image_id}

    if filter is not None:
        new_values = {
            "$set": {
                "is_deleted": True,
                "updated_at": datetime.now()
            }
        }
        result = request.app.col_name_plant_potato.update_one(
            filter, new_values)

        if result.modified_count > 0:
            return {"message": "Image deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Image with id {image_id} not found"
    )


@router.delete("/tomato/{image_id}")
def delete_image_tomato(image_id: int, request: Request):

    filter = {"id": image_id}

    if filter is not None:
        new_values = {
            "$set": {
                "is_deleted": True,
                "updated_at": datetime.now()
            }
        }
        result = request.app.col_name_plant_tomato.update_one(
            filter, new_values)

        if result.modified_count > 0:
            return {"message": "Image deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Image with id {image_id} not found"
    )


@router.delete("/pepper/{image_id}")
def delete_image_pepper(image_id: int, request: Request):

    filter = {"id": image_id}

    if filter is not None:
        new_values = {
            "$set": {
                "is_deleted": True,
                "updated_at": datetime.now()
            }
        }
        result = request.app.col_name_plant_pepper.update_one(
            filter, new_values)

        if result.modified_count > 0:
            return {"message": "Image deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Image with id {image_id} not found"
    )
