# import
from posixpath import basename
from socket import herror
from tkinter import *
from urllib import response
from PIL import Image, ImageTk
from io import BytesIO
from urllib.request import urlopen
import random
import requests
import json
from paho.mqtt import client as mqtt_client

####################__VARIBLE__#######################
broker = 'test.mosquitto.org'
port = 1883
deviceId = "C21283M384"
topic = "/topic/detected/" + deviceId
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjE0ODg0Mzk2NDE2NDE0NDA0MDciLCJlbWFpbCI6InRob25ndG1AaGFuZXQuY29tIiwiY2xpZW50X2lkIjoiNzBlNWJhYTU0ZDc5MzBmZWJmZjdjZTMyMWFiZTExYTEiLCJ0eXBlIjoiYXV0aG9yaXphdGlvbl9jb2RlIiwiaWF0IjoxNjUxMjI4NDk3LCJleHAiOjE2NTM4MjA0OTd9.6ctzTyPEl7OzdZHKB139odkz2Y2dBUv2uAYQHI4qAZI"
api = "https://partner.hanet.ai/person/getUserInfoByPersonID"
####################__FUNCTION__#######################


def get_image_from_url(url):
    img = Image.open(urlopen(url))
    photo = ImageTk.PhotoImage(img)
    return photo


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def change_img(url):
    innercanvas.delete("all")
    innercanvas.img = get_image_from_url(url)
    innercanvas.create_image(
        innercanvas.winfo_reqwidth()/2, innercanvas.winfo_reqheight()/2, image=innercanvas.img)


def get_user_info(personID):
    headers = {'Content-Type': 'application/json'}
    payloads = json.dumps({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjE0ODg0Mzk2NDE2NDE0NDA0MDciLCJlbWFpbCI6InRob25ndG1AaGFuZXQuY29tIiwiY2xpZW50X2lkIjoiNzBlNWJhYTU0ZDc5MzBmZWJmZjdjZTMyMWFiZTExYTEiLCJ0eXBlIjoiYXV0aG9yaXphdGlvbl9jb2RlIiwiaWF0IjoxNjUxMjI4NDk3LCJleHAiOjE2NTM4MjA0OTd9.6ctzTyPEl7OzdZHKB139odkz2Y2dBUv2uAYQHI4qAZI",
        "personID": "2159905179002994688"
    })

    response = requests.post(api, headers=headers, data=payloads)
    return json.loads(response.text)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        data = msg.payload.decode("utf-8")
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        data_json = json.loads(data)
        resp = get_user_info(data_json["person_id"])
        if resp["returnCode"] == 1:
            print(resp)

            change_img(resp["data"]["avatar"])

    client.subscribe(topic)
    client.on_message = on_message


# create windows app
window = Tk()
window.attributes("-fullscreen", True)
window.title("MQTT-image")

srceenHeight = window.winfo_screenheight()
srceenWidth = window.winfo_screenwidth()
window.geometry(str(srceenWidth) + "x" + str(srceenHeight))

# create a white canvas
outercanvas = Canvas(bg='white')
bg = Image.open("bg.png")
new_bg = bg.resize((srceenWidth, srceenHeight))
pic = ImageTk.PhotoImage(new_bg)
outercanvas.create_image(0, 0, image=pic, anchor=NW)
outercanvas.pack(side='top', fill='both', expand='yes')

innercanvas = Canvas(outercanvas, width=srceenWidth/2, height=srceenHeight*2/3)
outercanvas.create_window(srceenWidth/2, srceenHeight/2, window=innercanvas)

photo = get_image_from_url(
    "https://img5.thuthuatphanmem.vn/uploads/2021/12/20/hinh-anh-dong-welcome-dep_075503112.jpg")
image_container = innercanvas.create_image(
    innercanvas.winfo_reqwidth()/2, innercanvas.winfo_reqheight()/2, image=photo)


def run():

    client = connect_mqtt()
    subscribe(client)
    client.loop_start()

    window.mainloop()


if __name__ == '__main__':
    run()
