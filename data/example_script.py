import sys
import random
import json

arg = sys.argv[1]

if arg.lower() == "-q":
    choice = random.choice(["Multiply", "Add"])

    question = "{0} the two given numbers together".format(choice)

    data = [random.randint(0, 10), random.randint(20, 25)]

    out = dict(question=question, data=data, storage=choice)

    sys.stdout.write(json.dumps(out))

elif arg.lower() == "-a":
    # data, storage, answer
    stdin = json.loads(sys.stdin.read())
    correct = False
    if stdin['storage'] == "Add":
        correct_answer = stdin['data'][0] + stdin['data'][1]
    elif stdin['storage'] == "Multiply":
        correct_answer = stdin['data'][0] * stdin['data'][1]
    else:
        sys.stderr.write("storage must contain either 'Add' or 'Multiply'")
        sys.exit(1)

    if int(stdin['answer']) == correct_answer:
        correct = True

    out = dict(correct=correct)

    sys.stdout.write(json.dumps(out))

sys.exit(0)