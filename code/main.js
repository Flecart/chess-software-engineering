/**
 * This is a simple file to test the deployment of the app
 */

const express = require('express');
const app = express();
app.get('/',(req, res, next) => {
    res.send("Root route is working");
});

app.listen(3000,() => {
    console.log("Server started on port 3000");
});