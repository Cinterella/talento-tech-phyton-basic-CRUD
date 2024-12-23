import sqlite3

con = sqlite3.connect("cuadros_db.db")
cursor = con.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cuadros(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        precio INTEGER,
        categoria TEXT,
        ancho INTEGER,
        alto INTEGER,
        stock INTEGER
    )
""")

# esto solo usamos las primera vez
cursor.execute("""
    INSERT INTO cuadros (titulo, precio, categoria, ancho, alto, stock) VALUES
        ('Los comedores de papa', 50000.00, 'Realismo', 114.0, 84.0, 10),
        ('La Gioconda', 85000.00, 'Renacimiento', 77.0, 53.0, 15),
        ('La noche estrellada', 60000.00, 'Postimpresionismo', 92.0, 73.0, 12),
        ('El grito', 70000.00, 'Expresionismo', 91.0, 73.5, 8),
        ('El jardín de las delicias', 80000.00, 'Renacimiento', 220.0, 390.0, 6),
        ('La joven de la perla', 75000.00, 'Barroco', 44.5, 39.0, 10),
        ('Las meninas', 90000.00, 'Barroco', 318.0, 276.0, 5),
        ('La persistencia de la memoria', 95000.00, 'Surrealismo', 24.0, 33.0, 20),
        ('La creación de Adán', 120000.00, 'Renacimiento', 280.0, 570.0, 9),
        ('El nacimiento de Venus', 100000.00, 'Renacimiento', 172.0, 278.0, 7),
        ('El beso', 95000.00, 'Simbolismo', 180.0, 180.0, 14),
        ('El abrazo', 50000.00, 'Expresionismo', 180.0, 140.0, 10),
        ('Mujer con sombrero', 55000.00, 'Fauvismo', 60.0, 50.0, 18),
        ('Guernica', 120000.00, 'Cubismo', 349.0, 777.0, 5),
        ('La rendición de Breda', 70000.00, 'Barroco', 300.0, 330.0, 6),
        ('La escuela de Atenas', 110000.00, 'Renacimiento', 500.0, 770.0, 7),
        ('Las tres gracias', 85000.00, 'Neoclasicismo', 140.0, 170.0, 8),
        ('El almuerzo de los remeros', 60000.00, 'Impresionismo', 130.0, 180.0, 13),
        ('Los jugadores de cartas', 95000.00, 'Cubismo', 100.0, 80.0, 10),
        ('El matrimonio Arnolfini', 65000.00, 'Renacimiento', 82.0, 60.0, 16);
""")
con.commit()
cursor.close()
con.close()