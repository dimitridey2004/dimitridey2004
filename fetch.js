const fs = require('fs');
const https = require('https');
https.get('https://github.com/dimitridey2004.png', (res) => {
  const chunks = [];
  res.on('data', d => chunks.push(d));
  res.on('end', () => {
    const buffer = Buffer.concat(chunks);
    fs.writeFileSync('avatar.b64', buffer.toString('base64'));
  });
});
