import base
import unittest


class TestBase(unittest.TestCase):

    def setUp(self):
        base.application.config['TESTING'] = True
        self.client = base.application.test_client()

    def test_post_message(self):
        message_json = {
            'id': 45,
            'message': "Hello World"
        }
        rv = self.client.post('/messages', json=message_json)
        json_val = rv.get_json()
        self.assertEqual(message_json['id'], json_val['id'], )
        self.assertEqual(message_json['message'], json_val['message'])
        self.assertEqual(201, rv.status_code)
        self.assertEqual('/messages/%s' % json_val['id'], rv.headers['Location'])

    def test_get_message(self):
        message_json = {
            'id': 15,
            'message': "Hello World"
        }
        # given idempotence this should be robust even running tests in parallel
        base.stored_messages[message_json['id']] = message_json
        rv = self.client.get('/messages/%s' % message_json['id'])
        json_val = rv.get_json()
        self.assertEqual(message_json['id'], json_val['id'], )
        self.assertEqual(message_json['message'], json_val['message'])
        self.assertEqual(200, rv.status_code)

    def test_get_non_existent_message(self):
        no_message_id = 450
        rv = self.client.get('/messages/%s' % no_message_id)
        self.assertEqual(404, rv.status_code)

    def test_delete_message(self):
        message_json = {
            'id': 123,
            'message': "Goodbye, cruel world"
        }
        base.stored_messages[message_json['id']] = message_json
        check_before_rv = self.client.get('/messages/%s' % message_json['id'])
        self.assertEqual(200, check_before_rv.status_code)
        json_val = check_before_rv.get_json()
        self.assertEqual(message_json['id'], json_val['id'], )
        self.assertEqual(message_json['message'], json_val['message'])

        rv = self.client.delete('/messages/%s' % message_json['id'])

        self.assertEqual(204, rv.status_code)
        check_after_rv = self.client.get('/messages/%s' % message_json['id'])
        self.assertEqual(404, check_after_rv.status_code)


if __name__ == "__main__":
    unittest.main()