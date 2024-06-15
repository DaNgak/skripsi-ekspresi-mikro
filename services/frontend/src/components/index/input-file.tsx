import { FC, useState, ChangeEvent } from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { IRequestUploadVideo, useUploadVideo } from '@/hooks/useModel';
import ResultFetching from './result-fetching';

interface IInputFile {
    file: File;
    filename: string;
}

const InputFile: FC = () => {
    const [input, setInput] = useState<IInputFile | null>(null);

    const { mutate, isPending, data } = useUploadVideo({
        onSuccess(response) {
            console.log(response);
        },
        onError(error) {
            if (error.code === 'ERR_NETWORK') {
                console.log('error network di backend');
            }
            console.log(error);
        },
    });

    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            // setInput({
            //     file: file,
            //     filename: file.name,
            // });
            const newInput: IInputFile = {
                file: file,
                filename: file.name,
            };
            setInput(newInput);
            mutate({ file: newInput.file } as IRequestUploadVideo);
        }
    };

    return (
        <div className="w-full flex flex-col gap-6">
            <div className="w-full flex flex-col gap-2">
                {input === null ? (
                    <>
                        <Label htmlFor="input">Input video</Label>
                        <Input
                            id="input"
                            type="file"
                            onChange={handleFileChange}
                        />
                    </>
                ) : (
                    <p>Selected file: {input.filename}</p>
                )}
                {isPending && <p>Loading...</p>}
                {!isPending && data && <ResultFetching response={data.data} />}
            </div>
        </div>
    );
};

export default InputFile;
