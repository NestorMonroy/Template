/* eslint-disable react/no-multi-comp */
/* eslint-disable react/display-name */
import React from 'react';
import BarChartIcon from '@material-ui/icons/BarChart';
import DashboardIcon from '@material-ui/icons/DashboardOutlined';
import SettingsIcon from '@material-ui/icons/SettingsOutlined';

export default [
  {
    items: [
      {
        title: 'Dashboards',
        href: '/dashboards',
        icon: DashboardIcon
      },
      {
        title: 'Management',
        href: '/management',
        icon: BarChartIcon,
        items: [
          {
            title: 'Projects',
            href: '/management/projects'
          },
          {
            title: 'Products',
            href: '/management/products'
          }
        ]
      },
      {
        title: 'Post',
        href: '/post',
        icon: SettingsIcon,
        items: [
          {
            title: 'General',
            href: '/post/general'
          },
          {
            title: 'Subscription',
            href: '/post/subscription'
          },
          {
            title: 'Notifications',
            href: '/post/notifications'
          },
          {
            title: 'Security',
            href: '/post/security'
          }
        ]
      },




    ]
  }
];
