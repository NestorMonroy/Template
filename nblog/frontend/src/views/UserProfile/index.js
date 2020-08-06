import React from "react";
import Header from "./Header";
import ProductList from "./ProductList";
import About from "./About";
import makeStyles from "@material-ui/core/styles/makeStyles";
import {
  Tabs,
  Tab,
} from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from "@material-ui/core/Box";
import PropTypes from "prop-types";


function TabPanel(props) {
  const {children, value, index, ...other} = props;

  return (
    <Typography
      component="div"
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box p={3}>{children}</Box>}
    </Typography>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
}));


function Profile() {
  // const classes = useStyles();
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <div>
      <Header/>
      <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
        <Tab label="Product"/>
        <Tab label="About"/>
      </Tabs>
      <TabPanel value={value} index={0}>
        <ProductList/>
      </TabPanel>
      <TabPanel value={value} index={1}>
        <About/>
      </TabPanel>
    </div>
  )
}

export default Profile;
