# first try at a basic script

from __future__ import print_function
import sys
import os
import json
import glob
import shutil

if len(sys.argv) != 2:
    print("Please specify exactly one argument (directory).")
    sys.exit(1)

root = sys.argv[1]
if not os.path.isdir(root):
    print("Can't open specified directory.")
    sys.exit(1)

notes = []
drawings = []
images = []

for q in os.listdir(root):
    current_note = os.path.join(root, q)
    if os.path.exists(os.path.join(current_note, 'memoinfo.jlqm')):
        with open(os.path.join(current_note, 'memoinfo.jlqm'), 'r') as f:
            notes.append(json.loads(f.read())['MemoObjectList'][0]['DescRaw'])
    if os.path.exists(os.path.join(current_note, 'drawings')):
        drawings.extend(
            glob.glob(
                os.path.join(os.path.join(current_note, 'drawings'), '**')
            )
        )
    if os.path.exists(os.path.join(current_note, 'images')):
        images.extend(
            filter(
                lambda f: not f.endswith('thumb.jpg'),
                glob.glob(
                    os.path.join(os.path.join(current_note, 'images'), '**')
                )
            )
        )

os.mkdir('results')
os.mkdir('results/visual')

for index, note in enumerate(notes):
    with open('results/{:05d}'.format(index), 'w') as f:
        print(note.strip(), file=f)

for drawing in drawings:
    shutil.copy(drawing, 'results/visual')

for image in images:
    shutil.copy(image, 'results/visual')
