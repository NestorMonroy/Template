import axios from 'src/utils/axios';

export function handleError(error) {
  console.log(error);
  localStorage.clear();
  window.location.replace('/auth/login');
}
