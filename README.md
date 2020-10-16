# KeySpeech simple
This is a simplified version of the original KeySpeech web app, updated for [DeepSpeech 0.8.1](https://github.com/mozilla/DeepSpeech)

## What it does
- With KeySpeech you can create a user account, record mp3 audios through your browser 
and then upload them so that key word extraction can be performed. 
- Key word lists are saved in the database and are presented in an easily searchable and filterable UI.
- The transcription is done using Mozilla's open source deep learning based STT model [DeepSpeech](https://github.com/mozilla/DeepSpeech).
- This simplified web app *does not* perform any tasks asynchronously therefore once you upload a file *you cannot* navigate away from that page on the web app until transcription is complete and you are redirected to the homepage.
- Asynchronous functionality can be introduced using [celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html)

## How to run locally (you must have Python 3 and pip installed)
- Clone the repo `git clone https://github.com/nrimsky/KeySpeech_simple.git`
- cd into the project directory `cd KeySpeech_simple`
- Create a virtual environment to download dependencies `python3 -m venv env` and activate it `source env/bin/activate`
- Install the requirements `pip install -r requirements.txt`
- Go into the static subdirectory of language_capture `cd language_capture/static`
- Download the DeepSpeech pretrained model `curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.8.1/deepspeech-0.8.1-models.pbmm` `curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.8.1/deepspeech-0.8.1-models.scorer`
- Go back into root project directory `cd ../..`
- Setup the database `python manage.py migrate`
- Finally (!) run the development server `python manage.py runserver`
