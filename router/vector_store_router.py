from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.vector_store_service import crud_add_documents, crud_get_all_files, crud_delete_file
from schemas.result import success_response, error_response
from utils.dbUtils import get_db

vector_store_router = APIRouter(
    prefix="/vector",
    tags=["vector"],)



@vector_store_router.post("/add_documents")
async def add_documents(file: UploadFile = File(...),db: AsyncSession = Depends(get_db)):

    flat = await crud_add_documents(db,file)
    print(type(file.file))
    if flat == 0:
        return success_response(message=f"文件 {file.filename} 已成功添加到向量数据库")
    elif flat == 1:
        return success_response(message=f"文件 {file.filename} 已经处理过，跳过")
    elif flat == 2:
        return success_response(message=f"文件 {file.filename} 内无有效文本内容，跳过")
    else:
        return error_response(message=f"文件 {file.filename} 处理失败")


@vector_store_router.get("/get_all_files")
async def get_all_files(db: AsyncSession = Depends(get_db)):
    files = await crud_get_all_files(db)
    return success_response(data=files)

@vector_store_router.delete("/delete_file/{file_id}")
async def delete_file(file_id: int, db: AsyncSession = Depends(get_db)):
    name,flat = await crud_delete_file(db, file_id)
    if flat == True:
        return success_response(message=f"文件 {name} 已成功删除")
    else:
        return error_response(message=f"文件 {name} 删除失败")
