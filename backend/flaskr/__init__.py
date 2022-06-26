import os
import random

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.operators import ColumnOperators
from sqlalchemy import and_, func
from models import Category, Question, setup_db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        result = [category.format() for category in categories]

        return jsonify({
            'success': True,
            'categories': result,
            'total': len(categories)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, int)
        questions = Question.query.all()
        categories = Category.query.all()

        paginate_questions = paginate_data(questions, page)
        question_result = [question.format() for question in paginate_questions]
        categories_result = [category.format() for category in categories]

        if len(question_result) == 0:
            return abort(404)

        return jsonify({
            'success': True,
            'questions': question_result,
            'categories': categories_result,
            'total_questions': len(questions),
            'current_category': 'All'
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/question/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                return abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'question_id': question_id
            }), 200
        except:
            return abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/question', methods=['POST'])
    def add_question():
        data = request.get_json()

        try:
            question = Question(
                question=data['question'],
                answer=data['answer'],
                category=data['category'],
                difficulty=data['difficulty']
            )
            question.insert()
        except:
            return abort(400)

        return jsonify({
            'success': True
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions', methods=['POST'])
    def search_questions():
        data = request.get_json()
        search_term = data.get('search_term')

        if 'search_term' in data:
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            result = [question.format() for question in questions]
        else:
            return abort(422)

        return jsonify({
            'success': True,
            'questions': result,
            'total_questions': len(result),
            'current_category': 'All'
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/category/<int:category_id>/questions')
    def get_questions_from_category(category_id):
        questions = Question.query.join(Category, Question.category == Category.id).filter(Category.id == category_id).all()
        
        if len(questions) == 0:
            return abort(404)
        else:
            result = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': result,
            'total_questions': len(questions),
            'current_category': category_id
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quiz/question', methods=['POST'])
    def next_question():
        data = request.get_json()
        
        if data['quiz_category'] == 0:
            question = Question.query.join(Category, Question.category == Category.id)\
            .filter(ColumnOperators.notin_(Question.id, data['previous_questions']))\
            .order_by(func.random()).one_or_none()
        else:
            question = Question.query.join(Category, Question.category == Category.id)\
            .filter(and_(Category.id == data['quiz_category'], ColumnOperators.notin_(Question.id, data['previous_questions'])))\
            .order_by(func.random()).one_or_none()

        if question is None:
            return abort(404)
        
        return jsonify({
            'success': True,
            'question': question.format()
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def page_not_found(e):
        return jsonify({
            'success': False,
            'error': 400,
            'data': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({
            'success': False,
            'error': 404,
            'data': 'Page not found'
        }), 404

    @app.errorhandler(405)
    def page_not_found(e):
        return jsonify({
            'success': False,
            'error': 405,
            'data': 'Method not allowed'
        }), 405

    @app.errorhandler(422)
    def page_not_found(e):
        return jsonify({
            'success': False,
            'error': 422,
            'data': 'Request cannot be processed'
        }), 422

    def paginate_data(list, page = 1, items=QUESTIONS_PER_PAGE):
        start = (page - 1) * items
        end = start + items

        return list[start:end]

    return app

