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
    print("trying")
    data = request.get_json()

    obj=Finger_Touch(
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
            age = data["age"],
            gender= data["gender"],            
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
        remote_presses=Remote_Press.query.all()
        stb_users=STB_User.query.all()
        finger_touches=Finger_Touch.query.all()


        # for button presses

        print("Results are",remote_presses)
        remote_presses_list={}
        remote_presses_list["id"]=[]
        remote_presses_list["timestamp"]=[]
        remote_presses_list["stb_id"]=[]
        remote_presses_list["button_pressed"]=[]

        
        for remote_press in remote_presses:            
            remote_presses_list["id"].append(remote_press.id)
            remote_presses_list["timestamp"].append(remote_press.timestamp)            
            remote_presses_list["stb_id"].append(remote_press.stb_id)
            remote_presses_list["button_pressed"].append(remote_press.button_pressed)
        
        remote_presses_df = pd.DataFrame(remote_presses_list)
        print("remote press dataframe is")
        print(remote_presses_df.head())

        # for stb_users
        stb_users_list={}
        stb_users_list["id"]=[]
        stb_users_list["age"]=[]
        stb_users_list["gender"]=[]
        stb_users_list["fingerprint_id"]=[]
        stb_users_list["stb_id"]=[]


        for stb_user in stb_users:
            stb_users_list["id"].append(stb_user.id)
            stb_users_list["age"].append(stb_user.age)
            stb_users_list["gender"].append(stb_user.gender)
            stb_users_list["fingerprint_id"].append(stb_user.fingerprint_id)
            stb_users_list["stb_id"].append(stb_user.stb_id)
        stb_users_df = pd.DataFrame(stb_users_list)
        print("stb user dataframe is")
        print(stb_users_df.head())


        # for finger touch
        finger_touch_list={}
        finger_touch_list["id"]=[]
        finger_touch_list["stb_id"]=[]
        finger_touch_list["fingerprint_id"]=[]
        finger_touch_list["timestamp"]=[]
        


        for finger_touch in finger_touches:
            finger_touch_list["id"].append(finger_touch.id)
            finger_touch_list["stb_id"].append(finger_touch.stb_id)
            finger_touch_list["fingerprint_id"].append(finger_touch.fingerprint_id)
            finger_touch_list["timestamp"].append(finger_touch.timestamp)
            
        finger_touch_df = pd.DataFrame(finger_touch_list)
        print("finger touch dataframe is")
        print(finger_touch_df.head())



        #change column type to make it date time
        finger_touch_df['timestamp'] =  pd.to_datetime(finger_touch_df['timestamp'])
        remote_presses_df['timestamp'] =  pd.to_datetime(remote_presses_df['timestamp'])


        # sort dataframes by datetime
        finger_touch_df.sort_values('timestamp')
        remote_presses_df.sort_values('timestamp')
        print("dframes sorted upon timestamp")

        print("After sorting by time")
        print("finger")
        print(finger_touch_df.head())
        print("remote")
        print(remote_presses_df.head())


        # now create the first dataframe
        # finger_duration
        # fingerprint_id, start_time, duration

        prev_finger=finger_touch_df.iloc[0]["fingerprint_id"]
        prev_start_time=finger_touch_df.iloc[0]["timestamp"]
        
        finger_duration={}
        finger_duration["start_time"]=[]
        finger_duration["fingerprint_id"]=[]
        finger_duration["end_time"]=[]

        finger_duration["start_time"].append(prev_start_time)
        finger_duration["fingerprint_id"].append(prev_finger)

        count=0
        for index, row in finger_touch_df.iterrows():
            if count==0:
                count=1
                continue
            if prev_finger!=row["fingerprint_id"]:
                time_of_change=row["timestamp"]
                finger_duration["end_time"].append(time_of_change)

                prev_finger=row["fingerprint_id"]
                prev_start_time=row["timestamp"]
                
                finger_duration["start_time"].append(prev_start_time)
                finger_duration["fingerprint_id"].append(prev_finger)
        print("now = ",pd.Timestamp.now())                
        finger_duration["end_time"].append(pd.Timestamp.now())
        print(finger_duration)
        finger_duration_df = pd.DataFrame(finger_duration)

        print("Individual duration")
        print(finger_duration_df.head())


        finger_channel_duration={}
        finger_channel_duration["start_time"]=[]
        finger_channel_duration["fingerprint_id"]=[]
        finger_channel_duration["age"]=[]
        finger_channel_duration["gender"]=[]
        finger_channel_duration["end_time"]=[]
        finger_channel_duration["button_pressed"]=[]
        




        for index, row in finger_duration_df.iterrows():
            start_time=row["start_time"]
            end_time=row["end_time"]
            the_fingerprint_id=row["fingerprint_id"]
            print("times are",start_time,end_time,the_fingerprint_id)
            
            # filter for all buttons pressed between a users
            # start of touching the finger print device
            # till any other person touches the finger print device

            filtered_remote=remote_presses_df[(remote_presses_df.timestamp >= start_time) & (remote_presses_df.timestamp <= end_time)]
            
            print("filtered on finger touch time")
            print(filtered_remote.head())
            prev_finger=the_fingerprint_id
            prev_start_time=filtered_remote.iloc[0]["timestamp"]
            prev_button=filtered_remote.iloc[0]["button_pressed"]

            print("getting data")

            # adding to the list
            finger_channel_duration["start_time"].append(prev_start_time)
            finger_channel_duration["fingerprint_id"].append(prev_finger)
            finger_channel_duration["button_pressed"].append(prev_button)
            # add user details by fingerprintid
            filtered_user=stb_users_df[(stb_users_df.fingerprint_id == prev_finger)]
            finger_channel_duration["age"].append(filtered_user.iloc[0]["age"])
            finger_channel_duration["gender"].append(filtered_user.iloc[0]["gender"])




            print("getting data2")
            count=0
            for index2,row2 in filtered_remote.iterrows():
                if count==0:
                    count+=1
                    continue
                if prev_button!=row2["button_pressed"]:
                    print("New value")
                    finger_channel_duration["end_time"].append(row2["timestamp"])
                    finger_channel_duration["start_time"].append(row2["timestamp"])
                    finger_channel_duration["button_pressed"].append(row2["button_pressed"])
                    finger_channel_duration["fingerprint_id"].append(prev_finger)

                    # add user details by fingerprintid
                    filtered_user=stb_users_df[(stb_users_df.fingerprint_id == prev_finger)]
                    finger_channel_duration["age"].append(filtered_user.iloc[0]["age"])
                    finger_channel_duration["gender"].append(filtered_user.iloc[0]["gender"])

                    prev_button=row2["button_pressed"]


            finger_channel_duration["end_time"].append(end_time)
        


        print("finger channel duration ",finger_channel_duration)
        finger_channel_duration_df = pd.DataFrame(finger_channel_duration)

        finger_channel_duration_df['start_time'] =  pd.to_datetime(finger_channel_duration_df['start_time'])
        finger_channel_duration_df['end_time'] =  pd.to_datetime(finger_channel_duration_df['end_time'])

        # this will break for days?
        finger_channel_duration_df["duration"]=finger_channel_duration_df["end_time"]-finger_channel_duration_df["start_time"]

        print("Final dataframe")
        print(finger_channel_duration_df.head(10))





    except Exception as e:
        return(str(e))    

    

    
    # return render_template("gallery.html", items=None)
    # return("Expressed")
    return render_template('gallery2.html',  tables=[finger_channel_duration_df.to_html(classes='data')], titles=finger_channel_duration_df.columns.values)


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


