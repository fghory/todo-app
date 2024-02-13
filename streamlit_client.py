# streamlit_client.py

import streamlit as st
import requests


BASE_URL = "http://127.0.0.1:8000"


def register_user():
    st.subheader("Register")
    username = st.text_input("Username", key="register_username")
    password = st.text_input("Password", type="password", key="register_password")
    if st.button("Register", key="register"):
        response = requests.post(
            f"{BASE_URL}/users/",
            data={"username": username, "password": password},
        )
        if response.status_code == 200:
            st.success("Registered successfully. Please log in.")
        else:
            st.error("Registration failed.")


def login_user():
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login"):
        response = requests.post(
            f"{BASE_URL}/login/", data={"username": username, "password": password}
        )
        print(response.text)
        if response.status_code == 200:
            st.session_state["token"] = response.json()["access_token"]
            st.success("Logged in successfully.")
            st.rerun()  # Rerun the app to show the list of todos
        else:
            st.error("Login failed.")


def create_todo():
    st.subheader("Add a new Todo")
    title = st.text_input("Title", key="create_title")
    description = st.text_area("Description", key="create_description")
    # print(title, description, st.session_state["token"])
    if st.button("Add Todo", key="create"):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        print(headers)
        response = requests.post(
            f"{BASE_URL}/todos/",
            json={"title": title, "description": description},
            headers=headers,
        )

        print(response.text)
        if response.status_code == 200:
            st.success("Todo added successfully")
        else:
            st.error("Failed to add Todo")


# key=f"{todo_id}"


def delete_todo(todo_id):
    if st.button("Delete Todo", key=f"{todo_id}"):
        response = requests.delete(
            f"{BASE_URL}/todos/{todo_id}/",
            headers={"Authorization": f"Bearer {st.session_state['token']}"},
        )
        if response.status_code == 200:
            st.success("Todo deleted successfully")
            st.rerun()
        else:
            st.error("Failed to delete Todo")


def list_todos():
    st.header("Your Todos")
    col1, col2, col3, col4 = st.columns(
        [1, 2, 3, 2],
        gap="small",
    )
    response = requests.get(
        f"{BASE_URL}/todos/",
        headers={"Authorization": f"Bearer {st.session_state['token']}"},
    )
    if response.status_code == 200:
        todos = response.json()

        with col1:
            st.subheader("ID")

        with col2:
            st.subheader("Title")

        with col3:
            st.subheader("Description")

        with col4:
            st.subheader("Button")

        for todo in todos:
            # st.text(
            #     f"ID: {todo['id']} - Title: {todo['title']} - Description: {todo['description']}"
            # )
            with col1:
                st.markdown(todo["id"])

            with col2:
                st.markdown(todo["title"])

            with col3:
                st.markdown(todo["description"])

            with col4:
                delete_todo(todo["id"])


def main():
    st.title("Todo App")

    # User Authentication
    if "token" not in st.session_state:
        register_user()
        login_user()
    else:
        create_todo()
        st.divider()
        list_todos()


if __name__ == "__main__":
    main()
