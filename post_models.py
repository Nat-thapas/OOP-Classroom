from pydantic import BaseModel

from classroom import Attachment

class RegisterCredential(BaseModel):
    name: str
    email: str
    password: str

class LoginCredential(BaseModel):
    email: str
    password: str

class ClassroomInfo(BaseModel):
    token: str
    name: str
    subject: str | None
    section: str | None
    room: str | None

class ClassroomCode(BaseModel):
    token: str
    code: str

class ClassAnnouncement(BaseModel):
    token: str
    topic_id: str | None
    attachments: list[str] | None  # Change to Attachment
    assigned_to: list[str] | None
    announcement_text: str

class ClassMaterial(BaseModel):
    token: str
    topic_id: str | None
    attachments: list[str] | None  # Change to Attachment
    assigned_to: list[str] | None
    title: str
    description: str | None

class ClassAssignment(BaseModel):
    token: str
    topic_id: str | None
    attachments: list[str] | None  # Change to Attachment
    assigned_to: list[str] | None
    title: str
    instruction: str | None
    due_date: float | None
    point: int | None
    rubric_id: str | None  # Change to Rubric

class ClassQuestion(BaseModel):
    token: str
    topic_id: str | None
    attachments: list[str] | None  # Change to Attachment
    assigned_to: list[str] | None
    question_text: str
    instruction: str | None
    due_date: float | None
    point: int | None

class ClassMultipleChoiceQuestion(BaseModel):
    token: str
    topic_id: str | None
    attachments: list[str] | None  # Change to Attachment
    assigned_to: list[str] | None
    question_text: str
    due_date: float | None
    point: int | None
    choices: list[str]