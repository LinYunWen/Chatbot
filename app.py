import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine
from telegram.ext import Updater, CommandHandler, Job
import time


API_TOKEN = '391243893:AAH_8KjeVxZvlIqsvlDkQmdFaznb7OI3swc'
WEBHOOK_URL = 'https://772ec1e5.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'state1',
        'state2',
        'state3',
        'setNote',
        'setNoteTimer',
        'uncomfort',
        'mouthache',
        'mouthacheReason',
        'mouthacheDoing',
        'backpain',
        'backpainLong',
        'backpainShort',
        'backpainSport',
        'backpainSit',
        'seeDoctor',
        'badMoodBegin',
        'badMood',
        'badMoodFinish',
        'eyehurt'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state3',
            'conditions': 'is_going_to_state3'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'setNote',
            'conditions': 'is_going_to_setNote'
        },
        {
            'trigger': 'advance',
            'source': 'setNote',
            'dest': 'setNoteTimer',
            'conditions': 'is_going_to_setNoteTimer'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'uncomfort',
            'conditions': 'is_going_to_uncomfort'
        },
        {
            'trigger': 'advance',
            'source': 'uncomfort',
            'dest': 'mouthache',
            'conditions': 'is_going_to_mouthache'
        },
        {
            'trigger': 'advance',
            'source': 'mouthache',
            'dest': 'mouthacheReason',
            'conditions': 'is_going_to_mouthacheReason'
        },
        {
            'trigger': 'advance',
            'source': 'mouthacheReason',
            'dest': 'mouthacheDoing',
            'conditions': 'is_going_to_mouthacheDoing'
        },
        {
            'trigger': 'advance',
            'source': 'mouthacheDoing',
            'dest': 'seeDoctor',
            'conditions': 'is_going_to_seeDoctor'
        },
        {
            'trigger': 'advance',
            'source': 'uncomfort',
            'dest': 'backpain',
            'conditions': 'is_going_to_backpain'
        },
        {
            'trigger': 'advance',
            'source': 'backpain',
            'dest': 'backpainLong',
            'conditions': 'is_going_to_backpainLong'
        },
        {
            'trigger': 'advance',
            'source': 'backpain',
            'dest': 'backpainShort',
            'conditions': 'is_going_to_backpainShort'
        },
        {
            'trigger': 'advance',
            'source': 'backpainLong',
            'dest': 'backpainSport',
            'conditions': 'is_going_to_backpainSport'
        },
        {
            'trigger': 'advance',
            'source': 'backpainLong',
            'dest': 'backpainSit',
            'conditions': 'is_going_to_backpainSit'
        },
        {
            'trigger': 'advance',
            'source': 'uncomfort',
            'dest': 'eyehurt',
            'conditions': 'is_going_to_eyehurt'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'badMoodBegin',
            'conditions': 'is_going_to_badMoodBegin'
        },
        {
            'trigger': 'advance',
            'source': 'badMoodBegin',
            'dest': 'badMood',
            'conditions': 'is_going_to_badMood'
        },
        {
            'trigger': 'advance',
            'source': 'badMood',
            'dest': 'badMood',
            'conditions': 'is_going_to_badMood'
        },
        {
            'trigger': 'advance',
            'source': 'badMood',
            'dest': 'badMoodFinish',
            'conditions': 'is_going_to_badMoodFinish'
        },
        {
            'trigger': 'advance',
            'source': 'backpainShort',
            'dest': 'seeDoctor',
            'conditions': 'is_going_to_seeDoctor'
        },
        {
            'trigger': 'advance',
            'source': 'backpainSport',
            'dest': 'seeDoctor',
            'conditions': 'is_going_to_seeDoctor'
        },
        {
            'trigger': 'advance',
            'source': 'backpainSit',
            'dest': 'seeDoctor',
            'conditions': 'is_going_to_seeDoctor'
        },
        {
            'trigger': 'go_back',
            'source': [
                'state1',
                'state2',
                'state3',
                'setNote',
                'seeDoctor',
                'badMoodFinish',
                'setNoteTimer',
                'eyehurt'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    #print(time.localtime()[3])
    #test()
    app.run()

