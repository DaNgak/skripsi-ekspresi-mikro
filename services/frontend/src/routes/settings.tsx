import Layout from '@/layout/Guest/Layout';
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/settings')({
    component: () => (
        <Layout>
            <div>Hello /settings!</div>
        </Layout>
    ),
});
