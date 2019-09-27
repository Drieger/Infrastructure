const app = require('express')();

app.get('/', (req, res) => {
  console.log(`${req.method} ${req.url} ${new Date()}`);
  res.send('Hello from server');
});

app.listen(3000, () => {
  console.log('Server is up and running on port 3000');
});
