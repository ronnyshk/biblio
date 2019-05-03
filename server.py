import json
import psycopg2

from aiohttp import web
from schema import schema
from graphql import format_error
from graphql_ws.aiohttp import AiohttpSubscriptionServer

from template import render_graphiql

def convert(list):
    s = [str(i) for i in list]
    res = int(", ".join(s))
    return(res)

async def graphql_view(request):
    payload = await request.json()
    response = await schema.execute(payload.get('query', ''), return_promise=True)
    data = {}
    if response.errors:
        data['errors'] = [format_error(e) for e in response.errors]
    if response.data:
        data['data'] = response.data
    jsondata = json.dumps(data,)
    return web.Response(text=jsondata, headers={'Content-Type': 'application/json'})


async def search(request):
    payload = await request.json()
    data = {}
    try:
        connection = psycopg2.connect(user = "postgres",
                                      password = "Reverbnationkiro",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "biblio")
        cursor = connection.cursor()
        query = payload.get('query', '')
        columns = ('id', 'title', 'subtitle', 'author', 'category', 'editor', 'description')
        cursor.execute("SELECT id, title, subtitle, author, category, editor, description FROM books WHERE id = " + query + " OR title::text LIKE '%" + query + "%'" + " OR subtitle::text LIKE '%" + query + "%'" + " OR author::text LIKE '%" + query + "%'" + " OR category::text LIKE '%" + query + "%'" + " OR category::text LIKE '%" + query + "%'"  + " OR editor::text LIKE '%" + query + "%'" + " OR description::text LIKE '%" + query + "%'")
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        if len(results) == 0:
            request = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + query + '&key=AIzaSyDoNktI8mIyGvHbylfFB-Jrh9cPm-VMjas')
            if request.status_code == 200:
                json_data = json.loads(request.text)
                columns = ('id', 'title', 'subtitle', 'authors', 'categories', 'publisher', 'description')
                for row in json_data['items']:
                    subtitle = row['volumeInfo'][columns[2]] if row["volumeInfo"].get(columns[2]) else ""
                    authors = row['volumeInfo'][columns[3]] if row["volumeInfo"].get(columns[3]) else ""
                    categories = row['volumeInfo'][columns[4]] if row["volumeInfo"].get(columns[4]) else ""
                    publisher = row['volumeInfo'][columns[5]] if row["volumeInfo"].get(columns[5]) else ""
                    description =  row['volumeInfo'][columns[6]] if row["volumeInfo"].get(columns[6]) else ""
                    results.append({columns[0]: row[columns[0]], columns[1]: row['volumeInfo'][columns[1]], columns[2]: subtitle, columns[3]: authors, columns[4]: categories, columns[5]: publisher, columns[6]: description})

                data = json.dumps(results, indent=2)
            else:
                data = json.dumps({ "error": "Query failed to run by returning code of {}. {}"})
        else:
            data = json.dumps(results, indent=2)
    except (Exception, psycopg2.Error) as error :
        error = "Error while connecting to PostgreSQL"
        data = json.dumps({"error": error})
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()

    return web.Response(text=data, headers={'Content-Type': 'application/json'})

async def delete(request):
    payload = await request.json()
    data = {}
    try:
        connection = psycopg2.connect(user = "postgres",
                                      password = "Reverbnationkiro",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "biblio")
        cursor = connection.cursor()
        query = payload.get('query', '')
        columns = ('id', 'title', 'subtitle', 'author', 'category', 'editor', 'description')
        cursor.execute("DELETE FROM books WHERE id = " + query)
        results = []
        data = json.dumps({"success": "Eliminado correctamente"})
    except (Exception, psycopg2.Error) as error :
        error = "Error while connecting to PostgreSQL"
        data = json.dumps({"error": error})
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()

    return web.Response(text=data, headers={'Content-Type': 'application/json'})

async def insert(request):
    payload = await request.json()
    data = {}
    try:
        connection = psycopg2.connect(user = "postgres",
                                      password = "Reverbnationkiro",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "biblio")
        cursor = connection.cursor()
        query = payload.get('query', '')
        columns = ('id', 'title', 'subtitle', 'author', 'category', 'editor', 'description')
        cursor.execute("SELECT id, title, subtitle, author, category, editor, description FROM books WHERE id = " + query)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        if len(results) == 0:
            request = requests.get('https://www.googleapis.com/books/v1/volumes/' + query + '?key=AIzaSyDoNktI8mIyGvHbylfFB-Jrh9cPm-VMjas')
            if request.status_code == 200:
                row = json.loads(request.text)

                columns = ('id', 'title', 'subtitle', 'authors', 'categories', 'publisher', 'description')

                subtitle = row['volumeInfo'][columns[2]] if row["volumeInfo"].get(columns[2]) else ""
                authors = row['volumeInfo'][columns[3]] if row["volumeInfo"].get(columns[3]) else ""
                categories = row['volumeInfo'][columns[4]] if row["volumeInfo"].get(columns[4]) else ""
                publisher = row['volumeInfo'][columns[5]] if row["volumeInfo"].get(columns[5]) else ""
                description =  row['volumeInfo'][columns[6]] if row["volumeInfo"].get(columns[6]) else ""
                results.append({columns[0]: row[columns[0]], columns[1]: row['volumeInfo'][columns[1]], columns[2]: subtitle, columns[3]: authors, columns[4]: categories, columns[5]: publisher, columns[6]: description})

                print(json.dumps(len(results[0])))

                cursor.execute("INSERT INTO books (id, title, subtitle, author, category, editor, description) VALUES ($$" + results[0][columns[0]] + "$$, $$" + results[0][columns[1]] + "$$, $$" + results[0][columns[2]].replace('\'', '´') + "$$, $$" + results[0][columns[3]][0] + "$$, $$" + results[0][columns[4]][0] + "$$, $$"  + results[0][columns[5]] + "$$, $$" + results[0][columns[6]] + "$$)")

                data = json.dumps(results, indent=2)
            else:
                data = json.dumps({ "error": "Query failed to run by returning code of {}. {}"})
        else:
            data = json.dumps(results, indent=2)
    except (Exception, psycopg2.Error) as error :
        error = "Error while connecting to PostgreSQL"
        data = json.dumps({"error": error})
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()

    return web.Response(text=data, headers={'Content-Type': 'application/json'})

async def graphiql_view(request):
    return web.Response(text=render_graphiql(), headers={'Content-Type': 'text/html'})

subscription_server = AiohttpSubscriptionServer(schema)


async def subscriptions(request):
    ws = web.WebSocketResponse(protocols=('graphql-ws',))
    await ws.prepare(request)

    await subscription_server.handle(ws)
    return ws


app = web.Application()
app.router.add_get('/subscriptions', subscriptions)
app.router.add_post('/insert', insert)
app.router.add_post('/search', search)
app.router.add_post('/delete', delete)

web.run_app(app, port=8000)
