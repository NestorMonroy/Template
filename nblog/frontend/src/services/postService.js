import axios from 'src/utils/axios';
import { handleResponse } from '../helpers/handleResponse';
import { handleError } from '../helpers/handleError';

export const postService = {
  updatePost,
};


const TOKEN = "6165f2762ac4358af1bdfceab20bb75b15d976d6"

function updatePost(pos_id, body) {

  return fetch(`http://127.0.0.1:8000/api/post/posts/${pos_id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${TOKEN}`,
    },
    body: JSON.stringify({ body })
  })
    .catch(error => console.log(error))
}