class TestItemCRUD:
    def test_get_items_from_empty_table(self, client):
        """ API endpoint
                /item [GET]
            Get items from empty table. Number of items should be 0.
        """
        resp = client.get('/item')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['items']) == 10

    def test_add_items(self, client):
        """ API endpoint
                /item [POST]
            Add 4 items. Number of items should be 4.
        """
        items = [
            {'name': 'testitem01', 'skill_point': 10},
            {'name': 'testitem02', 'skill_point': 20},
            {'name': 'testitem03', 'skill_point': 30},
            {'name': 'testitem04', 'skill_point': 40},
        ]
        for i in items:
            resp = client.post('/item', json=i)
            json_data = resp.get_json()
            assert resp.status_code == 201
            assert json_data['success'] == 'true'
        resp = client.get('/item')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['items']) == 14

    def test_add_items_name_already_exists(self, client):
        """ API endpoint
                /item [POST]
            Add a item name which already exists in database table. Should give an error.
        """
        item = {'name': 'testitem03'}

        resp = client.post('/item', json=item)
        json_data = resp.get_json()
        assert resp.status_code == 400
        assert json_data['success'] == 'false'
        assert 'already exists' in json_data['error_message'] and 'name' in json_data['error_message']

    def test_show_a_item(self, client):
        """ API endpoint
                /item/<name> [GET]
            show a item
        """
        resp = client.get('/item/testitem02')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['item']['skill_point'] == 20

    def test_show_a_item_not_in_database(self, client):
        """ API endpoint
                /item/<name> [GET]
            show a item who doesn't exist in database
        """
        resp = client.get('/item/testitem100')
        json_data = resp.get_json()
        assert resp.status_code == 404
        assert json_data['success'] == 'false'
        assert json_data['error_message'] == 'Not found'

    def test_update_a_item_with_post(self, client):
        """ API endpoint
                /item/<name> [POST]
            update a item with POST method
        """
        update_item = {'name': 'post_testitem02', 'skill_point': 20}
        resp = client.post('/item/testitem02', json=update_item)
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        resp = client.get('/item/post_testitem02')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['item']['skill_point'] == 20

    def test_update_a_item_with_put(self, client):
        """ API endpoint
                /item/<name> [PUT]
            update a item with PUT method
        """
        update_item = {'name': 'put_testitem02', 'skill_point': 20}
        resp = client.put('/item/post_testitem02', json=update_item)
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        resp = client.get('/item/put_testitem02')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['item']['skill_point'] == 20

    def test_delete_a_item_with_post(self, client):
        """ API endpoint
                /item/<name>/delete [POST]
            delete a item with POST method
        """
        resp = client.post('/item/testitem01/delete')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'

    def test_delete_a_item_with_delete(self, client):
        """ API endpoint
                /item/<name>/delete [DELETE]
            delete a item with DELETE method
        """
        resp = client.delete('/item/testitem04/delete')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
