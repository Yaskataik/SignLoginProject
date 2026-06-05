<script setup lang="ts">
import { ref } from 'vue'
import api from './api'
import ResetPassword from './ResetPassword.vue' // Added this import

const isSignIn = ref(true)
const showReset = ref(false) // Added this state

// Form fields
const email = ref('')
const password = ref('')
const username = ref('')

// Feedback messages for the user
const errorMessage = ref('')
const successMessage = ref('')

const resetForm = () => {
  username.value = ''
  email.value = ''
  password.value = ''
}

const handleSubmit = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  
  try {
    if (isSignIn.value) {
      // 1. Hit your Django Login endpoint
      const response = await api.post('login/', {
        email: email.value,
        password: password.value
      })
      
      resetForm()
      successMessage.value = 'Login successful! Redirecting...'
      setTimeout(() => { successMessage.value = '' }, 3000)
      
      console.log('Backend response:', response.data)
      
    } else {
      // 2. Hit your Django Registration endpoint
      const response = await api.post('register/', {
        username: username.value,
        email: email.value,
        password: password.value
      })
      
      resetForm()
      successMessage.value = 'Registration successful! You can now sign in.'
      setTimeout(() => { successMessage.value = '' }, 3000)
      
      isSignIn.value = true // automatically switch them to login view
    }
} catch (error: any) {
    console.error('API Error:', error)
    
    if (error.response) {
      
      if (error.response.status === 401) {
        errorMessage.value = 'Invalid password. Click here to reset your password.'
      } 

      else if (error.response.data) {
        // This takes the object (e.g., {username: [...]}) and turns it into a readable string
        const errors = error.response.data
        const firstErrorKey = Object.keys(errors)[0]
        errorMessage.value = `${firstErrorKey}: ${errors[firstErrorKey][0]}`
      }
    } else {
      errorMessage.value = 'Something went wrong. Is the backend running?'
    }
  }
}
</script>

<template>
  <div class="min-h-screen bg-slate-900 flex items-center justify-center p-4">
    <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl max-w-md w-full border border-slate-700 transition-all duration-300">
      
      <div v-if="!showReset" class="text-center mb-8">
        <h2 class="text-3xl font-bold text-white tracking-tight">
          {{ isSignIn ? 'Welcome Back' : 'Create Account' }}
        </h2>
        <p class="text-slate-400 mt-2 text-sm">
          {{ isSignIn ? 'Please enter your details to sign in' : 'Sign up to get started with your account' }}
        </p>
      </div>

      <div v-if="errorMessage" class="mb-4 p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-sm text-red-400 text-center">
        <div>{{ errorMessage.replace('Click here', '') }}</div>
        <button v-if="errorMessage.includes('Click here')" 
                @click="showReset = true"
                class="text-indigo-300 hover:text-white underline font-semibold mt-1 block w-full">
          Click here to reset.
        </button>
      </div>

      <div v-if="successMessage" class="mb-4 p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-sm text-emerald-400 text-center animate-pulse">
        {{ successMessage }}
      </div>

      <form v-if="!showReset" @submit.prevent="handleSubmit" class="space-y-5">
        <div v-if="!isSignIn" class="space-y-1">
          <label class="text-xs font-semibold text-slate-300 uppercase tracking-wider">Username</label>
          <input v-model="username" type="text" placeholder="johndoe" required class="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors" />
        </div>

        <div class="space-y-1">
          <label class="text-xs font-semibold text-slate-300 uppercase tracking-wider">Email Address</label>
          <input v-model="email" type="email" placeholder="you@example.com" required class="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors" />
        </div>

        <div class="space-y-1">
          <label class="text-xs font-semibold text-slate-300 uppercase tracking-wider">Password</label>
          <input v-model="password" type="password" placeholder="••••••••" required class="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors" />
        </div>

        <button type="submit" class="w-full py-3 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-semibold rounded-lg shadow-lg hover:shadow-indigo-500/20 transition-all duration-200 mt-2">
          {{ isSignIn ? 'Sign In' : 'Sign Up' }}
        </button>
      </form>

      <div v-if="!showReset" class="mt-6 text-center text-sm border-t border-slate-700/50 pt-4">
        <p class="text-slate-400">
          {{ isSignIn ? "Don't have an account?" : "Already have an account?" }}
          <button @click="isSignIn = !isSignIn" class="text-indigo-400 hover:text-indigo-300 font-medium ml-1 focus:outline-none underline decoration-indigo-400/30 hover:decoration-indigo-300 transition-all">
            {{ isSignIn ? 'Sign up here' : 'Sign in here' }}
          </button>
        </p>
      </div>

      <ResetPassword 
        v-if="showReset" 
        @back="showReset = false" 
        @success="showReset = false; successMessage = 'Password reset! Please log in.'; errorMessage = ''" 
      />

    </div>
  </div>
</template>