![Logo](![logo](https://github.com/user-attachments/assets/dc0b38e6-903d-4a1a-98fc-67ba63053fd6))


# MoewImage
File system storage image sharing service written in python

### What is this?
It's a hobbyist project written in python to for sharing images/screenshots on the internet, Currently it's not hosted anywhere because of the way it's built and I don't want to deal with running it.

### How does it work?
You upload an image with an optional limitations (can be changed in `config.html`). Once you upload and submit the selected file it generates a code for it (using python's random library) and a website with the name of this code will get created in `shares` while the image itself will get uploaded to `uploads`. The `/shared/<Code>` website will contains the image itself with an embed to be able to see it when sent in social media apps (like discord)

### How can I run it?
By running the `app.py` it will run the website on your IP address on the port "8080". (Can be changed in `app.py`), And it will use the following configurations:
 ```
{
  "URL_PLACEHOLDER": "https://example.com",
  "UPLOAD_FOLDER": "uploads",
  "SHARES_FOLDER": "shares",
  "ALLOWED_EXTENSIONS": ["png", "jpg", "jpeg"],
  "MAX_SIZE": 16000000
}

 ```

`URL_PLACEHOLDER`: The URL you're planning to use

`UPLOAD_FOLDER`: The folder that will contain the images 

`SHARES_FOLDER`:The folder that will contain the sites 

`ALLOWED_EXTENSIONS`: The allowed file extensions

`MAX_SIZE`: the max size you can upload to (16000000 = 16mb)

### Is it safe to use as a large scale?
**No** it's not, The only real security thing that it uses is `Flask_Limiter` to limit the amount of the sent requests, It is not the best way to make a secure website.

### Clearing the saved images 
You can use the `clear.py` script to clear both upload and share folders:
```
python clear.py
```
### Requirments 
It only uses Flask and Flask_Limiter libraries the rest are built-in python libraries: 
```
pip install flask flask_limiter
```



