import requests
import pytest

BASE_URL_LOGIN = "https://uat.acadally.com/login/token.php"

def test_login_success():
    USERNAME = "uat_101"
    PASSWORD = "Trial@123"
    SERVICE = "moodle_mobile_app"

    Myurl = f"{BASE_URL_LOGIN}?username={USERNAME}&password={PASSWORD}&service={SERVICE}"
    response = requests.get(Myurl)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    assert response.status_code == 200

    try:
        response_json = response.json()
        print("Response JSON:", response_json)

        assert "token" in response_json
        assert response_json["token"] is not None
        print("Login test passed: Token received successfully.")

    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON")
    except AssertionError:
        pytest.fail("Login failed or token not found")


BASE_URL_PROFILE = "https://uat.acadally.com/webservice/rest/server.php?moodlewsrestformat=json&wstoken=3595d317e9c8d64e580d2239dbd0cc8d&wsfunction=local_user_chapters&subjectid=2231"

def test_user_details():
    response = requests.get(BASE_URL_PROFILE)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    try:
        response_json = response.json()
        print("Response JSON:", response_json)

        assert response_json.get("status") == True, f"User details not found: {response_json.get('message')}"
        print("User details fetched successfully.")

    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON")
    except AssertionError as e:
        pytest.fail(str(e))
        print("Test is failed")


BASE_URL_CHAPTERS = "https://uat.acadally.com/webservice/rest/server.php?wsfunction=local_user_chapters_data&subjectid=2231&wstoken=3595d317e9c8d64e580d2239dbd0cc8d&moodlewsrestformat=json"

def test_chapters_details():
    response = requests.get(BASE_URL_CHAPTERS)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    try:
        response_json = response.json()
        print("Response JSON:", response_json)

        assert response_json.get("status") == True, f"Chapters details not found: {response_json.get('message')}"
        print("Chapters details fetched successfully.")

    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON")
    except AssertionError as e:
        pytest.fail(str(e))


BASE_URL_USER_CHAPTER_DATA = "https://uat.acadally.com/webservice/rest/server.php?wsfunction=local_user_chapters_data&subjectid=2124&wstoken=6403bccca9285c104d202edb276f2972&moodlewsrestformat=json"

def test_user_chapter_data():
    response = requests.get(BASE_URL_USER_CHAPTER_DATA)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    try:
        response_json = response.json()
        print("Response JSON:", response_json)

        assert response_json.get("status") == True, "User chapter data not found"
        print("User chapter data fetched successfully.")

    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON")
    except AssertionError as e:
        pytest.fail(str(e))


BASE_URL_GET_CHAPTERS = "https://uat.acadally.com/webservice/rest/server.php?moodlewsrestformat=json&wstoken=6403bccca9285c104d202edb276f2972&wsfunction=local_webservice_get_chapters&userid=7281&courseid=120"

def test_get_chapters():
    response = requests.get(BASE_URL_GET_CHAPTERS)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
        if isinstance(response_json,dict):

            assert response_json.get("status") == True, f"User chapter data not found: {response_json.get('message')}"
            assert "data" in response_json, "No 'data' field found in the response"
            assert len(response_json["data"]) > 0, "The 'data' field is empty"
            print("User chapter data fetched successfully.")
        elif isinstance(response_json,list):
            assert len(response_json) > 0, "The response list is empty"
            print(f"Response contains {len(response_json)} items.")

    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON")
    except AssertionError as e:
        pytest.fail(str(e))

#-----------------------------------------------------------------------------------------------------------------

BASE_URL_COURSE_QUIZZES = "https://uat.acadally.com/webservice/rest/server.php?moodlewsrestformat=json&wstoken=3595d317e9c8d64e580d2239dbd0cc8d&wsfunction=mod_quiz_get_quizzes_by_courses&courseids[0]=220"

def test_course_quizzes():
    response = requests.get(BASE_URL_COURSE_QUIZZES)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    try:
        response_json = response.json()
        print("Response JSON:", response_json)

        if isinstance(response_json, dict):
            assert "quizzes" in response_json, "No 'quizzes' field found in the response"
            quizzes_data = response_json["quizzes"]
            assert isinstance(quizzes_data, list), "'quizzes' field is not a list"
            assert len(quizzes_data) > 0, "The 'quizzes' field is empty"
            print("Course quizzes data fetched successfully.")
        else:
            pytest.fail("Unexpected response format: Expected a dictionary")

    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON")
    except AssertionError as e:
        pytest.fail(str(e))

# ---------------------------------------------------------------------------------------------------------------------
BASE_URL = 'https://uat.acadally.com/webservice/rest/server.php?moodlewsrestformat=json&wstoken=3595d317e9c8d64e580d2239dbd0cc8d&wsfunction=mod_quiz_start_attempt&quizid=8011'

def test_quiz_start_attempt():
    response = requests.get(BASE_URL)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    try:
        response_json = response.json()
        print("Keys in JSON response:", response_json.keys())

        if "exception" in response_json:
            error_message = response_json.get("message", "No error message provided")
            pytest.fail(f"API returned an exception: {error_message}")

        if isinstance(response_json, dict):
            if "message" in response_json:
                quizzes_data = response_json["message"]
                assert isinstance(quizzes_data, list), "'message' field is not a list"
                assert len(quizzes_data) > 0, "The 'quizzes' field is empty"
                print("Course quizzes data fetched successfully.")
            else:
                pytest.fail(f"No 'quizzes' field found in the response. Available keys: {list(response_json.keys())}")
        else:
            pytest.fail("Unexpected response format: Expected a dictionary")

    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON")
    except AssertionError as e:
        pytest.fail(str(e))
