import unittest

from app import app


class AdminAssetTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_admin_login_page_uses_static_assets(self):
        response = self.client.get('/admin/login')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('/static/admin/css/login.css', html)
        self.assertIn('/static/admin/js/login.js', html)


if __name__ == '__main__':
    unittest.main()
