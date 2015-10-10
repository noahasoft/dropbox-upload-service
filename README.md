# Dropbox Upload Service

This is a tiny web service that copies a requested file from within a fixed source directory to a fixed target directory.

My application of this functionality is to copy files from an external media drive to my Dropbox folder on demand, and thereby upload the files automatically. The messages output by this web service reflect this intended usage.

Since this service does not actually provide the capability to *list* files in the fixed source directory, this service is best paired with a static file server (like Apache) that *can* list files.

### Requirements

* Python 3.4 or later

### Installation

* Copy `settings.example.py` to `settings.py` and fill it out with appropriate settings for your environment.

### Starting the Service

```
$ python3 dropbox_upload_service.py
```

### Example Requests and Responses

* <http://localhost:1337/CuteCats.mp4>
    * Queueing... (0%)
* <http://localhost:1337/CuteCats.mp4>
    * Queueing... (72%)
* <http://localhost:1337/CuteCats.mp4>
    * Queued. (100%)
* <http://localhost:1337/NoSuchFile.txt>
    * File not found.


### License

MIT.