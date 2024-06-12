import azure.functions as func
import logging
import base64
import json
from pydub import AudioSegment
from pydub.utils import which
AudioSegment.converter = which("ffmpeg")
import whisper
import io
import os
import torch
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = whisper.load_model("small", device=device)
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="AudioToTranscribe",methods=['POST'])
def AudioToTranscribe(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')
    try:
        data = req.get_json()
       
        # iteration = data.get('iteration')
        iteration = data['iteration']
        # print("blob",data.get('blob'),type(data.get('blob')))
        # blob = data.get('blob')
        blob = data['blob']
        isCompleteBlob=data['isCompleteBlob']
        byteData = base64.b64decode(blob)
        # blob1 = pickle.dumps(blob)
        print("iteration",type(blob))
        print("iteration 2",type(byteData))
        fileName = "audio_"+str(iteration)+".wav"
        print("100=======")
        # audio = AudioSegment.from_file(blob1,format="wav")
 
        audio = AudioSegment.from_file(io.BytesIO(byteData),format="wav")
        print("101=======")
        audio.export(fileName,format="wav")
 
        result = model.transcribe(fileName, language="en")
        print("Result text:====",result['text'])
        if os.path.exists(fileName):
            os.remove(fileName)
        return json.dumps({'transcript': result['text'],
                           'isCompleteBlob':isCompleteBlob})
    except Exception as e:
        return json.dumps({'error': str(e)})
    