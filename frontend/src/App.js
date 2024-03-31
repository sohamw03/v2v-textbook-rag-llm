import { LoaderCircle } from "lucide-react";
import React, { useEffect, useRef, useState } from "react";
import "./App.css";

export default function App() {
  const [pauseButtonData, setPauseButtonData] = useState("Pause");
  const [formatsData, setFormatsData] = useState("Format: start recording to see sample rate");
  const [chatbotResponse, setChatbotResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const input = useRef(null);
  const audioContext = useRef(null);
  const rec = useRef(null);
  const gumStream = useRef(null);

  const recordRef = useRef(null);
  const pauseRef = useRef(null);
  const stopRef = useRef(null);
  const outputAudio = useRef(null);

  let AudioContext;

  function startRecording() {
    console.log("recordButton clicked");
    var constraints = { audio: true, video: false };
    recordRef.current.disabled = true;
    stopRef.current.disabled = false;
    pauseRef.current.disabled = false;
    navigator.mediaDevices
      .getUserMedia(constraints)
      .then(function (stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
        audioContext.current = new AudioContext({ sampleRate: 16000 });

        setFormatsData("Format: 1 channel pcm @ " + audioContext.current.sampleRate / 1000 + "kHz");

        /*  assign to gumStream for later use  */
        gumStream.current = stream;

        /* use the stream */
        input.current = audioContext.current.createMediaStreamSource(stream);

        rec.current = new window.Recorder(input.current, { numChannels: 1 });

        rec.current.record();

        console.log("Recording started");
      })
      .catch(function (err) {
        //enable the record button if getUserMedia() fails
        recordRef.current.disabled = false;
        stopRef.current.disabled = true;
        pauseRef.current.disabled = true;
        console.log(err);
      });
  }

  function pauseRecording() {
    console.log("pauseButton clicked rec.recording=", rec.current.recording);
    if (rec.current.recording) {
      //pause
      rec.current.stop();
      setPauseButtonData("Resume");
    } else {
      //resume
      rec.current.record();
      setPauseButtonData("Pause");
    }
  }

  function stopRecording() {
    console.log("stopButton clicked");
    setLoading(true);

    //disable the stop button, enable the record too allow for new recordings
    stopRef.current.disabled = true;
    recordRef.current.disabled = false;
    pauseRef.current.disabled = true;

    //reset button just in case the recording is stopped while paused
    setPauseButtonData("Pause");

    //tell the recorder to stop the recording
    rec.current.stop();

    //stop microphone access
    gumStream.current.getAudioTracks()[0].stop();

    //create the wav blob and pass it on to createDownloadLink
    rec.current.exportWAV(createDownloadLink);
  }

  function createDownloadLink(blob) {
    let url = URL.createObjectURL(blob);
    let au = document.createElement("audio");
    let li = document.createElement("li");
    let link = document.createElement("a");

    //name of .wav file to use during upload and download (without extension)
    var filename = new Date().toISOString();

    //add controls to the <audio> element
    au.controls = true;
    au.src = url;

    //save to disk link
    link.href = url;
    link.download = filename + ".wav"; //download forces the browser to donwload the file using the  filename
    link.innerHTML = "Save to disk";

    //add the new audio element to li
    li.appendChild(au);

    //add the filename to the li
    li.appendChild(document.createTextNode(filename + ".wav "));

    //add the save to disk link to li
    li.appendChild(link);

    //upload link
    var formData = new FormData();
    formData.append("audio", blob, filename);

    fetch("https://yozu-speech-services.azurewebsites.net/chat", {
      method: "POST",
      body: formData,
    })
      .then(async function (response) {
        if (response.ok) {
          const responseJson = await response.json();
          handleApiResponse(responseJson);
          console.log("Server returned: ", responseJson);
        } else {
          throw new Error("Server returned: " + response.status);
        }
      })
      .catch(function (error) {
        console.log("Error: ", error);
      });

    //add the li element to the ol
    // recordingsList.appendChild(li);
  }

  function handleApiResponse(data) {
    setLoading(false);
    setChatbotResponse({
      user: data.detectedText,
      bot: data.chatResponse,
    });

    const audioDataBase64 = data.audio;
    const audioElement = outputAudio.current;
    audioElement.src = "data:audio/wav;base64," + audioDataBase64;
    audioElement.play();
  }

  useEffect(() => {
    AudioContext = window.AudioContext || window.webkitAudioContext;
  }, []);

  return (
    <>
      <div id="controls">
        <button id="recordButton" onClick={startRecording} ref={recordRef} disabled={recordRef?.current?.disabled} className={recordRef?.current?.disabled ? "disabled" : ""}>
          Record
        </button>
        <button id="pauseButton" ref={pauseRef} onClick={pauseRecording} disabled={pauseRef?.current?.disabled} className={pauseRef?.current?.disabled ? "disabled" : ""}>
          {pauseButtonData}
        </button>
        <button id="stopButton" onClick={stopRecording} ref={stopRef} disabled={stopRef?.current?.disabled} className={stopRef?.current?.disabled ? "disabled" : ""}>
          {loading ? <LoaderCircle size={16} id="loader" /> : "Stop"}
        </button>
        <div id="formats">{formatsData}</div>
        <div id="visual-data">
          <p>Chatbot Response: </p>
          <p id="chatbot-response">User : {chatbotResponse.user}</p>
          <p id="chatbot-response">Bot : {chatbotResponse.bot}</p>
        </div>
      </div>
      <audio id="output" style={{ display: "none" }} ref={outputAudio}></audio>
      <audio id="testoutput" controls src="data:audio/wav;base64,"></audio>
    </>
  );
}
