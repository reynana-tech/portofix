import unittest
import uuid

from app import app
from model import get_db


class AdminSaveFlowTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as sess:
            sess['admin_logged_in'] = True

    def tearDown(self):
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM profiles WHERE name=%s", ('Flow Test Profile',))
            conn.commit()
        finally:
            conn.close()

    def test_profile_save_is_persisted_and_visible_on_public_api(self):
        payload = {
            'name': 'Flow Test Profile',
            'title': 'Developer',
            'bio': 'Inserted from test',
            'email': 'flow@example.com',
            'phone': '08123456789',
            'location': 'Jakarta',
            'github': 'https://github.com/example',
            'linkedin': 'https://linkedin.com/in/example',
            'photo_url': 'https://example.com/profile.jpg'
        }

        response = self.client.post('/api/admin/profiles', json=payload)
        self.assertEqual(response.status_code, 200)

        public_response = self.client.get('/api/profile')
        self.assertEqual(public_response.status_code, 200)
        body = public_response.get_json()
        self.assertTrue(body['success'])
        self.assertIsNotNone(body['data'])
        self.assertEqual(body['data']['name'], payload['name'])


if __name__ == '__main__':
    unittest.main()
