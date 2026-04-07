# ReAct Agent Demo

A simple web application demonstrating the ReAct (Reason + Act) pattern for AI agents.

## Features

- **ReAct Pattern**: Shows step-by-step reasoning, tool usage, and answer generation
- **Web Search**: Uses DuckDuckGo API for information retrieval
- **AI-Powered Answers**: Leverages OpenAI GPT-3.5-turbo for intelligent response formatting
- **Modern UI**: Clean, responsive interface with smooth animations

## Project Structure

```
├── backend/          # Express server
│   ├── server.js     # Main server file
│   └── package.json
├── frontend/         # Client-side code
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── agent/            # ReAct agent logic
│   ├── agent.js      # Main agent implementation
│   └── searchTool.js # Web search functionality
└── package.json      # Root dependencies
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Harishmitha11/GenAi_Training.git
   cd GenAi_Training
   ```

2. **Install dependencies**
   ```bash
   # Install OpenAI (root level)
   npm install

   # Install backend dependencies
   cd backend
   npm install
   cd ..
   ```

3. **Set up OpenAI API Key**
   - Get your API key from [OpenAI](https://platform.openai.com/api-keys)
   - Set the environment variable:
     ```bash
     export OPENAI_API_KEY=your-api-key-here
     ```
   - Or create a `.env` file in the root directory:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```

4. **Run the application**
   ```bash
   cd backend
   npm start
   ```

5. **Open in browser**
   - Visit `http://localhost:3000`

## Usage

- Enter a question in the input field
- Click "Ask" to see the ReAct process in action
- The interface displays:
  - Reasoning steps
  - Tool usage (when applicable)
  - Search results
  - Final AI-generated answer

## Example Questions

- "Hello" (direct response)
- "What is the capital of France?" (uses search + AI)
- "Who won the Nobel Prize in Physics 2023?" (demonstrates full ReAct flow)

## Technologies Used

- **Backend**: Node.js, Express
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **AI**: OpenAI GPT-3.5-turbo
- **Search**: DuckDuckGo Instant Answer API

## ReAct Pattern

The agent follows the ReAct pattern:
1. **Reason**: Analyze the question
2. **Act**: Decide to use tools or respond directly
3. **Observe**: Capture tool results
4. **Answer**: Generate final response

This educational demo shows how AI agents can combine reasoning with tool usage for complex tasks.