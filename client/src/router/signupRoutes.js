import { signupStore } from '@/stores/signup';
import { tokenChecker } from '@/utils.js';

// Lazy Load
const SignupView1 = () => import('@/views/Signup/Signup1.vue');
const SignupView2 = () => import('@/views/Signup/Signup2.vue');
const SignupView3 = () => import('@/views/Signup/Signup3.vue');

const signupRoutes = [
  {
    path: '/signup',
    name: 'signup',
    redirect: '/signup/choose-account-type',
  },
  {
    path: '/signup/choose-account-type',
    name: 'signup-step1',
    component: SignupView1,
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
    path: '/signup/personal-info',
    name: 'signup-step2',
    component: SignupView2,
    beforeEnter: (to, from, next) => {
      if (!['signup-step1', 'signup-step3'].includes(from.name)) {
        next('/signup/choose-account-type');
      } else {
        next();
      }
    },
  },
  {
    path: '/signup/additional-info',
    name: 'signup-step3',
    component: SignupView3,
    beforeEnter: (to, from, next) => {
      const chekcer = oauthHandler()
      if (from.name === 'signup-step2' || chekcer) {
        next();
      } else {
        next('/signup/choose-account-type');
      }
    },
  },
];

function oauthHandler() {
  const query = window.location.search
  const params = new URLSearchParams(query)
  const requiredParams = ['role', 'username', 'email', 'name', 'platform', 'unique_id']
  const checker = requiredParams.every(param => params.has(param))

  if (checker) {
    const signup_Store = signupStore()
    signup_Store.changeRole(params.get('role'))
    signup_Store.changeUsername(params.get('username'))
    signup_Store.changeEmail(params.get('email'))
    signup_Store.changeOauth()
    signup_Store.changeName(params.get('name'))
    signup_Store.changePlatform(params.get('platform'))
    signup_Store.changeUniqueId(params.get('unique_id'))
    return true;
  }
  return false;
}

export default signupRoutes;
