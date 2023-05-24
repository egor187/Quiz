from pydantic import BaseModel


class QuestionsRequest(BaseModel):
    questions_number_requested: int = 1


class Question(BaseModel):
    text: str


class Quiz(BaseModel):
    question: str

    class Config:
        orm_mode = True


class QuestionAnswer(BaseModel):
    questions: list[Quiz]
