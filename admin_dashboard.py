import streamlit as st
import sqlite3
import pandas as pd
import hashlib

st.title("⚙️ Manage App & Preferences")
st.markdown("Configure your individual theme settings or, if authorized, manage the application user roster.")

st.divider()

# Role check for specific tabs
is_admin = st.session_state.get("role") == "admin"
current_user = st.session_state.get("username")

# --- Functions ---
def fetch_users():
    conn = sqlite3.connect("auth.db")
    df = pd.read_sql_query("SELECT username, email, role FROM users", conn)
    conn.close()
    return df

def get_username_list():
    df = fetch_users()
    return df['username'].tolist() if not df.empty else []

def get_user_details(username):
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email, role FROM users WHERE username=?", (username,))
    res = cursor.fetchone()
    conn.close()
    return res

def direct_register(username, email, password, role):
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    success = False
    try:
        cursor.execute("INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)", (username, hashed_pw, role, email))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        pass
    conn.close()
    return success

def edit_user(target_username, new_email, new_password, new_role):
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    success = False
    try:
        if new_password.strip() == "":
            # Update without altering password
            cursor.execute("UPDATE users SET email=?, role=? WHERE username=?", (new_email, new_role, target_username))
        else:
            # Update entirely
            hashed_pw = hashlib.sha256(new_password.encode()).hexdigest()
            cursor.execute("UPDATE users SET email=?, role=?, password=? WHERE username=?", (new_email, new_role, hashed_pw, target_username))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        pass
    conn.close()
    return success

def delete_user(target_username):
    # Protect against deleting the only admin 
    if target_username == "admin":
        return False
        
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username=?", (target_username,))
    conn.commit()
    conn.close()
    return True

def update_theme(username, color):
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET theme_color=? WHERE username=?", (color, username))
    conn.commit()
    conn.close()

# --- Layout ---
if is_admin:
    tab_view, tab_add, tab_edit, tab_del, tab_theme = st.tabs(["👁️ View Roster", "➕ Add User", "✏️ Edit Identity", "🗑️ Purge User", "🎨 App Theme"])
    
    with tab_view:
        st.subheader("Live System Access List")
        st.info("Rendered securely from actual SQLite Database.")
        df = fetch_users()
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab_add:
        st.subheader("+ Direct Console Generation")
        with st.form("admin_add_user", clear_on_submit=True):
            new_username = st.text_input("Designate Username")
            new_email = st.text_input("Designate Email Address")
            new_password = st.text_input("Assign Secure Password", type="password")
            new_role = st.selectbox("Designate Permission Logic", ["admin", "faculty", "student"], index=2)
            
            submit_add = st.form_submit_button("Force Registration")
            
            if submit_add:
                if not new_username or not new_email or not new_password:
                    st.error("Attributes cannot be empty!")
                else:
                    if direct_register(new_username, new_email, new_password, new_role):
                        st.success(f"Fully authorized `{new_username}` instantaneously with '{new_role}' clearance!")
                        st.rerun() 
                    else:
                        st.error("Database conflict. Username or Email already in active assignment.")

    with tab_edit:
        st.subheader("✏️ Overwrite Authentication Details")
        active_users = get_username_list()
        
        if len(active_users) > 0:
            target_edit = st.selectbox("Select User Profile to Edit:", active_users, key="edit_selector")
            
            current_email, current_role = get_user_details(target_edit)
            roles = ["admin", "faculty", "student"]
            r_index = roles.index(current_role) if current_role in roles else 2
            
            with st.form("admin_edit_user"):
                st.info(f"Currently modifying: **{target_edit}**")
                edit_email = st.text_input("Overwrite Email Address", value=current_email)
                edit_role = st.selectbox("Shift Permission Authority", roles, index=r_index)
                edit_password = st.text_input("Reset Password (Leave blank to keep current!)", type="password")
                
                submit_edit = st.form_submit_button("Commit Changes to Database")
                
                if submit_edit:
                    if not edit_email:
                        st.error("Email cannot be form-empty.")
                    else:
                        if edit_user(target_edit, edit_email, edit_password, edit_role):
                            st.success(f"Successfully modified credentials for `{target_edit}`!")
                            st.rerun()
                        else:
                            st.error("Error committing changes.")
        else:
            st.warning("No users available to edit.")

    with tab_del:
        st.subheader("🗑️ Permanently Terminate User")
        active_users_del = get_username_list()
        
        if len(active_users_del) > 0:
            target_del = st.selectbox("Select User Target:", active_users_del, key="del_selector")
            
            with st.form("admin_del_user"):
                st.warning(f"CAUTION: This will explicitly permanently destroy the `{target_del}` account.")
                submit_del = st.form_submit_button(f"Annihilate User '{target_del}'")
                
                if submit_del:
                    if delete_user(target_del):
                        st.success(f"Purged `{target_del}` from existence.")
                        st.rerun()
                    else:
                        st.error("Operation Denied. Cannot purge the primary root `admin` account.")
        else:
            st.warning("No users available.")
            
else:
    tab_theme = st.tabs(["🎨 App Theme"])[0]
    st.info("As a regular user, you have access to personalize your application theme. Core administrative tools are restricted to Admin roles.")

with tab_theme:
    st.subheader("🎨 Personalize Application Theme")
    st.markdown("Choose a primary color that suits your style. This will update buttons, accents, and highlights across the entire app.")
    
    current_theme = st.session_state.get("theme_color", "#2563eb")
    new_color = st.color_picker("Pick your accent color", current_theme)
    
    if st.button("Apply and Save Theme"):
        update_theme(st.session_state["username"], new_color)
        st.session_state["theme_color"] = new_color
        st.success("Theme preference saved! Refreshing interface...")
        st.rerun()
