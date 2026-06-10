<template>
  <div class="min-h-screen bg-slate-900 flex items-center justify-center p-4">
    <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl max-w-md w-full border border-slate-700">
      <h2 class="text-2xl font-bold text-white mb-6">Set New Password</h2>
      
      <form @submit.prevent="submitNewPassword" class="space-y-4">
        <input v-model="newPassword" type="password" placeholder="Enter new password" required 
               class="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white" />
        <button type="submit" class="w-full py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-500">
          Reset Password
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import api from "../api"

const route = useRoute()
const newPassword = ref('')
const uid = route.params.uid
const token = route.params.token

const submitNewPassword = async () => {
  try {
    await api.post(`password-reset-confirm/${uid}/${token}/`, { 
      password: newPassword.value 
    })
    alert("Password reset successfully!")
  } catch (error) {
    alert("Invalid or expired link.")
  }
}
</script>