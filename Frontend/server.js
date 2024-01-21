const express = require('express');
const path = require('path');
const serveStatic = require('serve-static');
const nodemailer = require('nodemailer');

const app = express();
const port = process.env.PORT || 3000;

// Serve static files from the React app
app.use(serveStatic(path.join(__dirname, 'my-app/build')));

// Endpoint to send email
app.get('/sendmail', (req, res) => {
    // Create a transporter using your email service and credentials
    let transporter = nodemailer.createTransport({
        service: 'gmail', // Example with Gmail, configure according to your provider
        auth: {
            user: 'kirksprojects@gmail.com', // Replace with your email
            pass: 'firk ynlv iukq yzhq' // Replace with your email password or app-specific password
        }
    });

    let mailOptions = {
        from: 'kirksprojects@gmail.com', // Replace with your email
        to: 'kirksprojects@gmail.com', // Replace with the receiver's email
        subject: 'ALERT',
        text: 'You just entered a dangerous bourough!'
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.error(error);
            res.status(500).send('Error while sending mail: ' + error);
            return;
        }
        res.send('Email sent successfully');
    });
});

// Handles any requests that don't match the ones above
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname + '/my-app/build/index.html'));
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
