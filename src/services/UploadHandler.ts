import { IncomingHttpHeaders } from 'http';
import path, { join } from 'path';
import { pipelineAsync } from '../util';
import { createWriteStream } from 'fs';

import Busboy from 'busboy';

class UploadHandler {
    newFileName?: string;

    registerEvents(headers: IncomingHttpHeaders, onFinish: () => void) {
        const busboy = new Busboy({ headers });
        busboy.on("file", this.onFile.bind(this));
        busboy.on("finish", onFinish);
        return busboy;
    }

    private async onFile(fieldname: string, file: NodeJS.ReadableStream, filename: string, encoding: string, mimetype: string) {
        const d = new Date();
        this.newFileName = Buffer.from((Math.random() * d.getMilliseconds()).toString()).toString('base64') + path.extname(filename);
        let saveFileTo = join(__dirname, '../../uploads', this.newFileName);
        
        await pipelineAsync(file, this.handleData.apply(this), createWriteStream(saveFileTo));
    }

    private handleData(): any {
        async function * handle(data: any) {
            for await (const item of data) yield item;
        }

        return handle;
    }
}

export { UploadHandler };