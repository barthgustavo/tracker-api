import { Request, Response } from 'express';
import { UploadHandler } from '../services/UploadHandler';
import { pipelineAsync } from '../util';

class UploadController {
    async upload(req: Request, res: Response) {
        const uploadHandler = new UploadHandler();

        const onFinish = (res: Response) => () => {
            res.json({ result: 'OK', filename: uploadHandler.newFileName });
        }

        const handlerInstance = uploadHandler.registerEvents(req.headers, onFinish(res));

        await pipelineAsync(req, handlerInstance);
    }
}

export { UploadController };