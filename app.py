import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import mysql.connector as sql
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import easyocr as ocr
from PIL import Image
import base64
import cv2 as cv
import re

# creating pagesetup
st.set_page_config(page_title="project")
selected = option_menu(menu_title="PROJECT BIZCARD",
                       options=["HOME", "DISPLAY", "MODIFY"],
                       icons=["house", "tv", "server"],
                       menu_icon="menu-app",
                       default_index=0,
                       orientation="horizontal")
# intializing dictionary to store data
k = {"NAME": [],
     "DESIGNATION": [],
     "MOBILENO": [],
     "COMPANY NAME": [],
     "EMAILID": [],
     "WEBSITE": [],
     "AREA": [],
     "CITY": [],
     "STATE": [],
     "PINCODE": [],
     "IMAGE": []
     }
# connecting to sql
mydb = sql.connect(host="localhost",
                   user="your_user_name",
                   password="your_password",
                   database="your_database_name")
mycursor = mydb.cursor()
mycursor.execute("""CREATE TABLE IF NOT EXISTS BusinessCards(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    designation VARCHAR(255),
    mobile_no VARCHAR(255),
    company_name VARCHAR(255),
    email_id VARCHAR(255),
    website VARCHAR(255),
    area VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    pincode VARCHAR(255),
    image LONGBLOB)""")

# HOME PAGE
if selected == "HOME":
    st.title(" WELCOME TO BIZCARD")
    st.header("Click on Display to perform OCR  ")

# image uploader


# display page
if selected == "DISPLAY":
    image = st.sidebar.file_uploader(" UPLOAD A BUSINESS CARD", type=['.png', '.jpg', '.jpeg'])
    if image is not None:

        # display image
        # st.image(image,caption='Uploaded Business Card', use_column_width=True)

        # preprocessing image using opencv
        img = cv.imdecode(np.fromstring(image.read(), np.uint8), 1)
        images = Image.open(image)

        images1 = image.read()
        binarydata = base64.b64encode(images1).decode('utf-8')  # converting to binary format
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        with st.container():
            st.image([img], caption=["Original Image"], width=300)
            st.write("---")  # a line
            st.write("##")  # space

        # using ocr
        reader = ocr.Reader(['en'])
        x = reader.readtext(np.array(gray_img))

        # extracting data
        info = []
        font = []
        cmpnames = []
        for i in x:
            text = i[1]  # index 1 has the text
            info.append(text)

            bbox = i[0]  # index 0 has the coordinates of bounding box
            fontsize = (bbox[3][1] - bbox[0][1])
            font.append(fontsize)
            if fontsize >= 50:
                cmpnames.append(text)


        # function for information seggregation information

        def extraction(inf):
            r = []
            for ind, j in enumerate(inf):
                # to get name
                if ind == 0:
                    k["NAME"].append(j)
                # to get designation
                elif ind == 1:
                    k["DESIGNATION"].append(j)
                # to get mobile no
                elif '-' in j:
                    k["MOBILENO"].append(j)
                    if len(k["MOBILENO"]) > 1:
                        k["MOBILENO"] = ",".join(k["MOBILENO"])
                # to get email id
                elif '@' in j:
                    k["EMAILID"].append(j)
                # to get website
                elif "@" not in j:
                    if re.search(r'[a-zA-Z.]+\.?(com)', j):
                        website = ""
                        website += re.search(r'[a-zA-Z.]+\.?(com)', j).group()
                        if not website.lower().startswith("www."):
                            website = "www." + website
                        if website[-4:] != ".com":
                            website = website[:-3] + "." + website[-3:]
                        if 'wwW' in website:
                            website = website.replace('wwW', 'www')
                        k["WEBSITE"].append(website)

            # to get pincode
            for j in inf:
                if re.search(r'[a-zA-Z+\s]?\d{6}', j):
                    r = re.search(r'[a-zA-Z+\s]?\d{6}', j).group()
                    k["PINCODE"].append(r)
                # to get area
                elif re.match(r'123\s', j):
                    x = re.split(',', j)
                    if "St" not in x[0]:
                        x[0] += " St"
                    k["AREA"].append(x[0])
            # to get city
            for j in inf:
                s = ""
                itr1 = re.search(r'123\s[a-zA-Z]+\sSt\s*,*\s*([A-Za-z]+)?[,;]?([\sA-Za-z]+)?[,;]?', j)
                itr2 = re.findall(r'^[E].*,+', j)
                if itr1:
                    s = re.match(r'123\s[a-zA-Z]+\sSt\s*,*\s*([A-Za-z]+)?[;,]?([\sA-Za-z]+)?[,;]?', j).group(1)
                    k["CITY"].append(s)
                elif itr2:
                    s = re.match(r'^[E][a-zA-Z]*', j).group()
                    k["CITY"].append(s)
            # to get state
            for j in inf:
                itr1 = re.search(r'123\s[a-zA-Z]+\sSt\s*,*\s*([A-Za-z]+)?[,;]?([\sA-Za-z]+)?[,;]?', j)
                itr2 = re.search(r'([a-zA-Z]+)\s\d+', j)
                if itr1:
                    s = re.match(r'123\s[a-zA-Z]+\sSt\s*,*\s*([A-Za-z]+)?[;,]?([\sA-Za-z]+)?[,;]?', j).group(2)
                    if s is not None:
                        k["STATE"].append(s)
                elif itr2:
                    s = re.search(r'([a-zA-Z]+)\s\d+', j).group(1)
                    k["STATE"].append(s)

            # to get company name
            if k["NAME"][0] in cmpnames:
                cmpnames.remove(k["NAME"][0])
            if k["DESIGNATION"][0] in cmpnames:
                cmpnames.remove(k["DESIGNATION"][0])
            cmpname = " ".join(cmpnames)
            k["COMPANY NAME"].append(cmpname)
            k["IMAGE"].append(binarydata)


        # passing exracted info to seggregate required information
        extraction(info)


    # converting seggregated data into dataframe using pandas
    def create_df(data):
        df = pd.DataFrame(data)
        return df


    df = create_df(k)
    # AgGrid(df)
    st.markdown("<h1 style='text_align: center;'>EXTRACTED DATA</h1>", unsafe_allow_html=True)
    # Create AgGrid options
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=True, groupable=True)
    gridoptions = gd.build()
    ag_grid = AgGrid(df, gridOptions=gridoptions, editable=True)

    edited_df = ag_grid["data"]
    # adding extracted data to the database
    try:
        if st.button("UPLOAD TO DB", use_container_width=False):
            sql = """INSERT INTO BusinessCards(
                  name,
                  designation,
                  mobile_no,
                  company_name,
                  email_id,
                  website,
                  area,
                  city,
                  state,
                  pincode,
                  image
                  ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"""
            for index, row in edited_df.iterrows():
                val = (
                    row["NAME"],
                    row["DESIGNATION"],
                    row["MOBILENO"],
                    row["COMPANY NAME"],
                    row["EMAILID"],
                    row["WEBSITE"],
                    row["AREA"],
                    row["CITY"],
                    row["STATE"],
                    row["PINCODE"],
                    row["IMAGE"]
                )
            mycursor.execute(sql, val)
            st.success("successfully uploaded")
            mydb.commit()
            mycursor.close()
            mydb.close()
    except Exception as e:
        st.write("Please upload an image")

if selected == "MODIFY":
    # creating select box
    ud = st.selectbox("SELECT BELOW TO UPDATE OR DELETE ", ["UPDATE", "DELETE"], index=0)

    if ud == "UPDATE":

        # to retrieve data from a database
        mycursor.execute(
            "SELECT name,designation,mobile_no,company_name,email_id,website, area,city,state,pincode,id FROM BusinessCards")
        db = mycursor.fetchall()
        chnames = [i[0] for i in db]
        selename = st.selectbox("CHOOSE A PERSON TO UPDATE INFO", chnames)
        if selename:
            with st.form("update form"):
                mycursor.execute(
                    "SELECT designation,mobile_no,company_name,email_id,website, area,city,state,pincode FROM BusinessCards WHERE name=%s",
                    (selename,))
                extrinfo = mycursor.fetchone()
                # displaying choosen person info to read and update
                # id = st.text_input("Id", extrinfo[9])
                udesignation = st.text_input("DESIGNATION", extrinfo[0])
                umobile_no = st.text_input("MOBILENO", extrinfo[1])
                ucompany_name = st.text_input("COMPANY NAME", extrinfo[2])
                uemail_id = st.text_input("EMAILID", extrinfo[3])
                uwebsite = st.text_input("WEBSITE", extrinfo[4])
                uarea = st.text_input("AREA", extrinfo[5])
                ucity = st.text_input("CITY", extrinfo[6])
                ustate = st.text_input("STATE", extrinfo[7])
                upincode = st.text_input("PINCODE", extrinfo[8])
                upbutton = st.form_submit_button("UPLOAD TO DB")
                if upbutton:
                    sql1 = "UPDATE BusinessCards set  designation = %s, mobile_no = %s, company_name = %s, email_id = %s, website = %s, area = %s, city = %s, state = %s, pincode = %s WHERE name = %s"
                    val1 = (
                    udesignation, umobile_no, ucompany_name, uemail_id, uwebsite, uarea, ucity, ustate, upincode,
                    selename)
                    mycursor.execute(sql1, val1)
                    mydb.commit()
                    mycursor.close()
                    mydb.close()
                    st.success("database updated")

    if ud == "DELETE":

        # to retrieve data from a database
        mycursor.execute(
            "SELECT name,designation,mobile_no,company_name,email_id,website, area,city,state,pincode FROM BusinessCards")
        db = mycursor.fetchall()
        chnames1 = [i[0] for i in db]
        selename1 = st.selectbox("CHOOSE A PERSON TO DELETE INFO", chnames1)
        # to delete chosen person detail in db
        with st.form("delete form"):
            l = st.form_submit_button("DELETE")
            if l:
                sql2 = "DELETE FROM BusinessCards WHERE name=%s"
                val2 = [selename1]
                mycursor.execute(sql2, val2)
                mydb.commit()
                mycursor.close()
                mydb.close()
                st.success("info deleted")
