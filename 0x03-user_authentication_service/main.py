#!/usr/bin/env python3
"""
Main file
"""

import requests


url = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """
    Registering user
    """
    data = {'email': email, 'password': password}
    response = requests.post(url + '/users', data=data)
    assert (response.status_code == 200)
    assert (response.json() == {"email": email,
                                "message": "user created"})
    response = requests.post(url + '/users', data=data)
    assert (response.status_code == 400)
    assert (response.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Logging in with wrong details
    """
    data = {'email': email, 'password': password}
    response = requests.post(url + '/sessions', data=data)
    assert (response.status_code == 401)


def log_in(email: str, password: str) -> str:
    """
    Logging in with crrect details
    """
    data = {'email': email, 'password': password}
    response = requests.post(url + '/sessions', data=data)

    assert (response.status_code == 200)
    assert (response.json() == {"email": email,
                                "message": "logged in"})
    assert ('session_id' in response.cookies)
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Checking if profile is not logged in
    """
    response = requests.get(url + '/profile')
    assert (response.status_code == 403)


def profile_logged(session_id: str) -> None:
    """
    Checks if user is logged in
    """
    cookies = {'session_id': session_id}
    response = requests.get(url + '/profile',
                            cookies=cookies)
    assert (response.status_code == 200)
    assert ('email' in response.json())


def log_out(session_id: str) -> None:
    """
    Logging user out
    """
    response = requests.delete(url + '/sessions',
                               cookies={'session_id': session_id})
    assert (response.status_code == 200)
    assert (response.json() == {"message": "Bienvenue"})


def reset_password_token(email: str) -> str:
    """
    Getting reset password token
    """
    response = requests.post(url + '/reset_password',
                             data={'email': email})
    assert (response.status_code == 200)
    assert ('email' in response.json())
    assert response.json()["email"] == email
    assert ('reset_token' in response.json())
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updating user password
    """
    data = {'email': email, 'new_password': new_password,
            'reset_token': reset_token}
    response = requests.put(url + '/reset_password',
                            data=data)
    assert (response.status_code == 200)
    assert (response.json() == {"email": email,
                                "message": "Password updated"})


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
