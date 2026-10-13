import streamlit as st
from datetime import date
from database.auth import authenticate_user
from database.sales import get_branches, get_sales_summary, get_sales, insert_sale
from database.payments import get_sale_details, get_payment_history, insert_payment, get_payment_method_summary
from database.reports import get_pending_collection_percentage, get_branch_performance, get_sales_by_status

st.set_page_config(page_title="SaleStack", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "selected_branch" not in st.session_state:
    st.session_state.selected_branch = None


def logout():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.branch_id = None
    st.session_state.selected_branch = None


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
                    error_msg = str(e)
                    if "Database connection failed" in error_msg:
                        st.error("Database connection error. Please check your configuration.")
                    elif "Authentication error" in error_msg:
                        st.error("Authentication failed. Contact administrator.")
                    else:
                        st.error("An error occurred during login. Please try again.")

else:
    with st.sidebar:
        st.markdown("### Account")
        st.markdown(f"**User:** {st.session_state.username}")
        st.markdown(f"**Role:** {st.session_state.role}")
        
        if st.session_state.role == "Super Admin":
            st.markdown("---")
            st.markdown("### Filter")
            branches = get_branches()
            branch_options = {b['branch_id']: b['branch_name'] for b in branches}
            
            selected_id = st.selectbox(
                "Select Branch",
                options=[None] + list(branch_options.keys()),
                format_func=lambda x: "All Branches" if x is None else branch_options.get(x, ""),
                key="branch_filter"
            )
            st.session_state.selected_branch = selected_id
        
        st.markdown("---")
        if st.button("Logout", key="logout_btn", use_container_width=True):
            logout()
            st.rerun()
    
    st.title("SaleStack")
    st.subheader("Branch Sales & Payment Management System")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Sales Records", "Add Sale", "Payments", "Reports"])
    
    with tab1:
        st.markdown("### Sales Summary")
        
        try:
            if st.session_state.role == "Super Admin":
                summary = get_sales_summary("Super Admin", st.session_state.selected_branch)
            else:
                summary = get_sales_summary("Admin", st.session_state.branch_id)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Sales", summary['total_sales'] or 0)
            with col2:
                st.metric("Total Gross Sales", f"₹{summary['total_gross'] or 0:,.2f}")
            with col3:
                st.metric("Total Received", f"₹{summary['total_received'] or 0:,.2f}")
            with col4:
                st.metric("Total Pending", f"₹{summary['total_pending'] or 0:,.2f}")
        
        except Exception as e:
            st.error("Error loading sales summary")
        
        st.markdown("---")
        st.markdown("### Sales Records")
        
        try:
            if st.session_state.role == "Super Admin":
                sales = get_sales("Super Admin", selected_branch=st.session_state.selected_branch)
            else:
                sales = get_sales("Admin", branch_id=st.session_state.branch_id)
            
            if sales:
                display_data = []
                for sale in sales:
                    display_data.append({
                        "Sale ID": sale['sale_id'],
                        "Date": sale['date'],
                        "Branch": sale['branch_name'],
                        "Customer": sale['name'],
                        "Mobile": sale['mobile_number'],
                        "Product": sale['product_name'],
                        "Gross Sales": f"₹{sale['gross_sales']:,.2f}",
                        "Received": f"₹{sale['received_amount']:,.2f}",
                        "Pending": f"₹{sale['pending_amount']:,.2f}",
                        "Status": sale['status']
                    })
                
                st.dataframe(display_data, use_container_width=True, hide_index=True)
            else:
                st.info("No sales records found")
        
        except Exception as e:
            st.error("Error loading sales records")
    
    with tab2:
        st.markdown("### Add New Sale")
        
        try:
            branches = get_branches()
            
            with st.form("add_sale_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    sale_date = st.date_input("Date", value=date.today())
                    customer_name = st.text_input("Customer Name")
                    mobile = st.text_input("Mobile Number")
                
                with col2:
                    product = st.selectbox("Product", ["DS", "DA", "BA", "FSD"])
                    gross_sales = st.number_input("Gross Sales (₹)", min_value=0.0, step=100.0)
                    status = st.selectbox("Status", ["Open", "Close"])
                
                if st.session_state.role == "Super Admin":
                    branch_options = {b['branch_id']: b['branch_name'] for b in branches}
                    selected_branch_id = st.selectbox(
                        "Branch",
                        options=list(branch_options.keys()),
                        format_func=lambda x: branch_options[x]
                    )
                else:
                    selected_branch_id = st.session_state.branch_id
                    branch_name = next((b['branch_name'] for b in branches if b['branch_id'] == selected_branch_id), "Unknown")
                    st.info(f"Your assigned branch: **{branch_name}**")
                
                submit = st.form_submit_button("Add Sale", use_container_width=True)
                
                if submit:
                    errors = []
                    
                    if not customer_name or not customer_name.strip():
                        errors.append("Customer name is required")
                    if not mobile or not mobile.strip():
                        errors.append("Mobile number is required")
                    if gross_sales <= 0:
                        errors.append("Gross sales must be greater than zero")
                    if not product:
                        errors.append("Product must be selected")
                    if not sale_date:
                        errors.append("Date is required")
                    
                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        try:
                            insert_sale(
                                selected_branch_id,
                                sale_date,
                                customer_name.strip(),
                                mobile.strip(),
                                product,
                                gross_sales,
                                status
                            )
                            st.success("Sale added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error("Error adding sale. Please try again.")
        
        except Exception as e:
            st.error("Error loading form data")
    
    with tab3:
        st.markdown("### Payment Management")
        
        try:
            if st.session_state.role == "Super Admin":
                sales = get_sales("Super Admin", selected_branch=st.session_state.selected_branch)
            else:
                sales = get_sales("Admin", branch_id=st.session_state.branch_id)
            
            if not sales:
                st.info("No sales available for payments")
            else:
                sales_options = {s['sale_id']: f"ID: {s['sale_id']} | {s['name']} | ₹{s['gross_sales']:,.0f}" for s in sales}
                selected_sale_id = st.selectbox(
                    "Select Sale",
                    options=list(sales_options.keys()),
                    format_func=lambda x: sales_options[x]
                )
                
                if selected_sale_id:
                    try:
                        sale = get_sale_details(selected_sale_id, st.session_state.role, st.session_state.branch_id)
                        
                        if not sale:
                            st.error("Sale not found or access denied")
                        else:
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Gross Sales", f"₹{sale['gross_sales']:,.2f}")
                            with col2:
                                st.metric("Received", f"₹{sale['received_amount']:,.2f}")
                            with col3:
                                st.metric("Pending", f"₹{sale['pending_amount']:,.2f}")
                            with col4:
                                st.metric("Status", sale['status'])
                            
                            st.markdown("---")
                            st.markdown("#### Payment History")
                            
                            payments = get_payment_history(selected_sale_id)
                            
                            if payments:
                                payment_data = []
                                for payment in payments:
                                    payment_data.append({
                                        "Payment ID": payment['payment_id'],
                                        "Date": payment['payment_date'],
                                        "Amount": f"₹{payment['amount_paid']:,.2f}",
                                        "Method": payment['payment_method']
                                    })
                                st.dataframe(payment_data, use_container_width=True, hide_index=True)
                            else:
                                st.info("No payments recorded for this sale")
                            
                            st.markdown("---")
                            st.markdown("#### Add Payment")
                            
                            with st.form("add_payment_form"):
                                payment_date = st.date_input("Payment Date", value=date.today())
                                amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
                                method = st.selectbox("Payment Method", ["Cash", "UPI", "Card"])
                                submit = st.form_submit_button("Record Payment", use_container_width=True)
                                
                                if submit:
                                    errors = []
                                    
                                    if not payment_date:
                                        errors.append("Payment date is required")
                                    if amount <= 0:
                                        errors.append("Amount must be greater than zero")
                                    if method not in ["Cash", "UPI", "Card"]:
                                        errors.append("Invalid payment method")
                                    
                                    max_payment = sale['pending_amount']
                                    if amount > max_payment:
                                        errors.append(f"Amount cannot exceed pending amount (₹{max_payment:,.2f})")
                                    
                                    if errors:
                                        for error in errors:
                                            st.error(error)
                                    else:
                                        try:
                                            insert_payment(selected_sale_id, payment_date, amount, method)
                                            st.success("Payment recorded successfully!")
                                            st.rerun()
                                        except Exception as e:
                                            st.error("Error recording payment. Please try again.")
                    
                    except Exception as e:
                        st.error("Error loading sale details")
        
        except Exception as e:
            st.error("Error loading payment interface")
        
        st.markdown("---")
        st.markdown("### Payment Method Summary")
        
        try:
            if st.session_state.role == "Super Admin":
                summary = get_payment_method_summary("Super Admin", selected_branch=st.session_state.selected_branch)
            else:
                summary = get_payment_method_summary("Admin", branch_id=st.session_state.branch_id)
            
            if summary:
                summary_data = []
                for item in summary:
                    summary_data.append({
                        "Method": item['payment_method'],
                        "Total": f"₹{item['total_amount']:,.2f}"
                    })
                
                col1, col2, col3 = st.columns(3)
                for idx, item in enumerate(summary):
                    if idx == 0:
                        with col1:
                            st.metric(f"{item['payment_method']}", f"₹{item['total_amount']:,.2f}")
                    elif idx == 1:
                        with col2:
                            st.metric(f"{item['payment_method']}", f"₹{item['total_amount']:,.2f}")
                    elif idx == 2:
                        with col3:
                            st.metric(f"{item['payment_method']}", f"₹{item['total_amount']:,.2f}")
            else:
                st.info("No payment data available")
        
        except Exception as e:
            st.error("Error loading payment method summary")
    
    with tab4:
        st.markdown("### Financial Reports & Analytics")
        
        try:
            if st.session_state.role == "Super Admin":
                pending_pct = get_pending_collection_percentage("Super Admin", selected_branch=st.session_state.selected_branch)
            else:
                pending_pct = get_pending_collection_percentage("Admin", branch_id=st.session_state.branch_id)
            
            col1, col2, col3 = st.columns(3)
            
            if st.session_state.role == "Super Admin":
                summary = get_sales_summary("Super Admin", st.session_state.selected_branch)
            else:
                summary = get_sales_summary("Admin", st.session_state.branch_id)
            
            with col1:
                st.metric("Collection Rate", f"{100 - pending_pct:.1f}%")
            with col2:
                st.metric("Pending Collection %", f"{pending_pct:.1f}%")
            with col3:
                if summary['total_gross'] and summary['total_received']:
                    avg_per_sale = summary['total_received'] / summary['total_sales'] if summary['total_sales'] > 0 else 0
                    st.metric("Avg Received/Sale", f"₹{avg_per_sale:,.0f}")
        
        except Exception as e:
            st.error("Error loading financial metrics")
        
        st.markdown("---")
        st.markdown("### Branch Performance Summary")
        
        try:
            if st.session_state.role == "Super Admin":
                performance = get_branch_performance("Super Admin", selected_branch=st.session_state.selected_branch)
            else:
                performance = get_branch_performance("Admin", branch_id=st.session_state.branch_id)
            
            if performance:
                perf_data = []
                for branch in performance:
                    perf_data.append({
                        "Branch": branch['branch_name'],
                        "Sales": branch['total_sales'] or 0,
                        "Revenue": f"₹{branch['total_revenue'] or 0:,.0f}",
                        "Collected": f"₹{branch['total_collected'] or 0:,.0f}",
                        "Pending": f"₹{branch['total_pending'] or 0:,.0f}",
                        "Collection Rate": f"{branch['collection_rate'] or 0:.1f}%"
                    })
                st.dataframe(perf_data, use_container_width=True, hide_index=True)
            else:
                st.info("No branch performance data available")
        
        except Exception as e:
            st.error("Error loading branch performance")
        
        st.markdown("---")
        st.markdown("### Sales by Status")
        
        try:
            if st.session_state.role == "Super Admin":
                status_data_raw = get_sales_by_status("Super Admin", selected_branch=st.session_state.selected_branch)
            else:
                status_data_raw = get_sales_by_status("Admin", branch_id=st.session_state.branch_id)
            
            if status_data_raw:
                status_data = []
                for item in status_data_raw:
                    status_data.append({
                        "Status": item['status'],
                        "Total Sales": item['total_sales'],
                        "Gross Sales": f"₹{item['total_gross_sales'] or 0:,.0f}",
                        "Received": f"₹{item['total_received'] or 0:,.0f}",
                        "Pending": f"₹{item['total_pending'] or 0:,.0f}"
                    })
                st.dataframe(status_data, use_container_width=True, hide_index=True)
            else:
                st.info("No sales status data available")
        
        except Exception as e:
            st.error("Error loading sales by status")
