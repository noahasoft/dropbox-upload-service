from bottle import HTTPResponse, route, run, template
import os
import os.path
import shutil
import sys
import threading

try:
    import settings
except ImportError:
    sys.exit('Not configured. Please create settings.py and fill it out.')


filepaths_being_queued = frozenset()


@route('/<filepath:path>')
def upload(filepath):
    global filepaths_being_queued
    
    source_filepath = os.path.join(settings.SOURCE_DIRPATH, filepath)
    destination_filepath = os.path.join(settings.DESTINATION_DIRPATH, filepath)
    
    if not os.path.isfile(source_filepath):
        return HTTPResponse(
            status=404,
            body='File not found.',
            headers={'Content-Type': 'text/plain'}
        )
    
    if source_filepath in filepaths_being_queued:
        copied_bytes = \
            0 if not os.path.exists(destination_filepath) else \
            os.path.getsize(destination_filepath)
        total_bytes = os.path.getsize(source_filepath)
        
        return HTTPResponse(
            status=409,
            body='Queueing... (%d%%)' % round(copied_bytes*100/total_bytes),
            headers={'Content-Type': 'text/plain'}
        )
    
    if os.path.exists(destination_filepath):
        return HTTPResponse(
            status=409,
            body='Queued. (100%)',
            headers={'Content-Type': 'text/plain'}
        )
    
    def queue(source_filepath, destination_filepath):
        global filepaths_being_queued
        
        os.makedirs(os.path.dirname(destination_filepath), exist_ok=True)
        shutil.copy2(source_filepath, destination_filepath)
        
        # Unlock
        filepaths_being_queued = filepaths_being_queued - frozenset([source_filepath])
    
    # Lock
    filepaths_being_queued = filepaths_being_queued | frozenset([source_filepath])
    
    # Copy file asynchronously
    threading.Thread(
        target=queue,
        args=(source_filepath, destination_filepath)
    ).start()
    
    return HTTPResponse(
        status=200,
        body='Queueing... (0%)',
        headers={'Content-Type': 'text/plain'}
    )


run(host='0.0.0.0', port=settings.PORT)
