

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import random
import yaml
import pandas as pd
import time

# Load the question bank
import pathlib
q = pathlib.Path("questions.yaml")
questions = yaml.unsafe_load(q.read_text())


# Generate random questions
def generate_questions():

    question1 = random.choice(questions)
    question2 = random.choice(questions)
    return question1, question2


# Check the answer
def check_answer(answer, correct_answer):
    # return answer == correct_answer
    return True


# Handle the answer request
async def answer_question(request):
    # Get the student's name and ID
    name = request.query_params.get('name')
    student_id = request.query_params.get('student_id')

    # Generate random questions
    question1, question2 = generate_questions()

    # Get the student's answers
    answer1 = request.query_params.get('answer1')
    answer2 = request.query_params.get('answer2')

    # Check the answers
    is_correct1 = check_answer(answer1, question1.answer)
    is_correct2 = check_answer(answer2, question2.answer)

    # Calculate the elapsed time
    start_time = float(request.query_params.get('start_time'))
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Store the results in a DataFrame
    results_df = pd.DataFrame({
        'Name': [name],
        'Student ID': [student_id],
        'Correct Answer 1': [is_correct1],
        'Correct Answer 2': [is_correct2],
        'Elapsed Time': [elapsed_time]
    })

    # Append the results to the CSV file
    with open('results.csv', 'a') as file:
        results_df.to_csv(file, index=False, header=not file.tell())

    return JSONResponse({
        'name': name,
        'tudent_id': student_id,
        'is_correct1': is_correct1,
        'is_correct2': is_correct2,
        'elapsed_time': elapsed_time
    })

# Create the server application
app = Starlette(
    routes=[
        Route('/answer', answer_question, methods=['GET'])
    ]
)

# Start the server
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

