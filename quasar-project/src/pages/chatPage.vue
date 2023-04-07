<template>
    <q-layout view="hHh Lpr lff">
      <q-page-container>
        <q-page>
          <div class="q-pa-md">
            <q-btn
              @click="toggleRecording"
              :label="isRecording ? 'Stop Recording' : 'Start Recording'"
              :disable="isProcessing"
              class="q-mt-md"
            />
            <div class="q-mt-md">{{ interimMessage }}</div>
            <div class="message-container q-mt-md">
              <div
                v-for="message in messages"
                :key="message.id"
                :class="{ 'sent-message': message.sent, 'received-message': !message.sent }"
              >
                {{ message.text }}
              </div>
            </div>
          </div>
        </q-page>
      </q-page-container>
    </q-layout>
  </template>
  
  <script>
  import { ref } from "vue";
  import axios from "axios";
  
  export default {
    setup() {
      let recognition;
      const messages = ref([]);
      const isRecording = ref(false);
      const isProcessing = ref(false);
      const interimMessage = ref("");
  
      const toggleRecording = () => {
        isRecording.value = !isRecording.value;
        if (isRecording.value) {
          startRecording();
        } else {
          stopRecording();
        }
      };
  
      const startRecording = () => {
        if (recognition) {
          recognition.stop();
        }

        if (!("webkitSpeechRecognition" in window)) {
          console.error("Webkit Speech Recognition API not supported in your browser");
          return;
        }
  
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";
  
        recognition.onresult = (event) => {
          interimMessage.value = "";
          for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
              interimMessage.value += event.results[i][0].transcript;
            } else {
              interimMessage.value += event.results[i][0].transcript;
            }
          }
        };
  
        recognition.onerror = (event) => {
          console.error("Speech recognition error:", event.error);
        };
  
        recognition.start();
      };
  
      const stopRecording = async () => {
        // ... Stop recording logic
        messages.value.push({ id: Date.now(), text: interimMessage.value, sent: true });
        isProcessing.value = true;
        const response = await axios.post("http://127.0.0.1:8000/send-message/", {
            content: interimMessage.value,
        });
        messages.value.push({ id: Date.now() + 1, text: response.data.message, sent: false });
        interimMessage.value = "";
        isProcessing.value = false;
      };
  
      return {
        messages,
        isRecording,
        isProcessing,
        toggleRecording,
        interimMessage,
      };
    },
  };
  </script>
  
<style scoped>
.message-container {
  border: 1px solid #ccc;
  padding: 16px;
  border-radius: 8px;
  height: 33vh;
  overflow-y: auto;
}

.sent-message {
  text-align: right;
  background-color: #f0f0f0;
  border-radius: 8px;
  padding: 8px;
  margin-bottom: 8px;
}

.received-message {
  text-align: left;
  background-color: #d0d0d0;
  border-radius: 8px;
  padding: 8px;
  margin-bottom: 8px;
}

</style>