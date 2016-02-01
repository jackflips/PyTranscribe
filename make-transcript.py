import sys
import speech_recognition as sr
from pydub import AudioSegment

kNumSecondsInSnippet = 8

def getSRAudio(wavFile):
	r = sr.Recognizer()
	with sr.WavFile(wavFile) as source:
		audio = r.record(source) # read the entire WAV file
		getGoogResults(audio)

def getGoogResults(audio):
	try:
		partialTranscript = r.recognize_google(audio)
		print str((float(i+1) / float(numSegments)) * 100) + "% done."
		transcript.write(str(partialTranscript))
	except sr.UnknownValueError:
		print "Getting throttled, trying again..."
		getGoogResults(audio)
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))

audioFilePath = sys.argv[1]
r = sr.Recognizer()
transcript = open("transcript.txt", 'w+')

audioFile = AudioSegment.from_mp3(audioFilePath)
duration = audioFile.duration_seconds
numSegments = (int(duration) / kNumSecondsInSnippet) + 1

for i in range(numSegments):
	snippet = audioFile[((i * kNumSecondsInSnippet) * 1000) : (((i + 1) * kNumSecondsInSnippet) * 1000)]
	print "duration" + str(snippet.duration_seconds)
	snippet = snippet.set_channels(1)
	snippet.export("snippet.wav", format="wav")
	snippetFile = open('snippet.wav')
	getSRAudio(snippetFile)

sys.exit(1)