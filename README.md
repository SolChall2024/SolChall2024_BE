# GSC_2024_POKI

## Quick Start

```
# Clone the application
$ git clone https://github.com/SolChall2024/SolChall2024_BE.git

# Install dependencies
python -m venv venv

#mac
source ./venv/Scripts/activate
#windows
.\venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver

## Project Setup

### 1. **Setting up Secret Key**
   - Create a `secrets.json` file in the root directory of the project.
   - Store the project's secret key in this file.
   - Add `secrets.json` to `.gitignore` to maintain security.

### 2. **Setting up Google STT API**
   - To use the Google STT API, you need to create a new project in the Google Cloud Console.
   - Enable the Google STT API in the created project.
   - Create a new service account and grant it permissions.
   - Download the JSON-formatted authentication information.
   - The authentication information contains permissions to call the Google STT API.

### 3. **Setting Environment Variable**
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the downloaded JSON file for the Google STT API authentication.
