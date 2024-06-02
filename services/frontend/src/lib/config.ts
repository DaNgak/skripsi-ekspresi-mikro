export type BaseResponse<T> = {
    code: number;
    message?: string | { title: string; description: string };
    data?: T;
    errors?: {
        [attribute: string]: string[];
    };
};

export type TAlertIcon = 'error' | 'warning' | 'info' | 'success';

export type TAlertMessage = {
    type: TAlertIcon;
    title: string;
    description?: string;
};

export const API_URL = process.env.NEXT_PUBLIC_API_BACKEND;
