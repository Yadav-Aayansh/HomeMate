import { createRouter, createWebHistory } from 'vue-router';
import homeRoutes from './homeRoutes.js';
import signupRoutes from './signupRoutes.js';
import loginRoutes from './loginRoutes.js';
import dashboardRoutes from './dashboardRoutes.js';

const routes = [
  ...homeRoutes,
  ...signupRoutes,
  ...loginRoutes,
  ...dashboardRoutes,
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
