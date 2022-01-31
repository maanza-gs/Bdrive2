# Bdrive2
BashDrive or BDrive

BDrive is a simple blob storage system where user can store any kind of data and share it with their peers.
Users can also download,rename,delete existing files or upload new files to their account.

FEATURES

1) Authentication:
	we supply our email and password once to the API and the API  responds back with a long string/token which is stored by our browsers. 
  The next time when we click on another resource that requires login, the browser will send back the token and the server would be able to identify the user.
  So as to extract the token from an HttpOnly cookie. HttpOnly cookies can't be accessed by javascript. 
  So, any client-side malicious javascript would not be able to access the cookie data and our application with be more secure. 


2) Apllication
  The features of the application are listed below.
	
	Upload Multiple files.
	List All files of current user.
	Delete a particular file.
	Share the file with other user.
	Rename a file.
  
	  
3) Web Based UI

Simple User friendly interface.
It is a Single Page Application.
Jinja2 and form are the backend tools.
Html used for frontend.
  
4) Sharing

User can share their resource to their fellow Bdrive users.

5) Deployment

Heroku is used.
  
	https://bashdrive.herokuapp.com/
