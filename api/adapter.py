import requests
from sqlalchemy.exc import IntegrityError

from .constants import EXTERNAL_API
from .db import QuizQuestion


class BaseAdapter:
    def __init__(
        self,
        db_session,
        url=EXTERNAL_API,
        requested_questions=1,
        timeout=10,
        retries=3,
        allow_redirects=False,
    ):
        self.url = url
        self.requested_question = requested_questions
        self.db_session = db_session
        self.timeout = timeout
        self.retries = retries
        self.allow_redirects = allow_redirects

    def get_quiz_question(self):
        response = self.parse_response(
            self.get_session().get(
                self.url,
                params={"count": self.requested_question},
                timeout=self.timeout,
                allow_redirects=self.allow_redirects,
            )
        )
        try:
            self.save(response)
        except IntegrityError:
            response = self.get_quiz_question()
        finally:
            return response

    @staticmethod
    def parse_response(response):
        response_data = response.json()
        parsed_data = [
            QuizQuestion(
                **{
                    "external_id": item.get("id"),
                    "question": item.get("question"),
                    "answer": item.get("answer"),
                }
            )
            for item in response_data
        ]
        return parsed_data

    def save(self, data: list[QuizQuestion]):
        self.db_session.add_all(data)
        self.db_session.commit()

    @property
    def session(self):
        if not hasattr(self, "_session"):
            self._session = self.get_session()
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    def get_session(self):
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=self.retries)
        session.mount("https://", adapter)
        return session
