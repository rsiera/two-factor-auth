// @flow
import {post} from './api';

async function loginUser(email: string, password: string, twoFaCode?: string): Promise<any> {
  return await post('/get-token', {
    data: {email, password, two_fa_code: twoFaCode}
  });
}

async function verifyToken(token: string): Promise<any> {
  return await post('/verify-token', {
    data: {token}
  });
}

export {
  loginUser,
  verifyToken
};
