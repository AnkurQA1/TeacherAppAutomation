import pytest
import requests

# from Acadally.QAWorkspace import BASE_URL_LOGIN


def teacher_login():
    BASE_URL_LOGIN="https://uat.acadally.com/login/index.php"
    USERNAME="uat_203"
    PASSWORD="Ttaps@12"
    SERVICE="moodle_mobile_app"
    URL=f"{BASE_URL_LOGIN}? username={USERNAME}& password={PASSWORD}&service={SERVICE}"

    response = requests.get(URL)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    try:
        response_json = response.json()
        assert "token" in response_json, "'token' key is missing in the response."
        assert response_json["token"], "Login failed, token not found."

    except requests.exceptions.JSONDecodeError:
        pytest.fail("Response is not valid JSON.")
