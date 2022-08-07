# Welcome to Note Up!
#### Created by: Dillon Blake

<hr>
Note Up is a dynamic note taking tool engineered specifically for STEM students. This project was born out of frustration while trying to take notes involving math and code on typical text editors. Note Up can be described as a markdown like language based around html and latex, but with an easy to use interface. The site comes pre loaded with keyboard shortcuts for common html tags and latex codes. For example, text can be easily highlighted then a simple press of control, alt, and h will surround the text with an h1 header. This increases efficiency as users don't need to type out lengthy html tags or latex codes. The shortcuts are also customizable. In addition, Note Up allows users to open code editors with syntax highlighting right in their notepad next to their html, latex, and other writing.

Note Up is simple to setup out of the box to run on a local server. For usage instructions, please see the help page within the site. Below, you will find instructions on how to start the app running

1. Navigate to the directory of Note Up
2. Run 
```
python manage.py makemigrations
```
3. Run
```
python manage.py migrate
```
4. Run
```
python manage.py runserver
```
5. Navigate to http://127.0.0.1:8000/accounts/login/

If you would like to enable Google authentication, please visit this tutorial and start from step 4: https://www.section.io/engineering-education/django-google-oauth/

## Known Issues
Note Up is still in early versions and is prone to bugs. At the time, there is no formal testing done beyond simple user interaction. In the future, it may be smart to write unit tests. Bellow are some of the main bugs:
* Notepad page scrolls to bottom when editing mid page, making it difficult to change something not at the bottom
* Sometimes, the application has trouble deciding if a user is typing an equation or if it should listen for html shortcuts
* There is no undo or redo function
* There is no good way to resize an image without hardcoding css into the editor