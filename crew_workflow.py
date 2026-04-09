from crewai import Agent, Task, Crew, Process
import os

def generate_blog_content(topic: str) -> str:
    """
    Orchestrates the Researcher, Writer, and Editor agents to generate a blog post.
    """
    # Using the LiteLLM string format which is standard for CrewAI
    llm = "groq/llama-3.3-70b-versatile"

    # 1. Researcher Agent
    researcher = Agent(
        role='Senior Content Researcher',
        goal=f'Uncover key facts, statistics, and subtopics about: {topic}',
        backstory='You are an expert researcher with a keen eye for finding accurate and relevant information. You know how to structure insights for writers to consume easily.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # 2. Writer Agent
    writer = Agent(
        role='Expert Blog Writer',
        goal=f'Transform research insights about "{topic}" into an engaging, well-structured drafting blog post.',
        backstory='You are an elite copywriter and tech blogger. You know how to take raw facts and turn them into an engaging narrative with logical flow, headings, and clear explanations.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # 3. Editor Agent
    editor = Agent(
        role='Managing Content Editor',
        goal='Refine and polish the blog draft into a publication-ready piece that is 600-900 words long.',
        backstory='You are a meticulous editor. You improve readability, grammar, and tone. You ensure the final piece is formatted in clean Markdown, without any meta commentary or mentioning of "agents". You cut repetition and fluff.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # Task 1: Research
    research_task = Task(
        description=f'Research the topic: "{topic}". Produce a structured list of key facts, concepts, relevant examples, and 3-5 important subtopics to cover. Ensure information is accurate.',
        expected_output='A bulleted list of research notes, statistics, concepts, and suggested subtopics.',
        agent=researcher
    )

    # Task 2: Writing
    writing_task = Task(
        description=f'Using the research provided, write a full blog draft about "{topic}". The draft must include an engaging title, an introduction, 3-5 sections with headings, and a concluding paragraph. Use practical examples where relevant and avoid unnecessary jargon.',
        expected_output='A full 600-900 word blog draft formatted in Markdown, with headings and paragraphs.',
        agent=writer,
        context=[research_task]
    )

    # Task 3: Editing
    editing_task = Task(
        description='Review the drafted blog post. Polish the output by improving clarity, grammar, and readability. Ensure the final article uses professional tone. Remove any awkward phrasing or repetition. IMPORTANT constraints: Final output must be pure Markdown formatted properly (headings, paragraphs). Do NOT include any meta commentary, and do NOT mention the agents. Ensure length is between 600-900 words.',
        expected_output='A final, polished, publication-ready blog post in Markdown format.',
        agent=editor,
        context=[writing_task]
    )

    # Instantiate the Crew
    blog_crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=True
    )

    # Start the workflow
    result = blog_crew.kickoff()
    
    # Return the raw result payload
    return str(result)
