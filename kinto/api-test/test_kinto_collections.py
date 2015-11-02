import unittest

from mockclient import MockClient


class Kinto_Collections(unittest.TestCase):
    """
        Tests to verify the Kinto collections function
        Docs: http://kinto.readthedocs.org/en/latest/api/collections.html
    """

    def setUp(self):
        self.client = MockClient()

    def tearDown(self):
        self.client = None

    def test_create_collection(self):
        # Create the bucket
        resource = 'buckets/test_bucket'
        response = self.client.put_request(resource)
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertEqual(response['data']['id'], 'test_bucket')

        # Create the collection
        resource = 'buckets/test_bucket/collections/test_collection'
        response = self.client.put_request(resource)
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertIn('schema', response['data'])
        self.assertIn('write', response['permissions'])
        self.assertEqual(response['data']['id'], 'test_collection')

    def test_update_collection_no_data(self):
        resource = 'buckets/test_bucket/collections/test_collection'
        data = ''
        response = self.client.patch_request(resource, data, status_code=400)
        self.assertIn('errno', response)
        self.assertIn('message', response)
        self.assertIn('code', response)
        self.assertIn('error', response)
        self.assertEqual(response['errno'], 107)
        self.assertEqual(response['message'], "Provide at least one of data or permissions")
        self.assertEqual(response['code'], 400)
        self.assertEqual(response['error'], 'Invalid parameters')

    def test_update_collection_with_data(self):
        resource = 'buckets/test_bucket/collections/test_collection'
        data = '{"data": {"fingerprint": "a_new_fingerprint"}}'
        response = self.client.patch_request(resource, data)
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('fingerprint', response['data'])
        self.assertIn('id', response['data'])
        self.assertIn('schema', response['data'])
        self.assertIn('write', response['permissions'])
        self.assertEqual(response['data']['fingerprint'], 'a_new_fingerprint')
        self.assertEqual(response['data']['id'], 'test_collection')

    def test_retrieve_collection(self):
        resource = 'buckets/test_bucket/collections/test_collection'
        response = self.client.get_request(resource)
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertIn('schema', response['data'])
        self.assertIn('write', response['permissions'])
        self.assertEqual(response['data']['id'], 'test_collection')

    def test_delete_collection(self):
        resource = 'buckets/test_bucket/collections/delete_collection'
        response = self.client.put_request(resource)
        self.assertIn('data', response)
        self.assertIn('permissions', response)
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertIn('schema', response['data'])
        self.assertIn('write', response['permissions'])
        self.assertEqual(response['data']['id'], 'delete_collection')

        resource = 'buckets/test_bucket/collections/delete_collection'
        response = self.client.delete_request(resource)
        self.assertIn('data', response)
        self.assertIn('deleted', response['data'])
        self.assertIn('last_modified', response['data'])
        self.assertIn('id', response['data'])
        self.assertEqual(response['data']['id'], 'delete_collection')
        self.assertEqual(response['data']['deleted'], True)

    def test_delete_collection_not_exist(self):
        resource = 'buckets/test_bucket/collections/invalid_delete'
        response = self.client.delete_request(resource, status_code=404)
        self.assertIn('errno', response)
        self.assertIn('message', response)
        self.assertIn('code', response)
        self.assertIn('error', response)
        self.assertEqual(response['errno'], 111)
        self.assertEqual(response['message'], "The resource you are looking for could not be found.")
        self.assertEqual(response['code'], 404)
        self.assertEqual(response['error'], 'Not Found')
