import tkinter as tk
import boto3
import os
import sys
from tempfile import gettempdir
from contextlib import closing

# Initializing Tkinter root window
root = tk.Tk()
root.geometry("400x240")  
root.title("T2S-Con Amazon Polly")

# Creating a Text widget
textexample = tk.Text(root, height=10)
textexample.pack()

def get_text():
    try:
        aws_mag_con = boto3.session.Session(profile_name='type your IAM user here')
        client = aws_mag_con.client(service_name='polly', region_name='us-east-1')
        
        # Get text from the Text widget
        result = textexample.get("1.0", "end").strip()
        if not result:
            print("No text provided.")
            return

        print(result)
        
        # Calling Polly to synthesize speech
        response = client.synthesize_speech(VoiceId='Joanna', SampleRate='8000', OutputFormat='mp3', Text=result, Engine='neural')
        
        print(response)
        
        # Save the audio stream to a file
        if "AudioStream" in response:
            with closing(response['AudioStream']) as stream:
                output = os.path.join(gettempdir(), "speech.mp3")
                try:
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    print(f"Error writing file: {error}")
                    return
        else:
            print("Could not find the stream")
            return

        # Play the audio file on Windows
        if sys.platform == 'win32':
            os.startfile(output)
        else:
            print(f"Audio saved at: {output}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Create a Button widget
btnRead = tk.Button(root, height=1, width=10, text="Read", command=get_text)
btnRead.pack()

# Start the Tkinter event loop
root.mainloop()
