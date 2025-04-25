# --------------------------- IMPORTS --------------------------- #
import os
import requests
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import subprocess
from langchain_groq import ChatGroq
import re

from dust import agent


# --------------------------- GROQ API SETTINGS --------------------------- #
GROQ_API_KEY = "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"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}
endpoint = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"



#---------------------------------------------AGENT 5: SOLUTION AGENT------------------------------------------------------
solution_explainer_prompt = PromptTemplate.from_template(
    """
You are a highly skilled math teacher.

### TASK:
Explain the following math problem in clear, simple, and step-by-step format.

### INPUT:
{combined_input}

### INSTRUCTIONS:
- Ignore any visual instructions or drawing hints.
- Only focus on solving the problem description and step by step solution logically and mathematically.
- Each step should be broken down with reasoning and intermediate calculations.
- Format output like:
  Step 1: ...
  Step 2: ...
  ...
  Final Answer: ...

-also provide analogy explain the mathematical sum in an simple way that even a child can understand
"""
)

# ------------------------- LLM: ChatGroq LLaMA3 ------------------------------ #
llm = ChatGroq(
    temperature=0,
    model_name="llama3-70b-8192",
    groq_api_key=GROQ_API_KEY
)

# ----------------------------- AGENT CHAINS --------------------------------- #

solution_explainer_chain=solution_explainer_prompt | llm


def ask_groq(prompt):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def process_question(question):
    prompt = f"""
    you should do this do not even skip it
    You are an AI tutor. Format your response in three simple sections with clear and accurate content.

    Problem Description:
    Summarize the given question. Mention all given data and what needs to be solved.
    give as an instruction for the another chatgroq model

    Solution Steps:
    Provide a step-by-step simple and effective solution for the problem.
    give as an instruction for the another chatgroq model

    Visual Hints(must without this do not proceed) :
    provide visual hints that is the object that can be added and the labels for it
    the video should be visually powerful and it entirely depends on your instruction
    since real world objects cannot be created in manim give hints like draw rectangle for train with circle as its wheels 
    it can also have spg objects if possible 
    give as an instruction for the another chatgroq model
    look at what hints can be provided 



    Now format the response for the question below:

    Question: {question} 
    """
    response = ask_groq(prompt)
    
    cleaned_response = response.strip()
    
    print("Solution Cleaned Successfully!")

    return cleaned_response

def solution_to_html(solution):
    prompt = f"""
    you should do the given solution to html code 
    just want <p> ,<li>,<ul> like this you wnt to give as a result
    
    IMPORTENT : give only html code no other additional preamble i dont want that like "Here is the HTML code without preamble:" this also
    {solution}
    """
    response = ask_groq(prompt)
    
    cleaned_response = response.strip()
    
    print("Solution Cleaned Successfully!")

    return cleaned_response

def AgentManager(question):
    cleaned_response = process_question(question)  # Get the cleaned response

    solution_explanation = solution_explainer_chain.invoke({"combined_input": cleaned_response})
    
    formatted_solution = solution_explanation.content.strip().replace("**", "").replace("\n\n", "\n")
    
    print("Formated solution")
    
    agent(cleaned_response)
    
    return solution_to_html(formatted_solution)
