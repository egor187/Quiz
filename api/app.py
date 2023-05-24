from fastapi import Depends, FastAPI, status

from .adapter import BaseAdapter
from .db import get_db
from .schemas import QuestionAnswer, QuestionsRequest

app = FastAPI()


def make_adapter(question_request: QuestionsRequest, db=Depends(get_db)):
    return BaseAdapter(
        requested_questions=question_request.questions_number_requested, db_session=db
    )


@app.post(
    "/question_number/",
    response_model=QuestionAnswer,
    status_code=status.HTTP_201_CREATED,
)
async def quiz(adapter=Depends(make_adapter)):
    quiz_question = adapter.get_quiz_question()
    return {"questions": quiz_question}
