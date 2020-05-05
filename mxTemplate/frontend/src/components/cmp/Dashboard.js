import React, { Fragment } from 'react';
import Form from './Form';
import Compras from './Compras';

export default function Dashboard() {
  return (
    <Fragment>
      <Form />
      <Compras />
    </Fragment>
  );
}
