import { axiosInstance } from '@/lib/axios';
import { BaseApiResponse } from '@/lib/config';
import { useMutation } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

// Interface for Request Form
export interface IRequestUploadVideo {
    file: File;
}

// Interface for Response Data
export interface IUploadVideoPrediction {
    name: string;
    count: number;
    percentage: number;
}

export interface IUploadVideoImage {
    name: string;
    url: string;
    prediction: {
        [key: string]: string;
    };
    components: {
        [key: string]: { url_source: string; url_result?: string };
    };
}

export interface IResponseUploadVideo {
    video: {
        name: string;
        url: string;
    };
    csv_file: {
        [key: string]: string;
    };
    result: {
        [key: string]: string;
    };
    list_predictions: {
        [key: string]: IUploadVideoPrediction[];
    };
    array_predictions?: {
        [key: string]: string[];
    };
    images?: IUploadVideoImage[];
}

export const useUploadVideo = ({
    onSuccess,
    onError,
    onSettled,
}: {
    onSuccess?: (
        data: AxiosResponse<BaseApiResponse<IResponseUploadVideo>>
    ) => void;
    onError?: (error: AxiosError<BaseApiResponse<null>>) => void;
    onSettled?: (
        data: AxiosResponse<BaseApiResponse<IResponseUploadVideo>> | undefined,
        error: AxiosError<BaseApiResponse<null>> | null
    ) => void;
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
        onSettled,
    });
};
