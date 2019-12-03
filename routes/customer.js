const express	= require('express');
const router	= express.Router();
const mysql		= require('mysql');
const args		= process.argv.slice(2);

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

router.get('/dashboard/:id', (req, res) => {
    console.log("Fetching user with id: " + req.params.id);

    const profId = req.params.id;
    const queryString = "SELECT * FROM customers WHERE id=?";

    connectionPool.query(queryString, [profId], (err, obj, fields) => {
    	if(err) {
    		console.log("GET failed: " + err);
    		res.sendStatus(500);
    		return;
    	}
    	res.render('dashboard', {page:'Customer Dashboard', customer:obj[0] });
    });
});

router.get('/profile/:id', (req, res) => {
    console.log("Fetching user with id: " + req.params.id);

    const profId = req.params.id;
    const queryString = "SELECT * FROM customers WHERE id=?";

    connectionPool.query(queryString, [profId], (err, obj, fields) => {
    	if(err) {
    		console.log("GET failed: " + err);
    		res.sendStatus(500);
    		return;
    	}
    	res.render('profile', {page:'Customer Profile', customer:obj[0] });
    });
});

router.post('/customer_add', (req, res) => {
	console.log("Adding customer to database");
	const first_name = req.body.new_first_name;
	const last_name = req.body.new_last_name;
	const email = req.body.new_email;
	const lat = req.body.new_lat;
	const long = req.body.new_email;
	const ip = req.body.new_ip;
	const created_at = null;
	const query = "INSERT INTO customers"+
	"(created_at, first_name, last_name, email, latitude, longitude, ip)"+
	"VALUES"+
	"(?, ?, ?, ?, ?, ?, ?,)";
	connectionPool.query(queryString,
		[created_at, first_name, last_name, email, lat, long, ip],
		(err, results, fields) => {
			if(err) {
				console.log("Could not add customer with error: "+ err);
				res.sendStatus(500);
				return;
			}
			console.log("Inserted new customer");
			res.end();
		});
});

module.exports = router;