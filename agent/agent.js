const { searchWeb } = require('./searchTool');
const { Configuration, OpenAIApi } = require('openai');

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY || 'your-openai-api-key-here'
});
const openai = new OpenAIApi(configuration);

// Simple ReAct agent implementation
async function runAgent(question) {
  const trace = [];

  // Step 1: Reason
  trace.push('Reason: Analyzing the question to understand what information is needed.');
  trace.push(`Question: ${question}`);

  // Determine if we need to search
  const needsSearch = !isSimpleQuestion(question);

  if (needsSearch) {
    trace.push('Decision: This requires external information. I will use the search tool.');
    
    // Step 2: Act - Call search tool
    trace.push('Act: Calling web search tool...');
    const searchResult = await searchWeb(question);
    trace.push(`Observation: Search result: ${searchResult}`);
    
    // Step 3: Final Answer - Use OpenAI to generate better answer
    const answer = await generateAnswerWithOpenAI(question, searchResult);
    
    return { trace, answer };
  } else {
    // Direct answer
    trace.push('Decision: This is a simple question I can answer directly.');
    const answer = getSimpleAnswer(question);
    
    return { trace, answer };
  }
}

// Helper to check if question needs search
function isSimpleQuestion(question) {
  const simpleKeywords = ['hello', 'hi', 'how are you', 'what is your name'];
  return simpleKeywords.some(keyword => question.toLowerCase().includes(keyword));
}

// Helper to generate answer using OpenAI
async function generateAnswerWithOpenAI(question, searchResult) {
  try {
    const prompt = `Based on this search result: "${searchResult}", provide a clear and concise answer to the question: "${question}". Keep the answer informative but brief.`;
    
    const response = await openai.createChatCompletion({
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 150,
      temperature: 0.7
    });
    
    return response.data.choices[0].message.content.trim();
  } catch (error) {
    console.error('OpenAI error:', error);
    return `Based on the search results: ${searchResult}`; // Fallback
  }
}

// Simple answers for demo
function getSimpleAnswer(question) {
  if (question.toLowerCase().includes('hello') || question.toLowerCase().includes('hi')) {
    return 'Hello! I am a simple AI agent demonstrating the ReAct pattern.';
  }
  if (question.toLowerCase().includes('how are you')) {
    return 'I am doing well, thank you for asking!';
  }
  if (question.toLowerCase().includes('what is your name')) {
    return 'My name is ReAct Demo Agent.';
  }
  return 'I am not sure about that simple question.';
}

module.exports = { runAgent };