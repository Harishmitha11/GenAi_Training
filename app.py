import streamlit as st
import os
from dotenv import load_dotenv
from crew_workflow import generate_blog_content

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Multi-Agent Blog Generator", page_icon="✍️", layout="centered")

st.title("✍️ CrewAI Blog Generator")
st.markdown("""
This application uses a 3-agent **CrewAI** team (Researcher, Writer, Editor) to collaboratively create a polished blog post.
""")

# Load API Key from environment or .env file (DO NOT HARDCODE IN GITHUB)
# Groq API key has been removed for security before pushing to GitHub.
# Make sure to set GROQ_API_KEY in your .env file.
# os.environ["GROQ_API_KEY"] = "your-api-key-here"

# Sidebar context
with st.sidebar:
    st.header("Agents at work")
    st.markdown("1. 🔍 **Researcher**: Gathers facts and subtopics.")
    st.markdown("2. ✍️ **Writer**: Drafts the structured article.")
    st.markdown("3. 📝 **Editor**: Polishes, tightens, and formats.")

# Main interface
st.subheader("Topic Selection")
example_topics = [
    "Benefits of AI in Healthcare",
    "Beginner Guide to Python",
    "Future of Remote Work",
    "Importance of Cybersecurity",
    "Custom Topic..."
]

selected_topic = st.selectbox("Choose a sample blog topic, or write your own!", example_topics)

if selected_topic == "Custom Topic...":
    topic = st.text_input("Enter your custom topic here", placeholder="e.g., The Impact of Quantum Computing")
else:
    topic = selected_topic

generate_btn = st.button("Generate Blog Post", type="primary")

if generate_btn:
    if not os.environ.get("GROQ_API_KEY"):
        st.error("Please enter your Groq API key in the sidebar.")
    elif not topic.strip():
        st.error("Please enter a valid topic.")
    else:
        with st.spinner(f"CrewAI Team is researching, writing, and editing: '{topic}'... This may take a couple of minutes."):
            try:
                final_post = generate_blog_content(topic)
                
                st.success("Blog post generated successfully!")
                
                # Display output
                st.markdown("### Final Publish-Ready Blog:")
                st.markdown(final_post)
                
                # Download button
                st.download_button(
                    label="Download Markdown",
                    data=final_post,
                    file_name=f"{topic.lower().replace(' ', '_')}_blog.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")
