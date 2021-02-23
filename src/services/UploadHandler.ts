import { IncomingHttpHeaders } from 'http';
import { join } from 'path';
import { pipelineAsync } from '../util';
import { createWriteStream } from 'fs';

import Busboy from 'busboy';

class UploadHandler {
    registerEvents(headers: IncomingHttpHeaders, onFinish: () => void) {
        const busboy = new Busboy({ headers });
        busboy.on("file", this.onFile.bind(this));
        busboy.on("finish", onFinish);
        return busboy;
    }

    private async onFile(fieldname: string, file: NodeJS.ReadableStream, filename: string, encoding: string, mimetype: string) {
        let d = new Date();

        let saveFileTo = join(__dirname, 'uploads', filename + '-' + d.getMilliseconds().toString());
        
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