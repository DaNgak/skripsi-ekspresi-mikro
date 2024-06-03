import { FC, useState, ChangeEvent, useCallback } from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';

interface IInputFile {
    file: File;
    filename: string;
}

const InputFile: FC = () => {
    const [input, setInput] = useState<IInputFile | null>(null);

    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            setInput({
                file: file,
                filename: file.name,
            });
        }
    };

    

    // const handleReset = () => {
    //     setInput(null);
    // };

    // const handleSubmit = (event: FormEvent) => {
    //     event.preventDefault();
    // };

    return (
        <div className="w-full flex flex-col gap-6">
            {input && <p>Selected file: {input.filename}</p>}
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
                    <>Loading</>
                )}
            </div>
        </div>
    );
};

export default InputFile;
