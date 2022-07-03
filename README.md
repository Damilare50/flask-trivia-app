# Full Stack Trivia

## Getting Started

Project is divided into `frontend` and `backend` directory.

Technologies used in the project:
**Frontend**

- React
- React Router
- Jquery

**Backend**

- Flask
- SQLAlchemy
- Flask CORS

**Database**

- PostgresSQL 14

## Installation

**Frontend**

```bash
cd frontend/
# Installing dependencies
npm install
# Starting the project
npm run start
```

**Backend**
Creating db and populating data.

**_NOTE: Make sure postgres in running_**

```bash
# Creating db
createdb trivia

cd backend/

# Populating database with tables and related data
psql trivia < trivia.psql
```

```bash
# Creating virtual environment
virtualenv venv

# Activating virtual environment
source venv/Scripts/activate

# Install packages
pip install -r requirements.txt

# Start your project in development mode
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## API Documentation

**_API follows Restful API convenctions._**

The main data returned for both success and failed responses are in the `data` object. For failed response data contains the message of why it failed and for successfull response data is the main thing requested by the client. Although, other supporting data will be contained in the successful response.

```JSON
{
    "success": True/False,
    ...
}
```

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


`DELETE '/questions/<int:question_id>'`

- Deletes a question
- Request Arguments: `'id'` of question to be deleted.
- Returns: An object with a single key, `success`, with a value of `true`.

```JSON
{
  "success": true
}
```


`POST '/questions'`

- Sends a request that searches for a question.
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
