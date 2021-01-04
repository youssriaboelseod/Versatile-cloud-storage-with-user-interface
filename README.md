# Versatile-cloud-storage-with-user-interface
About the project 👾  

The project is designed for remote storage of files and access to them from anywhere in the world. 🌐  

Principle of operation: 

👉 User opens the app.

👉 If the user does not have an account in the system, then he clicks on the registration button and is transferred to the registration page (redirection is implemented by the library - webbrowser)

👉 After successful registration, the user returns to the application and enters the login data (username and password) and then presses the Login button to authorize in the system (at this moment the program will receive the data entered by the user and send them to the server by POST, after which the server returns a response if the response status is "OK", then a local database is created in which the data entered by the user is saved, if the server returns the "ERR" status, the user will be shown the message "Invalid Username or Password") 

👉 If the user has not uploaded any files before, he will see two buttons "Upload file" and "Logout". The "Upload file" button is intended for uploading files (after clicking on it, a window will open for the user to select a file to upload, after choosing a POST server, the selected file will be sent by a request). The "Logout" button is designed to "log out" of the account (after clicking on it, the user will be transferred to the authorization page) 

👉 If the user has previously downloaded files, they will be displayed on the screen as a block, which includes: file name, file icon (depending on the file extension), "Download" button and "Delete" button. When you click on the "Download" button, a menu will open in which the user can select which directory the selected file will be downloaded to (a GET request will be sent to the server, and the server will return the requested file in response). Clicking the "Delete" button will delete the file    


The following technologies were used to implement the project: 

👉 PyQt5 - to implement the user interface.

👉 Django and addition to it DjangoRestFramework - to implement the server side of the project.

👉 Library Requests - for communication with a remote server by sending GET and POST requests to it.

👉 SQlite database - for local storage of user data, in particular login and password, for automatic authorization in the program.
