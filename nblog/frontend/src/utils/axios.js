import axios from 'axios';

const instance = axios.create({
  mode: 'no-cors'
});

export default instance;
