var express    = require('express');
var mysql      = require('mysql');
var dbconfig   = require('./config/database.js');
var connection = mysql.createConnection(dbconfig);
var app = express();
var mysql = require('mysql');
var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'postgres',
    password : 'soso112233',
    port     :  5433,
    database : 'postgres'
});

connection.connect();

connection.query('SELECT * from finance_list', function(err, rows, fields) {
  if (!err)
    console.log('The solution is: ', rows);
  else
    console.log('Error while performing Query.', err);
});

connection.end();

app.set('port', process.env.PORT || 8080);

/*app.get('/finance_list/coun', function(req, res){
  connection.query('SELECT * from finance_list', function(err, rows) {
    if(err) throw err;
    console.log('The solution is: ', rows);
    res.send(rows);
  });
});
*/

app.listen(app.get('port'), function () {
  console.log('Express server listening on port ' + app.get('port'));
});
