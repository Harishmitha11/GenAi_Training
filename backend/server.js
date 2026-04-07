const express = require('express');
const cors = require('cors');
const path = require('path');
const { runAgent } = require('../agent/agent');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// Serve static files from frontend directory
app.use(express.static(path.join(__dirname, '../frontend')));

app.post('/ask', async (req, res) => {
  const { question } = req.body;
  try {
    const result = await runAgent(question);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});