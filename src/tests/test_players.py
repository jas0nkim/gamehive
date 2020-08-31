class TestPlayerCRUD:
    def test_get_players_from_initial_table(self, client):
        """ API endpoint
                /player [GET]
            Get players from initial table. Number of players should be 15.
        """
        resp = client.get('/player')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['players']) == 15

    def test_add_players(self, client):
        """ API endpoint
                /player [POST]
            Add 3 players. Number of players should be 18.
        """
        players = [
            {'nickname': 'test01', 'email': 'test01@mail.com',},
            {'nickname': 'test02', 'email': 'test02@mail.com',},
            {'nickname': 'test03', 'email': 'test03@mail.com',},
        ]
        for p in players:
            resp = client.post('/player', json=p)
            json_data = resp.get_json()
            assert resp.status_code == 201
            assert json_data['success'] == 'true'
        resp = client.get('/player')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['players']) == 18

    def test_add_players_nickname_already_exists(self, client):
        """ API endpoint
                /player [POST]
            Add a player who has a nickname already exists in database table. Should give an error.
        """
        player = {'nickname': 'test02', 'email': 'test04@mail.com',}

        resp = client.post('/player', json=player)
        json_data = resp.get_json()
        assert resp.status_code == 400
        assert json_data['success'] == 'false'
        assert 'already exists' in json_data['error_message'] and 'nickname' in json_data['error_message']

    def test_add_players_email_already_exists(self, client):
        """ API endpoint
                /player [POST]
            Add a player who has an email already exists in database table. Should give an error.
        """
        player = {'nickname': 'test10', 'email': 'test02@mail.com',}

        resp = client.post('/player', json=player)
        json_data = resp.get_json()
        assert resp.status_code == 400
        assert json_data['success'] == 'false'
        assert 'already exists' in json_data['error_message'] and 'email' in json_data['error_message']

    def test_show_a_player(self, client):
        """ API endpoint
                /player/<nickname> [GET]
            show a player exists in database
        """
        resp = client.get('/player/test03')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['player']['email'] == 'test03@mail.com'

    def test_show_a_player_not_in_database(self, client):
        """ API endpoint
                /player/<nickname> [GET]
            show a player who doesn't exist in database
        """
        resp = client.get('/player/test10')
        json_data = resp.get_json()
        assert resp.status_code == 404
        assert json_data['success'] == 'false'
        assert json_data['error_message'] == 'Not found'

    def test_update_a_player_with_post(self, client):
        """ API endpoint
                /player/<nickname> [POST]
            update a player with POST method
        """
        update_player = {'nickname': 'test03', 'email': 'post_updated_test03@mail.com',}
        resp = client.post('/player/test03', json=update_player)
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        resp = client.get('/player/test03')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['player']['email'] == 'post_updated_test03@mail.com'

    def test_update_a_player_with_put(self, client):
        """ API endpoint
                /player/<nickname> [PUT]
            update a player with PUT method
        """
        update_player = {'nickname': 'test03', 'email': 'put_updated_test03@mail.com',}
        resp = client.put('/player/test03', json=update_player)
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        resp = client.get('/player/test03')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['player']['email'] == 'put_updated_test03@mail.com'

    def test_delete_a_player_with_post(self, client):
        """ API endpoint
                /player/<nickname>/delete [POST]
            delete a player with POST method
        """
        resp = client.post('/player/test01/delete')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'

    def test_delete_a_player_with_delete(self, client):
        """ API endpoint
                /player/<nickname>/delete [DELETE]
            delete a player with DELETE method
        """
        resp = client.delete('/player/test02/delete')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'

class TestPlayerItem:
    def test_add_item_to_player(self, client):
        """ API endpoint
                /player/<nickname>/add-item [POST]
            add an item to a player. and test add same item again to the same player (an error should be given).
        """
        item = {'name': 'oitem01'}
        resp = client.post('/player/oplayer01/add-item', json=item)
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['items']) == 1
        assert json_data['items'][0]['name'] == 'oitem01'
        resp = client.post('/player/oplayer01/add-item', json=item)
        json_data = resp.get_json()
        assert resp.status_code == 400
        assert json_data['success'] == 'false'
        assert json_data['error_message'] == 'Item already exists to the player.'

    def test_remove_item_from_player_with_post(self, client):
        """ API endpoint
                /player/<nickname>/remove-item/<itemname> [POST, DELETE]
            remove an item from a player with POST method
        """
        resp = client.post('/player/oplayer10/remove-item/oitem01')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['items']) == 4
        resp = client.post('/player/oplayer10/remove-item/oitem01')
        json_data = resp.get_json()
        assert resp.status_code == 400
        assert json_data['success'] == 'false'
        assert json_data['error_message'] == 'Player does not have the item.'

    def test_remove_item_from_player_with_delete(self, client):
        """ API endpoint
                /player/<nickname>/remove-item/<itemname> [POST, DELETE]
            remove an item from a player with DELETE
        """
        resp = client.delete('/player/oplayer10/remove-item/oitem02')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert len(json_data['items']) == 3

class TestPlayerGuild:
    def test_join_guild(self, client):
        """ API endpoint
                /player/<nickname>/join-guild [POST]
            join a player into a guild
        """
        guild = {'name': 'oguild01'}
        resp = client.post('/player/oplayer01/join-guild', json=guild)
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['player']['guild_id'] is not None
        guild = {'name': 'oguild02'}
        resp = client.post('/player/oplayer01/join-guild', json=guild)
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['player']['guild_id'] is not None

    def test_leave_guild(self, client):
        """ API endpoint
                /player/<nickname>/leave-guild [POST]
            leave from a joined guild
        """
        resp = client.post('/player/oplayer01/leave-guild')
        json_data = resp.get_json()
        assert resp.status_code == 200
        assert json_data['success'] == 'true'
        assert json_data['player']['guild_id'] is None
