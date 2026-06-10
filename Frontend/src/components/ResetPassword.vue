<template>
  <div class="min-h-screen bg-slate-900 flex items-center justify-center p-4">
    <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl max-w-md w-full border border-slate-700">
      <h2 class="text-2xl font-bold text-white mb-6">Reset Password</h2>
      <p v-if="message" class="text-indigo-400 mb-4 text-sm">{{ message }}</p>

      <form @submit.prevent="handleRequestReset" class="space-y-4">
        <input v-model="email" type="email" placeholder="Enter your email" required 
               class="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white" />
        <button type="submit" class="w-full py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-500">
          Send Reset Link
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from "../api"

const email = ref('')
const message = ref('')

const handleRequestReset = async () => {
  try {
    await api.post('request-reset/', { email: email.value })
    message.value = "If that email exists, a reset link has been sent."
  } catch (error) {
    message.value = "An error occurred."
  }
}
</script>