"""ORM model for the `file_info` table.

This mirrors the provided SQL:

CREATE TYPE file_status AS ENUM (0, 1);
CREATE TABLE file_info (
    id BIGSERIAL PRIMARY KEY,
    uploaded_by_user_id INTEGER NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    stored_path TEXT NOT NULL UNIQUE,
    hash_sha256 CHAR(64),
    file_size BIGINT NOT NULL CHECK (file_size >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status INT DEFAULT 0
);

Notes:
- We represent `status` as an INT with an accompanying Python IntEnum `FileStatus`.
- A CheckConstraint is added for non-negative file_size to match the SQL CHECK.
"""

from enum import IntEnum

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Text,
    DateTime,
    CheckConstraint,
    func,
    text, Float,
)

from model.base import Base


class FileStatus(IntEnum):
    """Simple integer-backed status enum for files."""
    INACTIVE = 0
    ACTIVE = 1


class FileInfo(Base):
    """ORM model for the `file_info` table."""
    __tablename__ = "file_info"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    uploaded_by_user_id = Column(Integer, nullable=False, comment="上传该文件的用户ID")
    original_name = Column(String(255), nullable=False, comment="文件原始名称")
    stored_path = Column(Text, nullable=False, comment="文件在存储系统中的路径或唯一标识符")
    hash_sha256 = Column(String(64), nullable=True, comment="文件内容的SHA256哈希值")
    file_size = Column(Float, nullable=False, comment="文件大小（字节）")
    created_at = Column(DateTime(timezone=True), default=func.now(), comment="记录创建时间")
    file_type = Column(String(24), nullable=True, comment="文件类型，例如：'pdf', 'docx', 'txt'")

    # Use server_default text("0") to match SQL DEFAULT 0
    status = Column(Integer, nullable=False, default=0, comment="文件的当前状态，0=inactive,1=active")

    __table_args__ = (
        CheckConstraint("file_size >= 0", name="ck_file_size_non_negative"),
    )

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return (
            f"<FileInfo(id={self.id!r}, original_name={self.original_name!r}, "
            f"stored_path={self.stored_path!r}, file_size={self.file_size!r})>"
        )
