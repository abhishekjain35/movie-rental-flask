import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db
unittest.TestLoader.sortTestMethodsUsing = None

class RentalAPITestCases(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "rentalapi_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_a_create_movie(self):
        result = self.client().post('/create-movie', headers={'Authorization': f'Bearer {os.environ["admin_token"]}'} ,json={'movie_name': 'Intersteller', 'price': 110})
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["movie"]["id"], 1)
        self.assertEqual(data["movie"]["movie_name"], 'Intersteller')
        self.assertEqual(data["movie"]["price"], 110)

    def test_b_create_movie_error(self):
        # No headers sent
        result = self.client().post('/create-movie', json={'movie_name': 'Intersteller', 'price': 110})
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 401)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_c_update_movie(self):
        result = self.client().patch('/movie/1', headers={'Authorization': f'Bearer {os.environ["admin_token"]}'} ,json={'movie_name': 'Avengers', 'price': 200})
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["movie"]["id"], 1)
        self.assertEqual(data["movie"]["movie_name"], 'Avengers')
        self.assertEqual(data["movie"]["price"], 200)

    def test_d_update_movie_error(self):
        # Sending user token (An user can't update movies)
        result = self.client().patch('/movie/1', headers={'Authorization': f'Bearer {os.environ["user_token"]}'}, json={'movie_name': 'Intersteller', 'price': 110})
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(data["code"], "unauthorized")

    def test_e_get_movies(self):
        result = self.client().get('/movies')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["movies"][0]["id"], 1)
        self.assertEqual(data["movies"][0]["movie_name"], 'Avengers')

    def test_f_rent_movie(self):
        result = self.client().post('/rent-movie', headers={'Authorization': f'Bearer {os.environ["user_token"]}'} ,json={'movie_id': '1', 'days': 4})
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["rented_movie"]["id"], data["rented_movie"]["movie"]["id"])
        self.assertEqual(data["rented_movie"]["charges"], 800)
        self.assertEqual(data["rented_movie"]["movie_id"], 1)

    def test_g_rent_movie_error(self):
        # Sending no token
        result = self.client().post('rent-movie')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 401)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_h_get_rented_movies(self):
        result = self.client().get('/rented-movies')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["movies"][0]["id"], 1)
        self.assertEqual(data["movies"][0]["charges"], 800)

    def test_i_get_rented_movies_error(self):
        # POST instead of GET
        result = self.client().post('/rented-movies')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 405)
        self.assertEqual(data["message"], "method not allowed")

    def test_j_delete_movies(self):
        # Sending user token (An user can't update movies)
        result = self.client().delete('/movie/1', headers={'Authorization': f'Bearer {os.environ["admin_token"]}'})
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["id"], 1)

    def test_k_delete_movie_error(self):
        # Sending no token only Bearer keyword
        result = self.client().delete('/movie/1', headers={'Authorization': f'Bearer'})
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 401)
        self.assertEqual(data["code"], "invalid_header")

    def test_l_get_movie_error(self):
        result = self.client().get('/movies')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()