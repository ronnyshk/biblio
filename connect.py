import psycopg2
import json
import requests

def convert(list):
    s = [str(i) for i in list]
    res = int(", ".join(s))
    return(res)

try:
    results = []
    connection = psycopg2.connect(user = "postgres",
                                  password = "Reverbnationkiro",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "biblio")
    cursor = connection.cursor()
    query = "9Nl9tZEHUtwC"
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
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
except ValueError:
    print("Error in ValueError")
finally:
    #closing database connection.
            print("PostgreSQL connection is closed")
            exit()
