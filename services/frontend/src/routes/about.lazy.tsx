import { createLazyFileRoute } from '@tanstack/react-router';

const AboutTest = () => {
    return <div>Test about</div>;
};

export const Route = createLazyFileRoute('/about')({
    pendingComponent: AboutTest,
    errorComponent: AboutTest,
    component: AboutTest,
});
