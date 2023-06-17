const db = require("./db_connection");

/**** Read the assignments table, joined with subjects table ****/


const select_recipe_sql = `
SELECT *
FROM recipe
`;

db.execute(select_recipe_sql, 
    (error, results) => {
        if (error) 
            throw error;

        console.log("Table 'recipe' contents:")
        console.log(results);
    }
);

db.end();