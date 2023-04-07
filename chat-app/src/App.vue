<template>
  <div id="app">
    <input v-model="inputMessage" placeholder="Type your message..." />
    <button @click="sendMessage" :disabled="isProcessing">Send</button>
    <button @click="toggleRecording" :disabled="isProcessing">
      {{ recording ? "Stop Recording" : "Start Recording" }}
    </button>
    <div class="chat">
      <p v-for="message in messages" :key="message.id">{{ message.text }}</p>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-undef */
import axios from "axios";

export default {
  data() {
    return {
      inputMessage: "",
      messages: [],
      recording: false,
      isProcessing: false,
      recognition: null
    };
  },
  methods: {
    async sendMessage() {
      if (this.inputMessage.trim() !== "") {
        this.isProcessing = true;
        try {
          const response = await axios.post("http://127.0.0.1:8000/send-message/", {
            content: this.inputMessage
          });
          this.messages.push({ id: Date.now(), text: response.data.message });
        } catch (error) {
          console.error("Error sending message:", error);
        } finally {
          this.isProcessing = false;
        }
        this.inputMessage = "";
      }
    },
    toggleRecording() {
      if (this.recording) {
        this.stopRecording();
      } else {
        this.startRecording();
      }
    },
    startRecording() {
      if ("webkitSpeechRecognition" in window) {
        this.recognition = new webkitSpeechRecognition();
        this.recognition.lang = "en-US";
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.onresult = (event) => {
          this.inputMessage = event.results[0][0].transcript;
          this.stopRecording();
          this.sendMessage();
        };
        this.recognition.onerror = (event) => {
          console.error("Error in speech recognition:", event.error);
          this.stopRecording();
        };
        this.recognition.start();
        this.recording = true;
      } else {
        alert("Speech recognition is not supported in this browser.");
      }
    },
    stopRecording() {
      if (this.recognition) {
        this.recognition.stop();
        this.recognition = null;
      }
      this.recording = false;
    }
  }
};
</script>

<style>
.chat {
  border: 1px solid #ccc;
  padding: 10px;
  max-width: 400px;
  margin-top: 20px;
}
</style>
