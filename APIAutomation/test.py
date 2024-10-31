import requests
import pytest
BASE_URL = "https://uat.acadally.com/webservice/rest/server.php"
LOGIN_URL = "https://uat.acadally.com/login/teachertoken.php"
MOODLE_WSREST_FORMAT = "json"
def construct_url(wsfunction, additional_params, token):
    return f"{BASE_URL}?moodlewsrestformat={MOODLE_WSREST_FORMAT}&wstoken={token}&wsfunction={wsfunction}&{additional_params}"

def login_and_get_token(username, password, service):
    params = {
        "username": username,
        "password": password,
        "service": service
    }
    response = requests.get(LOGIN_URL, params=params)
    assert response.status_code == 200, f"Login failed: {response.status_code}"
    response_json = response.json()
    token = response_json.get('token')
    if not token:
        pytest.fail("Failed to retrieve token")
    return token

def get_teacher_classes(token):
    params = {"moodlewsrestformat": MOODLE_WSREST_FORMAT, "wstoken": token,
              "wsfunction": "local_teacher_get_my_classes"}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def get_upcoming_chapters(token, classid):
    params = {"classid": classid}
    url = construct_url("local_teacher_get_upcoming_chapters", f"classid={classid}", token)
    response = requests.get(url)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def get_chapter_details(token, chapterid, deptid):
    params = {"chapterid": chapterid, "deptid": deptid}
    url = construct_url("local_teacher_get_chapter_details", f"chapterid={chapterid}&deptid={deptid}", token)
    response = requests.get(url)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def start_chapter(token, chapterid, courseid, deptid, start_date, due_date, topic_ids):
    params = f"chapterid={chapterid}&courseid={courseid}&deptid={deptid}&startdate={start_date}&duedate={due_date}"
    for index, topic_id in enumerate(topic_ids):
        params += f"&topicids[{index}]={topic_id}"
    url = construct_url("local_teacher_start_chapter", params, token)
    response = requests.post(url)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def get_ongoing_chapter(token, deptid):
    url = construct_url("local_teacher_ongoing_chapter", f"deptid={deptid}", token)
    response = requests.get(url)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def get_ongoing_chapter_details(token, chapterid, deptid):
    url = construct_url("local_teacher_ongoing_chapter_details", f"chapterid={chapterid}&deptid={deptid}", token)
    response = requests.get(url)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def end_chapter(token, chapterid, courseid, deptid):
    url = construct_url("local_teacher_end_chapter", f"chapterid={chapterid}&courseid={courseid}&deptid={deptid}",
                        token)
    response = requests.get(url)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def get_completed_chapters(token, deptid, page, per_page):
    url = construct_url("local_teacher_get_completed_chapters", f"deptid={deptid}&page={page}&per_page={per_page}",
                        token)
    response = requests.get(url)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def get_all_chapters(token, classid):
    url = construct_url("local_teacher_get_all_chapters", f"classid={classid}", token)
    response = requests.get(url)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def get_quiz_questions(token, courseid, cmid):
    url = construct_url("local_teacher_quiz_questions", f"courseid={courseid}&cmid={cmid}", token)
    response = requests.get(url)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def get_video_url(token, courseid, cmid, instanceid):
    url = construct_url("local_teacher_videourl", f"courseid={courseid}&cmid={cmid}&instanceid={instanceid}", token)
    response = requests.get(url)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def get_completed_chapter_details(token, chapterid, deptid):
    url = construct_url("local_teacher_completed_chapter_details", f"chapterid={chapterid}&deptid={deptid}", token)
    response = requests.get(url)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

# Master Function
def test_master_sequence():
    token = "d6041defb0339ee125153a9cdb21fc5d"
    USERNAME = "uta_2067"
    PASSWORD = "Apspl@78"
    SERVICE = "moodle_mobile_app"

    try:
        token = login_and_get_token(USERNAME, PASSWORD, SERVICE)

        # Get mobile user
        mobile = "6351025333"
        url = construct_url("local_webservice_get_mobile_users", f"mobile={mobile}", token)
        response = requests.get(url)
        assert response.status_code == 200, "Failed to get mobile user"
        mobile_user_data = response.json()
        print(f"Mobile user fetched successfully: {mobile_user_data}")

        # Send OTP
        username = "uta_2067"
        url = construct_url("local_webservice_send_otp", f"username={username}", token)
        response = requests.get(url)
        assert response.status_code == 200, "Failed to send OTP"
        otp_data = response.json()
        print(f"OTP sent successfully: {otp_data}")

        # Verify OTP
        user_id = "7297"
        otp = "643215"
        url = construct_url("local_webservice_verify_otp", f"userid={user_id}&otp={otp}", token)
        response = requests.get(url)
        assert response.status_code == 200, "Failed to verify OTP"
        verify_otp_data = response.json()
        print(f"OTP verified successfully: {verify_otp_data}")

        # Reset password
        new_password = "P@ssw0rd"
        confirm_password = "P@ssw0rd"
        url = construct_url(
            "local_webservice_reset_password",
            f"userid={user_id}&otp={otp}&newpassword={new_password}&confirmpassword={confirm_password}",
            token
        )
        response = requests.get(url)
        assert response.status_code == 200, "Failed to reset password"
        reset_password_data = response.json()
        print(f"Password reset successfully: {reset_password_data}")

        # Step 5: Insert app data
        imei_no = "null"
        token_device = "null"
        device_type = "null"
        current_app_version = "null"
        url = construct_url(
            "local_webservice_insert_app_data",
            f"userid={user_id}&imei_no={imei_no}&token={token_device}&device_type={device_type}&currentappversion={current_app_version}",
            token
        )
        response = requests.get(url)
        assert response.status_code == 200, "Failed to insert app data"
        insert_app_data = response.json()
        print(f"App data inserted successfully: {insert_app_data}")

        # Get user profile
        url = construct_url("local_user_profile", f"userid={user_id}", token)
        response = requests.post(url, data={})
        assert response.status_code == 200, "Failed to fetch user profile"
        user_profile = response.json()
        print(f"User profile fetched successfully: {user_profile}")

        # Get user chapters
        subject_id = "2135"
        url = construct_url("local_user_chapters", f"subjectid={subject_id}", token)
        response = requests.get(url)
        assert response.status_code == 200, "Failed to fetch user chapters"
        user_chapters = response.json()
        print(f"User chapters fetched successfully: {user_chapters}")

        # Get chapter data
        chapter_id = "4850"
        url = construct_url("local_user_chapters_data", f"subjectid={subject_id}&chapterid={chapter_id}", token)
        response = requests.get(url)
        assert response.status_code == 200, "Failed to fetch chapter data"
        chapter_data = response.json()
        print(f"Chapter data fetched successfully: {chapter_data}")

        # Override activity completion
        cmid = "6071"
        new_state = "1"
        url = construct_url(
            "core_completion_override_activity_completion_status",
            f"userid={user_id}&cmid={cmid}&newstate={new_state}",
            token
        )
        response = requests.post(url)
        assert response.status_code == 200, "Failed to override activity completion"
        override_data = response.json()
        print(f"Activity completion overridden successfully: {override_data}")

        # Notification
        url = construct_url("message_popup_get_custompopup_notifications", f"useridto={user_id}", token)
        response = requests.get(url)
        assert response.status_code == 200, "Failed to get popup notifications"
        notifications = response.json()
        print(f"Popup notifications fetched successfully: {notifications}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"API request failed: {str(e)}")
    except AssertionError as e:
        pytest.fail(f"Assertion failed: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")