import streamlit as st
import streamlit_authenticator as stauth
import yaml

from streamlit_authenticator.utilities.hasher import Hasher
from st_pages import show_pages_from_config, hide_pages
from yaml.loader import SafeLoader


def user_info(config):
    df = []
    initial_data = config['credentials']['usernames']
    registered_user = initial_data.keys()
    for username, details in initial_data.items():
        entry = {'username':username}
        entry.update(details)
        df.append(entry)
    return df, registered_user

def input_password(edited_df, registered_user):
    for item in edited_df:
        if item['username'] not in registered_user:
            item['password'] = Hasher([item['password']]).generate()[0]
    return edited_df        

def update_config(df):
    new = dict()
    for item in df:
        val = item['username']
        item.pop('username')
        new[val] = item
    return new

def save_changes(df, config):
    new = update_config(df)
    config['credentials']['usernames'] = new
    with open('./config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
            
def main():
    with st.container(border=True):
        st.subheader("User Management", anchor=False)
        df, registered_user = user_info(config)
        
        edit_df = st.data_editor(df,column_order=['name', 'role', 'username', 'password'], 
                    column_config={'name': st.column_config.TextColumn(label='Name'),
                                    'role': st.column_config.SelectboxColumn(label='Role', options=['admin', 'mitra', 'taksonom lapangan', 'pengembang model']),
                                    'username': st.column_config.TextColumn(label='Username'),
                                    'password': st.column_config.TextColumn(label='Password')},
                        num_rows='dynamic', hide_index=True)
        edit_btn = st.button(label='Save Changes', key='unique edit button')
        if edit_btn:
            edit_df = input_password(edit_df, registered_user)
            save_changes(edit_df, config)
            st.rerun()


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
        # get role for authorize page access
        current_user = st.session_state['username']
        current_role = config['credentials']['usernames'][current_user]['role']
        st.session_state["role"] = current_role

        authenticator.logout(location='sidebar', key='logout user mgnt')
        show_pages_from_config()
        
        # hide pages based on role: only admin can access
        if st.session_state['role'] == 'admin':
            hide_pages([''])
            main()
        else:
            # prevent direct access from URL
            st.warning("You don't have access to this page")
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
