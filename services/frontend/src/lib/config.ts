export type BaseApiResponse<T> = {
    code: number;
    message?: string | { title: string; description: string };
    data?: T;
    errors?: {
        [attribute: string]: string[] | string;
    };
};

export type TAlertIcon = 'error' | 'warning' | 'info' | 'success';

export type TAlertMessage = {
    type: TAlertIcon;
    title: string;
    description?: string;
};

export const API_URL = import.meta.env.VITE_PUBLIC_API_BACKEND;
