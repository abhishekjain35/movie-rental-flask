import os
from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Rents
from auth import requires_auth, AuthError

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/" : {"origins": '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
        return response

    @app.route('/', methods=["GET"])
    def check_app():
        return jsonify({
            "status": "App is working fine."
        })

    @app.route("/movies", methods=['GET'])
    def get_all_movies():
        movies = Movies.query.all()
        if len(movies) == 0: 
            abort(404)
        formatted_movies = [m.format() for m in movies]

        return jsonify({
            "success": True,
            "movies": formatted_movies
        })

    @app.route("/create-movie", methods=["POST"])
    @requires_auth('create:movie')
    def create_movie(userData):
        data = request.get_json()

        if 'movie_name' and 'price' not in data:
            abort(422)
        movie = Movies(data['movie_name'], data['price'])
        movie.insert()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route("/movie/<int:id>", methods=["PATCH"])
    @requires_auth('update:movie')
    def update_movie(userData,id):
        data = request.get_json()
        if 'movie_name' and 'price' not in data:
            abort(400)

        movie = Movies.query.filter(Movies.id==id).one_or_none()

        if not movie:
            abort(404)

        if 'movie_name' in data:
            movie.movie_name = data['movie_name']
        if 'price' in data:
            movie.price = data['price']

        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/movie/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(userData, id):
        movie = Movies.query.filter(Movies.id==id).one_or_none()

        if not movie:
            abort(404)

        movie.delete()
        return jsonify({
            'success': True,
            'id': id
        })

    @app.route('/rented-movies', methods=['GET'])
    def get_rented_movies():
        try:
            data = Rents.query.join(Movies).all()
            all_rented_movies = [r.format() for r in data]

            return jsonify({
                'success': True,
                'movies': all_rented_movies
            })

        except:
            abort(422)

    @app.route('/rent-movie', methods=["POST"])
    @requires_auth('rent:movie')
    def rent_a_movie(userData):
        try:
            data = request.get_json()
            if 'movie_id' not in data or 'days' not in data:
                abort(400)
            
            movie = Movies.query.get(data['movie_id'])
            charge = movie.price * data['days']

            rented_movie = Rents(movie_id=data['movie_id'], charges=charge)
            rented_movie.insert()
            return jsonify({
                'success': True,
                'rented_movie': rented_movie.format()
            })

        except:
            abort(404)

    @app.errorhandler(404)
    def handler_not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def handler_unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def handler_bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
        }), 400
    
    @app.errorhandler(405)
    def handler_bad_request(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(AuthError)
    def handle_auth_error(err):
        jsonRes = jsonify(err.error)
        jsonRes.status_code = err.status_code
        return jsonRes
    

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)