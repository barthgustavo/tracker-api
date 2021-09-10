import { Router } from "express";
import { UploadController } from "./controllers/UploadController";

const router = Router();

const uploadController = new UploadController();

router.get('/', (req, res) => {
    res.send('API OK');
});

router.post('/upload', uploadController.upload);
router.post('/process', (req, res) => {
    console.log(req.body);
    res.send('ok');
});

export { router };