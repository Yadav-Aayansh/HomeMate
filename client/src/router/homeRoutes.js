// Lazy Load
const HomeView = () => import('@/views/Home.vue')

const homeRoutes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
];

export default homeRoutes;
