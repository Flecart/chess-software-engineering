// https://chat.openai.com/share/b66c3384-8054-41de-bc44-b77335f451de

const express = require('express');
const { exec } = require('child_process');

const app = express();
const secretToken = 'your_secret_token'; // Replace with your secret token

app.use(express.json());

app.post('/webhook', (req, res) => {
  if (req.header('X-Gitlab-Token') === secretToken) {
    exec('./build.sh', (error, stdout, stderr) => {
      if (error) {
        console.error(`Build failed: ${error}`);
        return res.status(500).send('Build failed');
      }
      console.log(`Build output: ${stdout}`);
      res.status(200).send('Build successful');
    });
  } else {
    res.status(403).send('Unauthorized');
  }
});

app.listen(3000, () => {
  console.log('Webhook listener running on port 3000');
});
