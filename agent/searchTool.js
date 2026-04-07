const https = require('https');

// Simple web search using DuckDuckGo Instant Answer API
function searchWeb(query) {
  return new Promise((resolve, reject) => {
    const url = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_html=1&skip_disambig=1`;
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
    };
    https.get(url, options, (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          // Extract a short snippet from various fields
          const answer = result.Answer || result.AbstractText || result.Definition || 
                         (result.RelatedTopics && result.RelatedTopics[0] && result.RelatedTopics[0].Text) || 
                         'No direct answer found.';
          resolve(answer.substring(0, 300)); // Limit to 300 chars for better info
        } catch (error) {
          reject(error);
        }
      });
    }).on('error', (error) => {
      reject(error);
    });
  });
}

module.exports = { searchWeb };