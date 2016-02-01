import sys
from wit import Wit
import speech_recognition as sr
from pydub import AudioSegment

kNumSecondsInSnippet = 8

r = sr.Recognizer()
transcript = open("transcript.txt", 'w+')
w = Wit('YCSG2BTKJWMXWCGSPWWSZMCJARNLXFNX')
audioFilePath = sys.argv[1]

audioFile = AudioSegment.from_mp3(audioFilePath)
duration = audioFile.duration_seconds
numSegments = (int(duration) / kNumSecondsInSnippet) + 1

def getSRAudio(wavFile):
	r = sr.Recognizer()
	with sr.WavFile(wavFile) as source:
		audio = r.record(source) # read the entire WAV file
		getGoogResults(audio)

def getGoogResults(audio):
	try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
		partialTranscript = r.recognize_google(audio)
		print str((float(i+1) / float(numSegments)) * 100) + "% done."
		transcript.write(str(partialTranscript))
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
		getGoogResults(audio)
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))


for i in range(numSegments):
	snippet = audioFile[((i * kNumSecondsInSnippet) * 1000) : (((i + 1) * kNumSecondsInSnippet) * 1000)]
	print "duration" + str(snippet.duration_seconds)
	snippet = snippet.set_channels(1)
	snippet.export("snippet.wav", format="wav")
	snippetFile = open('snippet.wav')
	getSRAudio(snippetFile)
	

	#result = w.post_speech(snippetFile)
	#print str((float(i+1) / float(numSegments)) * 100) + "% done."
	#transcript.write(str(result["_text"]))

sys.exit(1)