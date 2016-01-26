# This import will give us our wrapper for the Pocketsphinx library which we can use to get the voice commands from the 
# user.
from pocket_sphinx_listener import PocketSphinxListener
import sys
import pyaudio
import wave



def play_wav(filename):
    CHUNK = 1024
    wf = wave.open(filename, 'rb')

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
    
    stream.stop_stream()
    stream.close()

    p.terminate()

def runMain():
    # Now we set up the voice recognition using Pocketsphinx from CMU Sphinx.
    # We can set debug for the listener here to see messages directly from Pocketsphinx
    pocketSphinxListener = PocketSphinxListener(debug=False)
    on_off = "off"
    while True:
        try:
            # We can set debug here to see what the decoder thinks we are saying as we say it
            command = pocketSphinxListener.getCommand(debug=False).lower()
            if command == "marcy turn on tv":
                if on_off == "off":
                    print("I am now turning on the TV.")
                    play_wav("tv_on.wav")
                    on_off = "on"
                else:
                    print("I cannot perform this task. The TV is already on.")
                    play_wav("cant_turn_on.wav")    
        
            elif command == "marcy turn off tv":
                if on_off == "on":
                    print("I am now turning on the TV.")
                    on_off = "off"
                    play_wav("tv_off.wav")
                    
            elif command == "marcy poop":
                print("I cannot perform this task, I do not consume food.")
            
            elif command == "hello marcy":
                print("Hello. What would you like me to do?")
            
            elif "go left" in command or "go right" in command or "go up" in command or "go down" in command:
                print("Going.")
            
            elif command == "select":
                print("Selected.")

        # Exit when control-c is pressed
        except (KeyboardInterrupt, SystemExit):
            print 'People sometimes make mistakes, Goodbye.'
            sys.exit()    
    
if __name__ == '__main__':
    runMain()
