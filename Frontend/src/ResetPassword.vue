<template>
  <div class="min-h-screen bg-slate-900 flex items-center justify-center p-4">
    <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl max-w-md w-full border border-slate-700">
      <h2 class="text-2xl font-bold text-white mb-6">Reset Password</h2>
      
      <form @submit.prevent="handleReset" class="space-y-4">
        <input v-model="email" type="email" placeholder="Enter your email" required 
               class="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white" />
        
        <input v-model="newPassword" type="password" placeholder="Enter new password" required 
               class="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white" />
        
        <button type="submit" class="w-full py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-500">
          Reset Password
        </button>
      </form>
      
      <button @click="$emit('back')" class="mt-4 text-slate-400 text-sm hover:text-white">
        ← Back to Login
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from './api'

const email = ref('')
const newPassword = ref('')
const emit = defineEmits(['back', 'success'])

const handleReset = async () => {
  try {
    // This sends the data to your Django backend
    await api.post('reset-password/', { email: email.value, new_password: newPassword.value })
    emit('success')
  } catch (e) {
    alert('Reset failed. Please check your email.')
  }
}
</script>