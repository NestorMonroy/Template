import axios from 'src/utils/axios';
import { handleResponse } from '../helpers/handleResponse';
import { handleError } from '../helpers/handleError';

export const subCategoryService = {
  findAll,
  findAllByCategory,
  findById,
};

function findAll() {
  return axios.get('/subcategories/')
    .catch(handleError)
    .then(handleResponse);
}

function findAllByCategory(categoryId) {
  return axios.get(`/subcategories/?categoryId=${categoryId}`)
      .catch(handleError)
      .then(handleResponse);
}

function findById(id) {
  return axios.get(`/subcategories/${id}`)
    .catch(handleError)
    .then(handleResponse);
}
