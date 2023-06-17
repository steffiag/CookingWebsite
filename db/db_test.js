
const db = require("./db_connection")

db.execute('SELECT 1 + 1 AS solution',
    (error, results) => {
        if (error)
            throw error;
        console.log(results);
    }
);

db.end();
