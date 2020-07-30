import axios from 'src/utils/axios';
import {handleResponse} from '../helpers/handleResponse';
import jwtDecode from 'jwt-decode';
import {handleError} from '../helpers/handleError';

export const authService = {
  login,
  logout,
  token,
  getClaim,
  getFirstName,
  getLastName,
  getProfilePicture,
  getClaims
};

function login(username, password, history) {
  axios.post('/auth', {username, password})
    .catch(handleError)
    .then(handleResponse)
    .then((data) => {
        localStorage.setItem('token', data.token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${data.token}`;
        history.push('/');
      }
    );
}

function token() {
  return localStorage.getItem('token');
}

function logout(history) {
  localStorage.removeItem('token');
  axios.defaults.headers.common['Authorization'] = null;
  history.push('/auth/login');
}

function getClaim(claim) {
  const token = token();
  if (!token) return null;
  const decoded = jwtDecode(token);
  return decoded[claim];
}

function getClaims() {
  const t = token();
  if (!t) return null;
  const decoded = jwtDecode(t);
  return decoded;
}

function getFirstName() {
  return getClaim('first_name');
}

function getLastName() {
  return getClaim('last_name');
}

function getProfilePicture() {
  return getClaim('profile_picture');

}
