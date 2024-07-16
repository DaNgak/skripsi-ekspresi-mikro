import { useEffect, useState, Fragment } from 'react';
import ReactPlayer from 'react-player';
import { AspectRatio } from '@/components/ui/aspect-ratio';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from '@/components/ui/accordion';
import {
    Carousel,
    CarouselContent,
    CarouselItem,
    type CarouselApi,
} from '@/components/ui/carousel';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Image404, MemoizedImage } from '@/components/ui/image';
import { capitalizeAndRemoveUnderscore, getFormatFile } from '@/lib/helper';
import { BaseApiResponse } from '@/lib/config';
import { IResponseUploadVideo } from '@/hooks/useModel';

interface IProps {
    response?: BaseApiResponse<IResponseUploadVideo> | BaseApiResponse<null>;
}

const ResultFetching = ({ response }: IProps) => {
    const [api, setApi] = useState<CarouselApi>();
    const [current, setCurrent] = useState(0);
    const [count, setCount] = useState(0);

    useEffect(() => {
        if (!api) {
            return;
        }

        setCount(api.scrollSnapList().length);
        setCurrent(api.selectedScrollSnap() + 1);

        api.on('select', () => {
            setCurrent(api.selectedScrollSnap() + 1);
        });
    }, [api]);

    return (
        <>
            {response && response.code === 200 && response.data !== null && (
                <div className="flex flex-col gap-4 mt-6 pb-10">
                    Name: {response.data?.video.name}
                    {response.data?.video ? (
                        getFormatFile(response.data.video.url) === 'webm' ? (
                            <AspectRatio
                                ratio={16 / 9}
                                className="w-full max-h-[512px] overflow-hidden rounded-md shadow-lg"
                            >
                                <ReactPlayer
                                    url={response.data?.video.url}
                                    width={'100%'}
                                    height={'100%'}
                                    controls={true}
                                />
                            </AspectRatio>
                        ) : (
                            <div className="w-full flex justify-start">
                                <a
                                    href={response.data.video.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="px-5 py-3 bg-primary text-white rounded-lg shadow-lg"
                                >
                                    Open Video
                                </a>
                            </div>
                        )
                    ) : (
                        <Alert>
                            <AlertTitle>Not Found</AlertTitle>
                            <AlertDescription>
                                Tidak ada response video
                            </AlertDescription>
                        </Alert>
                    )}
                    <div className="text-sm font-normal flex flex-col gap-1">
                        <h5>Hasil Prediksi : </h5>
                        {response.data?.result && (
                            <div>
                                {Object.entries(response.data.result).map(
                                    ([key, value]) => (
                                        <div key={key}>
                                            <span className="text-base text-primary font-semibold tracking-wide">
                                                {capitalizeAndRemoveUnderscore(
                                                    key
                                                )}
                                                : {value}
                                            </span>
                                        </div>
                                    )
                                )}
                            </div>
                        )}
                        {/* <span className="text-base text-primary font-semibold tracking-wide">
                            {response.data?.result}
                        </span> */}
                    </div>
                    <div className="text-sm font-normal flex flex-col gap-2">
                        <h5>Detail Perhitungan Prediksi:</h5>
                        {response.data?.list_predictions && (
                            <Table classNameParent="border border-primary rounded-lg shadow-lg">
                                <TableHeader>
                                    <TableRow className="font-semibold">
                                        <TableHead className="text-start">
                                            Label
                                        </TableHead>
                                        <TableHead className="text-center">
                                            Jumlah Data
                                        </TableHead>
                                        <TableHead className="text-center">
                                            Persentase
                                        </TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {Object.entries(
                                        response.data.list_predictions
                                    ).map(([key, predictions], index) => (
                                        <Fragment key={index}>
                                            <TableRow className="font-semibold bg-gray-200 hover:bg-gray-200">
                                                <TableCell colSpan={3}>
                                                    {capitalizeAndRemoveUnderscore(
                                                        key
                                                    )}
                                                </TableCell>
                                            </TableRow>
                                            {predictions.map(
                                                (item, itemIndex) => (
                                                    <TableRow
                                                        className="font-medium"
                                                        key={itemIndex}
                                                    >
                                                        <TableCell className="text-start">
                                                            {item.name}
                                                        </TableCell>
                                                        <TableCell className="text-center">
                                                            {item.count}
                                                        </TableCell>
                                                        <TableCell className="text-center">
                                                            {item.percentage} %
                                                        </TableCell>
                                                    </TableRow>
                                                )
                                            )}
                                        </Fragment>
                                    ))}
                                </TableBody>
                            </Table>
                        )}
                        {/* <Table classNameParent="border border-primary rounded-lg shadow-lg">
                            <TableHeader>
                                <TableRow className="font-semibold">
                                    <TableHead className="text-start">
                                        Label
                                    </TableHead>
                                    <TableHead className="text-center">
                                        Jumlah Data
                                    </TableHead>
                                    <TableHead className="text-center">
                                        Persentase
                                    </TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {response.data &&
                                    response.data.list_predictions.map(
                                        (item, index) => (
                                            <TableRow
                                                className="font-medium"
                                                key={index}
                                            >
                                                <TableCell className="text-start">
                                                    {item.name}
                                                </TableCell>
                                                <TableCell className="text-center">
                                                    {item.count}
                                                </TableCell>
                                                <TableCell className="text-center">
                                                    {item.percentage} %
                                                </TableCell>
                                            </TableRow>
                                        )
                                    )}
                            </TableBody>
                        </Table> */}
                    </div>
                    {/* {response.data?.images && (
                        <Accordion
                            type="single"
                            collapsible
                            className="border border-primary rounded-lg shadow-lg "
                        >
                            <AccordionItem
                                value="detail-image"
                                className="border-0"
                            >
                                <AccordionTrigger className="px-4 py-3 text-sm font-normal border-0 hover:text-primary focus:text-primary data-[state=open]:text-primary">
                                    Detail Gambar FPS
                                </AccordionTrigger>
                                <AccordionContent className="p-4">
                                    <Carousel
                                        setApi={setApi}
                                        className="w-full"
                                    >
                                        <CarouselContent>
                                            {response.data &&
                                                response.data.images.map(
                                                    (item, index) => (
                                                        <CarouselItem
                                                            key={index}
                                                            className="w-full rounded-md flex flex-col gap-4"
                                                        >
                                                            <div className="flex flex-col gap-2 text-center">
                                                                <h6 className="text-base font-normal">
                                                                    Frame{' '}
                                                                    <span className="text-base font-medium text-secondary">
                                                                        {index +
                                                                            1}
                                                                    </span>
                                                                </h6>
                                                                <p className="text-sm font-normal text-secondary">
                                                                    {item.name}
                                                                </p>
                                                                <p>
                                                                    Hasil
                                                                    Prediksi:{' '}
                                                                    <span className="text-base font-medium text-secondary">
                                                                        {
                                                                            item.prediction
                                                                        }
                                                                    </span>
                                                                </p>
                                                            </div>
                                                            <AspectRatio
                                                                ratio={16 / 9}
                                                                className="w-full min-w-full overflow-hidden rounded-lg shadow-lg bg-secondary/50"
                                                            >
                                                                {item.url ? (
                                                                    <MemoizedImage
                                                                        src={
                                                                            item.url
                                                                        }
                                                                        alt={
                                                                            item.name
                                                                        }
                                                                        className="w-full h-full rounded-md object-contain"
                                                                    />
                                                                ) : (
                                                                    <Image404 />
                                                                )}
                                                            </AspectRatio>
                                                            <Table classNameParent="border border-primary rounded-lg shadow-lg">
                                                                <TableHeader>
                                                                    <TableRow className="font-semibold">
                                                                        <TableHead className="w-24 text-start">
                                                                            Component
                                                                        </TableHead>
                                                                        <TableHead className="text-center">
                                                                            Image
                                                                            Awal
                                                                        </TableHead>
                                                                        <TableHead className="text-center">
                                                                            Image
                                                                            Hasil
                                                                        </TableHead>
                                                                    </TableRow>
                                                                </TableHeader>
                                                                <TableBody>
                                                                    {item.components &&
                                                                    item.components !==
                                                                        null ? (
                                                                        Object.entries(
                                                                            item.components
                                                                        ).map(
                                                                            (
                                                                                [
                                                                                    key,
                                                                                    component,
                                                                                ],
                                                                                indexComponent
                                                                            ) => (
                                                                                <TableRow
                                                                                    className="font-medium"
                                                                                    key={
                                                                                        indexComponent
                                                                                    }
                                                                                >
                                                                                    <TableCell className="text-start">
                                                                                        {capitalizeAndRemoveUnderscore(
                                                                                            key
                                                                                        )}
                                                                                    </TableCell>
                                                                                    <TableCell className="text-center">
                                                                                        <AspectRatio
                                                                                            ratio={
                                                                                                16 /
                                                                                                9
                                                                                            }
                                                                                            className="w-full overflow-hidden rounded-md shadow-md bg-secondary/50"
                                                                                        >
                                                                                            {component.url_source ? (
                                                                                                <MemoizedImage
                                                                                                    src={
                                                                                                        component.url_source
                                                                                                    }
                                                                                                    alt={`Frame ${index + 1}  ${capitalizeAndRemoveUnderscore(
                                                                                                        key
                                                                                                    )}`}
                                                                                                    className="w-full h-full rounded-md object-contain"
                                                                                                />
                                                                                            ) : (
                                                                                                <Image404 />
                                                                                            )}
                                                                                        </AspectRatio>
                                                                                    </TableCell>
                                                                                    <TableCell className="text-center">
                                                                                        <AspectRatio
                                                                                            ratio={
                                                                                                16 /
                                                                                                9
                                                                                            }
                                                                                            className="w-full overflow-hidden rounded-md shadow-md bg-secondary/50"
                                                                                        >
                                                                                            {component.url_result ? (
                                                                                                <MemoizedImage
                                                                                                    src={
                                                                                                        component.url_result
                                                                                                    }
                                                                                                    alt={`Frame ${index + 1}  ${capitalizeAndRemoveUnderscore(
                                                                                                        key
                                                                                                    )}`}
                                                                                                    className="w-full h-full rounded-md object-contain"
                                                                                                />
                                                                                            ) : (
                                                                                                <Image404 message="No Component Image" />
                                                                                            )}
                                                                                        </AspectRatio>
                                                                                    </TableCell>
                                                                                </TableRow>
                                                                            )
                                                                        )
                                                                    ) : (
                                                                        <Alert>
                                                                            <AlertTitle>
                                                                                No
                                                                                Data
                                                                            </AlertTitle>
                                                                            <AlertDescription>
                                                                                Tidak
                                                                                ada
                                                                                data
                                                                                component
                                                                            </AlertDescription>
                                                                        </Alert>
                                                                    )}
                                                                </TableBody>
                                                            </Table>
                                                        </CarouselItem>
                                                    )
                                                )}
                                        </CarouselContent>
                                    </Carousel>
                                    <div className="py-2 text-center text-sm text-muted-foreground">
                                        Frame {current} of {count}
                                    </div>
                                </AccordionContent>
                            </AccordionItem>
                        </Accordion>
                    )} */}
                </div>
            )}
        </>
    );
};

export default ResultFetching;
