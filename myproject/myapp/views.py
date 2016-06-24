# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm

from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
sys.path.append("/home/ubuntu/code/tutorial/GCloud")
from max_goggle import visual_engine 

SYSTEM_IP = "http://54.254.219.1"
PORT_NUM = ":8080/"

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            imagePath = newdoc.docfile.path 
            imageName = imagePath.split('/')[-1]
            resourcePath = SYSTEM_IP+PORT_NUM+imageName
            result = visual_engine(imagePath)
            faceAnnotations, labelAnnotations, landmarkAnnotations, textAnnotations = result['responses'][:4]
            face_found = faceAnnotations != {}
            landmark_found = landmarkAnnotations != {}
            text_found = textAnnotations != {}

            htmlBody = ""
            
            if True:
                """Every image will have a label"""
                labels = labelAnnotations['labelAnnotations']
                htmlBody+="<br>Goggly's insights... <ul>"
                for label in labels:
                    htmlBody+="<li>Goggly says (with <i>{0:.2f}%</i> confidence that) the image is about <b>{1}</b>.</li>".format(label['score']*100.0,label['description'])
                htmlBody+="</ul>"
            if face_found:
                htmlBody+="<h3> Faces... </h3>"
                faces = faceAnnotations['faceAnnotations']
                htmlBody+= "Goggly found <b>{0} face{1}</b>.<br>".format(len(faces), '' if len(faces)==1 else 's')

                for i,face in enumerate(faces):
                    headwearLikelihood = face['headwearLikelihood'] == 'VERY_LIKELY'
                    htmlBody+="<br>Goggly says, Face {0} is <b>{1}</b> wearing something on the head!".format(i+1, '' if headwearLikelihood else 'not')
                    sorrowLikelihood, surpriseLikelihood, angerLikelihood, joyLikelihood = face['sorrowLikelihood']=='VERY_LIKELY', face['surpriseLikelihood']=='VERY_LIKELY',['angerLikelihood']=='VERY_LIKELY',face['joyLikelihood']=='VERY_LIKELY'
                    htmlBody+= "<br>Emotion analysis of Face {0}. <b>{1}</b> <b>{2}</b> <b>{3}</b> <b>{4}</b> <i>{5}</i><hr>".format(i+1, 'Happy :)' if joyLikelihood else '', 'Sad :( ' if sorrowLikelihood else '', 'Suprised :O' if surpriseLikelihood else '','Angry >:[' if angerLikelihood else '', '' if angerLikelihood or surpriseLikelihood or joyLikelihood or sorrowLikelihood else 'Neutral Expression')
                     
            if landmark_found:
                htmlBody+="<h4>Location found</h4>"
                for landmark in landmarkAnnotations['landmarkAnnotations']:
                    htmlBody+="Goggly says with <i>{0:.2f}%</i> confidence that the image is taken in <b>{1}</b>!<hr>".format(landmark['score']*100.0,landmark['description'])
            

            if text_found:
                htmlBody+="<h4>Goggly found some text!</h4>"
                text = textAnnotations['textAnnotations'][0]
                htmlBody+="\"<i>{0}</i>.\"".format(text['description'])
            
#            htmlBody+="<hr><hr>For data lovers, the entire JSON response from the image is available below!<hr><br>"
#            htmlBody+=str(result)
            htmlBody+="<footer> <p>Designed by: <b>Sivaraman (@ShivaSitaraman) </b> Contact information: <a href=\"mailto:kssivaraman1993@gmail.com\">kssivaraman1993@gmail.com</a></p></footer>"
            backButton="<a href=\""+SYSTEM_IP+":8000\">Back</a>"
            htmlBody+=backButton
            aboutMe = "<center><a target=_blank href=\"https://www.quora.com/profile/Shiva-Sitaraman/answers?sort=views\"><img src=\"https://assets.about.me/background/users/s/i/v/sivaramanks_1466757065_62.jpg\" width=200,height=200><br><h3>About Me</h3></a></center>"

            htmlBody+=aboutMe

            return HttpResponse("<html><head><title>Goggly saw...</title></head><body> <hr><img src="+resourcePath+" alt=\"This server messes up the file name\" width=200,height=200> "+htmlBody+"</body></html>")
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
