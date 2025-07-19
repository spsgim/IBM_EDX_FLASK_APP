"""
Module for analyzing text emotion using IBM Watson NLP EmotionPredict API.
Includes the `emotion_detector` function which returns a dictionary of
emotion scores and the dominant emotion, or handles errors gracefully.
Author: Shailendra
"""

import requests
import json

def emotion_detector(text_to_analyse):
    """
    Analyzes input text and returns emotion scores or None values if invalid.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyse}}

    response = requests.post(url, json=myobj, headers=header)

    if response.status_code == 200:
        formatted_response = json.loads(response.text)
        emotions = formatted_response['emotionPredictions'][0]['emotion']
        required_emotions = {emo: emotions[emo] for emo in ['anger', 'disgust', 'fear', 'joy', 'sadness']}
        dominant_emotion = max(required_emotions, key=required_emotions.get)
        required_emotions['dominant_emotion'] = dominant_emotion
        return required_emotions

    elif response.status_code == 400:
        # Return all emotions as None if invalid input
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    return None  # Fallback for other status codes
