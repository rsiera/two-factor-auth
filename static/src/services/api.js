// @flow
import 'regenerator-runtime/runtime';
import axios from 'axios';

const API_PREFIX = '/api';

const getUrl = (url: string) => `${process.env.API_HOST}${API_PREFIX}${url}`;

class APIError extends Error {
  name: string = 'APIError';
  data: ?string | ?Object = null;

  constructor(message: string, errorData: string | Object) {
    super(message);
    this.data = errorData;
  }
}

class InvalidRequestError extends APIError {
  name: string = 'InvalidRequestError';
}

class InvalidResponseError extends APIError {
  name: string = 'InvalidResponseError';
}

class NotFoundError extends APIError {
  name = 'NotFound';
}

const handleErrorResponse = (error: Object) => {
  const {response, request} = error;
  if (!response) {
    throw new InvalidRequestError('Response undefined or incorrect.', request);
  }

  if (response.status === 400) {
    throw new InvalidResponseError('Request finished with errors.', response.data);
  } else if (response.status === 404) {
    throw new NotFoundError('Resource not found.', response.data);
  }

  throw new APIError('API error', error);
};

const getHeaders = () => {
  return {
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  };
};

const post = async (url: string, data: Object): Promise<any> => {
  try {
    const res = await axios({
      url: getUrl(url),
      method: 'POST',
      headers: getHeaders(),
      ...data
    });
    return res.data;
  } catch (error) {
    handleErrorResponse(error);
  }
};

const get = async (url: string, headers: Object): Promise<any> => {
   try {
     const res = await axios({
       url: getUrl(url),
       method: 'GET',
       headers: {...getHeaders(), ...headers}
     })
     return res.data
   } catch (error) {
     handleErrorResponse(error);
   }
};

export {
  get,
  post,
  InvalidResponseError,
  InvalidRequestError
};
