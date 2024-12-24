import { tokenChecker } from '@/utils'

// Lazy Load
const LoginView = () => import('@/views/Login.vue')
const ForgotPasswordView = () => import('@/views/ForgotPassword.vue')
const ResetPasswordView = () => import('@/views/ResetPassword.vue')

const loginRoutes = [
    {
        path: '/login',
        name: 'login',
        component: LoginView,
        beforeEnter: async (to, from, next) => {
            const checker = await tokenChecker()
            if (checker) {
              next('/dashboard')
            } else (
              next()
            )
          }
    },
    {
      path: '/forgot-password',
      name: 'forgotPassword',
      component: ForgotPasswordView,
  },
  {
    path: '/reset-password',
    name: 'resetPassword',
    component: ResetPasswordView,
}
]

export default loginRoutes;