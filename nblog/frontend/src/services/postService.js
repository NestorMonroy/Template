import axios from 'src/utils/axios';
import {handleResponse} from '../helpers/handleResponse';
import {handleError} from '../helpers/handleError';

export const postService = {
  findAll,
  saveProduct
};

function findAll() {
  return axios.get('/post/posts/')
    .then(handleResponse);
}

function saveProduct(name, price, description, subCategoryId) {
    return axios.post('/post/posts/', {name, price, description, subCategoryId})
      .catch(handleError)
      .then(handleResponse);
  }