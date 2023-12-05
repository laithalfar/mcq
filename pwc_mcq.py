import openai
from IPython.display import Markdown, display
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
import re
import streamlit as st
import os


# API key set as environment and then implemented

os.environ['OPENAI_API_KEY'] = "YOUR_API_KEY"
openai.api_key = os.getenv('OPENAI_API_KEY')



def generate_quiz_prompt():
    template = """
    You are an expert quiz maker in any field you are asked about. Create a quiz with {num_questions} questions about this topic after thinking about it step by step: {quiz_context}.
    The format of the quiz should be as follows; where the minimum number of choices is 4 for each question:
- Multiple-choice: 

- Questions:
    <Question1>: <a. Answer 1>, <b. Answer 2>, <c. Answer 3>, <d. Answer 4>
    <Question2>: <a. Answer 1>, <b. Answer 2>, <c. Answer 3>, <d. Answer 4>
    ....
- Answers:
    <Answer1>: <a|b|c|d>
    <Answer2>: <a|b|c|d>
    ....

    Example:
    - Questions:
    - 1. Who won the 2022 world cup?
        a. France
        b. Morroco
        c. Spain
        d. Argentina
    - Answers: 
        1. d
"""

    #the prompt specified and executed
    
    prompt = PromptTemplate.from_template(template)
    prompt.format(num_questions=3, quiz_context="Data Structures in Python Programming")

    return prompt

#generates the chain
def generate_chain(prompt_template, llm):
     return LLMChain(llm = llm, prompt = prompt_template )
     
# split the questions and answers from the response
def split_questions_answers(quiz_response):
    questions = quiz_response.split("Answers:")[0]
    answers = quiz_response.split("Answers:")[1]
    return questions, answers


def main():
    #title of page in the UI
    st.title("OpenAI Quiz Application")

    prompt_template = generate_quiz_prompt()
    llm = ChatOpenAI(openai_api_key ="YOUR_API_KEY")
        #openai_api_key = openai.api_key)
    chain = generate_chain(prompt_template, llm)
    context = st.text_area("Enter the context for the quiz")
    num_questions = st.number_input("Enter the number of questions", min_value=1, max_value=10, value =3)
    #quiz_type= st.selectbox("Select the quiz type",["multiple-choice", "true-false","open question"] )
    if st.button("Generate Quiz"):
        quiz_response = chain.run(num_questions = num_questions, quiz_context = context )
        st.write("Quiz Generated!")
        questions, answers = split_questions_answers(quiz_response)

        #When stored in st.session_state, these variables keep their values
        # even when the user interacts with other parts of the app 
        # or triggers other buttons such as in this case when show answers is pressed.
        st.session_state.answers = answers
        st.session_state.questions = questions
        st.write(questions)
    if st.button("Show Answers"):
        # questions, answer = split_questions_answers(quiz_response)
        st.write(st.session_state.questions)
        st.write("----")
        st.write(st.session_state.answers)


if __name__ == "__main__":
    main()



# get response from prompt question
#def get_response(prompt_question):

    #response form gpt-3.5-turbo model where for the system acts as a research and programming assisstant
    #and the user asks the prompt question
 #  response = openai.chat.completions.create(
  #      model="gpt-3.5-turbo",
   #     messages=[{"role": "system", "content": "You are a helpful research and\
    #        programming assistant"},
     #             {"role": "user", "content": prompt_question}]
   #)
    
  # return response.choices[0].message.content




# quiz_response = chain.run(num_questions=10, quiz_type="multiple-choice", quiz_context="Data Structures in Python Programming")
#quiz_python = get_response(prompt)


# Markdown(quiz_response)



