class TestGuildCRUD:
    def test_get_guilds_from_initial_table(self, client):
        """ API endpoint
                /guild [GET]
            Get guilds from initial table. Number of guilds should be 7.
        """
        resp = client.get('/guild')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['guilds']) == 7

    def test_add_guilds(self, client):
        """ API endpoint
                /guild [POST]
            Add 4 guilds. Number of guilds should be 11.
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

class TestGuildPlayer:
    def test_add_player(self, client):
        """ API endpoint
                /guild/<name>/add-player [POST]
            add player
        """
        player = {'nickname': 'oplayer02'}
        resp = client.post('/guild/oguild01/add-player', json=player)
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['players']) == 1
        player = {'nickname': 'oplayer03'}
        resp = client.post('/guild/oguild01/add-player', json=player)
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['players']) == 2

    def test_remove_player(self, client):
        """ API endpoint
                /guild/<name>/remove-player/<nickname> [DELETE, POST]
            leave from a joined guild
        """
        resp = client.post('/guild/oguild01/remove-player/oplayer02')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['players']) == 1
        resp = client.post('/guild/oguild01/remove-player/oplayer10')
        json_data = resp.get_json()
        assert resp.status_code == 400
        assert json_data['success'] == 'false'
        assert json_data['error_message'] == 'Player not a member.'
        resp = client.delete('/guild/oguild01/remove-player/oplayer03')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['players']) == 0

class TestGuildSkillPoint:
    def test_guild_skill_point_having_players_with_items(self, client):
        """ API endpoint
                /guild/<name>/points [GET]
            get the total number of skill points in a guild
        """
        resp = client.get('/guild/oguild05/points')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['total_points'] == 1610

    def test_guild_skill_point_having_players_with_no_items(self, client):
        """ API endpoint
                /guild/<name>/points [GET]
            get the total number of skill points in a guild
        """
        resp = client.get('/guild/oguild04/points')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['total_points'] == 300

    def test_guild_skill_point_having_no_players(self, client):
        """ API endpoint
                /guild/<name>/points [GET]
            get the total number of skill points in a guild
        """
        resp = client.get('/guild/oguild03/points')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['total_points'] == 0
