import { axiosInstance } from '@/lib/axios';
import { BaseApiResponse } from '@/lib/config';
import { useMutation } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

// Interface for Request Form
export interface IRequestUploadVideo {
    file: File;
}

// Interface for Response Data
export interface IResponseUploadVideo {
    video: {
        url: string;
        name: string;
    };
    result: string;
    list_predictions: {
        [key: string]: {
            count: number;
            percentage: number;
        };
    };
    images: {
        name: string;
        url: string;
        prediction: string;
        components: {
            [key: string]: { url: string };
        };
    }[];
}

export const useUploadVideo = ({
    onSuccess,
    onError,
}: {
    onSuccess: (
        response: AxiosResponse<BaseApiResponse<IResponseUploadVideo>>
    ) => void;
    onError: (error: AxiosError<BaseApiResponse<null>>) => void;
}) => {
    return useMutation({
        mutationFn: async (body: IRequestUploadVideo) => {
            const response = await axiosInstance.post<
                BaseApiResponse<IResponseUploadVideo>
            >(
                '/data-model/data-test',
                {
                    file: body.file,
                },
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );
            return response;
        },
        onSuccess,
        onError,
    });
};
