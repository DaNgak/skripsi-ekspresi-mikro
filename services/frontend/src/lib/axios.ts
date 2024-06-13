import { API_URL } from '@/lib/config';
import axios from 'axios';

export const axiosInstance = axios.create({
    baseURL: API_URL,
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
    },
    withCredentials: true,
});
