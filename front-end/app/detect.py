#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
For more information, the documentation at
https://cloud.google.com/vision/docs.
"""

import argparse
import json
from google.protobuf.json_format import MessageToJson
import logging
from google.cloud import vision
from app.errors import ImageDetectionError
import io
#from errors import ImageDetectionError

# gcp_client = None


# def init_gcp_image_api():
#     global gcp_client
#     gcp_client = vision.ImageAnnotatorClient()


# [START vision_landmark_detection]
def detect_landmarks(path):
    """Detects landmarks in the file.

    Args:
        path (str): Path of the original image.

    Returns:
        dict: The possible detected landmarks on the image.
    """
    print('[detect_landmarks]')
    gcp_client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_landmark_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = gcp_client.landmark_detection(image=image, max_results=3)
    landmarks = response.landmark_annotations

    if len(landmarks) == 0:
        logging.warning('No landmark detected on picture.')
        # return None
        raise ImageDetectionError

    # logging.debug('Landmarks:')
    # for landmark in landmarks:
    #     logging.debug(landmark)

        # print(landmark.description)
        # for location in landmark.locations:
        #     lat_lng = location.lat_lng
        #     print('Latitude {}'.format(lat_lng.latitude))
        #     print('Longitude {}'.format(lat_lng.longitude))

    #if response.error.message:
     #   raise Exception(
      #      '{}\nFor more info on error messages, check: '
       #     'https://cloud.google.com/apis/design/errors'.format(
        #        response.error.message))

    annotations = json.loads(MessageToJson(
        response, preserving_proto_field_name=True))
    # print(type(annotations))
    # print(response)
    # print(type(annotations['landmark_annotations']))
    return annotations['landmark_annotations']

    # [END vision_python_migration_landmark_detection]
# [END vision_landmark_detection]


# [START vision_landmark_detection_gcs]
def detect_landmarks_uri(uri):
    """Detects landmarks in the file located in Google Cloud Storage or on the
    Web."""
    # gcp_client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = gcp_client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    logging.debug('Landmarks:')

    for landmark in landmarks:
        logging.debug(landmark)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
# [END vision_landmark_detection_gcs]
