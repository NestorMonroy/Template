import axios from 'src/utils/axios';
import {handleResponse} from '../helpers/handleResponse';
import {handleError} from '../helpers/handleError';

export const productService = {
  findAll,
  findAllBySubCategoryId,
  findAllByCategoryId,
  saveProduct
};

function findAll() {
  return axios.get('/products/')
    .catch(handleError)
    .then(handleResponse);
}

function findAllBySubCategoryId(subCategoryId) {
  return axios.get(`/products/?subCategoryId=${subCategoryId}`)
    .catch(handleError)
    .then(handleResponse);
}

function findAllByCategoryId(categoryId) {
  return axios.get(`/products/?categoryId=${categoryId}`)
    .catch(handleError)
    .then(handleResponse);
}

function saveProduct(name, price, description, subCategoryId) {
  return axios.post('/products/', {name, price, description, subCategoryId})
    .catch(handleError)
    .then(handleResponse);
}

