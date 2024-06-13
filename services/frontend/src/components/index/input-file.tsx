import { FC, useState, ChangeEvent } from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { IResponseUploadVideo, useUploadVideo } from '@/hooks/useModel';
import { useQueryClient } from '@tanstack/react-query';
import { BaseApiResponse } from '@/lib/config';

interface IInputFile {
    file: File;
    filename: string;
}

const InputFile: FC = () => {
    const [input, setInput] = useState<IInputFile | null>(null);
    const [response, setResponse] =
        useState<BaseApiResponse<IResponseUploadVideo> | null>(null);

    const { mutate, isPending } = useUploadVideo({
        onSuccess(response) {
            console.log(response);
            setResponse(response.data);
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
            mutate(newInput);
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
                {isPending ? (
                    <>Loading</>
                ) : (
                    <>
                        Result <br />
                        <h4>{JSON.stringify(response)}</h4>
                    </>
                )}
            </div>
        </div>
    );
};

export default InputFile;
