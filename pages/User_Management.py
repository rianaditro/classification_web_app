import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


with open('config.yaml') as f:
        config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'])

with st.form("user_management"):
    st.subheader("User Management", anchor=False)


if __name__ == "__main__":
    # the authentication start here
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'])

    authenticator.login()

    if st.session_state["authentication_status"]:
        current_user = st.session_state['username']
        current_role = config['credentials']['usernames'][current_user]['role']
        st.session_state["role"] = current_role
        if st.session_state["role"] == 'admin':
            authenticator.logout(location='sidebar')
            # main()
            st.write("Login as admin")
        else:
            st.warning("You don't have access this page")
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
