import { tokenChecker } from '@/utils.js';

// Lazy Load
const DashboardView = () => import('@/views/Dashboard.vue')
const DefaultView = () => import('@/views/Default.vue')
const ProfileView = () => import('@/views/Profile.vue')
const ServiceRequestsView = () => import('@/views/ServiceRequests.vue')
const ServiceProfessionalsView = () => import('@/views/ServiceProfessionals.vue')
const ServiceBookingView = () => import('@/views/ServiceBooking.vue')
const ServicesView = () => import('@/views/Services.vue')
const CustomersView = () => import('@/views/Customers.vue')

const dashboardRoutes = [
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    beforeEnter: async (to, from, next) => {
      const checker = await tokenChecker();
      if (checker) {
        next();
      } else {
        next('/login');
      }
    },
    children: [
      {
        path: '',
        name: 'defaultDashboard',
        component: DefaultView,
      },
      {
        path: 'profile',
        name: 'profile',
        component: ProfileView,
      },
      {
        path: 'services',
        name: 'services',
        component: ServicesView,
      },
      {
        path: 'service-requests',
        name: 'serviceRequests',
        component: ServiceRequestsView,
      },
      {
        path: 'customers',
        name: 'customers',
        component: CustomersView,
      },
      {
        path: 'service-professionals',
        name: 'serviceProfessionals',
        component: ServiceProfessionalsView,
      },
      {
        path: 'service-professionals/:id',
        name: 'serviceBooking',
        component: ServiceBookingView,
        beforeEnter: (to, from, next) => {
          if (from.name === 'serviceProfessionals') {
            next();
          } else {
            next({name: 'serviceProfessionals'});
          }
        },
      },

    ],
  },
];

export default dashboardRoutes;