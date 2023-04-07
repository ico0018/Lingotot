<template>
  <div id="app">
    <input v-model="inputMessage" placeholder="Type your message..." />
    <button @click="sendMessage" :disabled="isProcessing">Send</button>
    <button @click="startRecording" :disabled="isProcessing">Start Recording</button>
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
      isProcessing: false,
    };
  },
  methods: {
    async startRecording() {
      this.isProcessing = true;
      const recognition = new webkitSpeechRecognition();
      recognition.lang = "en-US";
      recognition.onresult = async (event) => {
        this.inputMessage = event.results[0][0].transcript;
        await this.sendMessage();
      };
      recognition.start();
    },
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
    }
  },
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
