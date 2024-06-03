import { FC, useRef, useState, useCallback, useEffect } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';

interface MediaDeviceInfo {
    deviceId: string;
    kind: string;
    label: string;
}

const WebcamStream: FC = () => {
    const webcamRef = useRef<Webcam>(null);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const [capturing, setCapturing] = useState<boolean>(false);
    const [recordedChunks, setRecordedChunks] = useState<Blob[]>([]);
    const [devices, setDevices] = useState<MediaDeviceInfo[]>([]);
    const [selectedDeviceId, setSelectedDeviceId] = useState<string | null>(
        null
    );

    const handleDataAvailable = useCallback(
        ({ data }: BlobEvent) => {
            if (data.size > 0) {
                setRecordedChunks((prev) => prev.concat(data));
            }
        },
        [setRecordedChunks]
    );

    const handleStartCaptureClick = useCallback(() => {
        setCapturing(true);
        if (webcamRef.current && webcamRef.current.stream) {
            mediaRecorderRef.current = new MediaRecorder(
                webcamRef.current.stream,
                {
                    mimeType: 'video/webm',
                }
            );
            mediaRecorderRef.current.addEventListener(
                'dataavailable',
                handleDataAvailable
            );
            mediaRecorderRef.current.start();
        }
    }, [webcamRef, setCapturing, mediaRecorderRef, handleDataAvailable]);

    const handleStopCaptureClick = useCallback(() => {
        if (mediaRecorderRef.current) {
            mediaRecorderRef.current.stop();
            setCapturing(false);
        }
    }, [mediaRecorderRef, setCapturing]);

    const uploadVideo = useCallback(async (blob: Blob) => {
        const formData = new FormData();
        formData.append('file', blob, 'react-webcam-stream-capture.webm');

        try {
            const response = await axios.post(
                'http://localhost:5000/upload',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );

            console.log('Upload successful:', response.data);
        } catch (error) {
            console.error('Error uploading video:', error);
        }
    }, []);

    const handleDownload = useCallback(() => {
        if (recordedChunks.length) {
            const blob = new Blob(recordedChunks, {
                type: 'video/webm',
            });
            const url = URL.createObjectURL(blob);
            console.log(url); // Print URL in website

            // Create a download link
            const a = document.createElement('a');
            document.body.appendChild(a);
            a.style.display = 'none';
            a.href = url;
            a.download = 'react-webcam-stream-capture.webm';
            a.click();
            window.URL.revokeObjectURL(url);

            // Upload the video to the server
            uploadVideo(blob);

            setRecordedChunks([]);
        }
    }, [recordedChunks, uploadVideo]);

    const handleDevices = useCallback(
        (mediaDevices: MediaDeviceInfo[]) => {
            const videoDevices = mediaDevices.filter(
                ({ kind }) => kind === 'videoinput'
            );
            setDevices(videoDevices);
        },
        [setDevices]
    );

    useEffect(() => {
        navigator.mediaDevices.enumerateDevices().then(handleDevices);
    }, [handleDevices]);

    useEffect(() => {
        if (devices.length > 0 && !selectedDeviceId) {
            setSelectedDeviceId(devices[0].deviceId);
        }
    }, [devices, selectedDeviceId]);

    return (
        <div className="w-full flex flex-col gap-6">
            <div className="h-full w-full aspect-auto rounded-md overflow-hidden shadow-lg">
                <Webcam
                    className="w-full"
                    audio={false}
                    ref={webcamRef}
                    videoConstraints={{
                        deviceId: selectedDeviceId || undefined,
                    }}
                />
            </div>
            <div className="text-pretty break-words">
                Device length {JSON.stringify(devices)}{' '}
            </div>
            {devices.length <= 1 ? (
                <div className="mx-auto text-red-500">No webcam detected</div>
            ) : (
                <Select
                    onValueChange={(value) => setSelectedDeviceId(value)}
                    value={selectedDeviceId || ''}
                >
                    <SelectTrigger className="max-w-xs mx-auto">
                        <SelectValue placeholder="Select list webcam" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectGroup>
                            {devices.map((device) => (
                                <SelectItem
                                    key={device.deviceId}
                                    value={device.deviceId}
                                >
                                    {device.label ||
                                        `Device ${device.deviceId}`}
                                </SelectItem>
                            ))}
                        </SelectGroup>
                    </SelectContent>
                </Select>
            )}
            {devices.length > 1 && (
                <>
                    {capturing ? (
                        <button
                            className="text-base font-normal dec"
                            onClick={handleStopCaptureClick}
                        >
                            Stop Capture
                        </button>
                    ) : (
                        <button onClick={handleStartCaptureClick}>
                            Start Capture
                        </button>
                    )}
                    {recordedChunks.length > 0 && (
                        <button onClick={handleDownload}>Download</button>
                    )}
                </>
            )}
        </div>
    );
};

export default WebcamStream;
