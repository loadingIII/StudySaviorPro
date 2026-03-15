from pydantic import BaseModel, Field



class FileVO(BaseModel):
    id: int = Field(..., description="文件ID")
    original_name: str = Field(..., description="文件名称")
    file_size: float = Field(..., description="文件大小，单位字节")
    file_type: str = Field(..., description="文件类型，例如：'pdf', 'docx', 'txt'")
    created_at: str = Field(..., description="文件上传时间，格式为ISO 8601字符串")