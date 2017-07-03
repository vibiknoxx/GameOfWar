"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import random

class Card(object):
    
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val
    
    def show(self):
        return(self.value, self.suit)
 
class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for v in range(1,14):
                self.cards.append(Card(s, v))
    
    def show(self):
        for c in self.cards:
            c.show()
    def shuffle(self):
        for i in range(len(self.cards)-1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def drawCard(self):
        return self.cards.pop()

class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0
    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self

    def showHand(self):
        for card in self.hand:
            return card.show()

    def discard(self):
        return self.hand.pop()

deck = Deck()
deck.shuffle()

player = Player("player")
computer = Player("computer")
player.score = 0
computer.score = 0

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title':  title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome to WAR!!"
    speech_output = "Welcome to the game of war, your deck has been shuffled and dealt to you and the computer" 
                  
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me to play a card, your opponent is waiting, you can also say Show score to see running total scores "
                    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for playing. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def handle_ShowMyScore(intent, session):
    
    card_title = "Your Score"
    session_attributes = {}
    should_end_session = False

    speech_output = "Your score is " + str(player.score) + " computers score is " + str(computer.score)
    reprompt_text = "Are you ready to keep playing?"
    should_end_session = True


    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))

def handle_ResetScore(intent, session):
    
    card_title = "Both scores have been resest to zero"
    session_attributes = {}
    should_end_session = False

    player.score = 0
    computer.score = 0
    
    speech_output = "Your scores have been reset to 0"
    reprompt_text = "Are you ready to keep playing?, if not say stop"
    should_end_session = True


    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))

def handle_ShuffleDeck(intent, session):
    
    card_title = "The deck has been shuffled"
    session_attributes = {}
    should_end_session = False

    deck.shuffle()

    speech_output = "deck has been shuffled"
    reprompt_text = "Are you ready to keep playing"
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))

def handle_PlayMyCard(intent, session):

    card_title = "your card has been played"
    session_attributes = {}
    should_end_session = False
    deck.shuffle()
    player.draw(deck)
    computer.draw(deck)
    x = player.showHand()
    y = computer.showHand()
    player.discard()
    computer.discard()

    if x > y:
        player.score += 1
        speech_output = "You win!! your card was " + str(x) + " computers card was " + str(y) + ",Want to play again?"
    elif y > x:
        computer.score += 1
        speech_output = "you lost, computers card was " + str(y) + " your card was " + str(x) + ",Want to play again?"
    else: 
        speech_output = "You and the Computer tied!" + ", Want to play again?"
    reprompt_text = "You can ask me to show your score, but do you want to play another card?"

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])


    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print(intent)
    print(intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "PlayMyCard":
        return handle_PlayMyCard(intent, session)
    elif intent_name == "ShuffleDeck":
        return handle_ShuffleDeck(intent, session)
    elif intent_name == "ShowMyScore":
        return handle_ShowMyScore(intent, session)
    elif intent_name == "ResetScore":
        return handle_ResetScore(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
