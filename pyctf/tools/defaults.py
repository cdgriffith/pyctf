#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import os
import uuid


def create_example_match(match_directory):
    os.makedirs(match_directory, exist_ok=True)
    with open(os.path.join(match_directory, "settings.json"), "w") as f:
        json.dump(default_settings, f)

    with open(os.path.join(match_directory, "questions.json"), "w") as f:
        json.dump(example_questions, f)

    media_dir = os.path.join(match_directory, "media")
    scripts_dir = os.path.join(match_directory, "scripts")
    os.makedirs(media_dir, exist_ok=True)
    os.makedirs(scripts_dir, exist_ok=True)

    with open(os.path.join(media_dir, "question_three"), "w") as f:
        f.write("The quick brown fox jumps over the lazy dog")

    with open(os.path.join(scripts_dir, "example_script.py"), "w") as f:
        f.write(example_script)


def generate_ssl_cert(match_directory):

    create_self_signed_cert("my_pyctf",
                            os.path.join(match_directory, "cert.crt"),
                            os.path.join(match_directory, "key.key"))


def create_self_signed_cert(hostname, cert_file, key_file, country="US", state="Maine",
                            city="Middle of Nowhere", org="Nonya", unit="Business"):
    try:
        from OpenSSL import crypto, SSL
    except ImportError:
        raise Exception("Please install PyOpenSSL")

    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)
        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = country
        cert.get_subject().ST = state
        cert.get_subject().L = city
        cert.get_subject().O = org
        cert.get_subject().OU = unit
        cert.get_subject().CN = hostname

        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(315360000)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha1')

        with open(cert_file, "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

        with open(key_file, "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))


default_settings = {
    "port": 47275,
    "host": "0.0.0.0",
    "media_directory": "media",
    "script_directory": "scripts",
    "website": True,
    "ssl": False,
    "ssl_cert": "ssl.pem",
    "ssl_key": "ssl.pem",
    "save_state": True,
    "save_file": "state.json",
    "auth_file": "users.json",
    "salt": str(uuid.uuid4()),
    "encoding": "utf-8",
    "auth_time_limit": 2400,
    "anonymous_users": False,
    "save_auth": True,
    "welcome_message": "<h2>Welcome to PyCTF!</h2> <p>Welcome to the example PyCTF Challenges.</p>"
}

example_questions = {
    "1": {
        "title": "Basic intro",
        "question": "what is 1 + 1?",
        "answer": 2,
        "time_limit": 0,
        "answer_type": "integer"
    },
    "2": {
        "title": "Script generated question and answer",
        "question_script": "python example_script.py -q",
        "answer_script": "python example_script.py -a",
        "time_limit": 10,
        "points": 2,
        "tags": ["script"]
    },
    "3": {
        "title": "Media File Exercise",
        "question": "open the media file and read back the contents as a decoded string",
        "answer": "The quick brown fox jumps over the lazy dog",
        "time_limit": 0,
        "media": "question_three",
        "tags": ["media", "encoding"]
    }
}

example_script = (
    "import sys\n"
    "import random\n"
    "import json\n"
    "\n"
    "\n"
    "def generate_question():\n"
    "    '''Generate a question that will specify to either multiply or add the supplied data'''\n"
    "    choice = random.choice([\"Multiply\", \"Add\"])\n"
    "    question = \"{0} the two given numbers together\".format(choice)\n"
    "    data = [random.randint(0, 10), random.randint(20, 25)]\n"
    "\n"
    "    out = dict(question=question, data=data, storage=choice)\n"
    "    # Storage is a place that the script can place additional information only it can access\n"
    "    # which can be used to help answer the question\n"
    "    return json.dumps(out)\n"
    "\n"
    "\n"
    "def check_answer(data):\n"
    "    '''Use the 'storage' field to know if we generated an 'add' or 'multiply'\n"
    "    question, and figure out the answer, then compare it to the one the user\n"
    "    supplied. '''\n"
    "\n"
    "    if data['storage'] == \"Add\":\n"
    "        correct_answer = data['data'][0] + data['data'][1]\n"
    "    elif stdin['storage'] == \"Multiply\":\n"
    "        correct_answer = data['data'][0] * data['data'][1]\n"
    "    else:\n"
    "        raise Exception(\"storage must contain either 'Add' or 'Multiply'\")\n"
    "\n"
    "    correct = True if int(data['answer']) == correct_answer else False\n"
    "\n"
    "    out = dict(correct=correct)\n"
    "    return json.dumps(out)\n"
    "\n"
    "\n"
    "def run_func(func, *args):\n"
    "    '''Function wrapper that will try to run a function and write it's output to stdout.\n"
    "    On failure it will print the exception and exit with an error status '''\n"
    "    try:\n"
    "        response = func(*args)\n"
    "    except Exception as err:\n"
    "        sys.stderr.write(str(err))\n"
    "        sys.exit(1)\n"
    "    else:\n"
    "        sys.stdout.write(response)\n"
    "\n"
    "if __name__ == '__main__':\n"
    "    arg = sys.argv[1]  # could use ArgumentParser but is cumbersome for our needs\n"
    "\n"
    "    if arg == \"-q\":\n"
    "        run_func(generate_question)\n"
    "    elif arg == \"-a\":\n"
    "        stdin = json.loads(sys.stdin.read())\n"
    "        run_func(check_answer, stdin)\n"
    "    else:\n"
    "        print(\"Must have the option either -q or -a\")\n"
    "        sys.exit(1)\n"
    "\n"
    "sys.exit(0)\n")
