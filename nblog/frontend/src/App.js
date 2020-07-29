import React, { useState } from "react";
import { Anchor, Box, Button, Collapsible, Header, Nav, Heading, Grid, Grommet, Layer, Menu, Text, ResponsiveContext } from 'grommet';
import { Notification, FormClose, FormDown } from 'grommet-icons';

import { PostsComponent } from './posts'


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
  // breakpoints: {
  //   small: {
  //     value: 600,
  //     edgeSize: {
  //       small: '1px',
  //     },
  //     borderSize: {
  //       small: '2px',
  //     },
  //     size: {
  //       xxsmall: '24px',
  //     },
  //   },
  //   medium: {
  //     value: 900,
  //     borderSize: {
  //       small: '2px',
  //     },
  //     edgeSize: {
  //       small: '1px',
  //     },
  //     size: {
  //       xxsmall: '24px',
  //     },
  //   },
  //   large: {
  //     value: 3000,
  //     borderSize: {
  //       small: '2px',
  //     },
  //     edgeSize: {
  //       small: '1px',
  //     },
  //     size: {
  //       xxsmall: '24px',
  //     },
  //   },
  //   xlarge: {
  //     value: 3000,
  //     borderSize: {
  //       small: '2px',
  //     },
  //     edgeSize: {
  //       small: '1px',
  //     },
  //     size: {
  //       xxsmall: '24px',
  //     },
  //   },
  // },
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
            {/* <AppBar>
              <Heading level='3' margin='none'>Nestor Blog</Heading>
              <Button
                icon={<Notification />}
                onClick={() => setShowSidebar(!showSidebar)}
              />
              <Menu
                dropProps={{ align: { top: 'bottom', left: 'left' } }}

                icon={false}
                items={[
                  { label: 'Launch', onClick: () => { } },
                  { label: 'Abort', onClick: () => { } },
                ]}
              >
                {({ drop, hover }) => {
                  const color = hover && !drop ? 'brand' : undefined;
                  return (
                    <Box
                      direction="row"
                      gap="small"
                      pad="small"
                      background={hover && drop ? 'light-2' : undefined}
                    >
                      <Text color={color}>actions</Text>
                      <FormDown color={color} />
                    </Box>
                  );
                }}
              </Menu>
            </AppBar> */}
            <Header background="dark-1" pad="medium">
              {/* <Box direction="row" align="center" gap="small">
                Resize the page to collapse the Nav into a Menu
              </Box> */}
              <Heading level='3' margin='none'>Nestor Blog</Heading>
              <Button
                icon={<Notification />}
                onClick={() => setShowSidebar(!showSidebar)}
              />
              <ResponsiveContext.Consumer>
                {responsive =>
                  responsive === 'small' ? (
                    <Menu
                      dropProps={{ align: { top: 'bottom', left: 'left' } }}

                      icon={false}
                      items={[
                        { label: 'Launch', onClick: () => { } },
                        { label: 'Abort', onClick: () => { } },
                      ]}
                    >
                      {({ drop, hover }) => {
                        const color = hover && !drop ? 'brand' : undefined;
                        return (
                          <Box
                            direction="row"
                            gap="small"
                            pad="small"
                            background={hover && drop ? 'light-2' : undefined}
                          >
                            <Text color={color}>actions</Text>
                            <FormDown color={color} />
                          </Box>
                        );
                      }}
                    </Menu>
                    // <Menu
                    //   label="Click me"
                    //   items={[
                    //     { label: 'This is', onClick: () => { } },
                    //     { label: 'The Menu', onClick: () => { } },
                    //     { label: 'Component', onClick: () => { } },
                    //   ]}
                    // />
                  ) : (
                      <Nav direction="row">
                        <Anchor href="#" label="This is" />
                        <Anchor href="#" label="The Nav" />
                        <Anchor href="#" label="Component" />
                      </Nav>
                    )
                }
              </ResponsiveContext.Consumer>
            </Header>
            <Box direction='row' flex overflow={{ horizontal: 'hidden' }}>
              {(!showSidebar || size !== 'small') ? (
                <Collapsible direction="horizontal" open={showSidebar}>
                  <Box
                    width='small'
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
              <Box flex align='center' justify='center'>
                <PostsComponent />
              </Box>
            </Box>

          </Box>
        )}
      </ResponsiveContext.Consumer>
    </Grommet >
  );
}

export default App;
