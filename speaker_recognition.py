import pickle

import speaker_verification_toolkit.tools as svt


class SpeakerRecognition:
    def __init__(self):
        # Load existing voice data from pickle file
        try:
            with open("data.pkl", "rb") as file:
                self.voices = pickle.load(file)
        except Exception as e:
            self.voices = {}

    def add_known_voice(self, sound_file_path: str, name: str) -> str:
        """
        Add a known voice to the system for future identification.

        :param sound_file_path: File path of the sound file
        :type sound_file_path: str

        :param name: Name of the person whose voice is being added
        :type name: str

        :return: Confirmation message that the voice was added
        :rtype: str
        """

        data = svt.extract_mfcc_from_wav_file(sound_file_path)
        self.voices[name] = data
        with open("data.pkl", "wb") as file:
            pickle.dump(self.voices, file)
        return F"{name} added to Known voices"

    def get_unknown_voice(self, sound_file_path: str) -> str:
        """
        Identify the person in the given sound file.

        :param sound_file_path: File path of the sound file
        :type sound_file_path: str

        :return: Name of the person in the sound file
        :rtype: str
        """
        if len(self.voices) == 0:
            return "UNKNOWN USER"
        data = svt.extract_mfcc_from_wav_file(sound_file_path)
        index = svt.find_nearest_voice_data(self.voices.values(), data)
        name = list(self.voices.keys())[index]
        return name
