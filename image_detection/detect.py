#!/usr/bin/env python

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

"""This application demonstrates how to perform basic operations with the
Google Cloud Vision API.
Example Usage:
python detect.py text ./resources/wakeupcat.jpg
python detect.py labels ./resources/landmark.jpg
python detect.py web ./resources/landmark.jpg
python detect.py web-uri http://wheresgus.com/dog.JPG
python detect.py web-geo ./resources/city.jpg
python detect.py faces-uri gs://your-bucket/file.jpg
python detect.py ocr-uri gs://python-docs-samples-tests/HodgeConj.pdf \
gs://BUCKET_NAME/PREFIX/
python detect.py object-localization ./resources/puppies.jpg
python detect.py object-localization-uri gs://...
python detect.py landmarks ./resources/landmark.jpg
python detect.py landmarks-uri https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=imgres&cd=&cad=rja&uact=8&ved=2ahUKEwi2gdeg5JnoAhUPJBoKHTXzBREQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.alhambra.info%2F&psig=AOvVaw0DZLkTsWWh_RjFmNYgyMdo&ust=1584269048813704
For more information, the documentation at
https://cloud.google.com/vision/docs.
"""

import argparse


# [START vision_landmark_detection]
def detect_landmarks(path):
    """Detects landmarks in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_landmark_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.landmark_detection(image=image, max_results=3)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark)
        # print(landmark.description)
        # for location in landmark.locations:
        #     lat_lng = location.lat_lng
        #     print('Latitude {}'.format(lat_lng.latitude))
        #     print('Longitude {}'.format(lat_lng.longitude))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    # [END vision_python_migration_landmark_detection]
# [END vision_landmark_detection]


# [START vision_landmark_detection_gcs]
def detect_landmarks_uri(uri):
    """Detects landmarks in the file located in Google Cloud Storage or on the
    Web."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        # print(landmark.description)
        print(landmark)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
# [END vision_landmark_detection_gcs]

def run_local(args):
    if args.command == 'faces':
        # detect_faces(args.path)
        exit(1)
    # elif args.command == 'labels':
    #     detect_labels(args.path)
    elif args.command == 'landmarks':
        detect_landmarks(args.path)
    # elif args.command == 'text':
    #     detect_text(args.path)
    # elif args.command == 'logos':
    #     detect_logos(args.path)
    # elif args.command == 'safe-search':
    #     detect_safe_search(args.path)
    # elif args.command == 'properties':
    #     detect_properties(args.path)
    # elif args.command == 'web':
    #     detect_web(args.path)
    # elif args.command == 'crophints':
    #     detect_crop_hints(args.path)
    # elif args.command == 'document':
    #     detect_document(args.path)
    # elif args.command == 'web-geo':
    #     web_entities_include_geo_results(args.path)
    # elif args.command == 'object-localization':
    #     localize_objects(args.path)


def run_uri(args):
    if args.command == 'text-uri':
        # detect_text_uri(args.uri)
        exit(1)
    # elif args.command == 'faces-uri':
    #     detect_faces_uri(args.uri)
    # elif args.command == 'labels-uri':
    #     detect_labels_uri(args.uri)
    elif args.command == 'landmarks-uri':
        detect_landmarks_uri(args.uri)
    # elif args.command == 'logos-uri':
    #     detect_logos_uri(args.uri)
    # elif args.command == 'safe-search-uri':
    #     detect_safe_search_uri(args.uri)
    # elif args.command == 'properties-uri':
    #     detect_properties_uri(args.uri)
    # elif args.command == 'web-uri':
    #     detect_web_uri(args.uri)
    # elif args.command == 'crophints-uri':
    #     detect_crop_hints_uri(args.uri)
    # elif args.command == 'document-uri':
    #     detect_document_uri(args.uri)
    # elif args.command == 'web-geo-uri':
    #     web_entities_include_geo_results_uri(args.uri)
    # elif args.command == 'ocr-uri':
    #     async_detect_document(args.uri, args.destination_uri)
    # elif args.command == 'object-localization-uri':
    #     localize_objects_uri(args.uri)


if __name__ == '__main__':
    import os
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']='credentials.json'
    print('Google credentials in:', os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    # detect_faces_parser = subparsers.add_parser(
    #     'faces', help=detect_faces.__doc__)
    # detect_faces_parser.add_argument('path')

    # faces_file_parser = subparsers.add_parser(
    #     'faces-uri', help=detect_faces_uri.__doc__)
    # faces_file_parser.add_argument('uri')

    # detect_labels_parser = subparsers.add_parser(
    #     'labels', help=detect_labels.__doc__)
    # detect_labels_parser.add_argument('path')

    # labels_file_parser = subparsers.add_parser(
    #     'labels-uri', help=detect_labels_uri.__doc__)
    # labels_file_parser.add_argument('uri')

    detect_landmarks_parser = subparsers.add_parser(
        'landmarks', help=detect_landmarks.__doc__)
    detect_landmarks_parser.add_argument('path')

    landmark_file_parser = subparsers.add_parser(
        'landmarks-uri', help=detect_landmarks_uri.__doc__)
    landmark_file_parser.add_argument('uri')

    # detect_text_parser = subparsers.add_parser(
    #     'text', help=detect_text.__doc__)
    # detect_text_parser.add_argument('path')

    # text_file_parser = subparsers.add_parser(
    #     'text-uri', help=detect_text_uri.__doc__)
    # text_file_parser.add_argument('uri')

    # detect_logos_parser = subparsers.add_parser(
    #     'logos', help=detect_logos.__doc__)
    # detect_logos_parser.add_argument('path')

    # logos_file_parser = subparsers.add_parser(
    #     'logos-uri', help=detect_logos_uri.__doc__)
    # logos_file_parser.add_argument('uri')

    # safe_search_parser = subparsers.add_parser(
    #     'safe-search', help=detect_safe_search.__doc__)
    # safe_search_parser.add_argument('path')

    # safe_search_file_parser = subparsers.add_parser(
    #     'safe-search-uri',
    #     help=detect_safe_search_uri.__doc__)
    # safe_search_file_parser.add_argument('uri')

    # properties_parser = subparsers.add_parser(
    #     'properties', help=detect_properties.__doc__)
    # properties_parser.add_argument('path')

    # properties_file_parser = subparsers.add_parser(
    #     'properties-uri',
    #     help=detect_properties_uri.__doc__)
    # properties_file_parser.add_argument('uri')

    # 1.1 Vision features
    # web_parser = subparsers.add_parser(
    #     'web', help=detect_web.__doc__)
    # web_parser.add_argument('path')

    # web_uri_parser = subparsers.add_parser(
    #     'web-uri',
    #     help=detect_web_uri.__doc__)
    # web_uri_parser.add_argument('uri')

    # web_geo_parser = subparsers.add_parser(
    #     'web-geo', help=web_entities_include_geo_results.__doc__)
    # web_geo_parser.add_argument('path')

    # web_geo_uri_parser = subparsers.add_parser(
    #     'web-geo-uri',
    #     help=web_entities_include_geo_results_uri.__doc__)
    # web_geo_uri_parser.add_argument('uri')

    # crop_hints_parser = subparsers.add_parser(
    #     'crophints', help=detect_crop_hints.__doc__)
    # crop_hints_parser.add_argument('path')

    # crop_hints_uri_parser = subparsers.add_parser(
    #     'crophints-uri', help=detect_crop_hints_uri.__doc__)
    # crop_hints_uri_parser.add_argument('uri')

    # document_parser = subparsers.add_parser(
    #     'document', help=detect_document.__doc__)
    # document_parser.add_argument('path')

    # document_uri_parser = subparsers.add_parser(
    #     'document-uri', help=detect_document_uri.__doc__)
    # document_uri_parser.add_argument('uri')

    # ocr_uri_parser = subparsers.add_parser(
    #     'ocr-uri', help=async_detect_document.__doc__)
    # ocr_uri_parser.add_argument('uri')
    # ocr_uri_parser.add_argument('destination_uri')

    # object_localization_parser = subparsers.add_parser(
    #     'object-localization', help=async_detect_document.__doc__)
    # object_localization_parser.add_argument('path')

    # object_localization_uri_parser = subparsers.add_parser(
    #     'object-localization-uri', help=async_detect_document.__doc__)
    # object_localization_uri_parser.add_argument('uri')

    args = parser.parse_args()

    if 'uri' in args.command:
        run_uri(args)
    else:
        run_local(args)