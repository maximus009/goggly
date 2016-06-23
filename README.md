# MAX Goggle: goggly

Goggly was programmed using Google Cloud Vision API, to extract as much information from a given image. Designed as a "Hyper-Crude" web app with a nearly crappy UI by an average web-designer (that's me); but a humble attempt to let people know of the advancements in Computer Vision and Deep Learning! So please, do try it out and let me know of your feedback.

Developed on Django 1.8.

Instructions to use it:
<code>$ sudo pip install django==1.8</code><br>
<code>$ git clone https://github.com/maximus009/goggly.git</code><br>
<code>$ cd goggly</code><br>
<code>$ python manage.py migrate<br>
      $ python manage.py runserver </code>

Have not included the python file that makes the Cloud Vision calls to the API (for security reasons). Please edit the "myproject/myapp/views.py" accordingly, before launching the app.

DISCLAIMER: Not really developed for distributive purposes;; Just on an experinmental basis. Peace!
