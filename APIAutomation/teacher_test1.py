import pytest
import requests
def login_and_get_token(USERNAME,PASSWORD,SERVICE):
    BASE_URL = "https://uat.acadally.com/login/teachertoken.php"
    params = {
        "username":USERNAME,
        "password": PASSWORD,
        "service": SERVICE
    }
    response = requests.get(BASE_URL,params)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    if "application/json" in response.headers.get("Content-Type", ""):
        try:
            response_json = response.json()
            assert "token" in response_json, "'token' key is missing in the response."
            assert response_json["token"], "Login failed, token not found."
            print(f"Token: {response_json['token']}")
        except requests.exceptions.JSONDecodeError:
            pytest.fail("Response is not valid JSON.")
    else:
        pytest.fail(f"Response is not JSON. Content-Type: {response.headers.get('Content-Type')}")

def get_teacher_classes():
    BASE_URL = "https://uat.acadally.com/webservice/rest/server.php"
    params = {
        "moodlewsrestformat": "json",
        "wstoken": "f7700471c6db9223ecf61714ca78f442",
        "wsfunction": "local_teacher_get_my_classes"
    }
    response = requests.get(BASE_URL, params=params)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    if "application/json" in response.headers.get("Content-Type", ""):
        try:
            response_json = response.json()
            print("Response JSON:", response_json)
            print("Response Keys:", response_json.keys())
            assert len(response_json) > 0, "The response is empty."
        except requests.exceptions.JSONDecodeError:
            pytest.fail("Response is not valid JSON.")
    else:
        pytest.fail(f"Response is not JSON. Content-Type: {response.headers.get('Content-Type')}")

BASE_URL = "https://uat.acadally.com/webservice/rest/server.php"
@pytest.fixture
def api_params():
    return {
        "token": "5f5ff1b75635428d2eeb14c4991aaaf8",
        "wsfunction": "local_teacher_get_upcoming_chapters",
        "classid": "2111"
    }
def make_request(params):
    url = f"{BASE_URL}?moodlewsrestformat=json&wstoken={params['token']}&wsfunction={params['wsfunction']}&classid={params['classid']}"
    response = requests.get(url)
    print("Request URL:", url)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    return response
def get_upcoming_chapters(api_params):
    response = make_request(api_params)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    try:
        response_json = response.json()
        print("Response JSON:", response_json)
        assert "status" in response_json, "'status' key is missing in the response."
        assert response_json["status"], "API returned failure status."
        assert "data" in response_json, "'data' key is missing in the response."
        assert isinstance(response_json["data"], list), "'data' should be a list."
        if len(response_json["data"]) == 0:
            print("No upcoming chapters found for the given class ID.")
        else:
            print(f"Found {len(response_json['data'])} upcoming chapters.")
    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON")
    except AssertionError as e:
        pytest.fail(str(e))

BASE_URL = "https://uat.acadally.com/webservice/rest/server.php"
MoodleWSRestFormat = "json"
@pytest.mark.parametrize("token, chapterid, deptid", [
    ("f7700471c6db9223ecf61714ca78f442", 487379, 2236),
])
def get_chapter_details(token, chapterid, deptid):
    params = {
        "moodlewsrestformat": MoodleWSRestFormat,
        "wstoken": token,
        "wsfunction": "local_teacher_get_chapter_details",
        "chapterid": chapterid,
        "deptid": deptid,
    }
    response = requests.get(BASE_URL, params=params)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    try:
        response_json = response.json()
        print("Response JSON:", response_json)
        assert "status" in response_json, "'status' key is missing in the response."
        assert response_json["status"], f"API Error: {response_json.get('message', 'No message available')}"
        if "data" in response_json:
            assert isinstance(response_json["data"], list), "'data' field is not a list."
            assert len(response_json["data"]) > 0, "The 'data' field is empty."
            print("Chapter details fetched successfully.")
        else:
            print("No 'data' field present, but the API call was successful.")
    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON.")
    except AssertionError as e:
        pytest.fail(str(e))

BASE_URL = "https://uat.acadally.com/webservice/rest/server.php"
MoodleWSRestFormat = "json"
@pytest.mark.parametrize("token, chapter_id, course_id, dept_id, start_date, due_date, topic_ids", [
    ("f7700471c6db9223ecf61714ca78f442", 487291, 221, 2236, 1728017998, 1728017998, [487380, 487381, 487382]),
])
def start_chapter(token, chapter_id, course_id, dept_id, start_date, due_date, topic_ids):
    params = {
        "moodlewsrestformat": MoodleWSRestFormat,
        "wstoken": token,
        "wsfunction": "local_teacher_start_chapter",
        "chapterid": chapter_id,
        "courseid": course_id,
        "deptid": dept_id,
        "startdate": start_date,
        "duedate": due_date,
    }
    for index, topic_id in enumerate(topic_ids):
        params[f"topicids[{index}]"] = topic_id
    response = requests.post(BASE_URL, data=params)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    if "application/json" in response.headers.get("Content-Type", ""):
        try:
            response_json = response.json()
            assert "status" in response_json, "'status' field is missing in the response."
            assert response_json["status"], f"API Error: {response_json.get('message', 'No message available')}"
            if "data" in response_json:
                assert isinstance(response_json["data"], list), "'data' field is not a list."
                assert len(response_json["data"]) > 0, "The 'data' field is empty."
            else:
                print("No 'data' field found in the response.")
        except requests.exceptions.JSONDecodeError:
            pytest.fail("Response is not valid JSON.")
    else:
        pytest.fail(f"Response is not JSON. Content-Type: {response.headers.get('Content-Type')}")

BASE_URL = "https://uat.acadally.com/webservice/rest/server.php"
MoodleWSRestFormat = "json"
@pytest.mark.parametrize("token, deptid", [
    ("f7700471c6db9223ecf61714ca78f442", 2236),
])
def get_ongoing_chapter(token, deptid):
    params = {
        "moodlewsrestformat": MoodleWSRestFormat,
        "wstoken": token,
        "wsfunction": "local_teacher_ongoing_chapter",
        "deptid": deptid
    }
    response = requests.get(BASE_URL, params=params)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    try:
        response_json = response.json()
        print("Response JSON:", response_json)
        assert "status" in response_json, "'status' key is missing in the response."
        assert response_json["status"], f"API Error: {response_json.get('message', 'No message available')}"
        if "data" in response_json:
            assert isinstance(response_json["data"], list), "'data' field is not a list."
            assert len(response_json["data"]) > 0, "The 'data' field is empty."
            print("Ongoing chapter data fetched successfully.")
        else:
            print("No 'data' field found in the response, but the request was successful.")
    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON.")
    except AssertionError as e:
        pytest.fail(str(e))

BASE_URL = "https://uat.acadally.com/webservice/rest/server.php"
MoodleWSRestFormat = "json"
@pytest.mark.parametrize("token, chapterid, deptid", [
    ("f7700471c6db9223ecf61714ca78f442", 487360, 2236),
])
def get_ongoing_chapter_details(token, chapterid, deptid):
    params = {
        "moodlewsrestformat": MoodleWSRestFormat,
        "wstoken": token,
        "wsfunction": "local_teacher_ongoing_chapter_details",
        "chapterid": chapterid,
        "deptid": deptid
    }
    response = requests.get(BASE_URL, params=params)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    try:
        response_json = response.json()
        print("Response JSON:", response_json)
        assert "status" in response_json, "'status' key is missing in the response."
        assert response_json["status"], f"API Error: {response_json.get('message', 'No message available')}"
        print("Response Keys:", response_json.keys())
        expected_fields = ["cname", "class", "courseid"]
        for field in expected_fields:
            assert field in response_json, f"'{field}' field is missing in the response."
        assert response_json.get("cname") is not None, "'cname' field is None."
        assert response_json.get("class") is not None, "'class' field is None."
        assert response_json.get("courseid") is not None, "'courseid' field is None."
        print("Ongoing chapter details fetched successfully.")
    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON.")
    except AssertionError as e:
        pytest.fail(str(e))

BASE_URL = "https://uat.acadally.com/webservice/rest/server.php"
MoodleWSRestFormat = "json"
@pytest.mark.parametrize("token, chapterid, courseid, deptid", [
    ("f7700471c6db9223ecf61714ca78f442", 487461, 222, 2235),
])
def end_chapter(token, chapterid, courseid, deptid):
    params = {
        "moodlewsrestformat": MoodleWSRestFormat,
        "wstoken": token,
        "wsfunction": "local_teacher_end_chapter",
        "chapterid": chapterid,
        "courseid": courseid,
        "deptid": deptid
    }
    response = requests.get(BASE_URL, params=params)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    try:
        response_json = response.json()
        print("Response JSON:", response_json)
        assert "status" in response_json, "'status' key is missing in the response."
        if response_json["status"]:
            print("Response Keys:", response_json.keys())
            expected_fields = ["status", "message"]
            for field in expected_fields:
                assert field in response_json, f"'{field}' field is missing in the response."
            if response_json.get("message") == "Chapter ended successfully":
                print("Chapter ended successfully.")
            else:
                pytest.fail(f"Unexpected message: {response_json.get('message')}")
        else:
            pytest.fail(f"API Error: {response_json.get('message', 'No message available')}")
    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON.")
    except AssertionError as e:
        pytest.fail(str(e))

BASE_URL = "https://uat.acadally.com/webservice/rest/server.php"
MoodleWSRestFormat = "json"
@pytest.mark.parametrize("token, deptid, page, per_page", [
    ("f7700471c6db9223ecf61714ca78f442", 2236, 1, 2),
])
def get_completed_chapters(token, deptid, page, per_page):
    params = {
        "moodlewsrestformat": MoodleWSRestFormat,
        "wstoken": token,
        "wsfunction": "local_teacher_get_completed_chapters",
        "deptid": deptid,
        "page": page,
        "per_page": per_page
    }
    response = requests.get(BASE_URL, params=params)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    if "application/json" in response.headers.get("Content-Type", ""):
        try:
            response_json = response.json()
            assert "status" in response_json, "'status' field is missing in the response."
            assert response_json["status"], f"API Error: {response_json.get('message', 'No message available')}"
            assert "data" in response_json, "'data' field is missing in the response."
            assert isinstance(response_json["data"], list), "'data' field is not a list."
            assert len(response_json["data"]) > 0, "The 'data' field is empty."
            print("Completed chapters data fetched successfully.")
        except requests.exceptions.JSONDecodeError:
            pytest.fail("Response is not valid JSON.")
    else:
        pytest.fail(f"Response is not JSON. Content-Type: {response.headers.get('Content-Type')}")

BASE_URL = "https://uat.acadally.com/webservice/rest/server.php"
MoodleWSRestFormat = "json"
@pytest.mark.parametrize("token, classid", [
    ("f7700471c6db9223ecf61714ca78f442", 2236),
])
def get_all_chapters(token, classid):
    params = {
        "moodlewsrestformat": MoodleWSRestFormat,
        "wstoken": token,
        "wsfunction": "local_teacher_get_all_chapters",
        "classid": classid
    }
    response = requests.get(BASE_URL, params=params)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    if "application/json" in response.headers.get("Content-Type", ""):
        try:
            response_json = response.json()
            assert "status" in response_json, "'status' field is missing in the response."
            assert response_json["status"], f"API Error: {response_json.get('message', 'No message available')}"
            assert "data" in response_json, "'data' field is missing in the response."
            assert isinstance(response_json["data"], list), "'data' field is not a list."
            assert len(response_json["data"]) > 0, "The 'data' field is empty."
            print("All chapters data fetched successfully.")
        except requests.exceptions.JSONDecodeError:
            pytest.fail("Response is not valid JSON.")
    else:
        pytest.fail(f"Response is not JSON. Content-Type: {response.headers.get('Content-Type')}")

API_URL = "https://uat.acadally.com/webservice/rest/server.php"
TOKEN = "f7700471c6db9223ecf61714ca78f442"
MOODLE_FUNCTION = "local_teacher_quiz_questions"
MOODLEWS_FORMAT = "json"
COURSE_ID = 221
cmid = 11707
@pytest.fixture
def api_url():
    return f"{API_URL}?moodlewsrestformat={MOODLEWS_FORMAT}&wstoken={TOKEN}&wsfunction={MOODLE_FUNCTION}&courseid={COURSE_ID}&cmid={cmid}"
def test_api_response_status_code(api_url):
    response = requests.get(api_url)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
def test_api_content_type(api_url):
    response = requests.get(api_url)
    assert response.headers["Content-Type"] == "application/json", \
        f"Unexpected content type: {response.headers['Content-Type']}"
def get_quiz_questions(api_url,COURSE_ID,cmid):
    response = requests.get(api_url)
    json_data = response.json()
    assert "questions" in json_data, "Key 'questions' not found in the response"
    assert isinstance(json_data["questions"], list), "Expected 'questions' to be a list"
    if not json_data["questions"]:
        pytest.skip("No questions found in the response")
    first_question = json_data["questions"][0]
    assert "id" in first_question or "questionid" in first_question, \
        "Key 'id' or 'questionid' not found in the first question"
    assert "name" in first_question, "Key 'name' not found in the first question"

BASE_URL = "https://uat.acadally.com/webservice/rest/server.php"
MoodleWSRestFormat = "json"
@pytest.mark.parametrize("token, courseid, cmid, instanceid", [
    ("f7700471c6db9223ecf61714ca78f442", 221, 11714, 2784),
])
def get_video_url(token, courseid, cmid, instanceid):
    params = {
        "moodlewsrestformat": MoodleWSRestFormat,
        "wstoken": token,
        "wsfunction": "local_teacher_videourl",
        "courseid": courseid,
        "cmid": cmid,
        "instanceid": instanceid
    }
    response = requests.get(BASE_URL, params=params)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    if "application/json" in response.headers.get("Content-Type", ""):
        try:
            response_json = response.json()
            print(response_json)
            assert "video_url" in response_json["data"], "'video_url' field is missing in the response."
            multimedia = response_json.get("multimedia", None)
            assert isinstance(multimedia, list) or multimedia is None or multimedia == "", \
                "Expected 'multimedia' to be a list, empty, or None."
            if not multimedia:
                assert "video_url" in response_json["data"], "No 'video_url' found even when 'multimedia' is empty"
                print("No multimedia, but video_url exists.")
            else:
                print("Multimedia found.")
        except requests.exceptions.JSONDecodeError:
            pytest.fail("Response is not valid JSON.")
    else:
        pytest.fail(f"Response is not JSON. Content-Type: {response.headers.get('Content-Type')}")

BASE_URL = "https://uat.acadally.com/webservice/rest/server.php"
MoodleWSRestFormat = "json"
@pytest.mark.parametrize("token, chapterid, deptid", [
    ("f7700471c6db9223ecf61714ca78f442", 487271, 2231),
])
def get_completed_chapter_details(token, chapterid, deptid):
    params = {
        "moodlewsrestformat": MoodleWSRestFormat,
        "wstoken": token,
        "wsfunction": "local_teacher_completed_chapter_details",
        "chapterid": chapterid,
        "deptid": deptid
    }
    response = requests.get(BASE_URL, params=params)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    if "application/json" in response.headers.get("Content-Type", ""):
        try:
            response_json = response.json()
            print(response_json)
            assert "status" in response_json, "'status' field is missing in the response."
            assert response_json["status"] is True, "Status is not True, something went wrong."
            assert "chapterdata" in response_json, "'chapterdata' field is missing in the response."
            assert isinstance(response_json["chapterdata"], list), "'chapterdata' should be a list."
            assert "topics" in response_json, "'topics' field is missing in the response."
            assert isinstance(response_json["topics"], list), "'topics' should be a list."
        except requests.exceptions.JSONDecodeError:
            pytest.fail("Response is not valid JSON.")
    else:
        pytest.fail(f"Response is not JSON. Content-Type: {response.headers.get('Content-Type')}")

#Master Function Code For Teacher App-
def test_master_function():
    USERNAME = "uat_203"
    PASSWORD = "Ttaps@12"
    SERVICE = "moodle_mobile_app"

    try:
        # Step 1: Login and get token
        token = login_and_get_token(USERNAME, PASSWORD, SERVICE)
        if not token:
            raise ValueError("Failed to get token")
        print(f"Received Token: {token}")

        # Step 2: Get teacher classes
        teacher_classes = get_teacher_classes(token)
        if teacher_classes is None:
            raise ValueError("Failed to retrieve teacher classes")
        print(f"Teacher classes: {teacher_classes}")

        # Step 3: Get upcoming chapters
        classid = "2111"
        upcoming_chapters = get_upcoming_chapters(token, classid)
        if upcoming_chapters is None:
            raise ValueError("Failed to retrieve upcoming chapters")
        print(f"Upcoming chapters: {upcoming_chapters}")

        # Step 4: Get chapter details
        chapterid = 487379
        deptid = 2236
        chapter_details = get_chapter_details(token, chapterid, deptid)
        if chapter_details is None:
            raise ValueError("Failed to retrieve chapter details")
        print(f"Chapter details: {chapter_details}")

        # Step 5: Start chapter
        courseid = 221
        start_date = "1728017998"
        due_date = "1728017998"
        topic_ids = [487380, 487381, 487382]
        start_chapter_data = start_chapter(token, chapterid, courseid, deptid, start_date, due_date, topic_ids)
        if start_chapter_data is None:
            raise ValueError("Failed to start chapter")
        print(f"Started chapter: {start_chapter_data}")

        # Step 6: Get ongoing chapter
        ongoing_chapter = get_ongoing_chapter(token, deptid)
        if ongoing_chapter is None:
            raise ValueError("Failed to retrieve ongoing chapter")
        print(f"Ongoing chapter: {ongoing_chapter}")

        # Step 7: Get ongoing chapter details
        ongoing_chapter_details = get_ongoing_chapter_details(token, chapterid, deptid)
        if ongoing_chapter_details is None:
            raise ValueError("Failed to retrieve ongoing chapter details")
        print(f"Ongoing chapter details: {ongoing_chapter_details}")

        # Step 8: End chapter
        end_chapter_data = end_chapter(token, chapterid, courseid, deptid)
        if end_chapter_data is None:
            raise ValueError("Failed to end chapter")
        print(f"Ended chapter: {end_chapter_data}")

        # Step 9: Get completed chapters
        page = 1
        per_page = 2
        completed_chapters = get_completed_chapters(token, deptid, page, per_page)
        if completed_chapters is None:
            raise ValueError("Failed to retrieve completed chapters")
        print(f"Completed chapters: {completed_chapters}")

        # Step 10: Get all chapters
        all_chapters = get_all_chapters(token, classid)
        if all_chapters is None:
            raise ValueError("Failed to retrieve all chapters")
        print(f"All chapters: {all_chapters}")

        # Step 11: Get quiz questions
        cmid = 11707
        quiz_questions = get_quiz_questions(token, courseid, cmid)
        if quiz_questions is None:
            raise ValueError("Failed to retrieve quiz questions")
        print(f"Quiz questions: {quiz_questions}")

        # Step 12: Get video URL
        instanceid = 2784
        video_url = get_video_url(token, courseid, cmid, instanceid)
        if video_url is None:
            raise ValueError("Failed to retrieve video URL")
        print(f"Video URL: {video_url}")

        # Step 13: Get completed chapter details
        completed_chapter_details = get_completed_chapter_details(token, chapterid, deptid)
        if completed_chapter_details is None:
            raise ValueError("Failed to retrieve completed chapter details")
        print(f"Completed chapter details: {completed_chapter_details}")
    except Exception as e:
        print(f"An error occurred: {e}")