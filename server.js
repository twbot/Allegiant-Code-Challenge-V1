// REQUIREMENTS
const express       = require('express');
const path          = require('path');
const http          = require('http');
const app           = express();
const port          = process.env.PORT || '4200';
const server        = http.createServer(app);
const mysql			= require('mysql');
const bodyParser	= require('body-parser');
const args			= process.argv.slice(2);

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

const connectionPool = mysql.createPool({
							host: 'localhost',
							user: 'root',
							password: args[0],
							database: 'customers',
							connectionLimit: 10
						});

function getConnection() {
	return connectionPool;
}

//MIDDLEWARE
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
	extended: false
}));

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
	console.log("Fetching users");

    const queryString = "SELECT * FROM customers";

    connectionPool.query(queryString, (err, obj, fields) => {
    	if(err) {
    		console.log("GET failed: " + err);
    		res.sendStatus(500);
    		return;
    	}
    	res.render('index', {page:'Customer Database', customers:obj });
    });

});

const router	= require('./routes/customer.js');

app.use(router);

// LISTENERS
app.set('port', port);

server.listen(port, () => console.log(`Running on localhost:${port}`));
