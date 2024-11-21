from app.appMain import mydb
from flask_cors import CORS
from app import blueprint


backend = mydb()
CORS(backend)
backend.register_blueprint(blueprint)


if __name__ == "__main__":
    backend.run(debug=True)




