from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

CUPCAKE_DATA_3 = {
    "flavor": "TestFlavor3",
    "size": "TestSize3",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        """ Testing getting all cupcakes from the database """

        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {                        
                        "flavor": "TestFlavor",
                        "id": self.cupcake.id,
                        "image": "http://test.com/cupcake.jpg",
                        "rating": 5,
                        "size": "TestSize"
                    }
                ]
            })

    def test_get_cupcake(self):
        """ Test getting a single cupcake from the database """

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        """ Test adding a new cupcake to the database """

        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_delete_existing_cupcake(self):
        """ Test deleting a cupcake from the database """

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)

            data = resp.json

            self.assertEqual(data, {
                "message": 'Deleted'
            })

            self.assertEqual(Cupcake.query.count(), 0)

    def test_delete_non_existing_cupcake(self):
        """ Test am attempt to delete from the database a cupcake that does not exist """

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id + 1}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 404)

            data = resp.json
            
            self.assertEqual(Cupcake.query.count(), 1)

    def test_update_existing_cupcake(self):
        """ Test updating a cupcake """

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.patch(url, json=CUPCAKE_DATA_3)
            data=resp.json
            del data['cupcake']['id']

            self.assertIn("TestFlavor3", data['cupcake']['flavor'])
            self.assertEqual(Cupcake.query.count(), 1)
            self.assertIn("TestSize3", data['cupcake']['size'])
            self.assertEqual(10.0, data['cupcake']['rating'])
            self.assertIn("http://test.com/cupcake2.jpg", data['cupcake']['image'])

    def test_update_non_existing_cupcake(self):
        """ Test trying to update a record that does not exist """
        
            with app.test_client() as client:
                url = f"/api/cupcakes/{self.cupcake.id+1}"
                resp = client.patch(url, json=CUPCAKE_DATA_3)

                self.assertEqual(resp.status_code, 404)

                data = resp.json

                self.assertEqual(Cupcake.query.count(), 1)
                