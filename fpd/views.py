from django.shortcuts import render
from django.shortcuts import render
import numpy as np
import tweepy
from keras.models import model_from_json
from numpy.random import seed
from django.http import HttpResponse
from django.views.generic import View
import instaloader
Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAKWjjQEAAAAAsOVpA5youCKrglMHuvoSa8rmsnI%3DNx2ixggog1OJQreK7xCgdp0lyCrpZD9QkajBQDAjensrL8fQOb"
seed(1)

#L = instaloader.Instaloader()

# Enter Instagram Account credentials In order to get Instagram Data

#user = "valorant.pointshop"
#password = "keval6946"
#L.login(user, password)

def Index(request):
    return render(request,"fpd/detect.html")


def Detect(request):
    status = int(request.POST['status'])
    followers = int(request.POST['followers'])
    friends = int(request.POST['friends'])
    fav = int(request.POST['fav'])
    lang_num = int(request.POST['lang_num'])
    listed_count = int(request.POST['listed_count'])
    geo = int(request.POST['geo'])
    pic = int(request.POST['pic'])
    json_file = open('fpd/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("fpd/model.h5")
    featuress = np.array([[status,followers,friends,fav,lang_num,listed_count,geo,pic]])
    prediction = loaded_model.predict(featuress)
    prediction = prediction[0]
    print('Prediction\n',prediction)
    print('\nThresholded output\n',(prediction>0.5)*1)
    if ((prediction>0.5)*1)==1:
        result="The Profile is Fake"
    else:
        result="The Profile is real"
    print(result)
 
    msg=result
    return render(request,'fpd/detect.html',{'msg':msg})







def tweet(request):
    return render(request,'fpd/twitter.html')


def twitter(request):

    inputusername1= str(request.POST['inputusername'])
    inputusername2 = inputusername1.removeprefix('https://twitter.com/')
    inputusername3 = inputusername2.removeprefix('http://twitter.com/')
    inputusername= inputusername3.removeprefix('twitter.com/')


    
    def getClient():
        client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAKWjjQEAAAAAsOVpA5youCKrglMHuvoSa8rmsnI%3DNx2ixggog1OJQreK7xCgdp0lyCrpZD9QkajBQDAjensrL8fQOb')
        return client
    def getUserInfo(client,username):
        user = client.get_user(username=username,user_fields='public_metrics,location,pinned_tweet_id,profile_image_url')
        return user

    client = getClient()
    d =getUserInfo(client,inputusername)
    public_metrics= d.data.public_metrics
    status= int(d.data.public_metrics['tweet_count'])
    followers= int(d.data.public_metrics['followers_count'])
    friends= int(d.data.public_metrics['following_count'])
    fav= str(d.data.pinned_tweet_id)
    if fav == 'None':
        fav = int(friends/3-7)
    else:
        fav = int(friends/2+3)
    lang_num= int(5)
    listed_count= int(d.data.public_metrics['listed_count'])
    geo= str(d.data.location)
    if geo == 'None':
        geo = int(0)
    else:
        geo = int(1)
    pic= d.data.profile_image_url
    if pic == 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png':
        pic = int(0)
    else:
        pic = int(1)
    twitteruserdata = np.array([[status,followers,friends,fav,lang_num,listed_count,geo,pic]])
    # print(twitteruserdata)
    json_file = open('fpd/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("fpd/model.h5")
    prediction = loaded_model.predict(twitteruserdata)
    prediction = prediction[0]
    print('Prediction\n',prediction)
    print('\nThresholded output\n',(prediction>0.5)*1)
    if ((prediction>0.5)*1)==1:
        result="The Profile is Fake"
    else:
        result="The Profile is real"
    print(result)
    msg=result
    return render(request,'fpd/twitter.html',{'msg':msg})






def insta(request):
    return render(request,'fpd/instagram.html')

def instagram(request):

    inputusername1= str(request.POST['inputusername'])
    inputusername2 = inputusername1.removesuffix('/')
    inputusername3 = inputusername2.removeprefix('https://instagram.com/')
    inputusername4 = inputusername3.removeprefix('http://instagram.com/')
    inputusername= inputusername4.removeprefix('instagram.com/')

    profile = instaloader.Profile.from_username(L.context, inputusername)

    status = int(profile.mediacount)
    followers = int(profile.followers)
    friends = int(profile.followees)
    fav = int(profile.has_viewable_story) 
    lang_num = int(5)
    if fav == 1:
        listed_count = int(friends/3-7)
    else:
        listed_count = int(friends/2+3)
    geo = int(0)
    pic = int(1)
    instauserdata = np.array([[status,followers,friends,fav,lang_num,listed_count,geo,pic]])
    json_file = open('fpd/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("fpd/model.h5")
    prediction = loaded_model.predict(instauserdata)
    prediction = prediction[0]
    print('Prediction\n',prediction)
    print('\nThresholded output\n',(prediction>0.5)*1)
    if ((prediction>0.5)*1)==1:
        result="The Profile is Fake"
    else:
        result="The Profile is real"
    print(result)
    msg=result
    return render(request,'fpd/instagram.html',{'msg':msg})
