import Layout from '@/layout/Guest/Layout';
import { createFileRoute } from '@tanstack/react-router';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import WebcamStream from '@/components/index/webcam';
import InputFile from '@/components/index/input-file';

export const Route = createFileRoute('/')({
    component: () => (
        <Layout className="items-center justify-center">
            <div className="flex w-full h-full flex-grow">
                <Tabs
                    defaultValue="webcam-stream"
                    className="w-full"
                >
                    <TabsList className="grid w-full grid-cols-2 gap-1">
                        <TabsTrigger value="webcam-stream">
                            Webcam Stream
                        </TabsTrigger>
                        <TabsTrigger value="input-file">Input File</TabsTrigger>
                    </TabsList>
                    <TabsContent value="webcam-stream">
                        <WebcamStream />
                    </TabsContent>
                    <TabsContent value="input-file">
                        <InputFile />
                    </TabsContent>
                </Tabs>
            </div>
        </Layout>
    ),
});
