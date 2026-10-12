import streamlit as st
from database.connection import get_db_connection

st.set_page_config(page_title="SaleStack", layout="centered")

st.title("SaleStack")
st.subheader("Branch Sales & Payment Management System")

st.markdown("""
---

### Database Connection Status
""")

try:
    connection = get_db_connection()
    if connection.is_connected():
        st.success("✓ Database connection successful")
        connection.close()
    else:
        st.error("✗ Database connection failed")
except Exception as e:
    st.error(f"✗ Connection error: {str(e)}")

st.markdown("""
---

### Welcome

The SaleStack foundation is ready. This application will provide comprehensive sales and payment management across multiple branches.

**Current Status**: Foundation setup complete with database connectivity

**Next Phase**: Authentication, dashboard, and data entry features coming soon.

---
""")

st.info("Configure your MySQL database in `.env` and run the application to verify connectivity.")
