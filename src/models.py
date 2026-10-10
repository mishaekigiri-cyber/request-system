from pydantic import BaseModel, ConfigDict, Field, field_validator

VALID_ROLES = {"Заявитель", "Оператор", "Исполнитель", "Администратор"}

class RequestCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=5, max_length=5000)
    user_id: int = Field(gt=0)
    category_id: int = Field(gt=0)
    assignee_id: int | None = Field(default=None, gt=0)

    @field_validator("title", "description")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Поле не должно быть пустым")
        return value

class RequestUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = Field(default=None, min_length=5, max_length=5000)
    category_id: int | None = Field(default=None, gt=0)
    assignee_id: int | None = Field(default=None, gt=0)

    @field_validator("title", "description")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("Поле не должно быть пустым")
        return value

class StatusChange(BaseModel):
    status_id: int = Field(gt=0)

class RequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    request_id: int
    title: str
    description: str
    created_at: str
    user_id: int
    category_id: int
    status_id: int
    assignee_id: int | None = None
    status: str
    category: str
    applicant: str
    assignee: str | None = None
