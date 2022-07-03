# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/categories'`

- Fetches a dictionary of categories and other params.
- Request Arguments: None
- Returns: An object with keys; `categories`, that contains an array of objects of `id: category_string` key: value pairs,; `success`, with a value of `true` and a `total` number of categories.

```json
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true,
  "total": 6
}
```


`GET '/questions?page=1'`

- Fetches a dictionary of questions and other parameters.
- Request Arguments: page
- Returns: An object with a keys: `categories`, that contains an array of objects of `id: category_string` key: value pairs; `questions`, that contains an array of different questions; `total_questions`, that contains the total number of questions returned; `success`, with a value of `'true'`.

```json
{
  "current_category": "All",
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    ...
  ],
  "questions": [
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    ...
  ],
  "success": true,
  "total_questions": 31
}
```


`DELETE '/question/<int:question_id>'`

- Deletes a question
- Request Arguments: `'id'` of question to be deleted.
- Returns: An object with a single key, `success`, with a value of `true`.

```JSON
{
  "success": true
}
```


`POST '/questions'`

- Searches for a question.
- Request Arguments: None
- Request Body: An object that contains the value of the search parameter eg. `{"search": "won"}`
- Returns: An object with keys: `questions`, that contains an array of questions that match the search parameter; `success`, with a value of `true` and `total_questions` with the total number of questions returned.

```JSON
{
  "success": true,
  "questions": [
      {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }
  ],
  "total_questions": 1
}
```


`GET '/category/<int:category_id>/questions'`

- Fetches all questions that belongs to the specified category.
- Request Arguments: category `id`
- Returns: An object with keys, `questions`, that contains an array of questions; `current_category`, that contains the current category; `success`, with a value of 'true', `total_questions`, with the number of questions returned.

```JSON
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```


`POST '/quiz/question'`

- Fetches a random next question.
- Request Arguments: None
- Request Body: An object with keys: `category` and `previous_questions` e.g. `{"category": 1, "previous_questions": [23]}` 
- Returns: An object with keys: `question`, that contains a question(as an object); `success`, with a value of 'true'.

```JSON
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```


`POST '/question'`

- Creates a new question.
- Request Arguments: None
- Request Body: An object with keys: `question`, `anwser`, `category` and `difficulty` e.g. `{
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "question": "What is the heaviest organ in the human body?"
  }`
- Returns: An object with a single key, `success`, with a value of 'true'.

```JSON
{
  "success": true
}
```

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```