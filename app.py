from flask import Flask, render_template, request,send_from_directory, jsonify

application = Flask(__name__)

# from scripts import helper
import requests


#this library to resize images
from PIL import Image

import json

import time
import datetime
import os
import pickle
import pandas as pd

#this part for downloading images in a azipped folder
import shutil

# This part for the DB
from flask_sqlalchemy import SQLAlchemy

#to upload image into S3
import boto3

application.config.from_object(os.environ['APP_SETTINGS'])
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

from models import STB_User,Remote_Press,STB,Finger_Touch


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@application.route("/")
def hello():
    return "Hello World of search!"

@application.route('/search')
def search():
    # data_json=helper.search_for_word(word)
    # return "data_json"
    return render_template('index.html')





#this function adds a file to the S3 bucket
def add_to_S3_bucket(foldername_in_S3,filename,file_location):
    S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
    AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')

    try:
        # Create an S3 client
        s3 = boto3.client('s3')

        
        print("Details follow")
        print("Source file at ",file_location)
        print("just filename ",filename)
        
        filename_in_S3=foldername_in_S3+"/"+filename
        print("Filename in S3",filename_in_S3)


        

        # Uploads the given file using a managed uploader, which will split up large
        # files automatically and upload parts in parallel.
        s3.upload_file(file_location, S3_BUCKET, filename_in_S3)

        return("Uploaded file successfully")
    except Exception as e:
        return str(e)

@application.route('/add/finger_touch',methods=["POST"])
def add_finger_touch():
    data = request.get_json()

    obj=Remote_Press(
            stb_id=data["stb_id"],
            fingerprint_id=data["fingerprint_id"],
            timestamp=data["timestamp"],
            )
    try:
        
        db.session.add(obj)
        db.session.commit()
        print( "finger_touch added. finger_touch id={}".format(obj.id),"finger_touch")
        return jsonify(data)
    except Exception as e:
        return(str(e),None)



@application.route('/add/remote_press',methods=["POST"])
def add_remote_press():
    data = request.get_json()

    obj=Remote_Press(
            timestamp=data["timestamp"],
            stb_id=data["stb_id"],
            button_pressed=data["button_pressed"],
            )
    try:
        
        db.session.add(obj)
        db.session.commit()
        print( "remote_press added. remote_press id={}".format(obj.id),"remote_press")
        return jsonify(data)
    except Exception as e:
        return(str(e),None)


@application.route('/add/stb_user',methods=["POST"])
def add_stb_user():
    data = request.get_json()

    obj=STB_User(
            name = data["name"],
            age = data["age"],
            gender= data["gender"],
            email= data["email"],
            contact = data["contact"],
            fingerprint_id = data["fingerprint_id"],
            stb_id = data["stb_id"],
            )
    try:
        
        db.session.add(obj)
        db.session.commit()
        print( "stb_user added. stb_user id={}".format(obj.id),"stb_user")
        return jsonify(data)
    except Exception as e:
        return(str(e),None)


@application.route('/add/stb',methods=["POST"])
def add_stb():
    data = request.get_json()

    obj=STB(
            stb_id = data["stb_id"],
            active_status = data["active_status"],
            lat= data["lat"],
            lon= data["lon"],
            )
    try:
        
        db.session.add(obj)
        db.session.commit()
        print( "stb added. stb id={}".format(obj.id),"stb")
        return jsonify(data)
    except Exception as e:
        return(str(e),None)        




@application.route('/load_in_db',methods=["POST"])
def serve_add_to_db():
    data = request.get_json()
    table_name=data["table_name"]
    print(data["table_name"])

    list_of_values=[]
    counter=0
    for key,val in data.items():
        if counter==0:
            counter+=1
            continue
        list_of_values.append(val)

    print(list_of_values)    
    status_string,result=add_to_db(table_name,list_of_values)
    print(status_string)
    if result==table_name:
        print("successfully inserted into ", table_name)



    return jsonify(data)


@application.route('/old_load_in_db',methods=["POST"])
def add_mosque():
    mosque_name=str(request.form['mosque_name'])
    mosque_lat=str(request.form['mosque_lat'])
    mosque_lon=str(request.form['mosque_lon'])
    fajr_time=str(request.form['fajr_time'])
    zuhur_time=str(request.form['zuhur_time'])
    asar_time=str(request.form['asar_time'])
    maghrib_time=str(request.form['maghrib_time'])
    isha_time=str(request.form['isha_time'])
    contact_num=str(request.form['contact_num'])
    uploader=str(request.form["uploader"])
    image_names=[]

    print(mosque_name,mosque_lat,mosque_lon,fajr_time,zuhur_time,asar_time,maghrib_time,isha_time,contact_num,uploader)


    #now to store the images
    folder_name=mosque_name+"_"+contact_num
    folder_name=folder_name.replace(" ","")
    target = os.path.join(APP_ROOT, 'files/{}'.format(folder_name))
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):

        
        

        

        print(upload)
        print("{} is the file name".format(upload.filename))
        

        



        filename = upload.filename
        image_names.append(filename)
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png") or (ext == ".jpeg"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        
        foo = Image.open(destination)
        
        basewidth = 160
        wpercent = (basewidth/float(foo.size[0]))
        hsize = int((float(foo.size[1])*float(wpercent)))
        foo=foo.resize([basewidth,hsize], Image.ANTIALIAS)

        # foo = foo.resize((160,300),Image.ANTIALIAS)
        # size=[300,300]
        # foo=foo.thumbnail(size, Image.ANTIALIAS)
        foo.save(destination)


        upload_return_string=add_to_S3_bucket("images/"+folder_name,filename, destination)
        print(upload_return_string)
        if "Uploaded file successfully" not in upload_return_string:
            return "Abort, some issue in uploading image"



    table_name="Mosque"
    result=add_to_db(table_name,[mosque_name,mosque_lat,mosque_lon,fajr_time,zuhur_time,asar_time,maghrib_time,isha_time,contact_num,folder_name,uploader,image_names])

    if "MOSQUE" in result:
        return get_gallery()
    else:
        return result



#this one is used specifically to get images
@application.route('/upload/<foldername>/<filename>')
def send_image(foldername,filename):
    
    print("files/"+foldername+"/"+filename)
    print("status of image file",os.path.isfile("files/"+foldername+"/"+filename))
    return send_from_directory("files/"+foldername, filename)






#this one is used to show all images
@application.route('/gallery')
def get_gallery():

    #first, get all details of Mosques
    try:
        mosques=Mosque.query.all()
        # print("Results are",mosques)
        # mosques=jsonify([e.serialize() for e in mosques])
        print("Results are",mosques[0])
    except Exception as e:
        return(str(e))    

    directories = os.listdir('./files')
    if ".gitignore" in directories:
        directories.remove(".gitignore")
    if ".DS_Store" in directories:
        directories.remove(".DS_Store")

    files=[]
    for directory in directories:
        current_files=os.listdir('./files/'+directory)        
        for file in current_files:
            files.append((directory,file))

    print(files)
    return render_template("gallery.html", items=mosques)


def get_time_stamp_with_prefix(pref):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    st=st.replace(" ","")
    st=st.replace("-","_")
    st=st.replace(":","_")
    st=pref+st
    return st

def create_dict_to_hold_data():
    dict_mosques={}
    dict_mosques["name"]=[]
    dict_mosques["lat"]=[]
    dict_mosques["lon"]=[]
    dict_mosques["FA"]=[]
    dict_mosques["ZU"]=[]
    dict_mosques["AS"]=[]
    dict_mosques["MA"]=[]
    dict_mosques["IS"]=[]
    dict_mosques["contact"]=[]
    dict_mosques["image_folder_name"]=[]
    dict_mosques["uploader_id"]=[]
    dict_mosques["image_names"]=[]
    return dict_mosques


@application.route("/getall/<format>")
def get_all(format):

    try:
        mosques=Mosque.query.all()
        print(mosques)
    except Exception as e:
        return(str(e))    





    if format=="json":
        return  jsonify([e.serialize() for e in mosques])
    else:
        location_of_file=os.path.join(APP_ROOT,"data")
        # first, the columns
        cols=["name","lat","lon", "FA", "ZU", "AS", "MA", "IS", "contact", "image_folder_name","uploader_id","image_names"]
        dict_mosques=create_dict_to_hold_data()

        for mosque in mosques:
            print(type(mosque))
            dict_mosques["name"].append(mosque.name)
            dict_mosques["lat"].append(mosque.lat)
            dict_mosques["lon"].append(mosque.lon)
            dict_mosques["FA"].append(mosque.FA)
            dict_mosques["ZU"].append(mosque.ZU)
            dict_mosques["AS"].append(mosque.AS)
            dict_mosques["MA"].append(mosque.MA)
            dict_mosques["IS"].append(mosque.IS)
            dict_mosques["contact"].append(mosque.contact)
            dict_mosques["image_folder_name"].append(mosque.image_folder_name)
            dict_mosques["uploader_id"].append(mosque.uploader_id)
            dict_mosques["image_names"].append(mosque.image_names)

        if format=="csv":
            dfObj = pd.DataFrame(dict_mosques)
            location_of_file=os.path.join(location_of_file,"csv")
            fname=get_time_stamp_with_prefix("cv_")
            final_file=os.path.join(location_of_file,fname)+".csv"
            dfObj.to_csv(final_file)

        if os.path.isfile(final_file):
            return send_from_directory(location_of_file,fname+".csv")
        else:
            return "Desired file not found"


            

                



@application.route("/getallimages")
def get_all_images():
    
    st=get_time_stamp_with_prefix("imgs_")
    print(APP_ROOT)
    location_of_zip_file=os.path.join(APP_ROOT,"data")
    location_of_zip_file=os.path.join(location_of_zip_file,"images")
    location_of_zip_file=os.path.join(location_of_zip_file,"zips")
    print("Zip file will be named ",st,"stored at ",location_of_zip_file)
    
    print("contents of ",location_of_zip_file,"are",os.listdir(location_of_zip_file))

    output_file=os.path.join(location_of_zip_file,st)

    
    extension="zip"
    try:
        shutil.make_archive(output_file,extension,"files")
        print(" after zipping contents of ",location_of_zip_file,"are",os.listdir(location_of_zip_file))

        if os.path.isfile(output_file+"."+extension):
            return send_from_directory(location_of_zip_file,st+"."+extension)
        else:
            return "Zip file not found"

    except Exception as e:
        return str(e)




if __name__ == "__main__":
    
    application.run(debug=True)


