import React, { useState } from "react";
import { Box, Button, Collapsible, Heading, Grid, Grommet, Layer, ResponsiveContext } from 'grommet';
import { Notification, FormClose } from 'grommet-icons';

const theme = {
  global: {
    colors: {
      brand: '#ee9933',
      'brand-contrast': '#ee993333',
      active: '#eecc33',
    },
    font: {
      family: 'Roboto',
      size: '18px',
      height: '20px',
    },
  },
  button: {
    default: {
      color: 'text',
      border: undefined,
      padding: {
        horizontal: '12px',
        vertical: '8px',
      },
    },
    primary: {
      background: { color: 'brand' },
      border: undefined,
      color: 'text-strong',
      font: { weight: 'bold' },
      padding: {
        horizontal: '12px',
        vertical: '8px',
      },
    },
    secondary: {
      border: { color: 'brand', width: '4px' },
      color: 'text',
      padding: {
        horizontal: '8px',
        vertical: '4px',
      },
    },
    active: {
      background: { color: 'brand-contrast' },
      color: 'text',
      secondary: {
        background: 'none',
        border: {
          color: 'brand-contrast',
        },
      },
    },
    disabled: {
      opacity: 0.3,
      secondary: {
        border: { color: 'text-weak' },
      },
    },
    hover: {
      background: { color: 'active' },
      secondary: {
        border: { color: 'active' },
      },
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
      <ResponsiveContext.Consumer>
        {size => (
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
              {(!showSidebar || size !== 'small') ? (
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
              ) : (
                  <Layer>
                    <Box
                      background='light-2'
                      tag='header'
                      justify='end'
                      align='center'
                      direction='row'
                    >
                      <Button
                        icon={<FormClose />}
                        onClick={() => setShowSidebar(false)}
                      />
                    </Box>
                    <Box
                      fill
                      background='light-2'
                      align='center'
                      justify='center'
                    >
                      sidebar
                      </Box>
                  </Layer>
                )}
            </Box>
          </Box>
        )}
      </ResponsiveContext.Consumer>
    </Grommet >
  );
}

export default App;
