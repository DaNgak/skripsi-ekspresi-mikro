import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import InitProvider from './lib/providers/InitProvider';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <InitProvider />
    </StrictMode>
);
