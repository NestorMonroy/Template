import axios from 'src/utils/axios';
import { handleResponse } from '../helpers/handleResponse';
import { handleError } from '../helpers/handleError';

export const categoryService = {
  findAll,
  findById,
};

function findAll() {
  return axios.get('/categories/')
    .catch(handleError)
    .then(handleResponse);
}

function findById(id) {
  return axios.get(`/categories/${id}`)
    .catch(handleError)
    .then(handleResponse);
}
