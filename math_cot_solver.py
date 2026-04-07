from groq import Groq
import ast
import os

# Set your Groq API key here - Use environment variable for security
client = Groq(api_key=os.getenv('GROQ_API_KEY', 'your_groq_api_key_here'))

def solve_math_problem(problem, model="llama-3.3-70b-versatile"):
    """
    Solves a math problem using Chain-of-Thought reasoning via Groq API.

    Args:
        problem (str): The math problem to solve.
        model (str): The Groq model to use (default: llama-3.3-70b-versatile).

    Returns:
        str: The step-by-step reasoning and final answer.
    """
    prompt = f"""Solve the following math problem using Chain-of-Thought (CoT) reasoning. Break it down into clear, logical steps. Show all intermediate calculations, reasoning, and dependencies between steps. Finally, state the final answer clearly.

Problem: {problem}

Step-by-step reasoning:"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.1  # Low temperature for consistent reasoning
        )
        reasoning = response.choices[0].message.content.strip()
        return reasoning
    except Exception as e:
        return f"Error calling Groq API: {e}"

def self_check_reasoning(problem, reasoning, model="llama-3.3-70b-versatile"):
    """
    Performs a self-check on the reasoning using the model.

    Args:
        problem (str): The original problem.
        reasoning (str): The generated reasoning.
        model (str): The Groq model to use.

    Returns:
        str: Feedback on the reasoning.
    """
    prompt = f"""Review the following Chain-of-Thought reasoning for the math problem. Check for logical errors, calculation mistakes, or incorrect steps. If correct, confirm it. If incorrect, explain the errors and provide the correct reasoning.

Problem: {problem}

Reasoning: {reasoning}

Review:"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.1
        )
        review = response.choices[0].message.content.strip()
        return review
    except Exception as e:
        return f"Error in self-check: {e}"

def review_python_code(code, model="llama-3.3-70b-versatile"):
    """
    Reviews Python code for errors and improvements using AST and Groq.

    Args:
        code (str): The Python code to review.
        model (str): The Groq model to use.

    Returns:
        str: Review feedback.
    """
    # First, check syntax with AST
    try:
        ast.parse(code)
        syntax_check = "Syntax is valid."
    except SyntaxError as e:
        syntax_check = f"Syntax error: {e}"

    # Then, use Groq for deeper review
    prompt = f"""Review the following Python code for errors, best practices, and improvements. Consider efficiency, readability, correctness, and potential bugs. Provide specific suggestions.

Code:
{code}

Syntax check: {syntax_check}

Review:"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.1
        )
        review = response.choices[0].message.content.strip()
        return review
    except Exception as e:
        return f"Error in code review: {e}"

# Example usage
if __name__ == "__main__":
    # Math problem example
    problem = "If a train travels at 60 miles per hour for 2.5 hours, how far does it travel? Also, if it then travels at 40 miles per hour for another 1 hour, what is the total distance?"
    print("Solving math problem...")
    reasoning = solve_math_problem(problem)
    print("Reasoning:\n", reasoning)
    
    print("\nSelf-checking reasoning...")
    check = self_check_reasoning(problem, reasoning)
    print("Self-check:\n", check)
    
    # Code review example (reviewing this script itself)
    print("\nReviewing the code...")
    with open(__file__, 'r') as f:
        code = f.read()
    review = review_python_code(code)
    print("Code review:\n", review)