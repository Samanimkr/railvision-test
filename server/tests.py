import unittest
from app import app


class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_create_thermometer(self):
        response = self.app.post('/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Created thermometer successfully!', response.text)


if __name__ == '__main__':
    unittest.main()
