import sqlite3
from rich import pretty
from rich.panel import Panel
from rich.console import Console
from rich.table import Table

console = Console()

# FUNCIONES
def mostrar_producto(productos: dict):
    # CREO LA TABLA
    product_table = Table(title="LISTA DE PRODUCTOS", show_header=True, header_style="bold green")
    
    # DEFINO LAS COLUMNAS
    product_table.add_column("ID", style="cyan", justify="left")
    product_table.add_column("Título", style="cyan", justify="left")
    product_table.add_column("Precio_unitario ($)", style="bold")
    product_table.add_column("Categoria", style="magenta", justify="right")
    product_table.add_column("Dimensiones (cm)", style="yellow", justify="right")
    product_table.add_column("Stock", style="cyan", justify="right")
    
    # AGREGO LAS FILAS
    for producto in productos:
        product_table.add_row(
            f"{producto[0]}",
            f"{producto[1]}",
            f"{producto[2]}",
            f"{producto[3]}",
            f"{producto[4]}x{producto[5]}",
            f"{producto[6]}"
        )

    # MUESTRO TABLA
    console.print(product_table)
    
def cargar_nuevo_producto():
    cursor = con.cursor()

    # DEFINO LAS VARIABLES
    titulo = ""
    precio = 0
    
    # VALIDO QUE EL TITULO DEL PRODUCTO NO SEA VACÍO
    while ( titulo == "" or titulo.strip() == "" ):
        try:
            titulo = input("Ingrese el nombre o título del cuadro: ")
            if ( titulo == "" or titulo.strip() == "" ):
                print("❗ ERROR: El título del producto no puede quedar vacío.")
        except:
            print("❗ ERROR: El título del producto no puede quedar vacío.")

    # VALIDO QUE EL PRECIO DEL PRODUCTO SEA MAYOR A CERO
    while not ( precio > 0 ):
        try: 
            precio = int( input("Ingrese el precio unitario: ") )
            if ( precio <= 0 ):
                print("❗ ERROR: El precio unitario debe ser un número entero válido mayor a 0.")
        except:
            print("❗ ERROR: El precio unitario debe ser un número entero válido mayor a 0.")
        
    stock = ""
    # VALIDO QUE EL STOCK DEL PRODUCTO SEA IGUAL O MAYOR A CERO
    while not (stock.isdigit() and int(stock) >= 0):
        stock = input("Ingrese el stock: ")
        if not stock.isdigit():
            print("❗ ERROR: El stock debe ser un número válido.")
        elif int(stock) < 0:
            print("❗ ERROR: El stock debe ser mayor o igual a 0.")
            
    categoria = ""
    # VALIDO QUE LA CATEGORÍA DEL PRODUCTO SEA DISTINTA DE VACÍO
    while categoria.strip() == "":
        categoria = input("Ingrese la categoría del cuadro: ")
        if categoria.strip() == "":
            print("❗ ERROR: La categoría del cuadro no puede quedar vacía.")

    ancho = ""
    # VALIDO QUE EL ANCHO DEL PRODUCTO SEA MAYOR A CERO
    while not (ancho.isdigit() and int(ancho) > 0):
        ancho = input("Ingrese el ancho del cuadro (en cm): ")
        if not ancho.isdigit() or int(ancho) <= 0:
            print("❗ ERROR: El ancho debe ser un número válido mayor a 0.")

    alto = ""
    # VALIDO QUE EL ALTO DEL PRODUCTO SEA MAYOR A CERO
    while not (alto.isdigit() and int(alto) > 0):
        alto = input("Ingrese el alto del cuadro (en cm): ")
        if not alto.isdigit() or int(alto) <= 0:
            print("❗ ERROR: El alto debe ser un número válido mayor a 0.")
    
    try:
        cursor.execute("""
            INSERT INTO cuadros (titulo, precio, categoria, ancho, alto, stock) VALUES (?, ?, ?, ?, ?, ?)
        """, (titulo, precio, categoria, ancho, alto, stock))
        con.commit()
        cursor.close()
        console.print("====== PRODUCTO AGREGADO CON ÉXITO ======", style="bold green")
    except:
        console.print("❗ ERROR AL INSERTAR EL PRODUCTO", style="bold red")

def borrar_producto():
    cursor = con.cursor()
    while (True):
        try:
            borrar_id = input("Ingrese el ID para borrar: ")
            if not borrar_id.isdigit() or int(borrar_id) <= 0:
                console.print("❗ ERROR: Debe ingresar un número válido como ID (mayor a 0).", style="bold red")
                continue
            borrar_id = int(borrar_id)
            cuadro_existente = cursor.execute("""
                SELECT id, titulo, precio, categoria, ancho, alto, stock FROM cuadros WHERE id=?""", (borrar_id,)).fetchone()
            
            if not cuadro_existente:
                console.print("❗ ERROR: EL ID INGRESADO NO EXISTE.", style="bold red")
                continue

            # CREO LA TABLA QUE MUESTRA EL DETALLE DE LO QUE VOY A ELIMINAR
            cuadro_a_borrar = Table(title="PRODUCTOS A ELIMINAR", show_header=True, header_style="bold red")
            # DEFINO LAS COLUMNAS
            cuadro_a_borrar.add_column("ID", style="red", justify="left")
            cuadro_a_borrar.add_column("Título", style="red", justify="left")
            cuadro_a_borrar.add_column("Precio_unitario ($)", style="bold red")
            cuadro_a_borrar.add_column("Categoria", style="red", justify="right")
            cuadro_a_borrar.add_column("Dimensiones (cm)", style="red", justify="right")
            cuadro_a_borrar.add_column("Stock", style="red", justify="right")
            # AGREGO LAS FILAS - (Tuve que convertir algunos datos porque solo me rendereaba como string).
            cuadro_a_borrar.add_row(
                str(cuadro_existente[0]),
                cuadro_existente[1],
                f"{cuadro_existente[2]:.2f}",
                cuadro_existente[3],
                f"{cuadro_existente[4]}x{cuadro_existente[5]}",
                str(cuadro_existente[6])
            )
            # MUESTRO TABLA 
            console.print(cuadro_a_borrar)
        
            confirmar_borrar = input("¿Quiere confirmar el borrado del producto? S/N: ")
            if confirmar_borrar.lower() == "s":
                cursor.execute("DELETE FROM cuadros WHERE id=?", (borrar_id,)).fetchone()
                con.commit()
                console.print(f"====== HA ELIMINADO EL CUADRO '{cuadro_existente[1]}'======", style="bold yellow")
                return
            else:
                console.print("====== EL BORRADO NO FUE CONFIRMADO ======", style="bold yellow")
                return
        except:
            console.print("❗ OCURRIÓ UN PROBLEMA AL PROCESAR LOS DATOS. INTENTE NUEVAMENTE.", style="bold red")
            return

def editar_stock_producto():
    cursor = con.cursor()
    mostrar_productos()
    while (True):
        try:
            id_a_editar = int(input("Ingrese el id del producto: "))
            
            cuadro_existente = cursor.execute("SELECT id, titulo FROM cuadros WHERE id=?", (id_a_editar,)).fetchone()
            
            if not cuadro_existente:
                console.print("====== EL ID INGRESADO NO EXISTE, INTENTE NUEVAMENTE CON OTRO ======", style="bold red")
                continue
            
            # GUARDO EL TITULO PARA AGREGARLO LUEGO AL MENSAJE
            titulo_producto = cuadro_existente[1]
            while (True):        
                try:
                    nuevo_stock = int(input("Ingrese el nuevo stock: "))
                    if nuevo_stock < 0:
                        console.print("El stock no puede ser negativo.", style="bold red")
                    cursor.execute("UPDATE cuadros SET stock=? WHERE id=?", (nuevo_stock, id_a_editar))
                    con.commit()
                    console.print(f"====== EL STOCK DEL CUADRO '{titulo_producto}' FUE ACTUALIZADO A {nuevo_stock} ======", style="bold cyan")
                    return
                except:
                    console.print("❗ OCURRIÓ UN ERROR AL PROCESAR EL STOCK. INTENTE NUEVAMENTE.", style="bold red")
        except:
            console.print("❗ OCURRIÓ UN ERROR AL PROCESAR EL ID. INTENTE NUEVAMENTE.", style="bold red")

def mostrar_productos():
    cursor = con.cursor()
    cursor.execute("SELECT id, titulo, precio, categoria, ancho, alto, stock FROM cuadros")
    cuadros_db = cursor.fetchall()
    # CREO LA TABLA
    product_table = Table(title="LISTA DE PRODUCTOS", show_header=True, header_style="bold green")
    # DEFINO LAS COLUMNAS
    product_table.add_column("ID", style="cyan", justify="left")
    product_table.add_column("Título", style="cyan", justify="left")
    product_table.add_column("Precio_unitario ($)", style="bold")
    product_table.add_column("Categoria", style="magenta", justify="right")
    product_table.add_column("Dimensiones (cm)", style="yellow", justify="right")
    product_table.add_column("Stock", style="cyan", justify="right")
    
    # AGREGO LAS FILAS
    # ID
    # TITULO
    # PRECIO
    # CATEGORIA
    # DIMENSION (ANCHOXALTO)
    # STOCK
    for producto in cuadros_db:
        product_table.add_row(
            str(producto[0]),
            producto[1],
            f"{producto[2]}",
            producto[3],
            f"{producto[4]}x{producto[5]}",
            str(producto[6])
        )
    
    # MUESTRO TABLA
    console.print(product_table)
    
def reporte_bajo_stock():
    while (True):
        try:
            cantidad_minima = input("Ingrese el número desde el cual considera bajo stock: ")
            if not cantidad_minima.isdigit():
                console.print("====== ERROR: INGRESE UN NÚMERO VÁLIDO PARA EL STOCK MÍNIMO ======", style="bold red")
                continue
            
            cantidad_minima = int(cantidad_minima)
            
            cursor = con.cursor()
            cursor.execute("SELECT id, titulo, precio, categoria, ancho, alto, stock FROM cuadros WHERE stock <= ?", (cantidad_minima,))
            cuadros_db = cursor.fetchall()
            
            if not cuadros_db:
                console.print("====== NO EXISTEN PRODUCTOS CON STOCK MENOR AL INGRESADO ======", style="bold yellow")
                continue
            mostrar_producto(cuadros_db)
            return

        except:
            console.print("❗ ERROR: Debe ingresar un número válido para el stock mínimo.", style="bold red")
            return

def buscar_por_nombre():
        cursor = con.cursor()
        
        try: 
            nombre_a_buscar = input("Ingrese el título del cuadro a buscar: ")
            
            # DIVIDO LA CADENA PARA BUSCAR CADA PALARBA
            palabras_a_buscar = nombre_a_buscar.split()
            
            # CREO Y GUARDO LA QUERY PRINCIPAL
            query = "SELECT id, titulo, precio, categoria, ancho, alto, stock FROM cuadros WHERE"
            
            # CREO EL LIKE PARA CADA PALABRA INGRESADA Y LO CONCATENO CON UN OR
            query_conditions = " OR ".join([" LOWER(titulo) LIKE LOWER(?)" for _ in palabras_a_buscar])
            query += " " + query_conditions

            #A CADA PALABRA LE AGREGO % PARA QUE COINCIDAN EN CUALQUIER LUGAR DE LA CADENA
            params = ['%' + palabra + '%' for palabra in palabras_a_buscar]
            
            # EJECUTO LA QUERY CON LOS PARAMETROS
            cursor.execute(query, tuple(params))
            
            cuadros_db = cursor.fetchall()
            
            # SI ENCUENTRO COINCIDENCIA MUESTRO LOS RESULTADOS USANDO LA FUNC MOSTRAR PRODUCTOS
            if cuadros_db:
                mostrar_producto(cuadros_db)
            else:
                console.print("====== NO EXISTEN PRODUCTOS QUE COINCIDAN CON LA BÚSQUEDA ======", style="bold yellow")
        except:
            console.print("❗ ERROR: Ocurrió un problema al realizar la búsqueda.", style="bold red")

def enter_para_continuar():
    input("Enter para continuar...")

# CONEXION A BASE DE DATOS
con = sqlite3.connect("cuadros_db.db")
cursor = con.cursor()

listado_productos = []
opcion = "in"
# MENU PRINCIPAL

while opcion != "0":
    texto_bienvenida = "Esta aplicación permite cargar y mostrar cuadros con sus respectivos atributos como título, precio, categoría, dimensiones y stock."
    console.print(Panel(texto_bienvenida, title="TIENDA DE CUADROS: MONO LISO", title_align="center", style="cyan bold", border_style="cyan"))

    menu_table = Table(show_header=True, header_style="bold cyan")
    # DEFINO LAS COLUMNAS
    menu_table.add_column("OPCIÓN", style="cyan", justify="center")
    menu_table.add_column("ACCIÓN", style="white")
    # LISTA DE OPCIONES DEL MENU
    menu_table.add_row("1", "➕ Cargar nuevo cuadro", style="cyan")
    menu_table.add_row("2", "👁️  Ver lista de cuadros", style="cyan")
    menu_table.add_row("3", "🔎  Buscar por título", style="cyan")
    menu_table.add_row("4", "✏️  Editar cuadro", style="cyan")
    menu_table.add_row("5", "🗑️  Borrar cuadro", style="cyan")
    menu_table.add_row("6", "⏬  Reporte bajo stock", style="cyan")
    menu_table.add_row("0", "❌ Salir del menú", style="cyan")

    # MUESTRO LA TABLA
    console.print(menu_table)
    
    opcion = input ("Ingrese una opción: ")
    
    if opcion == "1":
        cargar_nuevo_producto()
        
    elif opcion == "2":
        mostrar_productos()
    
    elif opcion == "3":
        buscar_por_nombre()
        
    elif opcion == "4":
        editar_stock_producto()
        
    elif opcion == "5":
        borrar_producto()
        
    elif opcion == "6":
        reporte_bajo_stock()
        
    elif opcion == "0":
        texto_al_salir = "====== Gracias por usar la app ====== Has abandonado el menú ======"
        console.print(Panel(texto_al_salir, title="", title_align="center", style="red bold", border_style="red"))
        cursor.close()
        con.close()

    else:
        console.print("⚠️  OPCIÓN INCORRECTA, INTENTE NUEVAMENTE ⚠️", style="bold yellow")

    enter_para_continuar()

    