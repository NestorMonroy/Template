import { Redirect, Route } from 'react-router';
import React from 'react';
import { authService } from './services/authService';


function PrivateRoute({ component: Component, ...rest }) {
  const token = authService.token();
  const props = { ...rest };

  if (!token) {
    return <Redirect to={{ pathname: '/auth/login', state: { from: props.location } }} />;
  } else {
    return <Component {...props} />;
  }

  return <Component {...props} />;
}

export default PrivateRoute;
