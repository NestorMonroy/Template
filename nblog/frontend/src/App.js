import React, { useState } from "react";
import { Box, Button, Collapsible, Heading, Grommet, ResponsiveContext } from 'grommet';
import { Notification } from 'grommet-icons';

const theme = {
  global: {
    colors: {
      brand: '#228BE6',
    },
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
  const [showSidebar, setShowSidebar] = useState(false);
  return (
    <Grommet theme={theme} full>
      <Box fill>
        <AppBar>
          <Heading level='3' margin='none'>Nestor Blog</Heading>
          <Button 
            icon={<Notification />} 
            onClick={() => setShowSidebar(!showSidebar)}
            />
        </AppBar>
        <Box direction='row' flex overflow={{ horizontal: 'hidden' }}>
          <Box flex align='center' justify='center'>
            app Body
          </Box>
          <Collapsible direction="horizontal" open={showSidebar}>
            <Box
               width='medium'
               background='light-2'
               elevation='small'
               align='center'
               justify='center'
              >
              sidebar
            </Box>
            </Collapsible>
        </Box>
      </Box>
    </Grommet>
  );
}

export default App;
