import requests
from bs4 import BeautifulSoup
import os
import cgi
import shutil

session = requests.Session()
baseURL = os.getenv('pfsense_url')


def FindCSRF(soup):
    for html_input in soup.find_all('input'):
        if html_input.attrs['name'] == '__csrf_magic':
            return html_input.attrs['value']


# Login
data = session.get(baseURL, verify=False)
soup = BeautifulSoup(data.text, 'html.parser')


data = {
    '__csrf_magic': FindCSRF(soup),
    'usernamefld': os.getenv('pfsense_username'),
    'passwordfld': os.getenv('pfsense_password'),
    'login': 'Sign In'
    }
data = session.post(baseURL, data, verify=False)

# Call Backup Endpoint
soup = BeautifulSoup(data.text, 'html.parser')
data = {
    '__csrf_magic': FindCSRF(soup),
    'backuparea': '',
    'donotbackuprrd': 'yes',
    'encrypt_password': '',
    'download': 'Download configuration as XML',
    'restorearea': '',
    'conffile': '(binary)',
    'decrypt_password': ''
    }

response = session.post(baseURL + 'diag_backup.php', data, stream=True)
if response.status_code != 200:
    raise ValueError('Failed to download')
params = cgi.parse_header(response.headers.get('Content-Disposition', ''))[-1]
if 'filename' not in params:
    raise ValueError('Could not find a filename')
filename = str(params['filename'])
filename = os.path.basename(filename)
with open("/tmp/"+filename, 'wb') as target:
    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, target)
