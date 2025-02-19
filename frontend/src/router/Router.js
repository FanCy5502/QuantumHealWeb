import { createRouter, createWebHistory } from 'vue-router'
const router = createRouter({
  history: createWebHistory(''),
  routes: [
    //默认转到/login页
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/register',
      name: 'register',
      meta: {
        title: '注册页',
      },
      component: () => import('../views/Register.vue')
    },
    {
      path: '/login',
      name: 'login',
      meta: {
        title: '登录页',
      },
      component: () => import('../views/Login.vue')
    },
    {
      path: '/home',
      name: 'HomePage',
      meta: {
        title: '主页',
      },
      component: () => import("../views/HomePage.vue")
    },
    {
      path: "/prediction/:patient_id",
      name: 'prediction',
      meta: {
        title: '预测结果',
      },
      component: () => import("../views/PredictionView.vue")
    },
    {
      path: "/clustering/:patient_id",
      name: 'clustering',
      meta: {
        title: '聚类结果',
      },
      component: () => import('../views/ClusteringView.vue')
    },
    {
      path: '/job',
      name: 'JobPage',
      meta: {
        title: '招聘信息页'
      },
      component: () => import('../views/JobComponent.vue')
    },
  ]
})

// 导出router这个方法函数，便于其他模块引用
export default router
