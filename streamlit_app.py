import streamlit as st
from math_cot_solver import solve_math_problem, self_check_reasoning, review_python_code

st.title("Chain-of-Thought Math Problem Solver with Self-Reflecting Code Review")

st.markdown("""
This app solves math problems using Chain-of-Thought (CoT) reasoning powered by OpenAI API.
It also includes a self-check for reasoning and a code review agent for Python code.
""")

# Math Problem Solver Section
st.header("Math Problem Solver")
problem = st.text_area("Enter a math problem (e.g., 'Solve 2x + 3 = 7' or word problems):", height=100)

if st.button("Solve Problem"):
    if problem.strip():
        try:
            with st.spinner("Generating reasoning..."):
                reasoning = solve_math_problem(problem)
            st.subheader("Step-by-Step Reasoning:")
            st.write(reasoning)
            
            with st.spinner("Self-checking reasoning..."):
                check = self_check_reasoning(problem, reasoning)
            st.subheader("Self-Check Review:")
            st.write(check)
        except Exception as e:
            if "insufficient_quota" in str(e):
                st.error("API Quota Exceeded: Your OpenAI API key has reached its usage limit. Please check your OpenAI billing dashboard and upgrade your plan if needed. Alternatively, use a different API key with available credits.")
            else:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a math problem.")

# Code Review Section
st.header("Self-Reflecting Code Review Agent")
code = st.text_area("Enter Python code to review:", height=200)

if st.button("Review Code"):
    if code.strip():
        try:
            with st.spinner("Reviewing code..."):
                review = review_python_code(code)
            st.subheader("Code Review:")
            st.write(review)
        except Exception as e:
            if "insufficient_quota" in str(e):
                st.error("API Quota Exceeded: Your OpenAI API key has reached its usage limit. Please check your OpenAI billing dashboard and upgrade your plan if needed. Alternatively, use a different API key with available credits.")
            else:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter Python code.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and OpenAI API. Ensure your API key is set in `math_cot_solver.py`.")