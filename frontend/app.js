// Frontend JavaScript for ReAct demo
document.getElementById('askButton').addEventListener('click', async () => {
  const question = document.getElementById('questionInput').value;
  if (!question) return;

  const output = document.getElementById('output');
  output.textContent = 'Thinking...';

  try {
    const response = await fetch('http://localhost:3000/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });

    const result = await response.json();
    output.textContent = result.trace.join('\n') + '\n\n' + result.answer;
  } catch (error) {
    output.textContent = 'Error: ' + error.message;
  }
});