# --------------------------- IMPORTS --------------------------- #
import os
import requests
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import subprocess
from langchain_groq import ChatGroq
import re


# --------------------------- GROQ API SETTINGS --------------------------- #
GROQ_API_KEY = "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"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}
endpoint = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"


# --------------------------- AGENT 1: CODE GENERATOR --------------------------- #
code_gen_prompt = PromptTemplate.from_template(
    """
### GOAL:
Generate a valid ManimCE Python script to animate the given math problem with class name as MyScene.

### INPUT:
{combined_input}

### REQUIREMENTS:
- padding = 2
-set fontsize 25 always
- black screen
- if the question has more than 15 words split it into several line so that it fits in frame properly
- no overlapping of objects in the animation
- Balance timing and pacing 
- Do NOT use `frame_height` or any automatic scaling tied to frame size.
- Use manual positioning with `.to_edge(DOWN|UP|LEFT|RIGHT, buff=...)` or `.next_to()` and `.move_to(...)` for clean structure.
- Layout should be:
  1. Top: Question text → Use `.to_edge(UP, buff=0.5)`
  2. Middle: All objects (shapes/graphics) → Use `.move_to(ORIGIN)` or `.next_to()` to align visuals.
  3. top: Final solution/summary text → Use `.to_edge(UP, buff=0.5)`all solution should be displayed at once
  4. Add labels to visuals using `.next_to(shape, direction)` (e.g., `label.next_to(sphere, DOWN)`).
- Fade in and fade out:
  - Fade in the question text from the top region, then fade out resize the text fit the frame accordingly.
  - Fade in the visuals from the Middle region, fade out.
  - Fade in the solution steps (math).

- Focus on visual strength with more objects.
- Label the objects properly (e.g., "car", "bridge").
- Do not include ShowCreation; instead, use Create function.
- Output: Only valid ManimCE code starting with `from manim import *`, using `class MyScene(Scene):`.
- refer this link while creating code 'https://docs.manim.community/en/stable/examples.html'
- refer this also 'https://github.com/ManimCommunity/manim'


DO NOT include explanations, backticks, or markdown.
Ensure it can be run with `manim -pql generated_scene.py MyScene` without error.
"""
)

# ---------------------- AGENT 2: VISUAL REALISM ENHANCER ---------------------- #
realism_prompt = PromptTemplate.from_template(
     """
You are a Manim animation expert. Improve the realism and visual accuracy of this Manim code.

### OBJECTIVES:
-set fontsize 25 always and split the question if it has more than 15 words
-if the question has more than 15 words split it into several line so that it fits in frame properly
- Replace crude SPGs with more realistic ones.
- Improve size, proportion, color, and spatial layout.
- Use manual positioning with `.to_edge(DOWN|UP|LEFT|RIGHT, buff=...)` or `.next_to()` and `.move_to(...)` for clean structure.
- Layout should be:
  1. Top: Question text → Use `.to_edge(UP, buff=0.5)`
  2. Middle: All objects (shapes/graphics) → Use `.move_to(ORIGIN)` or `.next_to()` to align visuals.
  3. top: Final solution/summary text → Use `.to_edge(UP, buff=0.5)`all solution should be displayed at once
  4. Add labels to visuals using `.next_to(shape, direction)` (e.g., `label.next_to(sphere, DOWN)`).
- Fade in and fade out:
  - Fade in the question text from the top region, then fade out resize the text fit the frame accordingly.
  - Fade in the visuals from the Middle region, fade out.
  - Fade in the solution steps (math).
- text should correctly fit the frame 
- it should perfectly fit in the frame
- Add proper labels to objects.
- Maintain animation logic, just refine the visuals.
- refer this link while creating code 'https://docs.manim.community/en/stable/examples.html'
- refer this also 'https://github.com/ManimCommunity/manim'
- text and objects should not overlap
-look at the fade in fade out the timing should be correct such that it oes not overlap
### INPUT:
{manim_code}


### OUTPUT:
Return only valid updated Manim code with visual enhancements.
No markdown, explanations, or backticks.
Ensure it can be run with `manim -pql generated_scene.py MyScene` without error.
"""
)

# -------------------- AGENT 3: ANIMATION BEAUTIFIER --------------------------- #
beautifier_prompt = PromptTemplate.from_template(
    """
You are a visual effects and animation expert. Enhance this Manim animation aesthetically.

### OBJECTIVES:
-set fontsize 25 always
-if the question has more than 15 words split it into several line so that it fits in frame properly
- Add elegant transitions: FadeIn, Transform, Succession, Waits
- sometimes the text moves out of the frame or screen avoid that and also avoid overlapping of manim objects and text
- only use FadeIn and FadeOut do not use Fadefromcentre etc
- Use manual positioning with `.to_edge(DOWN|UP|LEFT|RIGHT, buff=...)` or `.next_to()` and `.move_to(...)` for clean structure.
- Layout should be:
  1. Top: Question text → Use `.to_edge(UP, buff=0.5)`
  2. Middle: All objects (shapes/graphics) → Use `.move_to(ORIGIN)` or `.next_to()` to align visuals.
  3. top: Final solution/summary text → Use `.to_edge(UP, buff=0.5)`all solution should be displayed at once
  4. Add labels to visuals using `.next_to(shape, direction)` (e.g., `label.next_to(sphere, DOWN)`).
- Fade in and fade out:
  - Fade in the question text from the top region, then fade out resize the text fit the frame accordingly.
  - Fade in the visuals from the Middle region, fade out.
  - Fade in the solution steps (math).
- Use color schemes and text styles
- Balance timing and pacing
- text and objects should not overlap
- Smooth camera movement or zooms
- refer this link while creating code 'https://docs.manim.community/en/stable/examples.html'
- refer this also 'https://github.com/ManimCommunity/manim'

### INPUT:
{manim_code}

### OUTPUT:
Return only valid enhanced Manim code.
No markdown, no explanations.
no 'here is enhanced code only the code
Ensure it can be run with `manim -pql generated_scene.py MyScene` without error.
"""
)

# -------------------- AGENT 4: CODE CHECKER --------------------------- #
code_checker_prompt = PromptTemplate.from_template(
    """
You are a Manim code checker and auto-fixer. Your job is to analyze the provided Manim code and return a corrected version if there are any errors.

Fix all of the following types of issues:
- Syntax errors (e.g. unexpected indent, missing colons, misused parentheses)
- Runtime errors (e.g. UnboundLocalError, TypeError, missing arguments)
- Incorrect usage of Manim classes or methods (e.g. Dot, Rectangle, Axes, get_graph)
- Improper object initialization (e.g. passing duplicate keyword arguments)
- Issues related to missing files (e.g. images or SVGs not found)
- Logical mistakes such as missing animations or scene breaks

❗️Never return the same code again if an error exists. Always analyze the given error and correct the code logically.

❌ Do NOT return:
- Markdown formatting (no triple backticks)
- Headings like "Here's the fixed code:"
- Any explanation or extra commentary

✅ Only return:
The corrected, clean, runnable Python code (Manim CE compatible). Ensure it can be run with `manim -pql generated_scene.py MyScene` without error.

### INPUT (Broken Code):
{manim_code}
{error_message}

### OUTPUT (Corrected Code):
Only corrected Python code, no explanations, no formatting tags.
"""
)


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
code_gen_chain = code_gen_prompt | llm
realism_chain = realism_prompt | llm
beautifier_chain = beautifier_prompt | llm
code_checker_chain = code_checker_prompt | llm
solution_explainer_chain=solution_explainer_prompt | llm

# Final pipeline with Code Checker
final_pipeline = RunnableSequence(
    code_gen_chain,
    realism_chain,
    beautifier_chain
)

error_pipeline = RunnableSequence(
    code_checker_chain,
    realism_chain,
    beautifier_chain

)

# ----------------------------- CLI INTERFACE -------------------------------- #

def check_and_fix_code(manim_code):
    is_code_fixed = False

    while not is_code_fixed:
        # ✅ Step 1: Strip markdown artifacts like backticks and 'python'
        code_lines = [
            line for line in manim_code.splitlines()
            if "```" not in line and not line.strip().lower().startswith("python")
        ]
        cleaned_code = "\n".join(code_lines).strip()

        # ✅ Step 2: Save cleaned code to file
        with open("generated_scene.py", "w", encoding="utf-8") as f:
            f.write(cleaned_code)

        try:
            print("code begin!!!")
            # ✅ Step 3: Try rendering with Manim
            result = subprocess.run(
                ['manim', '-ql', 'generated_scene.py', 'MyScene', '--media_dir', './static/renders'],
                capture_output=True,
                text=True
            )
            print("code checker!!!")

            if result.returncode == 0:
                print("✅ Code ran successfully.")
                is_code_fixed = True
            else:
                print("❌ Runtime errors found, sending to checker agent...")
                # ✅ Step 4: Use agent to fix and return new code
                manim_code = error_pipeline.invoke({
                    "manim_code": cleaned_code,
                    "error_message": result.stderr
                }).content.strip()
                print("Error Corrected")

        except Exception as e:
            print(f"🔥 Unexpected exception: {str(e)}")
            break

    return cleaned_code

def agent(cleaned_response):
    
    initial_code = final_pipeline.invoke({
        "combined_input": cleaned_response  # Pass the full cleaned response as the input
    })
    raw_code = initial_code.content.strip()
    
    print("RAW CODE : ",raw_code)

    # Remove all lines that contain backticks or language declarations
    code_lines = [
        line for line in raw_code.splitlines()
        if "```" not in line and not line.strip().lower().startswith("python")
    ]
    cleaned_code = "\n".join(code_lines).strip()

    # Step 2: Pass the cleaned code to the checker for fixes and beautification
    final_code = check_and_fix_code(cleaned_code).strip()
