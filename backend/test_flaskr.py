import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:damilaresimeon@localhost:5432/{}'.format(self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Get all categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(data['total'], 0)


    # Get all questions
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 'All')
        self.assertGreater(data['total_questions'], 0)

    def test_get_questions_with_invalid_page(self):
        res = self.client().get("/questions?page=10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['data'], 'Page not found')


    # Delete question using question_id
    def test_delete_question(self):
        res = self.client().delete('/question/10')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(question, None)


    def test_delete_question_with_invalid_id(self):
        res = self.client().delete('/question/200000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['data'], 'Request cannot be processed')


    # Create a new question
    def test_add_question(self):
        res = self.client().post('/question', json = {'question': 'Test', 'answer': 'test', 'category': 1, 'difficulty': 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_add_question_with_incomplete_body(self):
        res = self.client().post('/question', json = {'question': ''})
        
        self.assertEqual(res.status_code, 400)


    # Search for a question
    def test_search_question_with_result(self):
        res = self.client().post('/questions', json = {'searchTerm': 'clay'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 1)

    def test_search_question_without_result(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_get_questions_from_category(self):
        res = self.client().get('/category/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(data['total_questions'], 0)

    def test_get_questions_from_invalid_category(self):
        res = self.client().get('/category/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)

    def test_next_question(self):
        res = self.client().post('/quiz/question', json = {'quiz_category': 1, 'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)

    def test_next_question_with_invalid_method(self):
        res = self.client().get('/quiz/question')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()