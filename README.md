Business Card OCR and Database Integration
Overview
This Python script is designed to extract information from business cards using Optical Character Recognition (OCR) and store the extracted data in a MySQL database. The script utilizes the Streamlit framework for creating a user interface, and it incorporates image processing libraries such as OpenCV and EasyOCR for text extraction. The extracted information is then segmented and stored in a Pandas DataFrame before being uploaded to the database.

Dependencies
pandas
numpy
streamlit
mysql-connector-python
st_aggrid
easyocr
PIL (Python Imaging Library)
base64
opencv-python
re (Regular Expressions)
Installation
Make sure you have Python installed on your system. You can install the required dependencies using pip:

bash
Copy code
pip install pandas numpy streamlit mysql-connector-python st_aggrid easyocr pillow opencv-python
Usage
Running the Script: Execute the Python script in your preferred environment (e.g., terminal, IDE).
Interface: Upon running the script, a Streamlit interface will be launched with three options: HOME, DISPLAY, and MODIFY.
HOME: Displays a welcome message.
DISPLAY: Allows users to upload a business card image for OCR processing.
MODIFY: Provides options to update or delete data from the database.
Displaying Business Card: In the DISPLAY section, users can upload an image of a business card. The script will then extract text from the image using OCR, segment the information, and display it in an editable grid.
Uploading to Database: After verifying and editing the extracted data, users can click the "UPLOAD TO DB" button to store the information in the MySQL database.
Modifying Database Entries: In the MODIFY section, users can choose to update or delete existing entries in the database.
Database Integration
The script connects to a MySQL database using the mysql-connector-python library.
It creates a table named BusinessCards to store information extracted from business cards.
The table schema includes fields for various details such as name, designation, mobile number, company name, email, website, address, and image (base64 encoded).
Data from the segmented DataFrame is uploaded to the database upon user confirmation.
Note
Ensure that MySQL is running on your system and accessible with the provided credentials.
Make sure to create a database named business_cards_db before running the script. If not, the script will create the database automatically.
Adjust database connection parameters (host, user, password) as per your MySQL configuration.
This script assumes a standard format for business cards and may require customization for different layouts or languages.
Author
Developed by Sarvan Kumar M
Email : soulsarvankumar007@gmail.com
License
This project is licensed under the MIT License.
