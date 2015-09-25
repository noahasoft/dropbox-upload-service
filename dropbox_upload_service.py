from bottle import HTTPResponse, route, run, template
import os
import os.path
import shutil


PORT = 9999
SOURCE_DIRPATH = '/Volumes/davidf/bin/server/mediaqueue/www'
DESTINATION_DIRPATH = '/Volumes/davidf/Dropbox (Personal)/From MediaQueue'


filepaths_being_queued = frozenset()


@route('/<filepath:path>')
def upload(filepath):
    source_filepath = os.path.join(SOURCE_DIRPATH, filepath)
    if not os.path.isfile(source_filepath):
        return HTTPResponse(
            status=404,
            body='File not found.',
            headers={'Content-Type': 'text/plain'}
        )
    
    destination_filepath = os.path.join(DESTINATION_DIRPATH, filepath)
    if os.path.exists(destination_filepath):
        return HTTPResponse(
            status=409,
            body='Already queued for upload.',
            headers={'Content-Type': 'text/plain'}
        )
    
    # Copy file immediately
    os.makedirs(os.path.dirname(destination_filepath), exist_ok=True)
    shutil.copy2(source_filepath, destination_filepath)
    
    return HTTPResponse(
        status=200,
        body='Queued for upload.',
        headers={'Content-Type': 'text/plain'}
    )


run(host='localhost', port=PORT)
