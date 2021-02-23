import { Router } from "express";
import { UploadController } from "./controllers/UploadController";

const router = Router();

const uploadController = new UploadController();

router.get('/', (req, res) => {
    res.send('API OK');
});

router.post('/', uploadController.upload);

export { router };