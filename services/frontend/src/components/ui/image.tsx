import * as React from 'react';
import { cn } from '@/lib/utils';

const MemoizedImage = React.memo(
    React.forwardRef<
        HTMLImageElement,
        React.ImgHTMLAttributes<HTMLImageElement>
    >(({ className, ...props }, ref) => (
        <img
            ref={ref}
            className={cn(
                'object-cover object-center w-full h-full',
                className
            )}
            {...props}
        />
    ))
);

MemoizedImage.displayName = 'MemoizedImage';

interface Image404Props extends React.HTMLAttributes<HTMLImageElement> {
    message?: string;
    classNameParent?: string;
    classNameText?: string;
}

const Image404 = React.forwardRef<HTMLImageElement, Image404Props>(
    (
        {
            className,
            message = '404 | Image Not Found',
            classNameParent,
            classNameText,
            ...props
        },
        ref
    ) => (
        <div
            className={cn(
                'w-full h-full relative bg-secondary rounded-lg shadow-lg overflow-hidden',
                classNameParent
            )}
        >
            <img
                ref={ref}
                src="https://images.unsplash.com/photo-1666813693672-fcb447dec506?q=80&w=2500&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                alt=""
                className={cn(
                    'object-cover object-center w-full h-full',
                    className
                )}
                {...props}
            />
            <p
                className={cn(
                    'absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-xl font-semibold text-white shadow-sm break-words',
                    classNameText
                )}
            >
                {message}
            </p>
        </div>
    )
);

Image404.displayName = 'Image404';

export { MemoizedImage, Image404 };
