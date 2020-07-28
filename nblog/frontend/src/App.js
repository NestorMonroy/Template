import React from 'react';
import { Box, Grommet } from 'grommet';
import { aruba } from 'grommet-theme-aruba';

const theme = {
  global: {
    font: {
      family: 'Roboto',
      size: '18px',
      height: '20px',
    },
  },
};

const AppBar = (props) => (
  <Box
    tag='header'
    direction='row'
    align='center'
    justify='between'
    background='brand'
    pad={{ left: 'medium', right: 'small', vertical: 'small' }}
    elevation='medium'
    style={{ zIndex: '1' }}
    {...props}
  />
);

function App() {

  return (
    <Grommet theme={theme}>
      <AppBar>Hello Grommet!</AppBar>
    </Grommet>
  );
}

export default App;
