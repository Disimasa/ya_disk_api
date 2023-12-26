from yadisk import Client
from yadisk.exceptions import PathNotFoundError, PathExistsError, NotFoundError
from fastapi import APIRouter, UploadFile, Form, HTTPException
from starlette.responses import Response
from starlette.status import HTTP_200_OK
from config import global_config


client = Client(token=global_config.YA_DISC_TOKEN)
router = APIRouter(redirect_slashes=False)


@router.get('/file')
async def get_files():
    with client:
        try:
            formatted_tree = [{'type': file.type, 'path': file.path} for file in client.listdir("/")]
        except PathNotFoundError:
            raise HTTPException(status_code=404, detail=f'Указанного пути не существует')
    return {"tree": formatted_tree}


@router.get('/file/download')
async def download_file(path: str, destination: str):
    with client:
        try:
            client.download(path, destination)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f'Указанный файл не найдет')
        except PathNotFoundError:
            raise HTTPException(status_code=404, detail=f'Указанного пути не существует')

    return Response(status_code=HTTP_200_OK)


@router.post('/file')
async def upload_file(file: UploadFile, destination: str = Form(...), overwrite: bool = Form(False)):
    with client:
        try:
            client.upload(file.file, destination, overwrite=overwrite)
        except PathExistsError:
            raise HTTPException(status_code=500, detail=f'Файл по указанному пути уже существует')
        except PathNotFoundError:
            raise HTTPException(status_code=404, detail=f'Указанного пути не существует')

    return Response(status_code=HTTP_200_OK)


@router.delete('/file')
async def delete_file(path: str):
    try:
        client.remove(path, permanently=True)
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f'Указанный файл не найдет')

    return Response(status_code=HTTP_200_OK)


@router.post('/dir')
async def create_dir(path: str):
    try:
        client.mkdir(path)
    except PathNotFoundError:
        raise HTTPException(status_code=404, detail=f'Указанного пути не существует')

    return Response(status_code=HTTP_200_OK)
