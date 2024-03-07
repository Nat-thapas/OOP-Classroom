from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile, status

from ..dependencies.authentication import get_current_user
from ..internal.controller import controller
from ..internal.user import User

router = APIRouter(
    prefix="/attachments",
    tags=["Attachment"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=201)
async def upload_file(
    file: UploadFile, user: Annotated[User, Depends(get_current_user)]
):
    attachment = controller.create_attachment(
        file.filename or "unknown",
        file.content_type or "application/unknown",
        file.file,
        user,
    )
    return attachment.to_dict()


@router.get("/{attachment_id}", dependencies=[Depends(get_current_user)])
async def get_file_info(attachment_id: str):
    attachment = controller.get_attachment_by_id(attachment_id)
    if attachment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Attachment not found")
    return attachment.to_dict()


@router.get("/{attachment_id}/data", dependencies=[Depends(get_current_user)])
async def get_file_data(attachment_id: str):
    attachment = controller.get_attachment_by_id(attachment_id)
    if attachment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Attachment not found")
    return Response(attachment.data.getvalue(), media_type=attachment.content_type)
