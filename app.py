import streamlit as st
from database.auth import authenticate_user

st.set_page_config(page_title="SaleStack", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def logout():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.branch_id = None


if not st.session_state.logged_in:
    st.title("SaleStack")
    st.subheader("Branch Sales & Payment Management System")
    
    st.markdown("---")
    
    with st.form("login_form"):
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                try:
                    user = authenticate_user(username, password)
                    
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user['user_id']
                        st.session_state.username = user['username']
                        st.session_state.role = user['role']
                        st.session_state.branch_id = user['branch_id']
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                
                except Exception as e:
                    st.error("An error occurred during login. Please try again.")

else:
    st.title("SaleStack")
    st.subheader("Branch Sales & Payment Management System")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### Welcome, {st.session_state.username}")
        st.markdown(f"**Role:** {st.session_state.role}")
    
    with col2:
        if st.button("Logout", key="logout_btn"):
            logout()
            st.rerun()
    
    st.markdown("---")
    
    st.info("Dashboard and features coming soon.")
