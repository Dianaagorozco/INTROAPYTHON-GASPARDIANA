from res.lifestore_file import lifestore_products, lifestore_sales, lifestore_searches

users = [
    "admin1",
    "admin2",
    "admin3",
]  # Lista de usuarios registrados para la visualización de reportes
passwords = [
    "admin",
    "1234",
    "5648",
]  # Lista de contraseñas en el orden correspondiente al listado de usuarios


logged_in = False

# while (
#     not logged_in
# ):  # Cicloque compara que el usuario y contraseña se encuentren en su respectiva lista, en el mismo indice. Se repite hasta que se ingresen las credenciales correctas
#     user = input("Username: ")
#     password = input("Password: ")
#     if user in users:
#         if password == passwords[users.index(user)]:
#             logged_in = True

#             print("Logged in\n\n")

#         else:
#             print("Incorrect password!")
#     else:
#         print("User does not exist!")

product_id = [
    num for num in range(0, len(lifestore_products))
]  # Lista creada con los IDs de productos en lifestore_products

sale_list = []  # Lista que guarda las ventas por ID de producto
for num in product_id:
    sale_list.append(0)
    for sale in lifestore_sales:
        if sale[1] == num + 1:
            sale_list[num] += 1

search_list = []  # Lista que guarda las busquedas por ID de producto
for id in range(len(lifestore_products)):
    search_list.append(0)
    for search in lifestore_searches:
        if search[1] == id + 1:
            search_list[id] += 1

score_list = []  # Lista que obtiene los scores por producto
for p_id in range(len(lifestore_products)):
    score_list.append(0)
    for sale in lifestore_sales:
        if sale[1] == p_id + 1:
            score_list[p_id] += sale[2]
    if sale_list[p_id] == 0:
        score_list[p_id] = 0
    else:
        score_list[p_id] = round(score_list[p_id] / sale_list[p_id], 1)
category_list = [product[3] for product in lifestore_products]

from datetime import datetime

for i in range(
    len(lifestore_sales)
):  # ciclo que añade monto y mes de venta a la lista de ventas
    for product in lifestore_products:
        if lifestore_sales[i][1] == product[0]:
            lifestore_sales[i].append(product[2])
            lifestore_sales[i].append(
                datetime.strptime(lifestore_sales[i][3], "%d/%m/%Y").month
            )

month_profit = (
    []
)  # lista para calcular los ingresos por cada uno de los meses (almacenará cada mes en un indice)
month_sales = []  # lista para guardar la cantidad de ventas por mes
avg_month_sales = []
for month in range(1, 13):
    month_profit.append(0)
    month_sales.append(0)
    avg_month_sales.append(0)
    for sale in lifestore_sales:
        if sale[6] == month:
            month_profit[month - 1] += sale[5]
            month_sales[month - 1] += 1
            avg_month_sales[month - 1] = (
                month_profit[month - 1] / month_sales[month - 1]
            )


def create_product_summary(category_list, sale_list, search_list, score_list):
    """summary = [product_id, sales, searched, score, category]"""
    summary = []
    for i in range(len(lifestore_products)):
        product_summary = [
            i + 1,
            sale_list[i],
            # lifestore_products[i][1],
            search_list[i],
            score_list[i],
            category_list[i],
            lifestore_products[i][2],
        ]
        summary.append(product_summary)
    return summary


def create_category_summary(category_list, product_summary):
    category_performance = []
    unique_cat_list = list(set(category_list))
    for i in range(len(set(category_list))):
        category_performance.append(["", 0, 0])
        for j in range(len(product_summary)):
            if product_summary[j][4] == unique_cat_list[i]:
                category_performance[i][0] = unique_cat_list[i]
                category_performance[i][1] += product_summary[j][1]  # Sales
                category_performance[i][2] += product_summary[j][2]  # Searches
    return category_performance


def split_into_categories(category_list, product_summary):
    unique_cat_list = list(set(category_list))
    products_by_category = []
    for i in range(len(unique_cat_list)):
        products_by_category.append([])
        for product in product_summary:
            if product[4] == unique_cat_list[i]:
                products_by_category[i].append(product)
    return products_by_category


def sort_id(var):
    return var[0]


def sort_sales(var):
    return var[1]


def sort_search(var):
    return var[2]


def sort_score(var):
    return var[3]


product_summary = create_product_summary(
    category_list, sale_list, search_list, score_list
)


def get_products(product_summary, n: int, filter_fn, descending=True):
    return sorted(product_summary, key=filter_fn, reverse=descending)[0:n]


def get_products_by_score(product_summary, n: int, descending=True):
    if descending:
        return sorted(product_summary, key=sort_score, reverse=True)[0:n]
    else:
        low_score = []
        for item in sorted(product_summary, key=sort_score, reverse=False):
            if item[3] > 0:
                low_score.append(item)
        return low_score[0:n]


def get_total_income(month_profit):
    return sum(month_profit)


def print_top_sales(data):  # Función para imrpimir el top5 de ventas
    print("TOP 5 Ventas")
    for i in range(len(data)):
        print("Rank: " + str(i + 1))
        print("ID: " + str(data[i][0]))
        print("Ventas: " + str(data[i][1]) + "\n")
    return


product_summary = create_product_summary(
    category_list, sale_list, search_list, score_list
)

category_summary = create_category_summary(category_list, product_summary)

products_by_category = split_into_categories(category_list, product_summary)

top_5 = get_products(product_summary, 5, sort_sales)
top_10 = get_products(product_summary, 10, sort_search)
# print_top_sales(top_5)


def print_top_searches(data):  # Función para imrpimir el top10 de búsquedas
    print("TOP 10 Búsquedas")
    for i in range(len(data)):
        print("Rank: " + str(i + 1))
        print("ID: " + str(data[i][0]))
        print("Ventas: " + str(data[i][1]) + "\n")
    return


def print_bottom_sales_by_cat(
    data,
):  # Función para imrpimir las ventas mas bajas por categoria
    for i in range(len(data)):
        print("Rank: " + str(i + 1))
        print("ID: " + str(data[i][0]))
        print("Ventas: " + str(data[i][1]) + "\n")
    return


def print_bottom_search_by_cat(
    data,
):  # Función para imrpimir las ventas mas bajas por categoria
    for i in range(len(data)):
        print("Rank: " + str(i + 1))
        print("ID: " + str(data[i][0]))
        print("Busquedas: " + str(data[i][2]) + "\n")
    return


def print_top_review(data):  # Función para imrpimir el top10 de búsquedas
    for i in range(len(data)):
        print("Rank: " + str(i + 1))
        print("ID: " + str(data[i][0]))
        print("Reseña: " + str(data[i][3]) + "\n")
    return


print("MENU\n")
print("1. TOP5 de productos con mayores ventas, y TOP10 de búsquedas")
print("2. BOTTOM5 de menores ventas por categoría y BOTTOM10 de menores búsquedas")
print(
    "3. TOP5 de productos con mejores reseñas y BOTTOM5 de productos con peores reseñas"
)
print("4. Total de ingresos y ventas mensuales")

option = int(
    input("Digite el numero correspondiente al reporte a desplegar\n")
)  # variable que guarda la opcion elegida por el usuario


if option == 1:
    print_top_sales(top_5)
    print_top_searches(top_10)

if option == 2:
    print("Ventas más bajas por categoría: ")
    for category_products in products_by_category:
        category_products_sorted = get_products(
            category_products, 10, sort_sales, False
        )
        print(str(category_products_sorted[0][4]) + "\n")
        print_bottom_sales_by_cat(category_products_sorted)

    print("Busquedas más bajas por categoría: ")
    for category_products in products_by_category:
        category_products_sorted = get_products(
            category_products, 10, sort_search, False
        )
        print(str(category_products_sorted[0][4]) + "\n")
        print_bottom_search_by_cat(category_products_sorted)

if option == 3:
    print("TOP 5 productos con mejores reseñas")
    top_review = get_products(product_summary, 5, sort_score)
    print_top_review(top_review)
    print("BOTTOM 5 productos con peores reseñas")
    bottom_review = get_products_by_score(product_summary, 5, False)
    print_top_review(bottom_review)

if option == 4:
    print("Total de ingresos: " + str(get_total_income(month_profit)))
    print("Ingresos de Enero: " + str(month_profit[0]))
    print("Ingresos de Febrero: " + str(month_profit[1]))
    print("Ingresos de Marzo: " + str(month_profit[2]))
    print("Ingresos de Abril: " + str(month_profit[3]))
    print("Ingresos de Mayo: " + str(month_profit[4]))
    print("Ingresos de Junio: " + str(month_profit[5]))
    print("Ingresos de Julio: " + str(month_profit[6]))
    print("Ingresos de Agosto: " + str(month_profit[7]))
    print("Ingresos de Septiembre: " + str(month_profit[8]))
    print("Ingresos de Octubre: " + str(month_profit[9]))
    print("Ingresos de Noviembre: " + str(month_profit[10]))
    print("Ingresos de Diciembre: " + str(month_profit[11]) + "\n")

    meses = [month for month in range(1, 13)]
    month_summary = []
    for i in range(len(meses)):
        month_summary.append([meses[i], month_profit[i]])
    month_sorted = get_products(month_summary, 12, sort_sales)

    print(
        "Los ingresos por mes (ordenados de mayor a menor) fueron: \n "
        + str(month_sorted)
        + "\n"
        "El mes de mayor venta fue el mes: " + str(month_sorted[0][0])
    )
