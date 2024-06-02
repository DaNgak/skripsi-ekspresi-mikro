import Layout from '@/layout/Guest/Layout';
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/user')({
    component: () => (
        <Layout>
            <div>Hello /User!</div>
        </Layout>
    ),
});
