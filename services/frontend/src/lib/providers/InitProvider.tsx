import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from './QueryProvider';
import { router } from './RouterProvider';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { RouterProvider } from '@tanstack/react-router';

function InitProvider() {
    return (
        <QueryClientProvider client={queryClient}>
            <RouterProvider router={router} />
            <ReactQueryDevtools
                initialIsOpen={false}
                buttonPosition="bottom-left"
            />
        </QueryClientProvider>
    );
}

export default InitProvider;
