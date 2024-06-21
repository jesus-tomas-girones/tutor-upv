# Tutor Socrático

Explicar...

app Web: https://tutor-upv.streamlit.app/

Hospedado en: https://share.streamlit.io/ (usuario jtomas@upv.es de github) - 
proyecto: tutor-upv 

Repositorio: https://github.com/jesus-tomas-girones/tutor-upv



## Overview of the App

- IU basado en Streamlit
- Registro basado en Firebase
- LLM basado en API de OpenAI


## Basado en el ejemplo de Streamlit:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://llm-examples.streamlit.app/)

## Get an OpenAI API key

You can get your own OpenAI API key by following the following instructions:

1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

## Enter the OpenAI API key in Streamlit Community Cloud

To set the OpenAI API key as an environment variable in Streamlit apps, do the following:

1. At the lower right corner, click on `< Manage app` then click on the vertical "..." followed by clicking on `Settings`.
2. This brings the **App settings**, next click on the `Secrets` tab and paste the API key into the text box as follows:

```sh
OPENAI_API_KEY='xxxxxxxxxx'
```
