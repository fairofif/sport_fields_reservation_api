# from static import *

# def test_create_chat_match_unposted():
#     # prereq
#     insert_admin_unittest_user()
#     player_username = 'unittest'
#     insert_player_unittest_user_custom(player_username)
#     player_token = newUserToken()
#     player_device = newVirtualDeviceID()
#     insert_unittest_device(player_device)
#     insert_player_unittest_token_custom(player_token, player_device, player_username)

#     # condition
#     header = {
#         'token': player_token
#     }
#     body = {
#         'admin_username': 'unittest'
#     }

#     # test
#     url = "/player/chatmatch"
#     client = app.test_client()

#     response = client.post(url, headers=header, json=body)

#     # clean unittest data
#     id_chat_match = response.get_json()['data']['id']
#     delete_player_unittest_token(id_chat_match)
#     delete_unittest_device(player_device)
#     delete_player_unittest_user_custom(player_username)
#     delete_admin_unittest_user()

#     assert response.status_code == 200
#     assert response.get_json()['status'] == True
#     assert response.get_json()['message'] == 'Create new match success'

# def test_create_chat_match_posted():
#     # prereq
#     insert_admin_unittest_user()
#     player_username = 'unittest'
#     insert_player_unittest_user_custom(player_username)
#     player_token = newUserToken()
#     player_device = newVirtualDeviceID()
#     insert_unittest_device(player_device)
#     insert_player_unittest_token_custom(player_token, player_device, player_username)

#     # condition
#     header = {
#         'token': player_token
#     }
#     body = {
#         'admin_username': 'unittest'
#     }
#     id_chat_match = newChatMatchUUID()
#     insert_chat_match(id_chat_match, 'unittest', player_username)

#     # test
#     url = "/player/chatmatch"
#     client = app.test_client()

#     response = client.post(url, headers=header, json=body)

#     # clean unittest data
#     delete_player_unittest_token(id_chat_match)
#     delete_unittest_device(player_device)
#     delete_player_unittest_user_custom(player_username)
#     delete_admin_unittest_user()

#     assert response.status_code == 200
#     assert response.get_json()['status'] == True
#     assert response.get_json()['message'] == 'Match had been created before, return the old one'
#     assert response.get_json()['data']['id'] == id_chat_match


