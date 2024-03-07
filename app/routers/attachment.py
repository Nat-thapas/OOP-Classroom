from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, Response

from ..dependencies.dependencies import get_current_user
from ..internal.user import User
from ..internal.controller import controller

router = APIRouter(
    prefix="/attachments",
    tags=["Attachment"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=201)
async def upload_file(file: UploadFile, user: User = Depends(get_current_user)):
    attachment = controller.create_attachment(
        file.filename or "unknown",
        file.content_type or "application/unknown",
        file.file,
        user,
    )
    return attachment.to_dict()


@router.get("/{attachment_id}")
async def get_file_info(attachment_id: str, _: User = Depends(get_current_user)):
    attachment = controller.get_attachment_by_id(attachment_id)
    if attachment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Attachment not found")
    return attachment.to_dict()


@router.get("/{attachment_id}/data")
async def get_file_data(attachment_id: str, _: User = Depends(get_current_user)):
    attachment = controller.get_attachment_by_id(attachment_id)
    if attachment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Attachment not found")
    return Response(attachment.data.getvalue(), media_type=attachment.content_type)
