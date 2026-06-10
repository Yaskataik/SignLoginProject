import { createRouter, createWebHistory } from 'vue-router'
// We use './components/' because the index.ts file is inside 'src/'
import AuthPage from './components/AuthPage.vue'
import ResetPasswordConfirm from './components/ResetPasswordConfirm.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: AuthPage },
    { path: '/reset-password-confirm/:uid/:token', component: ResetPasswordConfirm }
  ]
})

export default router