# GSC_2024_POKI

# Quick Start

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
