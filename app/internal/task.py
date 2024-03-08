from abc import ABC, abstractmethod

from ..constants.enums import TaskStatus
from .classroom import Classroom
from .items import Assignment, MultipleChoiceQuestion, Question
from .user import User


class Task(ABC):
    def __init__(
        self,
        classroom: Classroom,
        item: Assignment | Question | MultipleChoiceQuestion,
        owner: User,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._classroom = classroom
        self._item = item
        self._owner = owner

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class ToDoTask(Task):
    def __init__(
        self,
        classroom: Classroom,
        item: Assignment | Question | MultipleChoiceQuestion,
        owner: User,
    ) -> None:
        super().__init__(classroom=classroom, item=item, owner=owner)
        self.__status: TaskStatus
        if submission := self._item.get_submission_by_owner(self._owner):
            if submission.point is not None:
                self.__status = TaskStatus.GRADED
            else:
                self.__status = TaskStatus.TURNED_IN
        else:
            self.__status = TaskStatus.ASSIGNED

    def to_dict(self) -> dict:
        return {
            "classroom_id": self._classroom.id,
            "item_id": self._item.id,
            "title": self._item.title,
            "classroom_name": self._classroom.name,
            "created_at": self._item.created_at.isoformat(),
            "edited_at": self._item.edited_at.isoformat(),
            "due_date": self._item.due_date,
            "status": self.__status.value,
        }


class ToReviewTask(Task):
    def __init__(
        self,
        classroom: Classroom,
        item: Assignment | Question | MultipleChoiceQuestion,
        owner: User,
    ) -> None:
        super().__init__(classroom=classroom, item=item, owner=owner)
        total_assigned_count = len(item.assigned_to_students or classroom.students)
        total_turned_in_count = len(item.submissions)
        total_graded_count = len(
            [submission.point is not None for submission in item.submissions]
        )
        self.__turned_in_count = total_turned_in_count - total_graded_count
        self.__assigned_count = total_assigned_count - total_turned_in_count
        self.__graded_count = total_graded_count

    def to_dict(self) -> dict:
        return {
            "classroom_id": self._classroom.id,
            "item_id": self._item.id,
            "title": self._item.title,
            "classroom_name": self._classroom.name,
            "created_at": self._item.created_at.isoformat(),
            "edited_at": self._item.edited_at.isoformat(),
            "turned_in_count": self.__turned_in_count,
            "assigned_count": self.__assigned_count,
            "graded_count": self.__graded_count,
        }
