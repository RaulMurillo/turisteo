<!-- # Turisteo -->
![turisteo logo](img/full_turisteo.png)   
===
Turisteo is a proyect for the subject "Tecnologías Multimedia e Interacción" (TMI) from Master in Computer Engineering at Complutense University of Madrid, course 2019-2020.

It consists of an App capable of recognizing artistic and cultural monuments and generating information of tourist interest in this regard.

## Dependencies installation

The following packages and libraries must be installed: Python 3, Google and [Google Cloud Vision API](https://cloud.google.com/vision/docs), [Pillow](https://pillow.readthedocs.io/en/stable/), [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) (and also parsers like [lxml](https://lxml.de/) and/or [html5lib](https://github.com/html5lib/) are recommended), playsound and num2words.

Those packages can be installed, for example using `pip`, as following:

```shell
pip install requests   
pip install google  
pip install google-cloud-vision  
pip install pillow  
pip install beautifulsoup4   
pip install lxml   
pip install html5lib
pip install playsound
pip install num2words
```
or simply by running 

```shell
pip install -r requirements.txt
```

The application also makes use of third-party APIs: 
[Translator Text](https://azure.microsoft.com/en-us/services/cognitive-services/translator-text-api/) and [Text to Speech](https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/), from Azure and [Cloud Vision](https://cloud.google.com/vision/docs), from Google Cloud Platform. Therefore, an account on such services is required to execute Turisteo.

