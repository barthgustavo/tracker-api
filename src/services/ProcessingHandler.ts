import { spawn } from 'child_process';
import { join } from 'path';

interface SelectedArea {
    x: number;
    y: number;
    width: number;
    height: number;
}

class ProcessingHandler {

    positioning: SelectedArea;
    filename: string;
    time: number;

    constructor(positioning: SelectedArea, filename: string, time: number) {
        this.positioning = positioning;
        this.filename = filename;
        this.time = time;
    }

    async processar() {
        console.log(this.time.toString());
        const completePythonLocation = join(__dirname, '../../python');
        const python = spawn('python3', [
            'mp-kcf-file.py',
            '--video', this.filename,
            '--time', this.time.toString()
        ], { cwd: completePythonLocation });

        //if i need to handle python's output
        /*var dataToSend: string;
        python.stdout.on('data', function (data) {
            console.log('Pipe data from python script ...');
            dataToSend = data.toString();
        });*/

        return await new Promise((resolve, reject) => {
            python.on('close', () => {
                resolve("processed-" + this.filename);
            });
        });
    }
}

export { ProcessingHandler, SelectedArea };