import streamlit as st
import pymysql


def defaultHome():
    try:
        my_css = """
                <style>
                    /* Target the .stButton>button element for button adjustments */
                    .stButton>button {
                        margin: 5px 10px;  /* Adjusted margin */
                        padding: 5px 10px; /* Adjusted padding */
                        width: 120px;      /* Adjusted width */
                        background-color: #4CAF50; /* Added background color */
                        color: white;               /* Added text color */
                        border: none;               /* Removed border */
                        border-radius: 5px;         /* Added border-radius */
                        cursor: pointer;
                        margin-right: 0px
                    }
                </style>
                """

        st.markdown(my_css, unsafe_allow_html=True)
        button_home, button_register, button_login = st.columns([1, 1, 1])
        with button_home:
            navBarHomeInHome = st.button('Home')
            if navBarHomeInHome:
                st.session_state.current_page = 'home'
                st.session_state.page = 'home'
                st.experimental_rerun()

        with button_register:
            navBarRegisterInHome = st.button('Register')
            if navBarRegisterInHome:
                st.session_state.current_page = 'register'
                st.session_state.page = 'register'
                st.experimental_rerun()
        with button_login:
            navBarLogin = st.button('Login')
            if navBarLogin:
                st.session_state.current_page = 'login'
                st.session_state.page = 'login'
                st.experimental_rerun()

    except Exception as e:
        print("In defaultHome:")
        raise Exception(e)


def defaultLogin(conn):
    my_css = """
            <style>
                    /* Target the .stButton>button element for button adjustments */
                    .stButton>button {
                        margin: 5px 10px;  /* Adjusted margin */
                        padding: 5px 10px; /* Adjusted padding */
                        width: 120px;      /* Adjusted width */
                        background-color: #4CAF50; /* Added background color */
                        color: white;               /* Added text color */
                        border: none;               /* Removed border */
                        border-radius: 5px;         /* Added border-radius */
                        cursor: pointer;

                    }
                    .stButton {
                        display: flex;
                        justify-content: flex-start;
                        }
                </style>
            """

    st.markdown(my_css, unsafe_allow_html=True)
    homeColInLogin, registerColInLogin = st.columns(2)

    with homeColInLogin:
        navBarHomeInLogin = st.button('Home')
        if navBarHomeInLogin:
            st.session_state.current_page = 'home'
            st.session_state.page = 'home'
            st.experimental_rerun()

    with registerColInLogin:
        navBarRegisterInLogin = st.button('Register')
        if navBarRegisterInLogin:
            st.session_state.current_page = 'register'
            st.session_state.page = 'register'
            st.experimental_rerun()

    try:
        print("In defaultLogin: ")
        print(st.session_state)

        loginPlaceholder = st.empty()
        loginSuccess = 0
        with loginPlaceholder.form("login"):
            st.title('Login')
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            login_button = st.form_submit_button("Login")
            print("u:", username)
            print("p:", password)
            if login_button:
                eQuery = f"SELECT * FROM user_details WHERE u_name = '{username}' AND pwd = '{password}'"
                print("QUERY: ", eQuery)
                user_data = runQuery(eQuery, conn)

                if user_data:
                    st.session_state.logged_in = True
                    st.session_state['username'] = username
                    st.success("Logged in successfully!")
                    st.experimental_rerun()

                else:
                    st.error('Invalid username or password. Please try again.')

    except Exception as e:
        print("In defaultLogin")
        raise Exception(e)


def runQuery(query, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    except pymysql.MySQLError as e:
        print(f"Error connecting to the MySQL Database: {e}")
        return None


def defaultRegister(conn):
    try:
        custom_css = """
                    <style>
                        /* Target the .stButton>button element for button adjustments */
                    .stButton>button {
                        margin: 5px 10px;  /* Adjusted margin */
                        padding: 5px 10px; /* Adjusted padding */
                        width: 120px;      /* Adjusted width */
                        background-color: #4CAF50; /* Added background color */
                        color: white;               /* Added text color */
                        border: none;               /* Removed border */
                        border-radius: 5px;         /* Added border-radius */
                        cursor: pointer;

                    }
                    .stButton {
                        display: flex;
                        justify-content: flex-start;
                        }
                    </style>
                    """

        st.markdown(custom_css, unsafe_allow_html=True)
        homeCol, registerCol, loginCol = st.columns(3)
        with homeCol:
            navBarHomeInRegister = st.button('Home')
            if navBarHomeInRegister:
                st.session_state.current_page = 'home'
                st.session_state.page = 'home'
                st.experimental_rerun()

        with loginCol:
            navBarLoginInRegister = st.button('Login')
            if navBarLoginInRegister:
                st.session_state.current_page = 'login'
                st.session_state.page = 'login'
                st.experimental_rerun()
        register = 0
        placeholder = st.empty()
        with placeholder.form("register"):
            st.title('Register')
            f_name = st.text_input('First Name')
            l_name = st.text_input('Last Name')
            email = st.text_input('Email')
            userName = st.text_input('User Name')
            password = st.text_input('Password', type='password')
            confirm_password = st.text_input('Confirm Password', type='password')
            registerButton = st.form_submit_button("Register")

            if registerButton:

                existing_user = runQuery(f"SELECT * FROM user_details WHERE u_name = '{userName}'", conn)
                if not (f_name or l_name or email or userName or password or confirm_password):
                    st.error('All fields are mandatory. Please fill in all required information.')
                    return

                elif password != confirm_password:
                    st.error('Passwords do not match. Please enter matching passwords.')
                    return

                elif existing_user:
                    st.error('Username already exists. Please choose a different username.')
                    return

                else:
                    sql = "INSERT INTO user_details (u_name, f_name, l_name, mail_id, pwd) VALUES (%s, %s, %s, %s, %s)"
                    with conn.cursor() as cursor:
                        cursor.execute(sql, (userName, f_name, l_name, email, password))
                    conn.commit()
                    st.success('Registered!')
                    register = 1
                    st.session_state['current_page'] = 'LoggedIn'
                    st.session_state['f_name'] = f_name
                    st.session_state['l_name'] = l_name
                    st.session_state['email'] = email
                    st.session_state['registered'] = True
                    placeholder.empty()
        if register == 1:
            registrationDone(conn)
    except Exception as e:
        print("In defaultRegister")
        raise Exception(e)


def loginSuccess(conn):
    try:
        custom_css = """
                    <style>
                        .stButton>button {
                        margin: 5px 10px;  /* Adjusted margin */
                        padding: 5px 10px; /* Adjusted padding */
                        width: 120px;      /* Adjusted width */
                        background-color: #4CAF50; /* Added background color */
                        color: white;               /* Added text color */
                        border: none;               /* Removed border */
                        border-radius: 5px;         /* Added border-radius */
                        cursor: pointer;

                    }
                    .stButton {
                        display: flex;
                        justify-content: flex-start;
                        }
                    </style>
                    """

        st.markdown(custom_css, unsafe_allow_html=True)
        homeColInFileUpload, registerColInFileUpload = st.columns(2)

        with homeColInFileUpload:
            navBarHomeInFileUpload = st.button('Home')
            if navBarHomeInFileUpload:
                st.session_state.current_page = 'home'
                st.session_state.page = 'home'
                st.experimental_rerun()

        with registerColInFileUpload:
            navBarRegisterInFileUpload = st.button('Register')
            if navBarRegisterInFileUpload:
                st.session_state.current_page = 'register'
                st.session_state.page = 'register'
                st.session_state.logged_in = False
                st.session_state.registered = False
                st.experimental_rerun()
        st.title("Login Page")
        fetchUserDetailsQuery = f"SELECT f_name, l_name, mail_id FROM user_details WHERE u_name = '{st.session_state.username}'"
        getUserContentQuery = f"""SELECT 
        content.info
    FROM
       user_details user_tbl
    LEFT JOIN
        file_data content
    ON
        user_tbl.u_name=content.u_name
    WHERE
        user_tbl.u_name='{st.session_state.username}'
        """
        data = runQuery(fetchUserDetailsQuery, conn)
        contentData = runQuery(getUserContentQuery, conn)
        st.write("First Name: " + data[0]['f_name'])
        st.write("Last Name: " + data[0]['l_name'])
        st.write("Email: " + data[0]['mail_id'])
        if st.button('Log out'):
            st.session_state.logged_in = False
            st.session_state.registered = False
            st.experimental_rerun()

    except Exception as e:
        raise Exception(e)


def registrationDone(conn):
    st.title("Successfully Registered.")
    welcomeMessage = 'Welcome {}'.format(st.session_state.f_name)
    st.title(welcomeMessage)
    st.write("First Name: " + st.session_state.f_name)
    st.write("Last Name: " + st.session_state.l_name)
    st.write("Email: " + st.session_state.email)
    st.session_state['current_page'] = 'register'
    login_button_sr = st.button("Go to Login")
    if login_button_sr:
        st.write(st.session_state)
        st.session_state.registered = True
        st.session_state.page = 'login'
        st.session_state.current_page = 'login'
        st.experimental_rerun()


def dbConnect():
    try:
        host = "cc-database.ch42qosgkjz3.us-east-2.rds.amazonaws.com"  
        user = "admin"  
        password = "Shiva2000"  
        db = "cloud" 
        conn = pymysql.connect(host=host,
                                     user=user,
                                     password=password,
                                     database=db,
                                     cursorclass=pymysql.cursors.DictCursor)
        print("Successfully connected to the database.")
        return conn
    except Exception as e:
        print("In Database conn: ")
        raise Exception(e)


conn = dbConnect()
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'registered' not in st.session_state:
    st.session_state['registered'] = False


if st.session_state.page == 'home':
    st.session_state['current_page'] = 'home'
    defaultHome()
elif st.session_state.page == 'login':
    st.session_state['current_page'] = 'login'
    if not st.session_state.logged_in:
        defaultLogin(conn)
    else:
        loginSuccess(conn)
elif st.session_state.page == 'register':
    st.session_state['current_page'] = 'register'
    if not st.session_state.registered:
        defaultRegister(conn)
    else:
        st.session_state['current_page'] = 'login'
        st.session_state['page'] = 'login'
        defaultLogin(conn)