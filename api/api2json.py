import os
from collections import defaultdict
import psycopg2
import flask

def main():
    start_api()

def get_measures_json():
    connection = psycopg2.connect(user=os.getenv('POSTGRES_USER'),
                                  password=os.environ.get('POSTGRES_PASSWORD'),
                                  host=os.environ.get('POSTGRES_HOST'),
                                  port=os.environ.get('POSTGRES_PORT'),
                                  database=os.environ.get('POSTGRES_DB'))

    cursor = connection.cursor()
    select_distinct = "select distinct id_entity from measureslog"

    cursor.execute(select_distinct)
    distinct_id_entity = cursor.fetchall()
    prettyjson = defaultdict(lambda: {"values": []})

    for did in distinct_id_entity:
        cursor.execute("""select row_to_json(row) from\
                   (select timestamp,so2,no2,co,o3,pm10,pm2_5 from measureslog\
                    where id_entity = %s) row""", (did))
        result = cursor.fetchall()
        prettyjson[str(did)]["values"].append(result)

    if connection:
        cursor.close()
        connection.close()

    return prettyjson

def start_api():
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    @app.route('/', methods=['GET'])
    def home():
        return "<h1>MEASURES API</h1><p>This is a prototype\
 API for get air quality measurements.</p>"

    # A route to return all of the available entries in our catalog.
    @app.route('/api/v1/resources/airq', methods=['GET'])
    def api_all():
        return get_measures_json()

    app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
