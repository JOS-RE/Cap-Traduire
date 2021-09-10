from dotenv import load_dotenv
from datetime import datetime
import os


from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk

global targetLanguage
targetLanguage = ''

def gui():

    # from tkinter import *
    # Explicit imports to satisfy Flake8

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()

    window.geometry("684x384")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=384,
        width=684,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        684.0,
        384.0,
        fill="#FFEEEE",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))

    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: makeFR(targetLanguage),
        relief="flat"
    )
    button_1.place(
        x=362.00000000000006,
        y=53.0,
        width=287.0,
        height=55.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))

    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: makeES(targetLanguage),
        relief="flat"
    )

    button_2.place(
        x=362.00000000000006,
        y=201.0,
        width=287.0,
        height=55.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))

    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: makeHI(targetLanguage),
        relief="flat"
    )
    button_3.place(
        x=362.00000000000006,
        y=275.0,
        width=287.0,
        height=55.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))

    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: makeDE(targetLanguage),
        relief="flat"
    )
    button_4.place(
        x=362.00000000000006,
        y=127.0,
        width=287.0,
        height=55.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))

    button_5 = Button(
        text="abcd",
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: makeqt(targetLanguage),
        relief="flat"
    )
    button_5.place(
        x=30.000000000000057,
        y=67.0,
        width=249.0,
        height=249.0
    )

    canvas.create_text(
        411.00000000000006,
        53.0,
        anchor="nw",
        text="Francais",
        fill="#FFFFFF",
        font=("VarelaRound Regular", 47 * -1)
    )

    canvas.create_text(
        452.00000000000006,
        276.0,
        anchor="nw",
        text="Hindi",
        fill="#FFFFFF",
        font=("VarelaRound Regular", 43 * -1)
    )

    canvas.create_text(
        411.00000000000006,
        201.0,
        anchor="nw",
        text="German",
        fill="#FFFFFF",
        font=("VarelaRound Regular", 42 * -1)
    )

    canvas.create_text(
        411.00000000000006,
        129.0,
        anchor="nw",
        text="Espanol",
        fill="#FFFFFF",
        font=("VarelaRound Regular", 42 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


def main(targetLanguage):
    try:
        global speech_config
        global translation_config

        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(
            cog_key, cog_region)
        translation_config.speech_recognition_language = 'en-US'
        translation_config.add_target_language('fr')
        translation_config.add_target_language('es')
        translation_config.add_target_language('hi')
        translation_config.add_target_language('de')
        print('ready to translate from',
              translation_config.speech_recognition_language)

        # Configure speech
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)

        # Get user input
        targetLanguag = ''
        while targetLanguag != 'quit':
            targetLanguag = gui()

# """
# boolean = True
# while boolean:
#     targetLanguage = input(
#         "What language would you like to translate to? (type 'quit' to exit) ")
#     if targetLanguage == 'quit':
#         boolean = False
#     else:
#         

# """

    except Exception as ex:
        print(ex)

def makeFR(targetLanguage):
    targetLanguage = "fr"
    Translate(targetLanguage)
    return targetLanguage


def makeES(targetLanguage):
    targetLanguage = "es"
    Translate(targetLanguage)
    return targetLanguage


def makeHI(targetLanguage):
    targetLanguage = "hi"
    Translate(targetLanguage)
    return targetLanguage


def makeDE(targetLanguage):
    targetLanguage = "de"
    Translate(targetLanguage)
    return targetLanguage


def makeqt(targetLanguage):
    return exit()

def Translate(targetLanguage):
    translation = ''

    # Translate speech
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(
        translation_config, audio_config)
    print("Speak now...")
    result = translator.recognize_once_async().get()
    print(f'Translating {result.text}')
    translation = result.translations[targetLanguage]
    print(translation)

    # Synthesize translation
    voices = {
        "fr": "fr-FR-Julie",
        "es": "es-ES-Laura",
        "hi": "hi-IN-Kalpana",
        "de": "de-DE-HeddaRUS"
    }
    speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)


if __name__ == "__main__":
    main(targetLanguage)
