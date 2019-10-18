from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_post_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_post = {
    'title': 'Math problem',
    'description': 'Need help with question 2',
    'videos': [
        'https://youtube.com/embed/hY7m5jjJ9mM',
        'https://www.youtube.com/embed/CQ85sUNBK7w'
    ]
}
sample_form_data = {
    'title': sample_post['title'],
    'description': sample_post['description'],
    'videos': '\n'.join(sample_post['videos'])
}

class helpMeTest(TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
    
    def test_index(self):
        '''Test the Homepage of HelpMe'''
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Post', result.data)

    def test_new(self):
        """Test the create new post page."""
        result = self.client.get('/posts/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Post', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_post(self, mock_find):
        """Test showing a single post."""
        mock_find.return_value = sample_post

        result = self.client.get(f'/posts/{sample_post_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Math problem', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_post(self, mock_find):
        """Test editing a single post."""
        mock_find.return_value = sample_post

        result = self.client.get(f'/posts/{sample_post_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Math problem', result.data)
    
    # @mock.patch('pymongo.collection.Collection.insert_one')
    # def test_submit_post(self, mock_insert):
    #     """Test submitting a new post."""
    #     result = self.client.post('/posts', data=sample_form_data)

    #     # After submitting, should redirect to that post's page
    #     self.assertEqual(result.status, '302 FOUND')
    #     mock_insert.assert_called_with(sample_post)

    # @mock.patch('pymongo.collection.Collection.update_one')
    # def test_update_post(self, mock_update):
    #     result = self.client.post(f'/posts/{sample_post_id}', data=sample_form_data)

    #     self.assertEqual(result.status, '302 FOUND')
    #     mock_update.assert_called_with({'_id': sample_post_id}, {'$set': sample_post})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_post(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/posts/{sample_post_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_post_id})

if __name__ == '__main__':
    unittest_main()