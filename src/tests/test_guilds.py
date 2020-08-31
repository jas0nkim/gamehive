class TestGuildCRUD:
    def test_get_guilds_from_empty_table(self, client):
        """ API endpoint
                /guild [GET]
            Get guilds from empty table. Number of guilds should be 0.
        """
        resp = client.get('/guild')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['guilds']) == 7

    def test_add_guilds(self, client):
        """ API endpoint
                /guild [POST]
            Add 4 guilds. Number of guilds should be 4.
        """
        guilds = [
            {'name': 'testguild01'},
            {'name': 'testguild02', 'country_code': 'US'},
            {'name': 'testguild03', 'country_code': 'CA'},
            {'name': 'testguild04'},
        ]
        for g in guilds:
            resp = client.post('/guild', json=g)
            json_data = resp.get_json()
            assert resp.status_code == 201
            assert json_data['success'] == 'true'
        resp = client.get('/guild')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['guilds']) == 11

    def test_add_guilds_name_already_exists(self, client):
        """ API endpoint
                /guild [POST]
            Add a guild name which already exists in database table. Should give an error.
        """
        guild = {'name': 'testguild03'}

        resp = client.post('/guild', json=guild)
        json_data = resp.get_json()
        assert resp.status_code == 400
        assert json_data['success'] == 'false'
        assert 'already exists' in json_data['error_message'] and 'name' in json_data['error_message']

    def test_show_a_guild(self, client):
        """ API endpoint
                /guild/<name> [GET]
            show a guild
        """
        resp = client.get('/guild/testguild02')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['guild']['country_code'] == 'US'

    def test_show_a_guild_not_in_database(self, client):
        """ API endpoint
                /guild/<name> [GET]
            show a guild who doesn't exist in database
        """
        resp = client.get('/guild/test10')
        json_data = resp.get_json()
        assert resp.status_code == 404
        assert json_data['success'] == 'false'
        assert json_data['error_message'] == 'Not found'

    def test_update_a_guild_with_post(self, client):
        """ API endpoint
                /guild/<name> [POST]
            update a guild with POST method
        """
        update_guild = {'name': 'post_testguild02', 'country_code': 'US'}
        resp = client.post('/guild/testguild02', json=update_guild)
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        resp = client.get('/guild/post_testguild02')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['guild']['country_code'] == 'US'

    def test_update_a_guild_with_put(self, client):
        """ API endpoint
                /guild/<name> [PUT]
            update a guild with PUT method
        """
        update_guild = {'name': 'put_testguild02', 'country_code': 'US'}
        resp = client.put('/guild/post_testguild02', json=update_guild)
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        resp = client.get('/guild/put_testguild02')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['guild']['country_code'] == 'US'

    def test_delete_a_guild_with_post(self, client):
        """ API endpoint
                /guild/<name>/delete [POST]
            delete a guild with POST method
        """
        resp = client.post('/guild/testguild01/delete')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'

    def test_delete_a_guild_with_delete(self, client):
        """ API endpoint
                /guild/<name>/delete [DELETE]
            delete a guild with DELETE method
        """
        resp = client.delete('/guild/testguild04/delete')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
