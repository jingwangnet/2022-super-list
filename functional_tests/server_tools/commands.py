from django.conf import settings
import subprocess
import os
import re


def create_session_on_server(mail):
    result = subprocess.run(
        f'ansible-playbook create_session.yml -e email={ mail }',
        shell=True, 
        capture_output=True, 
        cwd=os.path.join(settings.BASE_DIR, 'functional_tests/server_tools')
    )
    
    result = result.stdout.decode('utf-8')
    
    for message in result.split(sep="\n\n"):
        msg_search = re.search(r'msg', message)
        if msg_search: 
            #print(message)
            for l in message.split():
                line_search = re.search(r'\w{10,}', l)
                if line_search: 
                    return line_search.group(0).strip()


