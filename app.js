// set up the server
const express = require("express" );
const app = express()
const port = 3000;


//start the server
app.listen(port, () => {
    console.log("App server listening on ${port}");
});

// define middleware that serves static resources in the public directory
app.use(express.static(__dirname));
// Configure Express to parse URL-encoded POST request bodies (traditional forms)
app.use( express.urlencoded({ extended: false }) );

// define a route for the default home page
app.get( "/", ( req, res ) => {
    res.sendFile(__dirname + "/login.html")
});