# ffcs-planner
VIT UNIVERSITY FFCS TIMETABLE PLANNER

VIT University is the only university which follows the fully flexible credit system.
In this system, every individual student has the freedom to choose which subjects he or she wants to study in the given semester.
It is an excelent system that gives student the freedom to decide what they want to learn, but oftenly, many students mess up during the registration period as they are not able to select a proper timetable comprising of the courses they want. Also, many times students are not satisfied with their timetables as the time slots are not convinient according to their needs.
So, in order to help every student make a steady timetable, I have tried to make a tool, which provides the student with all the possible timetables with their requested subjects included, so as to help them decide what slots to choose during the actual registration.

Right now, the project just makes the time-table but no data is shown to the user on which slot to take for which subject but that is the very next feature in pipeline for this project.

This is a Python-Django based web framework. The front-end basically BOOTSTRAP as of now. no additional css files have been included except for a necessary one.

Installation:

  Create a virtual environment(prefferd but not necessary).
  Pip install the following packages:
     django
     django-crispy-forms
     more-itertools
     pandas
     
  Go to command prompt and cd to the project directory.
  type:   py manage.py makemigrations
          py manage.py migrate
          py manage.py createsuperuser    (some additional inputs will be asked)
          py manage.py runserver
  Head to 127.0.0.1/
  Initially the databases are blank. We need to upload some data inorder to release results.
  go to 127.0.0.1/slot_up and upload 'slot list.csv' file provided in myapp folder.
  go to 127.0.0.1/teacher_up and upload a csv file with pattern as provided in 'teachers.csv' as example.
  go to 127.0.0.1/course_up and upload a csv file with pattern as provided in 'courses.csv' as example.
  go to 127.0.0.1/offer_up and upload a csv file with pattern as provided in 'offers.csv' as example.
  now we are all set to head to our home page to test the product.
          
