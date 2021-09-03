import { SelectedArea, ProcessingHandler  } from "../src/services/ProcessingHandler";

/*{
    currentTime: 0.997348,
    selectedArea: { x: 360, y: 48, width: 100, height: 100 }
}*/

test("testa se api recebe parametros do quadrado e processa o vídeo", async () => {
    //receber parametros e vídeo
    const currentTime: number = 0.997348;
    const positioning: SelectedArea = { x: 360, y: 48, width: 100, height: 100 };
    const nomeVideo: string = "biceps.mp4";

    const objHandler = new ProcessingHandler(positioning, nomeVideo);

    //processar vai devolver o destino do video processado
    let result = await objHandler.processar();
    expect(typeof result).toBe('string');
    expect(result).toBe(`processed-${nomeVideo}`);
});