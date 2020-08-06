import {
  Avatar,
  Divider,
  Drawer,
  Hidden,
  Paper,
  Typography,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/styles";
import clsx from "clsx";
import { getAccessToken } from 'src/helpers/localStorage';
import jwt_decode from "jwt-decode";
import PropTypes from "prop-types";
import { useSelector } from 'react-redux';
import useRouter from 'src/utils/useRouter';

import React, { Fragment, useEffect, useState } from "react";
import { Link as RouterLink } from "react-router-dom";
import { Navigation } from 'src/components/Navigation';
//import useRouter from 'utils/useRouter';
import navigationConfig from "./navigationConfig";


const useStyles = makeStyles(theme => ({
  root: {
    height: '100%',
    overflowY: 'auto'
  },
  content: {
    padding: theme.spacing(2)
  },
  profile: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    minHeight: 'fit-content'
  },
  avatar: {
    width: 60,
    height: 60
  },
  name: {
    marginTop: theme.spacing(1)
  },
  divider: {
    marginTop: theme.spacing(2)
  },
  navigation: {
    marginTop: theme.spacing(2)
  }
}));

const NavBar = props => {
  const { onCloseNavBar,openMobile, onMobileClose, className, ...rest } = props;

  const classes = useStyles();
  const router = useRouter();
  const session = useSelector(state => state.session);
  
  const [user, setUser] = useState({
    sub: "contacto@nestorblog.com",
    scopes: "ROLE_ADMIN,ROLE_USER",
    first_name: "Nestor",
    last_name: "Mpnroy",
    birth_day: 1590,
    iat: 159,
    exp: 159,
  });

  useEffect(() => {
    if (openMobile) {
      onMobileClose && onMobileClose();
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [router.location.pathname]);

  const navbarContent = (
    <div className={classes.content}>
      <div className={classes.profile}>
        <Avatar
          alt="Person"
          className={classes.avatar}
          component={RouterLink}
          to=""
        />
        <Typography className={classes.name} variant="h6">
          {user.first_name.toUpperCase()} {user.last_name.toUpperCase()}
        </Typography>
        <Typography variant="body2">{user.sub}</Typography>
      </div>
      <Divider className={classes.divider} />
      <nav className={classes.navigation}>
        {navigationConfig.map((list) => (
          <Navigation
            onCloseNavBar={onCloseNavBar}
            component="div"
            key={list.title}
            pages={list.pages}
            title={list.title}
          />
        ))}
      </nav>
    </div>
  );

  return (
    <Fragment>
      <Hidden lgUp>
        <Drawer
          anchor="left"
          onClose={onMobileClose}
          open={openMobile}
          variant="temporary"
        >
          <div
            {...rest}
            className={clsx(classes.root, className)}
          >
            {navbarContent}
          </div>
        </Drawer>
      </Hidden>
      <Hidden mdDown>
        <Paper
          {...rest}
          className={clsx(classes.root, className)}
          elevation={1}
          square
        >
          {navbarContent}
        </Paper>
      </Hidden>
    </Fragment>
  );
};

NavBar.propTypes = {
  className: PropTypes.string,
  onMobileClose: PropTypes.func,
  openMobile: PropTypes.bool
};

export default NavBar;
