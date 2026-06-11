import { createRouter, createWebHistory } from 'vue-router'

import AuthPage from './components/AuthPage.vue'
import ResetPasswordConfirm from './components/ResetPasswordConfirm.vue'
import Dashboard from './components/Dashboard.vue' 

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: AuthPage },
    { path: '/reset-password-confirm/:uid/:token', component: ResetPasswordConfirm },
    { path: '/dashboard', component: Dashboard, name: 'Dashboard' } // 2. Added the Dashboard route
  ]
})

export default router