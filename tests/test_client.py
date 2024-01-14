import unittest
from unittest.mock import patch
from .my_client_v2 import HunterClient, EmailStorage, json


class TestHunterClient(unittest.TestCase):
    def setUp(self):
        self.client = HunterClient(api_key='test_api_key')
        self.client.storage = EmailStorage()

    @patch('client.requests.get')
    def test_verify_email_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            'data': {'status': 'verified'},
        }
        status = self.client.verify_email('test@example.com')
        self.assertEqual(status['data']['status'], 'verified')

    @patch('client.requests.get')
    def test_verify_email_failure(self, mock_get):
        mock_get.return_value.json.return_value = {'error': 'Some error message'}
        status = self.client.verify_email('invalid_email')
        self.assertEqual(status, {'error': 'Some error message'})

    @patch('client.requests.get')
    def test_save_email_result_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            'data': {'status': 'verified'},
        }
        with patch('builtins.print') as mock_print:
            self.client.save_email_result('test@example.com')
            mock_print.assert_called_with('test@example.com', json.dumps({"data": {"status": "verified"}}, indent=2))

    @patch('client.requests.get')
    def test_save_email_result_failure(self, mock_get):
        mock_get.side_effect = Exception('Some error')
        with patch('builtins.print') as mock_print:
            self.client.save_email_result('invalid_email')
            mock_print.assert_called_with('Error, exist : Some error')

    def test_is_valid_email_valid(self):
        valid_emails = ['test@example.com', 'user@mail.domain']
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(self.client.is_valid_email(email))

    def test_is_valid_email_invalid(self):
        invalid_emails = ['invalid.email@', 'missing@domain', '@missing_username']
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(self.client.is_valid_email(email))

    def test_create_email_result(self):
        self.client.create_email_result('test@example.com', {'status': 'verified'})
        result = self.client.storage.get_one('test@example.com')
        self.assertEqual(result, {'status': 'verified'})

    def test_update_email_result(self):
        self.client.storage.save_email_result('test@example.com', {'status': 'unverified'})
        self.client.update_email_result('test@example.com', {'status': 'verified'})
        result = self.client.storage.get_one('test@example.com')
        self.assertEqual(result, {'status': 'verified'})

    def test_delete_email_result(self):
        self.client.storage.save_email_result('test@example.com', {'status': 'verified'})
        self.client.delete_email_result('test@example.com')
        result = self.client.storage.get_one('test@example.com')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
