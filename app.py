import streamlit as st

st.set_page_config(page_title="SaleStack", layout="centered")

st.title("SaleStack")
st.subheader("Branch Sales & Payment Management System")

st.markdown("""
---

### Welcome

The SaleStack foundation is ready. This application will provide comprehensive sales and payment management across multiple branches.

**Current Status**: Foundation setup complete

**Next Phase**: Authentication, dashboard, and data entry features coming soon.

---
""")

st.info("Configure your MySQL database in `.env` and run the application to get started.")
