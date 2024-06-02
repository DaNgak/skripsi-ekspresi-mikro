import { QueryClient } from '@tanstack/react-query';

const queryClientOptions = {
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
        },
    },
};

export const queryClient = new QueryClient(queryClientOptions);
