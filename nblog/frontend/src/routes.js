import React, { lazy } from 'react';
import { Redirect } from 'react-router-dom';
import AuthLayout from './layouts/Auth';
import ErrorLayout from './layouts/Error';
import Dashboard from './layouts/Dashboard';
import PrivateRoute from './privateRoute';
import DefaultLayout from "./layouts/DefaultLayout";
import Home from "./views/Home";
import Profile from "./views/UserProfile";
import TypographyView from "./views/Typography"
// import PresentationView from './views/Presentation';


export default [
  {
    path: '/',
    exact: true,
    component: Home
  },
  {
    path: '/auth',
    component: AuthLayout,
    routes: [
      {
        path: '/auth/login',
        exact: true,
        component: lazy(() => import('src/views/Login'))
      },
      {
        path: '/auth/register',
        exact: true,
        component: lazy(() => import('src/views/Register'))
      },
      {
        component: () => <Redirect to="/errors/error-404" />
      }
    ]
  },
  {
    path: '/errors',
    component: ErrorLayout,
    routes: [
      {
        path: '/errors/error-401',
        exact: true,
        component: lazy(() => import('src/views/Error401'))
      },
      {
        path: '/errors/error-404',
        exact: true,
        component: lazy(() => import('src/views/Error404'))
      },
      {
        path: '/errors/error-500',
        exact: true,
        component: lazy(() => import('src/views/Error500'))
      },
      {
        component: () => <Redirect to="/errors/error-404" />
      }
    ]
  },
  {
    route: '*',
    component: Dashboard,

    // component: (props) => <PrivateRoute component={DefaultLayout} {...props}/>,
    routes: [
      {
        path: '/',
        exact: true,
        component: Home
      },
      // {
      //   path: '/presentation',
      //   exact: true,
      //   component: TypographyView
      // },
      // {
      //   path: '/profile',
      //   exact: true,
      //   component: Profile
      // },
      {
        component: () => <Redirect to="/errors/error-404" />
      }
    ]
  }
];
