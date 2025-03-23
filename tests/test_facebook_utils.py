# from facebook_utils import get_user_id
#
# def test_valid_user():
#     fbid = get_user_id("zuck")
#     assert fbid == 4, f"Expected 4, got {fbid}"
#     print("test_valid_user passed")
#
# def test_nonexistent_user():
#     fbid = get_user_id("thisusernamedoesnotexist123456")
#     assert fbid is None, f"Expected None, got {fbid}"
#     print("test_nonexistent_user passed")
#
# def test_empty_username():
#     fbid = get_user_id("")
#     assert fbid is None, f"Expected None for empty username, got {fbid}"
#     print("test_empty_username passed")
#
# if __name__ == "__main__":
#     test_valid_user()
#     test_nonexistent_user()
#     test_empty_username()
#     print("All tests passed")
