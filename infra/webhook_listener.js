// https://chat.openai.com/share/b66c3384-8054-41de-bc44-b77335f451de

const express = require('express');
const { exec } = require('child_process');

const app = express();

// Look for the "--secret" argument

const secretToken = process.argv[2];  // like node webhook_listener.js 123456

app.use(express.json());

app.post('/webhook', (req, res) => {
  if (req.header('X-Gitlab-Token') === secretToken) {
    exec('bash ./build.sh', (error, stdout, stderr) => {
      if (error) {
        console.error(`Build failed: ${error}`);
        return res.status(500).send('Build failed');
      }
      console.log(`Build output: ${stdout}`);
      res.status(200).send('Build successful');
    });
  } else {
    console.log("-" + req.header('X-Gitlab-Token') + "-");
    console.log("-" + secretToken + "-");
    res.status(403).send('Unauthorized');
  }
});

app.listen(4000, () => {
  console.log('Webhook listener running on port 4000');
});
