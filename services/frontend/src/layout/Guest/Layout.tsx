import { HTMLAttributes, ReactNode } from 'react';
import Footer from './Footer';
import Header from './Header';
import { cn } from '@/lib/utils';

interface IProps extends HTMLAttributes<HTMLDivElement> {
    children: ReactNode;
}

const Layout = ({ children, className, ...props }: IProps) => {
    return (
        <div className="w-full max-w-xl h-screen text-sm bg-white mx-auto flex flex-col hidden-scrollbar">
            <Header />
            <main
                className={cn(
                    'w-full flex-auto bg-slate-50 flex flex-col overflow-x-hidden overflow-y-auto hidden-scrollbar px-6 py-5 sm:px-10',
                    className
                )}
                {...props}
            >
                {children}
            </main>
            <Footer />
        </div>
    );
};

export default Layout;
