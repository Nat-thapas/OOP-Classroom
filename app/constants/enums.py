from enum import Enum

class ClassroomItemType(Enum):
    ANNOUNCEMENT = "Announcement"
    MATERIAL = "Material"
    ASSIGNMENT = "Assignment"
    QUESTION = "Question"
    MULTIPLE_CHOICE_QUESTION = "MultipleChoiceQuestion"

class TaskType(Enum):
    TODO = "ToDo"
    TO_REVIEW = "ToReview"

class TaskStatus(Enum):
    ASSIGNED = "Assigned"
    TURNED_IN = "TurnedIn"
    GRADED = "Graded"
