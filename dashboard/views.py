from django.shortcuts import render
import mariadb
import sys
import os
import json

def get_db_connection():
    try:
        conn = mariadb.connect(
            user=os.getenv('MARIADB_USER'),
            password=os.getenv('MARIADB_PASSWORD'),
            host=os.getenv('MARIADB_HOST'),
            port=int(os.getenv('MARIADB_PORT')),
            database=os.getenv('MARIADB_DATABASE'),
        )
        return conn
    except mariadb.Error as e:
        print(f"Error de conexión a MariaDB: {e}")
        sys.exit(1)

def get_customers_count(cursor):
    cursor.execute('SELECT COUNT(*) FROM customer')
    return cursor.fetchone()[0]

def get_films_count(cursor):
    cursor.execute('SELECT COUNT(*) FROM film')
    count = cursor.fetchone()[0]
    return f'{count:,}'

def get_total_payments(cursor):
    cursor.execute('SELECT SUM(amount) FROM payment')
    total = cursor.fetchone()[0]
    return f'{total:,.2f}'

def get_films_by_category(cursor):
    query = '''
            SELECT c.name AS categoria, COUNT(fc.film_id) AS num_peliculas
            FROM category c
                     LEFT JOIN film_category fc ON c.category_id = fc.category_id
            GROUP BY c.category_id, c.name
            ORDER BY num_peliculas DESC
            '''
    cursor.execute(query)
    results = cursor.fetchall()

    categories = [row[0] for row in results]
    movies = [row[1] for row in results]
    return categories, movies

def get_revenue_by_month(cursor):
    query = '''
        SELECT DATE_FORMAT(payment_date, '%Y-%m') AS month, SUM(amount) AS total
        FROM payment
        GROUP BY month
        ORDER BY month;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    months = [row[0] for row in results]
    totals = [float(row[1]) for row in results]
    return months, totals


def get_top10_profitable_films(cursor):
    query = '''
        SELECT f.title, SUM(p.amount) AS total
        FROM payment p
        JOIN rental r ON p.rental_id = r.rental_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        GROUP BY f.film_id, f.title
        ORDER BY total DESC
        LIMIT 10;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    films = [row[0] for row in results]
    totals = [float(row[1]) for row in results]
    return films, totals


def get_customers_by_country(cursor):
    query = '''
        SELECT co.country, COUNT(c.customer_id) AS num_clientes
        FROM customer c
        JOIN address a ON c.address_id = a.address_id
        JOIN city ci ON a.city_id = ci.city_id
        JOIN country co ON ci.country_id = co.country_id
        GROUP BY co.country
        ORDER BY num_clientes DESC
        LIMIT 10;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    countries = [row[0] for row in results]
    totals = [row[1] for row in results]
    return countries, totals

def index(request):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        customers = get_customers_count(cursor)
        films = get_films_count(cursor)
        payments = get_total_payments(cursor)
        categories, movies = get_films_by_category(cursor)
        months, revenue = get_revenue_by_month(cursor)
        top_films, top_revenue = get_top10_profitable_films(cursor)
        countries, clients = get_customers_by_country(cursor)

        context = {
            'customers': customers,
            'films': films,
            'payments': payments,
            'categories': json.dumps(categories),
            'movies': json.dumps(movies),
            'months': json.dumps(months),
            'revenue': json.dumps(revenue),
            'top_films': json.dumps(top_films),
            'top_revenue': json.dumps(top_revenue),
            'countries': json.dumps(countries),
            'clients': json.dumps(clients)
        }

        return render(request, 'dashboard/index.html', context)
    finally:
        cursor.close()
        conn.close()