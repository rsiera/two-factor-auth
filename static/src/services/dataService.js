// @flow
import {get} from './api';


async function fetchUserData(token: string) {
    return await get('/user', {'Authorization': token});
}

export {
  fetchUserData,
};
