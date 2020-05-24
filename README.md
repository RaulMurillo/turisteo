<!-- # Turisteo -->
![turisteo logo](img/full_turisteo.png)   
===

This application is able to recognize artistic and cultural monuments in a photograph and display tourist information about them, either in text or audio format.

## Dependencies installation

Turisteo runs on Python >= 3.6. All Python packages and dependencies can be installed by simply running 

```shell
pip install -r requirements.txt
```

Additionally, for web application, you shoud install multiple JavaScript packages, We suggest using npm tool for that.

The application heavily relies on third-party APIs: 
[Translator Text](https://azure.microsoft.com/en-us/services/cognitive-services/translator-text-api/) and [Text to Speech](https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/), from Azure and [Cloud Vision](https://cloud.google.com/vision/docs), from Google Cloud Platform. Therefore, an account on such services is required to execute Turisteo.

## Credits

Turisteo is a proyect for the subject "Tecnologías Multimedia e Interacción" (TMI) from Master in Computer Engineering at Complutense University of Madrid, course 2019-2020.

## License

[Apache License 2.0](LICENSE)
