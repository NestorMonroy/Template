/* eslint-disable no-unused-vars */
import React, { useState, useRef, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { useHistory } from 'react-router';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { useDispatch } from 'react-redux';
import { makeStyles } from '@material-ui/styles';
import {
  AppBar,
  Badge,
  Button,
  IconButton,
  Toolbar,
  Hidden,
  Input,
  colors,
  Popper,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ClickAwayListener,
  SvgIcon
} from '@material-ui/core';
import LockIcon from '@material-ui/icons/LockOutlined';
import NotificationsIcon from '@material-ui/icons/NotificationsOutlined';
import PeopleIcon from '@material-ui/icons/PeopleOutline';
import InputIcon from '@material-ui/icons/Input';
import MenuIcon from '@material-ui/icons/Menu';
import SearchIcon from '@material-ui/icons/Search';
import axios from 'src/utils/axios';
import NotificationsPopover from 'src/components/NotificationsPopover';
import PricingModal from 'src/components/PricingModal';
import { logout } from 'src/actions';
import ChatBar from './ChatBar';
import { authService } from '../../services/authService';

const useStyles = makeStyles((theme) => ({
  root: {
    boxShadow: 'none'
  },
  flexGrow: {
    flexGrow: 1
  },
  search: {
    backgroundColor: 'rgba(255,255,255, 0.1)',
    borderRadius: 4,
    flexBasis: 300,
    height: 36,
    padding: theme.spacing(0, 2),
    display: 'flex',
    alignItems: 'center'
  },
  searchIcon: {
    marginRight: theme.spacing(2),
    color: 'inherit'
  },
  searchInput: {
    flexGrow: 1,
    color: 'inherit',
    '& input::placeholder': {
      opacity: 1,
      color: 'inherit'
    }
  },
  searchPopper: {
    zIndex: theme.zIndex.appBar + 100
  },
  searchPopperContent: {
    marginTop: theme.spacing(1)
  },
  trialButton: {
    marginLeft: theme.spacing(2),
    color: theme.palette.common.white,
    backgroundColor: colors.green[600],
    '&:hover': {
      backgroundColor: colors.green[900]
    }
  },
  trialIcon: {
    marginRight: theme.spacing(1)
  },
  menuButton: {
    marginRight: theme.spacing(1)
  },
  chatButton: {
    marginLeft: theme.spacing(1)
  },
  logoutButton: {
    marginLeft: theme.spacing(1)
  },
  logoutIcon: {
    marginRight: theme.spacing(1)
  },
  logoIcon: {
    marginRight: theme.spacing(1)
  }
}));

const popularSearches = [
  'Devias React Dashboards',
  'Devias',
  'Admin Pannel',
  'Project',
  'Pages'
];

function TopBar({
  onOpenNavBarMobile,
  className,
  ...rest
}) {
  const classes = useStyles();
  const history = useHistory();
  const searchRef = useRef(null);
  const dispatch = useDispatch();
  const [openSearchPopover, setOpenSearchPopover] = useState(false);
  const [searchValue, setSearchValue] = useState('');
  const [openChatBar, setOpenChatBar] = useState(false);
  const [pricingModalOpen, setPricingModalOpen] = useState(false);

  const handleLogout = () => {
    authService.logout(history);
  };

  const handlePricingModalOpen = () => {
    setPricingModalOpen(true);
  };

  const handlePricingModalClose = () => {
    setPricingModalOpen(false);
  };

  const handleSearchChange = (event) => {
    setSearchValue(event.target.value);

    if (event.target.value) {
      if (!openSearchPopover) {
        setOpenSearchPopover(true);
      }
    } else {
      setOpenSearchPopover(false);
    }
  };

  const handleSearchPopverClose = () => {
    setOpenSearchPopover(false);
  };

  return (
    <AppBar
      {...rest}
      className={clsx(classes.root, className)}
      color="primary"
    >
      <Toolbar >
        <Hidden lgUp>
          <IconButton
            className={classes.menuButton}
            color="inherit"
            onClick={onOpenNavBarMobile}
          >
            <MenuIcon />
          </IconButton>
        </Hidden>

        <RouterLink to="/">
          <img
            alt="Logo"
            src="/images/logos/gaggenau-vector-logo.svg"
            width="200" height="50" 
          />
        </RouterLink>
        {/* <SvgIcon
          className={classes.logoIcon}>
           https://jakearchibald.github.io/svgomg/

          <svg xmlns="http://www.w3.org/2000/svg" viewBox="19 15 859 645">
            <defs />
            <path fill="#f70000" stroke="#000" stroke-width="18" d="M448 646L31 160 172 24h552l141 136-417 486z" />
            <g fill="#fff800" stroke="#000" stroke-width="16">
              <path stroke-miterlimit="4.7" d="M207 298l72 85c39-36 131-28 160 22 79 1 147 5 173-27 7-11 10-22 0-30-47-32-216-15-405-50zM93 164l99-97h49c-50 40-84 94-100 154l-48-57zm256 298l99 115 95-110c-48 11-102 16-194-5z" />
              <path stroke-miterlimit="9.6" d="M594 67h42c1 16-7 25-11 30-10-13-26-26-31-30z" />
              <path d="M709 276l94-112-68-67v75H595c-4-73-78-104-164-103-79 0-145 20-151 65-7 24 21 66 187 58 132-3 213 26 242 84z" />
            </g>
          </svg>

        </SvgIcon> */}

          <img
            alt="Logo"
            src="/images/logos/gaggenau-vector-logo.svg"
            width="200" height="50" 
          />
        <div className={classes.flexGrow} />
        <Hidden smDown>
          <div
            className={classes.search}
            ref={searchRef}
          >
            <SearchIcon className={classes.searchIcon} />
            <Input
              className={classes.searchInput}
              disableUnderline
              onChange={handleSearchChange}
              placeholder="Search people &amp; places"
              value={searchValue}
            />
          </div>
          <Popper
            anchorEl={searchRef.current}
            className={classes.searchPopper}
            open={openSearchPopover}
            transition
          >
            <ClickAwayListener onClickAway={handleSearchPopverClose}>
              <Paper
                className={classes.searchPopperContent}
                elevation={3}
              >
                <List>
                  {popularSearches.map((search) => (
                    <ListItem
                      button
                      key={search}
                      onClick={handleSearchPopverClose}
                    >
                      <ListItemIcon>
                        <SearchIcon />
                      </ListItemIcon>
                      <ListItemText primary={search} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </ClickAwayListener>
          </Popper>
        </Hidden>
        <IconButton
          className={classes.chatButton}
          color="inherit"
        >
          <Badge
            badgeContent={6}
            color="secondary"
          >
            <PeopleIcon />
          </Badge>
        </IconButton>
        <Hidden mdDown>
          <Button
            className={classes.logoutButton}
            color="inherit"
            onClick={handleLogout}
          >
            <InputIcon className={classes.logoutIcon} />
            Sign out
          </Button>
        </Hidden>
      </Toolbar>
      <PricingModal
        onClose={handlePricingModalClose}
        open={pricingModalOpen}
      />
    </AppBar>
  );
}

TopBar.propTypes = {
  className: PropTypes.string,
  onOpenNavBarMobile: PropTypes.func
};

export default TopBar;
