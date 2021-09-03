import express from 'express';
import { router } from './routes';
import path from 'path';
import cors from 'cors';

const app = express();
app.use('/video', express.static(path.join(__dirname, '/services/uploads')));
app.use(cors());
app.use(express.json());
app.use(router);
app.listen(3001, () => console.log('Servidor iniciado!'));