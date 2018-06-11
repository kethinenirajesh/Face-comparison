import boto3
import signal
import tempfile
import os
from flask import Flask, request

app = Flask(__name__)


time_out = 20


class Timeout():
    """Timeout class using ALARM signal."""

    class Timeout(Exception):
        pass

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)  # disable alarm

    def raise_timeout(self, *args):
        raise Exception("Request time out")


def check_face_match(source, target):
    try:
        with Timeout(time_out):
            result = client.compare_faces(SourceImage={'Bytes': source}, TargetImage={'Bytes': target}, SimilarityThreshold=05)
            if not result[u'FaceMatches']:
                return {'status':0, 'message': "Picture didn't match", 'similarity': 0}
            else:
                return {'status':1, 'message': "Picture matched", 'similarity': result[u'FaceMatches'][0][u'Similarity']}
    except Exception as e:
        return {'status':1, 'message':e.message}


@app.route('/')
def hello_world():
    print "hai1234"
    return '''
        <form action="/query" method="post" enctype="multipart/form-data">
            <input type="file" name="pic1" accept="image/*">
            <input type="file" name="pic2" accept="image/*">
            <p><input type=submit value=Submit>
        </form>
    '''

@app.route('/query', methods=['POST'])
def query_method():
    input_file_1 = request.files.get('pic1')
    inputfile_name_1 = input_file_1.filename

    input_file_2 = request.files.get('pic2')
    inputfile_name_2 = input_file_2.filename

    new_generated_eng_dir = tempfile.mkdtemp()
    path_1 = os.path.join(new_generated_eng_dir, inputfile_name_1)
    path_2 = os.path.join(new_generated_eng_dir, inputfile_name_2)
    input_file_1.save(os.path.join(new_generated_eng_dir, inputfile_name_1))

    input_file_2.save(os.path.join(new_generated_eng_dir, inputfile_name_2))

    print type(input_file_1), type(input_file_2), input_file_1, inputfile_name_1, inputfile_name_2

    with open(path_1, "rb") as imageFile:
        image1 = imageFile.read()

    with open(path_2, "rb") as imageFile:
        image2 = imageFile.read()

    os.remove(path_1)
    os.remove(path_2)
    os.rmdir(new_generated_eng_dir)
    result = check_face_match(image1, image2)
    sm = result['similarity'] if 'similarity' in result else "Pic is not matched"
    return '''<html><p>match result:{}</p><p>Similarity: {}</p><p> message: {}</html>'''.format(result['status'], sm, result['message'])

if __name__ == '__main__':
    #start_aplication()
    print "start"
    client = boto3.client('rekognition', region_name='us-west-2', aws_access_key_id="****",
                          aws_secret_access_key="*****")
    app.run("0.0.0.0",8042)